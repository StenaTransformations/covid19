try:
  import unzip_requirements
except ImportError:
  pass

import os
import json
import boto3
import logging
import numpy as np
import pandas as pd
from io import StringIO
from ast import literal_eval
from scipy.optimize import curve_fit
from botocore.exceptions import ClientError

logger = logging.getLogger()
if logger.handlers:
  for handler in logger.handlers:
    logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

try:
  BUCKET_EXPORTS = os.environ['BUCKET_EXPORTS']
  PATIENTS_DATA = os.environ['PATIENTS_DATA']
  PATIENTS_MODEL = os.environ['PATIENTS_MODEL']
except:
  logger.exception('failed to retrieve one or more env. vars')

S3 = boto3.resource('s3')

def create(event, context):
  logger.info('-> BEGIN - create')
  df = read_data()
  xdata = df['days']
  ydata = df['count']
  popt, pcov = curve_fit(
    function,  
    xdata,  
    ydata,
    p0=(4, 0.01)
  )
  write_model(popt)
  logger.info('-> END - create')

def function(t, a, b):
  return a * np.exp(b * t)

def read_data():
  logger.info('-> reading csv file')
  obj = S3.Object(BUCKET_EXPORTS, PATIENTS_DATA)
  body = obj.get()['Body'].read().decode('utf-8')
  return pd.read_csv(StringIO(body))

def write_model(ndarray):
  logger.info(f'-> persisting ndarray {ndarray}')
  model = np.array2string(ndarray, separator=',')
  S3.Object(BUCKET_EXPORTS, PATIENTS_MODEL).put(Body=model)

def read_model():
  logger.info('-> reading ndarray from file')
  obj = S3.Object(BUCKET_EXPORTS, PATIENTS_MODEL)
  body = obj.get()['Body'].read().decode('utf-8')
  return np.array(literal_eval(body))

def predict(event, context):
  logger.info('-> BEGIN - predict')
  days = int(event['queryStringParameters']['days'])
  logger.info(f'-> predicting patients in {days} days')
  if days < 1:
    days = 1
  df = read_data()
  total = df.shape[0]
  model = read_model()
  when = total + days
  count = function(when, *model)
  body = {
    "message": f'estimating {int(count)} patients in {days} days.',
  }
  response = {
    "statusCode": 200,
    "headers": {
      'Access-Control-Allow-Origin': '*',
    },
    "body": json.dumps(body)
  }
  logger.info('-> END - predict')
  return response


if __name__ == "__main__":
  create('', '')