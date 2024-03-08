from bs4 import BeautifulSoup
import logging

#TODO [All func] dokument + list helyett map or dict / not important /

def table_scrape_last_games(html): 
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
    

def table_scrape_wide(html): 
    soup = BeautifulSoup(html, 'html.parser')
    
    table = soup.select_one("table.detailed-table")
    table_rows = table.tbody.find_all('tr')

    table_data = []
    for tr in table_rows:
        td = tr.find_all('td')  
        row = [col.text.strip() for col in td if col.text.strip()]
        row[1] = td[2].a.get('title').strip() # TODO merge with the list comp above
        table_data.append(row)      
    logging.debug(table_data)   
    
    
    headers_table_wide = ["rank", "team", "MP-T", "W-T", "D-T", "L-T", "GF-T", "GA-T", "MP-H", "W-H", "D-H", "L-H", "GF-H", "GA-H", "MP-A", "W-A", "D-A", "L-A", "GF-A", "GA-A", "GD", "P"]
    return headers_table_wide, table_data

def table_scrape_topscorers(html): 
    '''
    top 15 scorers
    '''
    soup = BeautifulSoup(html, 'html.parser')
    
    table = soup.select_one("table.playerstats")
    table_rows = table.tbody.find_all('tr')

    table_data = []
    for tr in table_rows:
        td = tr.find_all('td')     
        row = [col.text.strip() for col in td if col.text.stri()]
        table_data.append(row)  
    logging.debug(table_data)   

    
    headers_table_topscorers = ["Player", "team", "G", "P", "1st"]
    return headers_table_topscorers, table_data


def table_scrape_over_under(html): 
    soup = BeautifulSoup(html, 'html.parser')
    #page_competition_1_block_competition_tables_11_block_competition_overunder_table_1_table
    table = soup.select_one("table.overundertable")
    table_rows = table.tbody.find_all('tr')

    
    table_data = []
    for tr in table_rows:
        td = tr.find_all('td')  
        row = [col.text.strip() for col in td if col.text.strip()]
        row[1] = td[1].a.text.strip() # TODO merge with the list comp above
        table_data.append(row)      
    logging.debug(table_data)   

    
    headers_table_over_under = ["rank", "team", "mp", "0", "1", "2", "3", "4", "5", "6", "7", ">7", "avg"]
    return headers_table_over_under, table_data
    

if __name__ == "__main__":
    pass