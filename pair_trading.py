# -*- coding: utf-8 -*-
"""Pair Trading.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JcmCesA7KIbE4jdS6bCwLcnYUYIh_buw
"""

!pip install yfinance

import pandas as pd
import numpy as np
import yfinance as yf
from google.colab import files
from datetime import datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import coint, adfuller
from scipy.stats import pearsonr
import statistics

data = yf.download('HDFCBANK.NS', start="2022-01-01", end="2022-01-31")
data.head()
data['Moving_average'] = data['Close'].rolling(window=20,min_periods=1,center=False).mean()
data.tail(20)

data[['Close', 'Moving_average']].plot()

# MOVING AVERAGE STRATEGY


Stock = "RELIANCE.NS"
data = yf.download(Stock, start="2021-01-01", end="2023-12-31")


T3 = pd.DataFrame({"Close": data["Close"]})
T3['Year'] = T3.index.year


T2 = pd.DataFrame(columns=["cumpnl_long", "cumpnl_short", "cumpnl", "SMA", "LMA", "Stock", "Year"])


for z in range(2021, 2024):
    T = T3[T3.Year == z].dropna()
    for x in range(1, 35, 2):
        for y in range(x, 35, 2):
            SMA = x
            LMA = y


            T['Short_average'] = T['Close'].rolling(window=SMA, min_periods=1).mean()
            T['Long_average'] = T['Close'].rolling(window=LMA, min_periods=1).mean()


            T['long_entry'] = T['Short_average'] > T['Long_average']
            T['long_exit'] = T['Short_average'] <= T['Long_average']
            T['positions_long'] = np.nan
            T.loc[T.long_entry, 'positions_long'] = 1
            T.loc[T.long_exit, 'positions_long'] = 0
            T.positions_long = T.positions_long.fillna(method='ffill')

            T['short_entry'] = T['Short_average'] < T['Long_average']
            T['short_exit'] = T['Short_average'] >= T['Long_average']
            T['positions_short'] = np.nan
            T.loc[T.short_entry, 'positions_short'] = -1
            T.loc[T.short_exit, 'positions_short'] = 0
            T.positions_short = T.positions_short.fillna(method='ffill')


            T['price_difference'] = T['Close'] - T['Close'].shift(1)
            T['pnllong'] = T.positions_long.shift(1) * T.price_difference
            T['pnlshort'] = T.positions_short.shift(1) * T.price_difference
            T['pnl'] = T['pnllong'] + T['pnlshort']
            T['cumpnl_long'] = T.pnllong.cumsum()
            T['cumpnl_short'] = T.pnlshort.cumsum()
            T['cumpnl'] = T.pnl.cumsum()


            T1 = T[['cumpnl_short', 'cumpnl_long', 'cumpnl']].tail(1)
            T1['SMA'] = SMA
            T1['LMA'] = LMA
            T1['Stock'] = Stock
            T1['Year'] = z
            T2 = pd.concat([T2, T1], ignore_index=True)

print(T2)

Pivot_Table1 = pd.pivot_table(T2, values ='cumpnl', index =['SMA', 'LMA'],
columns =['Year'], aggfunc = np.sum)
print (Pivot_Table1)
# Download of results in Excel
Pivot_Table1.to_csv("PV_T.csv", index=True, encoding='utf8')
from google.colab import files
files.download('PV_T.csv')

data['return'] = data['Close'].pct_change()
plt.hist(data['return'], bins=[-1,0,1])

import yfinance as yf
import numpy as np


nifty_50_tickers = [
    'ADANIPORTS.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS',
    'BAJAJFINSV.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'BRITANNIA.NS', 'CIPLA.NS',
    'COALINDIA.NS', 'DIVISLAB.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GRASIM.NS',
    'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS',
    'HINDALCO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS', 'INFY.NS',
    'IOC.NS', 'ITC.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LT.NS',
    'M&M.NS', 'MARUTI.NS', 'NESTLEIND.NS', 'NTPC.NS', 'ONGC.NS',
    'POWERGRID.NS', 'RELIANCE.NS', 'SBILIFE.NS', 'SBIN.NS', 'SUNPHARMA.NS',
    'TCS.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS', 'TECHM.NS',
    'TITAN.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'WIPRO.NS'
]


