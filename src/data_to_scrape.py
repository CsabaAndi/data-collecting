from bs4 import BeautifulSoup
import logging



def wide_table_scrape(html): # csinálni + dokument

    soup = BeautifulSoup(html, 'html.parser')
    
    table = soup.select_one("table.detailed-table")
    table_rows = table.tbody.find_all('tr')
    #headers = table.thead.find_all('th')

    # TODO refactor to list comp to make it faster
    res = []
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
            res.append(row)  
    logging.debug(res)   
    
    
    headers_table_wide = ["index", "team", "MP-T", "W-T", "D-T", "L-T", "GF-T", "GA-T", "MP-H", "W-H", "D-H", "L-H", "GF-H", "GA-H", "MP-A", "W-A", "D-A", "L-A", "GF-A", "GA-A", "GD", "P"]
    return headers_table_wide, res


if __name__ == "__main__":
    pass