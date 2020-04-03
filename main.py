import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from modeller import write_model, read_model, function, predict
from updater import update_csv

if __name__ == "__main__":
  st.title('COVID-19 Analysis')

  update_csv()

  df = pd.read_csv('exports/data.csv')
  st.header('Patients Growth')
  st.write(df)

  # let's have write & read separated for the sake of demo.
  write_model()
  model = read_model()

  st.header('Sweden Patients Count')  
  xdata = df['days']
  ydata = df['count']
  plt.plot(xdata, ydata, 'bo', label='data')
  plt.plot(xdata, function(xdata, *model), '-', label='fit')
  plt.xlabel('x')
  plt.ylabel('y')
  plt.legend()
  st.pyplot()

  n = 2
  st.write(f'patients in {n} days: ', predict(2))
