import datetime

def create_buy_sell_pairs(tsdaily_dfs, symbol, start_date = '2019-01-01', end_date = datetime.date.today()):
  curr_state = 0
  buy_sell_pairs = []
  curr_buy = None
  for idx, row in tsdaily_dfs[symbol][start_date:end_date].iterrows():
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