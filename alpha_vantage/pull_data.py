import requests
from alpha_vantage import api_keys
# from api_keys import get_api_key
import pandas as pd

def generate_dfs(symbol, bollinger_range = 2, sma_range = 20):
  print(symbol)
  # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
  function = 'EARNINGS'
  url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_keys.get_api_key()}'
  r = requests.get(url)
  data = r.json()
  earnings_df = pd.DataFrame.from_records(data['quarterlyEarnings'])

  # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
  function = 'TIME_SERIES_DAILY'
  outputsize = 'full'
  url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_keys.get_api_key()}&outputsize={outputsize}'
  r = requests.get(url)
  data = r.json()
  tsdaily_df = pd.DataFrame.from_records(data['Time Series (Daily)']).transpose()

  for col in tsdaily_df.columns:
    tsdaily_df[col] = pd.to_numeric(tsdaily_df[col])
  tsdaily_df.index = pd.to_datetime(tsdaily_df.index)

  for col in earnings_df.columns[2:]:
    earnings_df[col] = pd.to_numeric(earnings_df[col], errors='coerce')
  for col in earnings_df.columns[:2]:
    earnings_df[col] = pd.to_datetime(earnings_df[col], errors='coerce')

  earnings_df = earnings_df.set_index('fiscalDateEnding').sort_index()
  pe_ratio_df = pd.merge_asof(earnings_df, tsdaily_df[['4. close']], left_index=True, right_index=True, direction='nearest').sort_index(ascending=False)
  pe_ratio_df['PE Ratio'] = pe_ratio_df['4. close']/pe_ratio_df['reportedEPS']/4
  pe_ratio_df['PE Ratio (SMA)'] = pe_ratio_df['4. close']/pe_ratio_df['reportedEPS']/4
  pe_ratio_df.index = pd.to_datetime(pe_ratio_df.index)
  ctr = 0
  for idx, row in pe_ratio_df.iterrows():
    try:
      pe_ratio_df.iloc[ctr,7] = (pe_ratio_df.iloc[ctr,6]+pe_ratio_df.iloc[ctr+1,6]+pe_ratio_df.iloc[ctr+2,6]+pe_ratio_df.iloc[ctr+3,6])/4
    except:
      print(ctr)
      break
    ctr += 1
  pe_ratio_df = pe_ratio_df.sort_index()

  tsdaily_df = tsdaily_df.sort_index(ascending=False)
  tsdaily_df['TP'] = (tsdaily_df['2. high']+tsdaily_df['3. low']+tsdaily_df['4. close'])/3
  tsdaily_df['S.D.'] = tsdaily_df['TP']
  tsdaily_df['SMA'] = tsdaily_df['TP']
  ctr = 0
  for idx, row in tsdaily_df.iterrows():
    try:
      tsdaily_df.iloc[ctr,6] = tsdaily_df.iloc[ctr:ctr+sma_range, 5].std()
      tsdaily_df.iloc[ctr,7] = tsdaily_df.iloc[ctr:ctr+sma_range, 5].mean()
    except:
      print(ctr)
      break
    ctr += 1
  tsdaily_df = tsdaily_df.sort_index()
  tsdaily_df['BOLU'] = tsdaily_df['SMA'] + bollinger_range * tsdaily_df['S.D.']
  tsdaily_df['BOLD'] = tsdaily_df['SMA'] - bollinger_range * tsdaily_df['S.D.']
  tsdaily_df['state'] = 0
  for idx, row in tsdaily_df.iterrows():
    if row['4. close'] < row['BOLD']:
      tsdaily_df.loc[idx,'state'] = -1
    elif row['4. close'] > row['BOLU']:
      tsdaily_df.loc[idx,'state'] = 1

  return tsdaily_df, pe_ratio_df

def pull_basic_data(symbol, function = 'OVERVIEW', freq = 'quarterlyReports'):
  # func_to_key = {'INCOME_STATEMENT':'quarterlyReports', 'BALANCE_SHEET':'quarterlyReports','CASH_FLOW':'quarterlyReports'}
  url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_keys.get_api_key()}'
  r = requests.get(url)
  data = r.json()
  
  if function == 'OVERVIEW':
    return data

  df = pd.DataFrame.from_records(data[freq])
  return df

def pull_metadata(symbol):
  url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol=AAPL&apikey={api_keys.get_api_key()}'
  r = requests.get(url)
  data = r.json()
  return data