def calculate_signals(ticker):
    data = yf.download(ticker, start="2021-01-01", end="2023-12-31")

    if data.empty:
        return {
            'Ticker': ticker,
            'TradingDays': 0,
            'TotalSignal': 0,
            'Probability': 0,
            'TotalProfit': 0
        }

    data['buysignal'] = np.where((data['Open'] > data['Close'].shift(+1)) &
                                 (data['Close'] > data['Close'].shift(+1)), 1.0, 0.0)
    data['sellsignal'] = np.where((data['Open'] < data['Close'].shift(+1)) &
                                  (data['Close'] < data['Close'].shift(+1)), -1.0, 0.0)

    data['buyqty'] = np.where((data['Low'] < data['Close'].shift(+1)),
                              (data['Close'] - data['Close'].shift(+1)) * data['buysignal'], 0.0)
    data['sellqty'] = np.where((data['High'] > data['Close'].shift(+1)),
                               (data['Close'].shift(+1) - data['Close']) * (data['sellsignal'] * -1), 0.0)
    data['profit'] = data['buyqty'] + data['sellqty']

    TotalSignal = data['buysignal'].sum() + (data['sellsignal'].sum() * -1)
    Tradingdays = data['Close'].count()
    prob = (TotalSignal / Tradingdays) * 100
    TotalProfit = data['profit'].sum()

    return {
        'Ticker': ticker,
        'TradingDays': Tradingdays,
        'TotalSignal': TotalSignal,
        'Probability': prob,
        'TotalProfit': TotalProfit
    }


results = [calculate_signals(ticker) for ticker in nifty_50_tickers]


filtered_results = [result for result in results if result['Probability'] > 60]


for result in filtered_results:
    print(f"Ticker: {result['Ticker']}")
    print(f"Trading Days: {result['TradingDays']}")
    print(f"Total Signal: {result['TotalSignal']}")
    print(f"Probability: {result['Probability']:.2f}%")
    print(f"Total Profit: {result['TotalProfit']:.2f}\n")

data['Close'].hist(bins=100, figsize=(8, 6))

data = yf.download('HDFCBANK.NS', start="2021-01-01", end="2023-12-31")


data['Moving_average'] = data['Close'].rolling(window=10, min_periods=1).mean()


data['Stdav'] = data['Close'].rolling(window=10, min_periods=1).std()


data['Upper_Band'] = data['Moving_average'] + (data['Stdav'] * 1.5)
data['Lower_Band'] = data['Moving_average'] - (data['Stdav'] * 1.5)


print(data[['Close', 'Moving_average', 'Stdav', 'Upper_Band', 'Lower_Band']].tail(10))

data[['Close', 'Moving_average', 'Upper_Band', 'Lower_Band']].plot(figsize=
(18,6))

Stock = "HDFCBANK.NS"
data = yf.download(Stock, start="2021-01-01", end="2023-12-31")


T3 = pd.DataFrame({"Close": data["Close"]})
T3['Year'] = T3.index.year


T2 = pd.DataFrame(columns=["cumpnl", "MA", "STD", "Stock", "Year"])


for z in range(2021, 2024):
    T = T3[T3.Year == z].dropna()


    for x in range(1, 37, 2):
        for y in range(1, 3, 1):
            MA = x
            STD = y


            T['moving_average'] = T.Close.rolling(MA).mean()
            T['moving_std_dev'] = T.Close.rolling(MA).std()
            T['upper_band'] = T.moving_average + (T.moving_std_dev * STD)
            T['lower_band'] = T.moving_average - (T.moving_std_dev * STD)


            T['long_entry'] = T.Close < T.lower_band
            T['long_exit'] = T.Close >= T.moving_average
            T['positions_long'] = np.nan
            T.loc[T.long_entry, 'positions_long'] = 1
            T.loc[T.long_exit, 'positions_long'] = 0
            T.positions_long = T.positions_long.fillna(method='ffill')


            T['short_entry'] = T.Close > T.upper_band
            T['short_exit'] = T.Close <= T.moving_average
            T['positions_short'] = np.nan
            T.loc[T.short_entry, 'positions_short'] = -1
            T.loc[T.short_exit, 'positions_short'] = 0
            T.positions_short = T.positions_short.fillna(method='ffill')


            T['positions'] = T.positions_long + T.positions_short


            T['price_difference'] = T.Close - T.Close.shift(1)
            T['pnl'] = T.positions.shift(1) * T.price_difference
            T['cumpnl'] = T.pnl.cumsum()


            T1 = T[['cumpnl']].tail(1)
            T1['MA'] = MA
            T1['STD'] = STD
            T1['Stock'] = Stock
            T1['Year'] = z
            T2 = pd.concat([T2, T1], ignore_index=True)


T2.to_csv("PV_T.csv", index=True, encoding='utf8')


files.download('PV_T.csv')

from scipy.stats import pearsonr
import yfinance as yf

