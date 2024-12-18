## Importing necessary packages
from urllib.request import urlopen
from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import time

## Scrapes game scores for a single NFL season
def single_game_scores(season):
    """
    Scrapes game scores for a single NFL season.
    """
    url = f'https://www.pro-football-reference.com/years/{season}/games.htm'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    # Locate the games table
    table_html = BeautifulSoup(urlopen(url), 'html.parser').findAll('table')

    if table_html is None:
        print(f"No table found for season {season}")
        return pd.DataFrame()

    # Read table into a DataFrame
    df = pd.read_html(StringIO(str(table_html)))[0]

    # Clean up the DataFrame
    df = df.dropna(how='all')  # Drop rows with all NaN values
    df.insert(0, 'Season', season)  # Add the season column

    return df

def multiple_game_scores(start_year, end_year):
    """
    Scrapes game scores for multiple NFL seasons.
    """
    df = single_game_scores(start_year)
    for year in range(start_year + 1, end_year):
        time.sleep(4)  # Pause to avoid too many requests
        df = pd.concat([df, single_game_scores(year)], ignore_index=True)
    return df

# Call the function for seasons from 2004 to 2023 (end_year is exclusive)
df = multiple_game_scores(2004, 2024)

# Save to CSV
output_file = 'NFL_Game_Scores_2004_2023.csv'
df.to_csv(output_file, index=False)

print(f"Data saved to {output_file}")
