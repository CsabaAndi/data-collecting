import data_to_scrape_tablepage, data_to_scrape_team
import pandas as pd


# TODO többi leszedett táblázatot is átalakitani majd csv or json !!!

def to_dataframe(html):
  
  headers, rows = data_to_scrape_tablepage.table_scrape_wide(html) 
  # headers = []
  df_table_wide = pd.DataFrame(rows, columns=headers)
  df_table_wide.to_csv(r'../exported_data/miez.csv', sep='\t', encoding='utf-8', index=False)
  
  wide=True
  if wide:
    df = df_table_wide.set_index('index')
  else:
    df = df_table_wide
  
  # Converts the dataframe into str object with formatting
  print(df.to_markdown())
  
  return 0


if __name__ == "__main__":
  pass