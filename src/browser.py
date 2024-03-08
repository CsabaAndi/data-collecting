from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import logging
import time
from resource_blocking_pkg import block as rb
import constans_pkg.constans as constans
import html_to_data_conversion


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
        league_team=index #TODO league or team name for output csv name:   
        
        page.route("**/*", rb.intercept_route)
        page.goto(constans.LINKS_2023_2024[index])
        #page.wait_for_timeout(1000)
      
        time_wait(0.5, msg="after page open")
        handle_privacy_popup(page)    
        time_wait(0.5)

        html_to_data_conversion.html_to_dataframe(html=page.content(), league_team=league_team, table_type="last")
        html_to_data_conversion.html_to_dataframe(html=page.content(), league_team=league_team, table_type="top")
        time_wait(2) 
        page.get_by_role("listitem").filter(has_text="Wide").click()
        time_wait(2) 
        html_to_data_conversion.html_to_dataframe(html=page.content(), league_team=league_team, table_type="wide")
        time_wait(2) 
        page.get_by_role("listitem").filter(has_text="Over/under").click()
        time_wait(2) 
        html_to_data_conversion.html_to_dataframe(html=page.content(), league_team=league_team, table_type="ou")
        
    logging.debug(f"DONE")
    #time_wait(1000000000000000)
    browser.close()


if __name__ == "__main__":
    pass