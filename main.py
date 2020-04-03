import requests
import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


if __name__ == "__main__":
  st.title('COVID-19 Analysis')

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
  df.columns = ['count', 'days']

  st.header('Patients Growth')
  st.write(df)

  def function(t, a, b):
    return a * np.exp(b * t)
    
  xdata = df['days']
  ydata = df['count']
  popt, pcov = curve_fit(lambda t,a,b: a * np.exp(b * t),  xdata,  ydata,  p0=(4, 0.1))

  st.header('Sweden Patients Count')  
  plt.plot(xdata, ydata, 'bo', label='data')
  plt.plot(xdata, function(xdata, *popt), '-', label='fit')
  plt.xlabel('x')
  plt.ylabel('y')
  plt.legend()
  st.pyplot()

  y_pred = function(97, *popt)
  st.write(y_pred)

