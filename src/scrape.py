from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
import pandas as pd
import logging
# import argparse
import time
from debug_pkg.logs import log as debuglog
from resource_blocking_pkg import block as rb
import constans_pkg.constans as constans


# mindent kiszervezni majd module/pkg 
'''
parser = argparse.ArgumentParser()
parser.add_argument( '-log',
                     '--loglevel',
                     default='warning',
                     help='Provide logging level. Example --loglevel debug, default=warning. Use debug for more info')

args = parser.parse_args()
levels = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warn': logging.WARNING,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}
# args.loglevel.upper  --> -log "debug"
# levels[args.loglevel.upper()]
'''
'''
# majd külön pkg
logger = logging.getLogger(__name__)
FORMAT = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s] %(levelname)s: %(message)s" 
logging.basicConfig(format=FORMAT, level=logging.INFO)
logging.info( 'Logging now setup.' )
'''

def time_wait(wait_time_seconds: float):
  """Calls time.sleep(wait_time_seconds), then prints the debug log if logging is set to debug
  
      Parameters:
      wait_time_seconds (float): time to wait in seconds

  """
  time.sleep(wait_time_seconds)
  logging.debug(f"waited: {wait_time_seconds} seconds")


def popup_privacy_onetime(page: any):
  """Clicks the reject button inside the privacy popup on first time page loading
  
      Parameters:
      browser (any): Browser window (e.g. chromium, firefox)
  """
  
  try:
    page.get_by_text("Reject All").click(timeout=100)
    logging.debug(f"privacy popup reject button clicked")
  except PlaywrightTimeoutError:
    logging.debug(f"privacy popup not visible or already saved in cookies, timeouterror")




def table_scrape(html): # csinálni + dokument

    soup = BeautifulSoup(html, 'html.parser')
    
    table = soup.select_one("table.detailed-table")
    table_rows = table.tbody.find_all('tr')
    #headers = table.thead.find_all('th')

    # FIXME levágja a szöveg végét 
    res = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text.strip() for tr in td if tr.text.strip()]
        if row:
            res.append(row)  
    logging.debug(res)   
    
    
    headers_table_wide = ["index", "team", "MP-T", "W-T", "D-T", "L-T", "GF-T", "GA-T", "MP-H", "W-H", "D-H", "L-H", "GF-H", "GA-H", "MP-A", "W-A", "D-A", "L-A", "GF-A", "GA-A", "GD", "P"]
    return headers_table_wide, res



def to_dataframe(html):
  
  
  headers, rows = table_scrape(html)
  # headers = []
  df_table_wide = pd.DataFrame(rows, columns=headers)
  df_table_wide.to_csv(r'./exported_data/test.csv', sep='\t', encoding='utf-8', index=False)
  
  df = df_table_wide.set_index('index')
  
  
  # Converts the dataframe into str object with formatting
  print(df.to_markdown())
  
  return 0

def main(debug_slow_down=0):
 with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=constans.BROWSER_DATA_DIR,
        headless=False,
        slow_mo=debug_slow_down,
        args=[
            f"--disable-extensions-except={constans.PATH_TO_EXTENSIONS+"/ublock_origin"}{","}{constans.PATH_TO_EXTENSIONS+"/adblock"}",
            f"--load-extension={constans.PATH_TO_EXTENSIONS+"/ublock_origin"}{","}{constans.PATH_TO_EXTENSIONS+"/adblock"}",
        ],
    )
    page = browser.new_page()

    page.route("**/*", rb.intercept_route)
    page.goto(constans.LINKS_2023_2024[0]) # TODO automatize scraping for all links
    #page.wait_for_timeout(1000)
   
    
    time_wait(0.5)
    popup_privacy_onetime(page)
    

    page.get_by_role("listitem").filter(has_text="Wide").click()
    time_wait(0.5)
        
    html = page.content()
    
    to_dataframe(html)
    
      
    # TODO tábla kattintás vissza gomb x20
    '''  
    for _ in range(20):
      page.get_by_text("Previous").click()'''
    

    # ide jön : csapat választás
    # ide jön : tábla választás
    # ide jön : scrape
    # ide jön : scrape adat lementés
    # automatizálás
    
    logging.debug(f"DONE")


    #time.sleep(0)
    browser.close()
   
   
if __name__ == "__main__":
  with debuglog.timed():
    main(debug_slow_down=0)