data = yf.download('RELIANCE.NS',start="2021-01-01", end="2023-12-31")
data1 = yf.download('^NSEI', start="2021-01-01", end="2023-12-31")
corr = pearsonr(data['Close'], data1['Close'])
print(corr)

from matplotlib import pyplot
pyplot.scatter(data['Close'], data1['Close'])
pyplot.show()

fig,ax = plt.subplots(figsize=(18,6))
ax.plot(data['Close'], color="red")
ax2=ax.twinx()
ax2.plot(data1['Close'],color="blue")
plt.show()

import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np
import yfinance as yf
from google.colab import files

data = yf.download('RELIANCE.NS', start="2021-01-01", end="2023-12-31")
data1 = yf.download('HDFCBANK.NS',start="2021-01-01", end="2023-12-31")

(data['Close'] - data1['Close']).plot(figsize=(18,6))
plt.axhline((data['Close'] - data1['Close']).mean(), color='red', linestyle='--')
plt.xlabel('Time')
plt.legend(['Price Difference', 'Mean'])
plt.show()

from statsmodels.tsa.stattools import adfuller
adf = adfuller(data['Close']-data1['Close'], maxlag = 1)
print (adf[0])
print (adf[1])
print (adf[4])

prices_df = pd.DataFrame({"Stock_1": data["Close"], "Stock_2": data1["Close"]})
prices_df['Diff'] = prices_df['Stock_1'] - prices_df['Stock_2']
prices_df[['Stock_1', 'Stock_2', 'Diff']].plot(grid=True, secondary_y='Diff', figsize=(14,6))

prices_df['moving_average'] = prices_df.Diff.rolling(5).mean()
prices_df['moving_std_dev'] = prices_df.Diff.rolling(5).std()
prices_df['upper_band'] = prices_df.moving_average + prices_df.moving_std_dev
prices_df['lower_band'] = prices_df.moving_average - prices_df.moving_std_dev

prices_df[['Diff', 'moving_average', 'upper_band', 'lower_band']].plot(figsize=(16,6))

import plotly.express as px
Table = prices_df[['Diff', 'moving_average', 'upper_band', 'lower_band']]
fig = px.line(Table)
fig.show()

#"Bollinger Bands Momentum Crossover Strategy
prices_df['long_entry'] = prices_df.Diff < prices_df.lower_band
prices_df['long_exit'] = prices_df.Diff >= prices_df.moving_average
prices_df['positions_long'] = np.nan
prices_df.loc[prices_df.long_entry,'positions_long'] = 1
prices_df.loc[prices_df.long_exit,'positions_long'] = 0
prices_df.positions_long = prices_df.positions_long.fillna(method='ffill')
prices_df['short_entry'] = prices_df.Diff > prices_df.upper_band
prices_df['short_exit'] = prices_df.Diff <= prices_df.moving_average
prices_df['positions_short'] = np.nan
prices_df.loc[prices_df.short_entry,'positions_short'] = -1
prices_df.loc[prices_df.short_exit,'positions_short'] = 0
prices_df.positions_short = prices_df.positions_short.fillna(method='ffill')
prices_df['positions'] = prices_df.positions_long + prices_df.positions_short
prices_df['price_difference']= prices_df.Diff - prices_df.Diff.shift(1)
prices_df['pnl'] = prices_df.positions.shift(1) * prices_df.price_difference
prices_df['cumpnl'] = prices_df.pnl.cumsum()
prices_df[['cumpnl']].plot(figsize=(16,8))

#Multi-Asset Cointegration and Correlation Analysis


data = yf.download('^NSEI', start="2021-01-01", end="2023-12-31")
data1 = yf.download('HDFCBANK.NS', start="2021-01-01", end="2023-12-31")
data2 = yf.download('ICICIBANK.NS', start="2021-01-01", end="2023-12-31")
data3 = yf.download('KOTAKBANK.NS', start="2021-01-01", end="2023-12-31")
data4 = yf.download('INDUSINDBK.NS', start="2021-01-01", end="2023-12-31")
data5 = yf.download('AXISBANK.NS', start="2021-01-01", end="2023-12-31")


abc = ["NSEI", "HDFCBK", "ICICIBK", "KOTAKBK", "INDUSINDBK", "AXISBK"]
prices_df = pd.DataFrame({
    "NSEI": data["Close"],
    "HDFCBK": data1["Close"],
    "ICICIBK": data2["Close"],
    "KOTAKBK": data3["Close"],
    "INDUSINDBK": data4["Close"],
    "AXISBK": data5["Close"]
})


