##importing packages needed for scrape
from urllib.request import urlopen
from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import time

##code below grabbed from https://raihanafiandi.medium.com/scraping-basketball-reference-data-using-python-f321c3f2903e
def single(season):
    url = f'https://www.pro-football-reference.com/years/{season}/kicking.htm'
    table_html = BeautifulSoup(urlopen(url), 'html.parser').findAll('table')
    df = pd.read_html(StringIO(str(table_html)))[0]

    df.columns = ['_'.join(col).strip() for col in df.columns.values]

    if 'Rk' in df.columns:
        df = df.drop(columns=['Rk'])

    # Find player column dynamically
    player_col = next((col for col in df.columns if 'Player' in col), None)
    if player_col:
        df[player_col] = df[player_col].str.replace('*', '')
    # ... handle the case if no player column as you see fit


    df.insert(0, 'Season', season)
    df = df.apply(pd.to_numeric, errors='coerce').fillna(df)
    return df


##function taken from same link above, altered to sleep to avoid too many requests error 
def multiple(start_year, end_year):
    df = single(start_year)
    for year in range(start_year + 1, end_year):  # More efficient looping
        time.sleep(4)
        df = pd.concat([df, single(year)], ignore_index=True)  # Use concat
    return df

##calling for all NFL seasons data except current(1949-50 until 2021-22) as current season is not yet finished
df = multiple(2004, 2024)

# More robust filtering to remove repeated headers

# 1. Find the player column name
player_col = next((col for col in df.columns if 'Player' in col), None)

# 2. Filter if the player column exists AND contains "Player" values
if player_col:
    df = df[df[player_col] != 'Player']

# Save to CSV
output_file = 'NFL Kicker Player Stats(2004 - 2024).csv'
df.to_csv(output_file, index=False)

print(f"Data saved to {output_file}")