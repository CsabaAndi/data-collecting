from bs4 import BeautifulSoup
import logging



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
    #logging.debug(res)   
    
    
    headers_table_wide = ["index", "team", "MP-T", "W-T", "D-T", "L-T", "GF-T", "GA-T", "MP-H", "W-H", "D-H", "L-H", "GF-H", "GA-H", "MP-A", "W-A", "D-A", "L-A", "GF-A", "GA-A", "GD", "P"]
    return headers_table_wide, res


if __name__ == "__main__":
    pass