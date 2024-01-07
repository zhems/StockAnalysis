import datetime
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from alpha_vantage.calculate_metrics import create_buy_sell_pairs, generate_bollinger_returns
import plotly.graph_objects as go

def plot_graph(tsdaily_dfs, pe_ratio_dfs, symbol, start_date = '2021-01-01', end_date = datetime.date.today()):
  step = 30
  fig = make_subplots(specs=[[{"secondary_y": True}]])

  if isinstance(tsdaily_dfs, dict) :
    tsdaily_df = tsdaily_dfs[symbol].loc[start_date: end_date]
  else:
    tsdaily_df = tsdaily_dfs.loc[start_date: end_date]
  if isinstance(pe_ratio_dfs, dict):
    pe_ratio_df = pe_ratio_dfs[symbol].loc[start_date: end_date]
  else:
    pe_ratio_df = pe_ratio_dfs.loc[start_date: end_date]

  # Add traces
  fig.add_trace(go.Scatter(x=tsdaily_df.index, y=tsdaily_df['4. close'], name="Daily Price"),secondary_y=False,)
  fig.add_trace(go.Scatter(x=tsdaily_df.index, y=tsdaily_df['SMA'], name="Mid"),secondary_y=False,)
  fig.add_trace(go.Scatter(x=tsdaily_df.index, y=tsdaily_df['BOLU'], name="Upper"),secondary_y=False,)
  fig.add_trace(go.Scatter(x=tsdaily_df.index, y=tsdaily_df['BOLD'], name="Lower"),secondary_y=False,)


  # Add traces
  fig.add_trace(go.Scatter(x=pe_ratio_df.index, y=pe_ratio_df['PE Ratio'], name="PE"),secondary_y=True,)
  fig.add_trace(go.Scatter(x=pe_ratio_df.index, y=pe_ratio_df['PE Ratio (SMA)'], name="PE (SMA)"),secondary_y=True,)

  bsp = create_buy_sell_pairs(tsdaily_dfs, symbol,start_date, end_date)
  for b,s in bsp:
    fig.add_trace(go.Scatter(x=(b[0], s[0]), y=(b[1], s[1]), name="Daily Price",showlegend=False,line_color='#000000'),secondary_y=False)

  # Add figure title
  fig.update_layout(title_text=f"{symbol}: {generate_bollinger_returns(bsp):.2f}")

  # Set x-axis title
  fig.update_xaxes(title_text="Time")

  # Set y-axes titles
  fig.update_yaxes(title_text="<b>Stock Price</b>", secondary_y=False)
  fig.update_yaxes(title_text="<b>PE Ratio</b>", secondary_y=True)

  fig.show()