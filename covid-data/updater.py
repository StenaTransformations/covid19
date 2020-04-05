try:
  import unzip_requirements
except ImportError:
  pass

import os
import json
import boto3
import logging
import requests
import pandas as pd
from io import StringIO
from botocore.exceptions import ClientError

logger = logging.getLogger()
if logger.handlers:
  for handler in logger.handlers:
    logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

try:
  BUCKET_EXPORTS = os.environ['BUCKET_EXPORTS']
  PATIENTS_DATA = os.environ['PATIENTS_DATA']
except:
  logger.exception('failed to retrieve one or more env. vars')

ENDPOINT_DATA = r"https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv"
COLS_EXCLUDED = [
  'Province/State',
  'Country/Region',
  'Lat', 'Long'
]

def update(event, context):
  logger.info('-> updating csv file')
  content = requests.get(ENDPOINT_DATA).text
  df = pd.read_csv(StringIO(content))  
  df = df[(df['Country/Region'] == 'Sweden')]
  df = df.drop(COLS_EXCLUDED, axis=1).transpose()
  df['days'] = range(1, len(df) + 1)
  df = df.reset_index(drop=False)
  df.columns = ['date', 'count', 'days']

  s3_write_df(df)

  logger.info('-> DONE')
  return success()

def s3_write_df(df):
  csv_buffer = StringIO()
  df.to_csv(csv_buffer)
  s3 = boto3.resource('s3')
  logger.info('-> writing csv file')
  s3.Object(
    BUCKET_EXPORTS, PATIENTS_DATA
  ).put(Body=csv_buffer.getvalue())

def success():
  body = { "message": "csv data written successfully" }
  response = {
    "statusCode": 200,
    "headers": { "Access-Control-Allow-Origin": "*" },
    "body": json.dumps(body)
  }
  return response

