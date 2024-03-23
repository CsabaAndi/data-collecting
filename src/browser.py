from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import logging
import time
import urllib.parse
from resource_blocking_pkg import block as rb
import constans_pkg.constans as constans
import data_to_csv


# TODO mindent kiszervezni majd module/pkg  / not important /
# TODO team-stat / másik link - vagy kattintás után csapat
# TODO team-history / másik link - vagy kattintás után csapat
# TODO


def time_wait(wait_time_seconds: float, msg="no msg"):
  """Calls time.sleep(wait_time_seconds), then prints the debug log if logging is set to debug
  
      Parameters:
      wait_time_seconds (float): time to wait in seconds
      msg (str): message for the logger

  """
  
  time.sleep(wait_time_seconds)
  logging.debug(f"waited: {wait_time_seconds} seconds [{msg}]")


def handle_privacy_popup(page: any):
  """Clicks the reject button inside the privacy popup on first time page loading
  
      Parameters:
      browser (any): Browser window (e.g. chromium, firefox)
  """
  
  try:
    page.get_by_role("button").filter(has_text="Reject All").click(timeout=100)
    logging.debug(f"privacy popup reject button clicked")
  except PlaywrightTimeoutError:
    logging.debug(f"privacy popup not visible or already saved in cookies, timeouterror")


def main(debug_slow_down=0, league_size_for_debug=1): # TODO külön class browser-nek / not important /
  with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=constans.BROWSER_DATA_DIR,
        headless=False,
        slow_mo=debug_slow_down,
        # f"--disable-extensions-except={constans.PATH_TO_EXTENSIONS+"/ublock_origin"}{","}{constans.PATH_TO_EXTENSIONS+"/adblock"}"
        # f"--load-extension={constans.PATH_TO_EXTENSIONS+"/ublock_origin"}{","}{constans.PATH_TO_EXTENSIONS+"/adblock"}"
        args=[
            f"--disable-extensions-except={constans.PATH_TO_EXTENSIONS+"/ublock_origin"}",
            f"--load-extension={constans.PATH_TO_EXTENSIONS+"/ublock_origin"}",
        ],
    )
    page = browser.new_page()


    for index in range(0,(len(constans.LINKS_2023_2024)-11+league_size_for_debug)):
        parsed_link_list = list(filter(None, (urllib.parse.urlparse(constans.LINKS_2023_2024[index]).path.split('/')))) # TODO dont use constans links, use page current url
        
        page.route("**/*", rb.intercept_route)
        page.goto(constans.LINKS_2023_2024[index])
        
        #page.wait_for_timeout(1000)
      
        time_wait(0.5, msg="after page open")
        handle_privacy_popup(page)    
        time_wait(0.5)

        data_to_csv.html_to_dataframe(html=page.content(), table_type="last", link_data=parsed_link_list)
        data_to_csv.html_to_dataframe(html=page.content(), table_type="top", link_data=parsed_link_list)
        time_wait(2) 
        page.get_by_role("listitem").filter(has_text="Wide").click()
        time_wait(2) 
        data_to_csv.html_to_dataframe(html=page.content(), table_type="wide", link_data=parsed_link_list)
        time_wait(2) 
        page.get_by_role("listitem").filter(has_text="Over/under").click()
        time_wait(2) 
        data_to_csv.html_to_dataframe(html=page.content(), table_type="ou", link_data=parsed_link_list)
        
    logging.debug(f"DONE")
    #time_wait(1000000000000000)
    browser.close()


if __name__ == "__main__":
    pass