import datetime

def create_buy_sell_pairs(tsdaily_dfs, symbol, start_date = '2019-01-01', end_date = datetime.date.today()):
  curr_state = 0
  buy_sell_pairs = []
  curr_buy = None
  if isinstance(tsdaily_dfs,dict):
    df = tsdaily_dfs[symbol][start_date:end_date]
  else:
    df = tsdaily_dfs[start_date:end_date]
  for idx, row in df.iterrows():
    if row['state'] == -1 and curr_state == 0:
      curr_buy = (idx,row['4. close'])
      curr_state = -1
    elif row['state'] == 1 and curr_state == -1:
      curr_sell = (idx,row['4. close'])
      buy_sell_pairs.append((curr_buy,curr_sell))
      curr_state = 0
  return buy_sell_pairs
def generate_bollinger_returns(buy_sell_pair):
  return sum([s[1] for b,s in buy_sell_pair]) - sum([b[1] for b,s in buy_sell_pair])

def modify_bollinger_sd(df, bollinger_range = 2):
  df = df.copy().sort_index()
  df['BOLU'] = df['SMA'] + bollinger_range * df['S.D.']
  df['BOLD'] = df['SMA'] - bollinger_range * df['S.D.']
  df['state'] = 0
  for idx, row in df.iterrows():
    if row['4. close'] < row['BOLD']:
      df.loc[idx,'state'] = -1
    elif row['4. close'] > row['BOLU']:
      df.loc[idx,'state'] = 1
  return df