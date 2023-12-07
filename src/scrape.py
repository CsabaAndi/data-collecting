from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import asyncio
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

async def time_wait(wait_time_seconds: float, bool_async: bool):
  """Waits x seconds, normal or async
  
      Parameters:
      wait_time_seconds (float): time to wait in seconds
      bool_async (bool): True --> async.sleep , False --> time.sleep

  """
  if bool_async is True:
    await asyncio.sleep(wait_time_seconds, result='done')
  time.sleep(wait_time_seconds)
  logging.debug(f"waited: {wait_time_seconds} seconds, async: {bool_async}")


async def popup_privacy_onetime(page: any):
  """Clicks the reject button inside the privacy popup on first time page loading
  
      Parameters:
      browser (any): Browser window (e.g. firefox)
  """
  
  try:
    await page.get_by_text("Reject All").click(timeout=100)
    logging.debug(f"privacy popup reject button clicked")
  except PlaywrightTimeoutError:
    logging.debug(f"privacy popup not visible or already saved in cookies, timeouterror")




async def table_scrape(html): # csinálni + dokument

    soup = BeautifulSoup(html, 'html.parser')
    
    table = soup.select_one("table.detailed-table")
    table_rows = table.tbody.find_all('tr')
    headers = table.thead.find_all('th')

    # levágja a nevet vagy mi 
    res = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text.strip() for tr in td if tr.text.strip()]
        if row:
            res.append(row)  
    logging.debug(res)   
    
    
    headers_table_wide = ["index", "team", "MP-T", "W-T", "D-T", "L-T", "GF-T", "GA-T", "MP-H", "W-H", "D-H", "L-H", "GF-H", "GA-H", "MP-A", "W-A", "D-A", "L-A", "GF-A", "GA-A", "GD", "P"]
    return headers_table_wide, res



async def to_dataframe(html):
  
  
  headers, rows = await table_scrape(html)
  # headers = []
  df_table_wide = pd.DataFrame(rows, columns=headers)
  df_table_wide.to_csv(r'./exported_data/test.csv', sep='\t', encoding='utf-8', index=False)
  
  df = df_table_wide.set_index('index')
  
  
  # Converts the dataframe into str object with formatting
  print(df.to_markdown())
  
  return 0

async def main(debug_slow_down=0):
 async with async_playwright() as p:
    browser = await p.chromium.launch_persistent_context(
        user_data_dir=constans.BROWSER_DATA_DIR,
        headless=False,
        slow_mo=debug_slow_down,
        args=[
            f"--disable-extensions-except={constans.PATH_TO_EXTENSIONS+"/ublock_origin"}{","}{constans.PATH_TO_EXTENSIONS+"/adblock"}",
            f"--load-extension={constans.PATH_TO_EXTENSIONS+"/ublock_origin"}{","}{constans.PATH_TO_EXTENSIONS+"/adblock"}",
        ],
    )
    page = await browser.new_page()

    await page.route("**/*", rb.intercept_route)
    await page.goto(constans.LINKS_2023_2024[0]) # todo
    #await page.wait_for_timeout(1000)
   
    
    await time_wait(0.5, False)
    await popup_privacy_onetime(page)
    

    await page.get_by_role("listitem").filter(has_text="Wide").click()
    await time_wait(0.5, False)
        
    html = await page.content()
    
    await to_dataframe(html)
    
      
    # tábla kattintás vissza gomb x20
    '''  
    for _ in range(20):
      await page.get_by_text("Previous").click()'''
    

    # ide jön : csapat választás
    # ide jön : tábla választás
    # ide jön : scrape
    # ide jön : scrape adat lementés
    # automatizálás
    
    logging.debug(f"DONE")
    #await asyncio.sleep(100000000)
    await asyncio.sleep(5) # excelbe irásra várás
    await browser.close()
   
   
if __name__ == "__main__":
  with debuglog.timed():
    asyncio.run(main(debug_slow_down=10))