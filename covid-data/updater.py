import json

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
  s3_write(df)
  body = {
    "message": "patients.csv is created",
  }
  response = {
    "statusCode": 200,
    "headers": {
      'Access-Control-Allow-Origin': '*',
    },
    "body": json.dumps(body)
  }
  logger.info('-> DONE')
  return response

def s3_write_df(dataframe):
  csv_buffer = StringIO()
  dataframe.to_csv(csv_buffer)
  s3 = boto3.resource('s3')
  logger.info('-> writing csv file')
  s3.Object(
    BUCKET_EXPORTS, PATIENTS_DATA
  ).put(Body=csv_buffer.getvalue())
