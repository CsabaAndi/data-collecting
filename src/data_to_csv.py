import scrape_tables_data, scrape_teams_data
import pandas as pd


# TODO rename file 

# TODO többi leszedett táblázatot is átalakitani majd csv or json !!!
def html_to_dataframe(html, league_team="error", table_type="wide",date="3000"):
  match table_type:
    case "last": #TODO gut
      headers, rows = scrape_tables_data.table_scrape_last_games(html) 
    case "wide": #TODO gut 
      headers, rows = scrape_tables_data.table_scrape_wide(html)
    case "ou": #TODO gut
      headers, rows = scrape_tables_data.table_scrape_over_under(html) 
    case "top": #TODO gut
        headers, rows = scrape_tables_data.table_scrape_topscorers(html)
    case "team-stat": #TODO 
      headers, rows = scrape_teams_data.table_scrape_statistic(html)
    case "team-history": #TODO 
      #headers, rows = data_to_scrape_team.table_scrape_match_history_per_page(html)
      pass
    case _:
      pass # TODO | default --> last_5 and topscorer

  df_table = pd.DataFrame(rows, columns=headers)
  df_table.to_csv(f"../exported_data/{league_team}-{table_type}-{date}.csv", encoding='utf-8', index=False)
  
  df = df_table
    
  # TODO - delete | [test] Converts the dataframe into str object with formatting
  print(df.to_markdown())
  
  return 0


if __name__ == "__main__":
  pass