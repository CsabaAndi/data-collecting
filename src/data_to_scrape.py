from bs4 import BeautifulSoup
import logging


def table_scrape_last_games(html): # TODO  dokument + list helyett map or dict / not important /

    soup = BeautifulSoup(html, 'html.parser')
    
    table = soup.select_one("table.detailed-table")
    table_rows = table.tbody.find_all('tr')

    table_data = []

    for tr in table_rows:
        team_col = tr.find_all('td')[2].a.get('title').strip()
        last_5_col = [ last_5.text.strip() for last_5 in tr.find_all('td')[11].contents if last_5.text.strip()]
        table_data.append([team_col, last_5_col])  
    logging.debug(table_data) 

    
    headers_table_wide = ["Team", "last 5"]
    return headers_table_wide, table_data
    
    

def table_scrape_wide(html): # csinálni + dokument

    soup = BeautifulSoup(html, 'html.parser')
    
    table = soup.select_one("table.detailed-table")
    table_rows = table.tbody.find_all('tr')
    #headers = table.thead.find_all('th')

    # TODO refactor to list comp to make it faster
    table_data = []
    for tr in table_rows:
        td = tr.find_all('td')     
        row = []
        index = 0
        for item in td:
            if item.text.strip():
                if index == 2:
                    row.append(item.a.get('title').strip())
                else:
                    row.append(item.text.strip())
            index += 1   
        if row:
            table_data.append(row)  
    logging.debug(table_data)   
    
    
    headers_table_wide = ["index", "team", "MP-T", "W-T", "D-T", "L-T", "GF-T", "GA-T", "MP-H", "W-H", "D-H", "L-H", "GF-H", "GA-H", "MP-A", "W-A", "D-A", "L-A", "GF-A", "GA-A", "GD", "P"]
    return headers_table_wide, table_data

def table_scrape_topscorers(html): # TODO dokument + reduce reused code / not important / 
    '''
    top 15 scorers
    '''
    soup = BeautifulSoup(html, 'html.parser')
    
    table = soup.select_one("table.playerstats")
    table_rows = table.tbody.find_all('tr')
    #headers = table.thead.find_all('th')

    table_data = []
    for tr in table_rows:
        td = tr.find_all('td')     
        row = [tr.text.strip() for tr in td if tr.text.strip()]
        if row:
            table_data.append(row)  
    logging.debug(table_data)   

    
    headers_table_topscorers = ["Player", "team", "G", "P", "1st"]
    return headers_table_topscorers, table_data




if __name__ == "__main__":
    pass