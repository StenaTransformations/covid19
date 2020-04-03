import os
import requests
from io import StringIO
import pandas as pd

def update_csv():
  url = r"https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv"
  content = requests.get(url).text
  df = pd.read_csv(StringIO(content))  
  df = df[(df['Country/Region'] == 'Sweden')]
  excludes = [
    'Province/State',
    'Country/Region',
    'Lat', 'Long'
  ]
  df = df.drop(excludes, axis=1).transpose()
  df['days'] = range(1, len(df) + 1)
  df = df.reset_index(drop=False)
  df.columns = ['date', 'count', 'days']
  if not os.path.exists('exports'):
    os.makedirs('exports')
  df.to_csv('exports/data.csv', encoding='utf-8')
