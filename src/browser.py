from playwright.sync_api import sync_playwright, Playwright, expect, TimeoutError as PlaywrightTimeoutError
import logging
import urllib.parse
from resource_blocking_pkg import block as rb
import constans_pkg.constans as constans
import data_to_csv
import scrape_teams_data
import time

from bs4 import BeautifulSoup
from io import StringIO
from pathlib import Path 
import pandas as pd
from tabulate import tabulate
import numpy as np


# TODO mindent kiszervezni majd module/pkg  / not important /
# TODO team-stat / másik link - vagy kattintás után csapat


def match_history_by_team(new_context, rows, test):
    with new_context.new_page() as new_page:
      for i in range(len(rows)): 
        history_start_time = time.time()        
        new_page.goto(f"{"https://us.soccerway.com"}{rows[i].locator("td.text.team.large-link > a").get_attribute("href")}{"matches/"}")   
        #expect(new_page.get_by_role("listitem").filter(has_text="Matches")).to_be_visible()
        #new_page.get_by_role("listitem").filter(has_text="Matches").click() 
        df= pd.DataFrame()                      
        for page_index in range(10):
          expect(new_page.locator("table.matches")).to_be_visible()                    
          #scrape_teams_data.team_match_history(html=new_page.content(), test=test, test_team=rows[i].locator("td.text.team.large-link > a").get_attribute("title")) # TODO new file every page --> merge df pages then write to one file

      
          # ---------------------------
          df_tmp = scrape_teams_data.team_match_history(new_page.content(), test, "w")
          df = pd.concat([df, df_tmp])
          # ---------------------------
          
          
          tmp_loc = new_page.locator("table.matches > tbody > tr:nth-child(1) > td:nth-child(1)").inner_text()
          try:
            expect(new_page.locator("span.nav_description > a").filter(has_text="Previous")).to_be_visible()
          except AssertionError as e:
            logging.debug(msg="Expected Error for reaching last page before end of the loop")
            logging.debug(msg="Exception: {}".format(type(e).__name__))
            logging.debug(msg="Exception message: {}".format(e))
            break
          with new_page.expect_response(lambda response: response.url, timeout=20000) as response_info: # TODO imout probably not set liek this
            new_page.locator("span.nav_description > a").filter(has_text="Previous").click()
          expect(new_page.locator("table.matches > tbody > tr:nth-child(1) > td:nth-child(1)")).not_to_have_text(tmp_loc) # nothing else worked
        #logging.debug(tabulate(df, headers = 'keys', tablefmt = 'psql')) 
        # TODO kiszervezni külön browseren kívülre, ne futásközben hozzon létre mindent
        filepath = Path(f"../exported_data/teams/{test[1]}/{rows[i].locator("td.text.team.large-link > a").get_attribute("title")}_{"match_history"}.csv")  
        filepath.parent.mkdir(parents=True, exist_ok=True)  
        df.to_csv(filepath, encoding='utf-8', index=False)
        df = pd.DataFrame() 
        history_end_time = time.time()   
        print("team history time: \033[31;1;4m{}\033[0m sec".format(history_end_time - history_start_time))

        
      new_page.close()

def run(playwright: Playwright, league_size_for_debug=1):
  
    browser = playwright.chromium.launch(
        headless=False,
        #slow_mo=0,
        # f"--disable-extensions-except={constans.PATH_TO_EXTENSIONS+"/ublock_origin"}{","}{constans.PATH_TO_EXTENSIONS+"/adblock"}"
        # f"--load-extension={constans.PATH_TO_EXTENSIONS+"/ublock_origin"}{","}{constans.PATH_TO_EXTENSIONS+"/adblock"}"
        args=[
            f"--disable-extensions-except={constans.PATH_TO_EXTENSIONS+"/ublock_origin"}",
            f"--load-extension={constans.PATH_TO_EXTENSIONS+"/ublock_origin"}",
        ],
    )
    context = browser.new_context(viewport={"width": 1280, "height": 720}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.3")
    
    context.route("**/*", rb.intercept_route)
    page = context.new_page()
    
    

    for index in range(0, (len(constans.LINKS_2023_2024)-11+league_size_for_debug)): 
        parsed_link_list = list(filter(None, (urllib.parse.urlparse(constans.LINKS_2023_2024[index]).path.split('/')))) # TODO dont use constans links, use page current url
        
        page.goto(constans.LINKS_2023_2024[index])
        '''
        pop = True
        while pop:
            page.on('popup', page.get_by_text("Reject All").click()) # closes popup window   
        '''
        if index == 0: # popup has to be clicked on the first page / starting index always
            page.on('popup', page.get_by_text("Reject All").click()) # closes popup window 
        
        
        expect(page.locator("table.detailed-table")).to_be_visible()    
        data_to_csv.html_to_dataframe(html=page.content(), table_type="last", link_data=parsed_link_list)

        expect(page.locator("table.playerstats")).to_be_visible() 
        data_to_csv.html_to_dataframe(html=page.content(), table_type="top", link_data=parsed_link_list)
      
        page.get_by_role("listitem").filter(has_text="Wide").click()
        expect(page.locator("table.detailed-table.fixed-wide-table")).to_be_visible()  
        data_to_csv.html_to_dataframe(html=page.content(), table_type="wide", link_data=parsed_link_list
                                      )
        page.get_by_role("listitem").filter(has_text="Over/under").click()
        expect(page.locator("table.overundertable")).to_be_visible()  
        data_to_csv.html_to_dataframe(html=page.content(), table_type="ou", link_data=parsed_link_list)

        
        page.get_by_role("listitem").filter(has_text="Wide").click()
        expect(page.locator("table.detailed-table.fixed-wide-table")).to_be_visible()  
        match_history_by_team(context, page.locator("table.detailed-table > tbody > tr").all(), parsed_link_list)
        
        
    logging.debug(f"DONE")
    context.close()
    browser.close()


def main(lgs):
   with sync_playwright() as playwright:
     run(playwright, league_size_for_debug=lgs)


if __name__ == "__main__":
    pass