import data_to_scrape_tablepage, data_to_scrape_team
import pandas as pd


# TODO rename file 

# TODO többi leszedett táblázatot is átalakitani majd csv or json !!!
def html_to_dataframe(html, league_team="error", table_type="wide",date="3000"):
  wide=False
  match table_type:
    case "last": #TODO gut
      headers, rows = data_to_scrape_tablepage.table_scrape_last_games(html) 
    case "wide": #TODO gut
      headers, rows = data_to_scrape_tablepage.table_scrape_wide(html) 
      wide=True
    case "ou": #TODO gut
      headers, rows = data_to_scrape_tablepage.table_scrape_over_under(html) 
    case "top": #TODO gut
        headers, rows = data_to_scrape_tablepage.table_scrape_topscorers(html)
    case "team-stat": #TODO 
      headers, rows = data_to_scrape_team.table_scrape_statistic(html)
    case "team-history": #TODO 
      #headers, rows = data_to_scrape_team.table_scrape_match_history_per_page(html)
      pass
    case _:
      pass #default --> last_5 and topscorer

  #headers = []
  df_table = pd.DataFrame(rows, columns=headers)
  df_table.to_csv(f"../exported_data/{league_team}-{table_type}-{date}.csv", sep='\t', encoding='utf-8', index=False)
  
  if wide:
    df = df_table.set_index('index')
  else:
    df = df_table
    
  # Converts the dataframe into str object with formatting
  print(df.to_markdown())
  
  return 0


if __name__ == "__main__":
  pass