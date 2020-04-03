import pandas as pd
import numpy as np
from ast import literal_eval
from scipy.optimize import curve_fit

def write_model():
  df = pd.read_csv('exports/data.csv')
  xdata = df['days']
  ydata = df['count']
  popt, pcov = curve_fit(function, xdata, ydata, p0=(4, 0.1))
  model = np.array2string(popt, separator=',')
  with open("exports/model.txt", "w") as file:
    file.write(model)

def read_model():
  data = ''
  with open('exports/model.txt', 'r') as file:
    data = file.read().replace('\n', '')
  return np.array(literal_eval(data))

def function(t, a, b):
  return a * np.exp(b * t)

def predict(days=1):
  if days < 1:
    days = 1
  df = pd.read_csv('exports/data.csv')
  total_count = df.shape[0]
  model = read_model()
  when = total_count + days
  return function(when, *model)
