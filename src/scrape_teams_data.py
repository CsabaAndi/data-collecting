from bs4 import BeautifulSoup
from io import StringIO
from pathlib import Path  
import logging
import pandas as pd
from tabulate import tabulate


# TODO works | newest | aaaa
def team_match_history(html, test, test_team):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.select_one("table.matches")           
    data = pd.read_html(StringIO(str(table)))[0]
    tmp_df = pd.DataFrame(data)
    tmp_df.columns=["Date", "Competition", "Home team", "Score", "Away team", "delete1", "delete2"]
    tmp_df.drop(columns=['delete1', 'delete2'], inplace=True) # fölösleges oszlopok
    tmp_df.dropna(inplace=True) # üres sorok
    tmp_df["Score"] = tmp_df["Score"].apply(lambda x: x.replace(' ', ''))
    
    logging.debug(tabulate(tmp_df, headers = 'keys', tablefmt = 'psql'))

    return tmp_df



# TODO fix whole
def table_scrape_statistic(html): # TODO  dokument + list helyett map or dict / not important /

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.select("table.compare")[1]
    table_rows = table.tbody.find_all('tr')

    table_data = [] # FIXME 16 sor és 3 col , jelenleg nem stimmt
    table_headers = []
    for tr in table_rows:
        td = tr.find_all('td')
        th = tr.find_all('th')  
        header_in_row = [head.text.strip() for head in th if head.text.strip()]   # FIXME - ne list comp mert igy csak külön lista egy elemmel 
        row = [tr.text.strip() for tr in td if tr.text.strip()]
        if row:
            table_data.append(row)
        table_headers.append(header_in_row)  
    logging.debug(table_data)  
    
    headers_table_over_under = table_headers 
    return headers_table_over_under, table_data


# TODO fix whole
def scrape_charts(html): 

    soup = BeautifulSoup(html, 'html.parser')

    charts = soup.select_one("#charts")
    print(charts)

    charts_data = []

    headers_table_over_under = ["index", "team", "mp", "0", "1", "2", "3", "4", "5", "6", "7", ">7", "avg"]
    return headers_table_over_under, charts_data

def table_scrape_match_history_per_page(html): # TODO egész

    soup = BeautifulSoup(html, 'html.parser')

    table_match_history_page = soup.select_one("")

    headers_table_over_under = ["date", "competition", "team-1", "score", "team-2"]
    return headers_table_over_under, 
   
if __name__ == "__main__":
  pass