for aa in range(len(abc)):
    for bb in range(aa + 1, len(abc)):
        Cointegration = coint(prices_df[abc[aa]], prices_df[abc[bb]])[0]
        correlation = pearsonr(prices_df[abc[aa]], prices_df[abc[bb]])[0]
        ADF = adfuller(prices_df[abc[aa]] - prices_df[abc[bb]], maxlag=1)[1]
        print(f"{abc[aa]} and {abc[bb]}: Cointegration = {Cointegration}, Correlation = {correlation}, ADF p-value = {ADF}")

# Commented out IPython magic to ensure Python compatibility.
#Z-Score Momentum Strategy
import yfinance as yf
from scipy.stats import pearsonr
from numpy import mean, std
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import statsmodels.api as sm


# %matplotlib inline

data = yf.download('^NSEI', start="2021-01-01", end="2023-12-31")
data1 = yf.download('HDFCBANK.NS', start="2021-01-01", end="2023-12-31")
data2 = yf.download('ICICIBANK.NS', start="2021-01-01", end="2023-12-31")
data3 = yf.download('KOTAKBANK.NS', start="2021-01-01", end="2023-12-31")
data4 = yf.download('INDUSINDBK.NS', start="2021-01-01", end="2023-12-31")
data5 = yf.download('AXISBANK.NS', start="2021-01-01", end="2023-12-31")


prices_df = pd.DataFrame({
    "^NSEI": data["Close"],
    "HDFCBK": data1["Close"],
    "ICICIBK": data2["Close"],
    "KOTAKBK": data3["Close"],
    "INDUSINDBK": data4["Close"],
    "AXISBK": data5["Close"]
})


prices_df.dropna(inplace=True)

abc = ["^NSEI", "HDFCBK", "ICICIBK", "KOTAKBK", "INDUSINDBK", "AXISBK"]


for x in range(len(abc)):
    for y in range(x, len(abc)):
        if x == y:
            continue
        adf_pvalue = adfuller(prices_df[abc[x]] - prices_df[abc[y]], maxlag=1)[1]
        print(abc[x], abc[y], "ADF", adf_pvalue)

def Zscore(X):
    return np.array((X - np.mean(X)) / np.std(X))

stocks = 6
capital = 10000
components = 1
max_pos = 1
S1 = []
L1 = []
i1 = []
pnls = []
dates = []

for i in range(len(prices_df)):
    if i < 10:
        continue
    prices = prices_df.iloc[0:i]
    pr = np.asarray(prices.T)
    pca = PCA(n_components=components)
    comps = pca.fit(pr.T).components_.T
    factors = sm.add_constant(pr.T.dot(comps))
    mm = [sm.OLS(s.T, factors).fit() for s in pr]
    resids = list(map(lambda x: x.resid, mm))
    zs = {}
    for inst in range(stocks):
        zs[inst] = Zscore(resids[inst])[-1]
    idx_long = np.argsort([zs[j] for j in zs])[:max_pos].item()
    idx_short = np.argsort([zs[j] for j in zs])[-max_pos:].item()
    L1.append(abc[idx_long])
    S1.append(abc[idx_short])
    dates.append(prices_df.index[i])
    i1.append(i)

df = pd.DataFrame(i1, index=dates)
df['Long'] = L1
df['Short'] = S1
df = df.join(prices_df)
df['Long_P'] = 0.0
df['Short_P'] = 0.0
df['Profit'] = 0.0
df['Total_Profit'] = 0.0


for x in range(len(df) - 1):
    y = x + 1
    a = df['Long'][x]
    b = df['Short'][x]
    if df.loc[df.index[y], a] != 0 and df.loc[df.index[x], a] != 0:
        df.loc[df.index[x], 'Long_P'] = (df.loc[df.index[y], a] - df.loc[df.index[x], a]) * (round(capital / df.loc[df.index[x], a]))
    if df.loc[df.index[x], b] != 0 and df.loc[df.index[y], b] != 0:
        df.loc[df.index[x], 'Short_P'] = (df.loc[df.index[x], b] - df.loc[df.index[y], b]) * (round(capital / df.loc[df.index[x], b]))
    df.loc[df.index[x], 'Profit'] = df.loc[df.index[x], 'Long_P'] + df.loc[df.index[x], 'Short_P']
    df.loc[df.index[x], 'Total_Profit'] = df['Profit'][:x + 1].sum()


if len(df) > 1:
    df.loc[df.index[-1], 'Total_Profit'] = df['Total_Profit'][-2] + df['Profit'][-2]


plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Total_Profit'])
plt.xlabel('Date')
plt.ylabel('Total Profit')
plt.title('Total Profit Over Time')
plt.grid(True)
plt.show()

df.to_csv("pair_pca.csv", index=True, encoding='utf8')
from google.colab import files
files.download('pair_pca.csv')