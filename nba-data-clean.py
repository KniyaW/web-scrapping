##Logan Lauton

##importing packages required for this dataset
import pandas as pd

##import csv to clean
df = pd.read_csv('NBA Player Stats(2004 - 2024).csv')

##removal of rows containing the column names
df = df[df['Player']!='Player']

##exporting as csv with same name to over write
df.to_csv('NBA Player Stats(2004 - 2024).csv', index = True)