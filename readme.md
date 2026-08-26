# AxionQuant Python SDK

The **AxionQuant Python SDK** is a Python client for the [Axion Financial Data API](https://axionquant.com). Access market data, company fundamentals, financial statements, SEC filings, economic data, ETF data, cryptocurrency, forex, futures, news, and alternative financial data directly from Python.

Built for **quantitative research, financial analysis, financial modeling, and machine learning**, the SDK integrates naturally with pandas, Jupyter notebooks, Plotly, scikit-learn, and TensorFlow.

* **Market data API** for stocks, crypto, forex, futures, and indices
* **Fundamental data API** for financial statements, ratios, earnings, and valuation
* **SEC filings API** for 10-K, 10-Q, and other regulatory filings
* **Economic data API** for macroeconomic and FRED data
* **ETF data API** for holdings, exposure, weights, and fund information
* **Technical analysis** with common indicators including RSI, MACD, SMA, EMA, ATR, Bollinger Bands, and VWAP
* **Interactive financial charts** powered by Plotly
* **Machine learning tools** for regression, beta analysis, and forecasting
* **Pandas integration** for quantitative analysis and research workflows

[Get a free Axion API key](https://axionquant.com/dashboard/api-keys) · [Read the API documentation](https://axionquant.com/docs) · [Learn about the Python SDK](https://axionquant.com/developers/libraries)

## Installation

Install the AxionQuant Python SDK from PyPI:

```bash
pip install axionquant-sdk
```

## Quick Start

Get your [free Axion API key](https://axionquant.com/dashboard/api-keys) and start retrieving financial market data in Python:

```python
from axion import Axion, ta, visualize, utils as axion_utils

client = Axion(api_key="your_api_key_here")

# Fetch historical stock prices and convert to a DataFrame
prices = client.stocks.prices("AAPL", from_date="2024-01-01")
df = axion_utils.df(prices)

# Calculate a technical indicator
roc = ta.roc(df, "close")

# Create an interactive candlestick chart
visualize.candles(df)
```

The SDK is designed for workflows ranging from simple **stock market data analysis in Python** to larger quantitative research and machine learning pipelines.

## Financial Market Data

The AxionQuant API provides programmatic access to financial market data across multiple asset classes.

### Stocks and Equities

Retrieve stock quotes, historical prices, ticker information, market gainers and losers, and other equity market data.

```python
client.stocks.tickers(country="america")
client.stocks.ticker("AAPL")
client.stocks.quote("AAPL")
client.stocks.prices(
    "AAPL",
    from_date="2024-01-01",
    to_date="2024-12-31",
    frame="daily"
)
client.stocks.gainers(days=5, limit=10)
client.stocks.losers(days=5, limit=10)
```

### Cryptocurrency Market Data

Retrieve cryptocurrency tickers, quotes, historical prices, gainers, and losers.

```python
client.crypto.tickers(type="coin")
client.crypto.ticker("BTC")
client.crypto.quote("BTC")
client.crypto.prices("BTC", from_date="2024-01-01", frame="weekly")
client.crypto.gainers(days=5, limit=10)
client.crypto.losers(days=5, limit=10)
```

### Forex Market Data

Access foreign exchange tickers, quotes, historical prices, and market performance data.

```python
client.forex.tickers()
client.forex.ticker("EURUSD")
client.forex.quote("EURUSD")
client.forex.prices("EURUSD", from_date="2024-01-01")
client.forex.gainers(limit=5)
client.forex.losers(limit=5)
```

### Futures Market Data

Access futures contracts, quotes, historical prices, and market performance.

```python
client.futures.tickers(exchange="CME")
client.futures.ticker("ES")
client.futures.quote("ES")
client.futures.prices("ES", from_date="2024-01-01")
client.futures.gainers(limit=5)
client.futures.losers(limit=5)
```

### Index Data

Retrieve index prices, constituents, exposure, quotes, gainers, and losers.

```python
client.indices.tickers()
client.indices.ticker("SPX")
client.indices.quote("SPX")
client.indices.prices("SPX", from_date="2024-01-01")
client.indices.components("SPX")
client.indices.exposure("AAPL")
client.indices.gainers(limit=5)
client.indices.losers(limit=5)
```

## Fundamental Data and Financial Analysis

Use the AxionQuant Python SDK to retrieve **company fundamentals, financial statements, earnings data, valuation metrics, ownership data, and analyst information**.

### Company Profiles

```python
client.profiles.profile("AAPL")
client.profiles.info("AAPL")
client.profiles.statistics("AAPL")
client.profiles.summary("AAPL")
client.profiles.recommendation("AAPL")
client.profiles.calendar("AAPL")
```

### Earnings Data

Access historical earnings, earnings trends, reports, earnings call transcripts, and transcript sentiment.

```python
client.earnings.history("AAPL")
client.earnings.trend("AAPL")
client.earnings.index("AAPL")
client.earnings.report("AAPL", year="2024", quarter="Q1")
client.earnings.transcript("AAPL", year="2024", quarter="Q1")
client.earnings.transcript_sentiment("base64_encoded_id")
```

### Financial Statements and Metrics

Retrieve balance sheets, income statements, cash flow statements, historical financial metrics, valuation ratios, and calculated financial ratios.

```python
# Financial statements
client.financials.balance_sheet("AAPL")
client.financials.income_statement("AAPL")
client.financials.cash_flow_statement("AAPL")

# Historical financial metrics
client.financials.revenue("AAPL", periods=8)
client.financials.net_income("AAPL")
client.financials.free_cash_flow("AAPL")
client.financials.total_assets("AAPL")
client.financials.total_liabilities("AAPL")
client.financials.current_assets("AAPL")
client.financials.current_liabilities("AAPL")
client.financials.stockholders_equity("AAPL")
client.financials.operating_cash_flow("AAPL")
client.financials.capital_expenditures("AAPL")
client.financials.shares_outstanding_basic("AAPL")
client.financials.shares_outstanding_diluted("AAPL")

# Financial ratios and valuation
client.financials.metrics("AAPL")
client.financials.eps("AAPL", from_date="2024-01-01", to_date="2024-12-31")
client.financials.pe("AAPL")
client.financials.market_cap("AAPL")
client.financials.roe("AAPL")
client.financials.enterprise_value("AAPL")
client.financials.ebitda("AAPL")
client.financials.debt_to_equity("AAPL")

# DCF valuation
client.financials.dcf_value("AAPL")
client.financials.dcf_rate("AAPL")
```

## SEC Filings and Regulatory Data

Access **SEC filings and corporate regulatory data** programmatically, including 10-K and 10-Q filings.

```python
client.filings.recent("AAPL", form="10-K", limit=10)

client.filings.history(
    "AAPL",
    form_type="10-Q",
    start_date="2024-01-01",
    end_date="2024-03-31"
)

client.filings.search(
    ticker="AAPL",
    form="10-K",
    year="2024",
    quarter="Q1"
)

client.filings.list_forms()
client.filings.document_text("document_id")
client.filings.document_sentiment("document_id")
```

## Insider Trading and Institutional Ownership

Analyze insider transactions, institutional ownership, fund ownership, and major shareholders.

```python
client.insiders.individuals("AAPL")
client.insiders.institutions("AAPL")
client.insiders.funds("AAPL")
client.insiders.ownership("AAPL")
client.insiders.transactions("AAPL")
client.insiders.activity("AAPL")
```

## Economic and Macroeconomic Data

Access economic indicators, macroeconomic datasets, economic calendars, and FRED data for quantitative research.

```python
client.econ.find("semiconductor spending")
client.econ.search("unemployment rate")
client.econ.dataset("UNRATE")

client.econ.calendar(
    from_date="2024-01-01",
    to_date="2024-12-31",
    country="US",
    min_importance=3,
    currency="USD",
    category="employment"
)
```

## ETF Data

Retrieve ETF information, fund holdings, portfolio exposure, sector weights, regional weights, quotes, and historical performance.

```python
client.etfs.tickers()
client.etfs.ticker("SPY")
client.etfs.fund("SPY")
client.etfs.holdings("SPY")
client.etfs.holdings_all("SPY")
client.etfs.exposure("SPY")
client.etfs.weights("SPY")
client.etfs.quote("SPY")
client.etfs.gainers(limit=5)
client.etfs.losers(limit=5)
```

## Financial News and Sentiment

Retrieve general financial news, company news, country-specific news, category-based news, and market sentiment.

```python
client.news.general()
client.news.company("AAPL")
client.news.country("US")
client.news.category("technology")
```

```python
client.sentiment.all("AAPL")
client.sentiment.social("AAPL")
client.sentiment.news("AAPL")
client.sentiment.analyst("AAPL")
```

## Alternative Financial Data

The SDK also provides access to additional datasets useful for fundamental and quantitative research.

### ESG Data

```python
client.esg.data("AAPL")
```

### Credit Ratings

```python
client.credit.search("Apple Inc")
client.credit.ratings("entity_id")
```

### Supply Chain Data

```python
client.supply_chain.customers("AAPL")
client.supply_chain.suppliers("AAPL")
client.supply_chain.peers("AAPL")
```

### Web Traffic Data

```python
client.web_traffic.traffic("AAPL")
```

## Technical Analysis

The `ta` module provides common **technical analysis indicators for Python and pandas**, including trend, momentum, volatility, volume, and market structure indicators.

```python
import axion.ta as ta
```

### Trend Indicators

```python
ta.sma(df, column="close", period=14)
ta.ema(df, column="close", period=14)
ta.dema(df, column="close", period=14)
ta.ssma(df, column="close", period=14)
ta.trima(df, column="close", period=14)
ta.kama(df, column="close", period=14)
```

### Momentum and Oscillators

```python
ta.rsi(df, column="close", period=14)
ta.macd(df)
ta.roc(df, column="close", period=10)
ta.mom(df, column="close", period=10)
ta.cmo(df, column="close", period=20)
ta.stochastic_oscillator(df)
ta.williams_r(df, period=14)
ta.adx(df, period=14)
```

### Volatility and Channels

```python
ta.atr(df, period=14)
ta.bbands(df)
ta.kc(df)
```

### Volume Indicators

```python
ta.obv(df)
ta.vpt(df)
ta.vwap(df)
```

### Trend Direction

```python
ta.vi(df, period=14)
ta.ichi(df)
ta.sar(df)
ta.fib(df)
```

## Financial Data Visualization

The `visualize` module provides interactive **Plotly charts for financial and quantitative analysis**.

```python
import axion.visualize as visualize
```

```python
visualize.candles(df)
visualize.line(df, x="time", y="close")
visualize.bar(df, x="time", y="volume")
visualize.barh(df, x="value", y="label")
visualize.scatter(df, x="time", y="close")
visualize.fit(df, x="revenue", y="price")
visualize.area(df, x="time", y="value", group="sector")
visualize.pie(df, values="marketCap", labels="ticker")
visualize.radar(df, values="score", labels="category")
visualize.heatmap(df, x="col1", y="col2")
visualize.cov(df)
visualize.polls(df)
visualize.spread(dfs, x="time", y="close")
visualize.tree(df)
visualize.graph(
    df,
    x="time",
    bars=["volume"],
    lines=["close", "sma"]
)
```

## Python Data Utilities

The `utils` module provides date handling, DataFrame transformation, comparison, resampling, caching, and concurrency utilities for financial data workflows.

```python
import axion.utils as axion_utils
```

```python
# Date helpers
axion_utils.d("1 month ago")
axion_utils.to_timestamp("2024-01-01")
axion_utils.nearest_day("2024-01-06")

# Date shorthand
axion_utils.today
axion_utils.yesterday
axion_utils.weekago
axion_utils.monthago
axion_utils.yearago
axion_utils.yearfrom

# DataFrame helpers
axion_utils.df(items)
axion_utils.pds(list_of_lists)
axion_utils.stack(dfs)
axion_utils.stitch(dfs, col="time")
axion_utils.snap(dfs, names, overwrite)
axion_utils.filter(df, col, items)
axion_utils.dedup(lst)
axion_utils.simmer(arr)
axion_utils.resample(df, "2024-01-01 2024-12-31")
```

## Machine Learning and Financial Modeling

The `models` module provides machine learning utilities for **financial forecasting, regression analysis, benchmark analysis, and quantitative modeling**.

```python
import axion.models as models
```

### Linear Regression

```python
preds = models.linearRegression(
    df,
    x="time",
    target="close",
    n_preds=10
)
```

### Multi-Feature Regression

```python
preds = models.multiLinearRegression(
    df,
    x="time",
    target="close",
    features=["volume", "rsi"],
    n_preds=10
)
```

### Beta Analysis

```python
b = models.beta(
    df,
    x="stock_return",
    y="market_return"
)
```

### LSTM Forecasting

```python
preds = models.lstm(
    df,
    x="time",
    target="close",
    features=["volume", "rsi"],
    n_preds=10
)
```

## Supported Date Formats and Time Frames

API date parameters use the `YYYY-MM-DD` format.

Supported historical price time frames:

* `daily`
* `weekly`
* `monthly`
* `quarterly`
* `yearly`

## Error Handling

```python
try:
    data = client.stocks.prices("INVALID")
except Exception as e:
    print(f"Error: {e}")
```

Common errors include:

* HTTP errors
* Connection errors
* Timeout errors
* Authentication errors

## Documentation and Resources

* [AxionQuant Financial Data API](https://axionquant.com)
* [API Documentation](https://axionquant.com/docs)
* [Python SDK Documentation](https://axionquant.com/developers/libraries)
* [Get a Free API Key](https://axionquant.com/dashboard/api-keys)
* [AxionQuant GitHub](https://github.com/axionquant/python-sdk)

## License

MIT

