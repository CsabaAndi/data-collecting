import data_to_scrape_tablepage, data_to_scrape_team
import pandas as pd


# TODO többi leszedett táblázatot is átalakitani majd csv or json !!!
def html_to_dataframe(html, table_type='wide'):
  wide=False
  match table_type:
    case "last":
      headers, rows = data_to_scrape_tablepage.table_scrape_last_games(html) 
    case "wide":
      headers, rows = data_to_scrape_tablepage.table_scrape_wide(html) 
      wide=True
    case "ou":
      headers, rows = data_to_scrape_tablepage.table_scrape_over_under(html) 
    case "team-stat":
      headers, rows = data_to_scrape_team.table_scrape_statistic(html)
    case "team-history":
      #headers, rows = data_to_scrape_team.table_scrape_match_history_per_page(html)
      pass
    case _:
      pass #default --> last_5 and topscorer

  # headers = []
  df_table = pd.DataFrame(rows, columns=headers)
  df_table.to_csv(r'../exported_data/miez.csv', sep='\t', encoding='utf-8', index=False)
  
  if wide:
    df = df_table.set_index('index')
  else:
    df = df_table
    
  # Converts the dataframe into str object with formatting
  print(df.to_markdown())
  
  return 0


if __name__ == "__main__":
  pass