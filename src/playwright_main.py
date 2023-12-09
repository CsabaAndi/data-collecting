from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import logging
# import argparse
import time
from debug_pkg.logs import log as debuglog
from resource_blocking_pkg import block as rb
import constans_pkg.constans as constans
import dataframes

# TODO mindent kiszervezni majd module/pkg  / not important /
''' TODO / not important /
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

def time_wait(wait_time_seconds: float, msg="no msg"):
  """Calls time.sleep(wait_time_seconds), then prints the debug log if logging is set to debug
  
      Parameters:
      wait_time_seconds (float): time to wait in seconds
      msg (str): message for the logger

  """
  time.sleep(wait_time_seconds)
  logging.debug(f"waited: {wait_time_seconds} seconds [{msg}]")


def popup_privacy_onetime(page: any):
  """Clicks the reject button inside the privacy popup on first time page loading
  
      Parameters:
      browser (any): Browser window (e.g. chromium, firefox)
  """
  
  try:
    page.get_by_role("button").filter(has_text="Reject All").click(timeout=100)
    logging.debug(f"privacy popup reject button clicked")
  except PlaywrightTimeoutError:
    logging.debug(f"privacy popup not visible or already saved in cookies, timeouterror")



def main(debug_slow_down=0): # TODO külön class browser-nek / not important /
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

    page.route("**/*", rb.intercept_route)
    page.goto(constans.LINKS_2023_2024[0]) # TODO automatize scraping for all links
    #page.wait_for_timeout(1000)
   

    time_wait(0.5, msg="after page open")
    popup_privacy_onetime(page)
       
       
    page.get_by_role("listitem").filter(has_text="Wide").click()
    time_wait(0.5)
        
    html = page.content()
    
    dataframes.to_dataframe(html)
    
      
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


    #time_wait(1000000000000000)
    browser.close()
   
   
if __name__ == "__main__":
  with debuglog.timed():
    main(debug_slow_down=0)