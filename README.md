### Trading Strategies Overview

#### Moving Average Crossover Strategy for Stock Trading

This strategy uses the crossover of moving averages to generate trading signals. The script:

- **Iterates Yearly**: Analyzes data from 2021 to 2023.
- **Tests Different Moving Averages**: Evaluates short (SMA) and long (LMA) moving averages ranging from 1 to 34 days, incremented by 2.
- **Long Entry**: Buys when the short moving average crosses above the long moving average.
- **Long Exit**: Sells when the short moving average crosses below the long moving average.
- **Short Entry**: Sells when the short moving average crosses below the long moving average.
- **Short Exit**: Buys back when the short moving average crosses above the long moving average.



#### Daily Buy/Sell Signal Strategy for Stock Trading

This approach focuses on daily price movements to trigger buy and sell signals:

- **Buy Signal**: Generated when today's opening price is higher than yesterday's closing price and today's closing price is also higher than yesterday's closing price.
- **Sell Signal**: Triggered when today's opening price is lower than yesterday's closing price and today's closing price is also lower than yesterday's closing price.
- **Evaluation**: Applied to NIFTY 50 stocks (excluding HDFC.NS). Metrics include the total number of trading days, total signals, signal probability, and total profit. Stocks with a signal probability greater than 60% are highlighted for potentially more reliable trading opportunities.



#### Bollinger Bands Strategy for HDFCBANK.NS

This strategy uses Bollinger Bands to generate trading signals for HDFCBANK.NS:

- **Long Entry**: Buy when the closing price is below the lower Bollinger Band.
- **Long Exit**: Sell when the closing price is at or above the moving average.
- **Short Entry**: Sell when the closing price is above the upper Bollinger Band.
- **Short Exit**: Buy back when the closing price is at or below the moving average.



#### Pearson Correlation Analysis for RELIANCE.NS and ^NSEI

This analysis measures the relationship between the closing prices of RELIANCE.NS and ^NSEI:

- **Pearson Correlation Coefficient**: Quantifies the linear relationship between the two series.
- **P-value**: Assesses the significance of the correlation. A lower p-value indicates a stronger, more significant relationship.



#### Augmented Dickey-Fuller (ADF) Test for Stationarity

The ADF test checks if a time series is stationary:

- **ADF Statistic**: Measures the strength of the null hypothesis that the series has a unit root (i.e., is non-stationary).
- **P-value**: A value below 0.05 suggests rejecting the null hypothesis, indicating that the series is stationary.
- **Critical Values**: Provide thresholds for the ADF statistic at various confidence levels. If the statistic is less than these values, it supports stationarity.



#### Bollinger Bands Momentum Crossover Strategy

This strategy combines Bollinger Bands with momentum signals:

- **Long Entry**: Buy when the difference (Diff) between two financial instruments is below the lower Bollinger Band.
- **Long Exit**: Sell when Diff is at or above the moving average.
- **Short Entry**: Sell when Diff is above the upper Bollinger Band.
- **Short Exit**: Buy back when Diff is at or below the moving average.
- **Positions**: Managed with forward-filling to maintain consistency.



#### Multi-Asset Cointegration and Correlation Analysis

This analysis assesses the relationship between different assets:

- **Cointegration Values**: Generally negative, indicating long-term equilibrium relationships between some pairs.
- **Correlation Values**: Show varying degrees of linear relationships.
- **ADF p-values**: Indicate stationarity of the pairs. Lower p-values suggest that the pairs are stationary, which is important for further modeling.
- **Significant Pairs**: Pairs like HDFC Bank and Kotak Bank show strong cointegration and correlations.



#### Z-Score Momentum Strategy

This strategy combines statistical methods with trading signals:

- **Long Positions**: Selected based on the lowest Z-scores.
- **Short Positions**: Chosen based on the highest Z-scores.
- **Goal**: To generate profits by leveraging statistical methods (ADF test, PCA) and trading signals (Z-scores).

These strategies offer various ways to analyze and trade stocks using technical indicators, statistical tests, and quantitative analysis.
