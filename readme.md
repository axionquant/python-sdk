# Axion Python SDK

A comprehensive Python client for the [Axion](https://axionquant.com) financial market data, technical analysis, visualization, and machine learning - built for quantitative research in Jupyter notebooks and Python scripts.

## Installation

```bash
pip install axionquant-sdk
```

## Quick Start

[Get your free API key](https://axionquant.com/dashboard/api-keys)

```python
from axion import Axion, ta, visualize, utils as axion_utils

client = Axion(api_key="your_api_key_here")

# Fetch stock prices and convert to DataFrame
prices = client.stocks.prices("AAPL", from_date="2024-01-01")
df = axion_utils.df(prices)

# Run technical analysis
roc = ta.roc(df, 'close')

# Visualize
visualize.candles(df)
```

## Modules

The SDK is organized into five importable modules:

```python
from axion import Axion        # API client
from axion import ta           # Technical analysis
from axion import visualize    # Charting & visualization
from axion import utils        # Data utilities
from axion import models       # ML / prediction models
```

---

## Axion Client

Initialize with your API key:

```python
client = Axion(api_key="your_api_key_here")
```

### Stocks
```python
client.stocks.tickers(country="america")
client.stocks.ticker("AAPL")              # Single ticker lookup
client.stocks.quote("AAPL")
client.stocks.prices("AAPL", from_date="2024-01-01", to_date="2024-12-31", frame="daily")
client.stocks.gainers(days=5, limit=10)  # Top gainers
client.stocks.losers(days=5, limit=10)   # Top losers
```

### Crypto
```python
client.crypto.tickers(type="coin")
client.crypto.ticker("BTC")              # Single ticker lookup
client.crypto.quote("BTC")
client.crypto.prices("BTC", from_date="2024-01-01", frame="weekly")
client.crypto.gainers(days=5, limit=10)
client.crypto.losers(days=5, limit=10)
```

### Forex
```python
client.forex.tickers()
client.forex.ticker("EURUSD")            # Single ticker lookup
client.forex.quote("EURUSD")
client.forex.prices("EURUSD", from_date="2024-01-01")
client.forex.gainers(limit=5)
client.forex.losers(limit=5)
```

### Futures
```python
client.futures.tickers(exchange="CME")
client.futures.ticker("ES")              # Single ticker lookup
client.futures.quote("ES")
client.futures.prices("ES", from_date="2024-01-01")
client.futures.gainers(limit=5)
client.futures.losers(limit=5)
```

### Indices
```python
client.indices.tickers()
client.indices.ticker("SPX")             # Single ticker lookup
client.indices.quote("SPX")
client.indices.prices("SPX", from_date="2024-01-01")
client.indices.components("SPX")         # Index constituents
client.indices.exposure("AAPL")          # Which indices hold AAPL
client.indices.gainers(limit=5)
client.indices.losers(limit=5)
```

### Company Profiles
```python
client.profiles.profile("AAPL")       # Business summary
client.profiles.info("AAPL")          # Company info
client.profiles.statistics("AAPL")    # Key ratios
client.profiles.summary("AAPL")       # Market data summary
client.profiles.recommendation("AAPL") # Analyst recommendations
client.profiles.calendar("AAPL")      # Earnings dates / dividends
```

### Earnings
```python
client.earnings.history("AAPL")
client.earnings.trend("AAPL")
client.earnings.index("AAPL")
client.earnings.report("AAPL", year="2024", quarter="Q1")
client.earnings.transcript("AAPL", year="2024", quarter="Q1")        # Earnings call transcript
client.earnings.transcript_sentiment("base64_encoded_id")             # Transcript sentiment
```

### Financials
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
client.financials.metrics("AAPL")     # Calculated ratios
client.financials.snapshot("AAPL")    # Full data snapshot
```

### Insiders & Ownership
```python
client.insiders.individuals("AAPL")   # Insider holders
client.insiders.institutions("AAPL")  # Institutional ownership
client.insiders.funds("AAPL")         # Fund ownership
client.insiders.ownership("AAPL")     # Major holders breakdown
client.insiders.transactions("AAPL")  # Insider transactions
client.insiders.activity("AAPL")      # Net share purchase activity
```

### SEC Filings
```python
client.filings.filings("AAPL", limit=10, form="10-K")
client.filings.forms("AAPL", form_type="10-Q", year="2024", quarter="Q2")
client.filings.search(year="2024", quarter="Q1", form="10-K", ticker="AAPL")
client.filings.desc_forms()           # List available form types
client.filings.document_text("document_id")     # Raw filing text
client.filings.document_sentiment("document_id") # Filing sentiment
```

### Economic Data
```python
client.econ.find("semiconductor spending")  # AI-powered FRED search
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

### ETFs
```python
client.etfs.tickers()
client.etfs.ticker("SPY")              # Single ticker lookup
client.etfs.fund("SPY")
client.etfs.holdings("SPY")
client.etfs.exposure("SPY")
client.etfs.weights("SPY")             # Sector & region weights
client.etfs.quote("SPY")
client.etfs.gainers(limit=5)
client.etfs.losers(limit=5)
```

### News
```python
client.news.general()
client.news.company("AAPL")
client.news.country("US")
client.news.category("technology")
```

### Sentiment
```python
client.sentiment.all("AAPL")
client.sentiment.social("AAPL")
client.sentiment.news("AAPL")
client.sentiment.analyst("AAPL")
```

### ESG
```python
client.esg.data("AAPL")
```

### Credit Ratings
```python
client.credit.search("Apple Inc")
client.credit.ratings("entity_id")
```

### Supply Chain
```python
client.supply_chain.customers("AAPL")
client.supply_chain.suppliers("AAPL")
client.supply_chain.peers("AAPL")
```

### Web Traffic
```python
client.web_traffic.traffic("AAPL")
```

---

## Technical Analysis (`ta`)

All functions accept a pandas DataFrame and return a Series (or tuple of Series).

```python
import axion.ta as ta

# Trend
ta.sma(df, column="close", period=14)
ta.ema(df, column="close", period=14)
ta.dema(df, column="close", period=14)
ta.ssma(df, column="close", period=14)
ta.trima(df, column="close", period=14)
ta.kama(df, column="close", period=14)

# Momentum & Oscillators
ta.rsi(df, column="close", period=14)
ta.macd(df)                            # returns (macd_line, signal, histogram)
ta.roc(df, column="close", period=10)
ta.mom(df, column="close", period=10)
ta.cmo(df, column="close", period=20)
ta.stochastic_oscillator(df)           # returns (K, D)
ta.williams_r(df, period=14)
ta.adx(df, period=14)

# Volatility & Channels
ta.atr(df, period=14)
ta.bbands(df)                          # returns (upper, mid, lower)
ta.kc(df)                              # Keltner Channels

# Volume
ta.obv(df)
ta.vpt(df)
ta.vwap(df)

# Trend Direction
ta.vi(df, period=14)                   # Vortex Indicator (VI+, VI-)
ta.ichi(df)                            # Ichimoku Cloud
ta.sar(df)                             # Parabolic SAR
ta.fib(df)                             # Fibonacci Pivot Points
```

---

## Visualization (`visualize`)

All chart functions accept a pandas DataFrame and render an interactive Plotly chart.

```python
import axion.visualize as visualize

visualize.candles(df)                            # Candlestick chart
visualize.line(df, x="time", y="close")          # Line chart
visualize.bar(df, x="time", y="volume")          # Bar chart
visualize.barh(df, x="value", y="label")         # Horizontal bar
visualize.scatter(df, x="time", y="close")       # Scatter plot
visualize.fit(df, x="revenue", y="price")        # Scatter + OLS trendline
visualize.area(df, x="time", y="value", group="sector")
visualize.pie(df, values="marketCap", labels="ticker")
visualize.radar(df, values="score", labels="category")
visualize.heatmap(df, x="col1", y="col2")
visualize.cov(df)                                # Correlation heatmap
visualize.polls(df)                              # Multi-series line chart
visualize.spread(dfs, x="time", y="close")       # Two assets + spread
visualize.tree(df)                               # Treemap (sector/industry/symbol)

# Flexible multi-series chart
visualize.graph(df, x="time", bars=["volume"], lines=["close", "sma"])
```

---

## Utilities (`utils`)

```python
import axion.utils as axion_utils

# Date helpers
axion_utils.d("1 month ago")           # Natural language → "YYYY-MM-DD"
axion_utils.to_timestamp("2024-01-01")
axion_utils.nearest_day("2024-01-06")  # Nearest market open day

# Date shorthand constants
axion_utils.today / axion_utils.yesterday / axion_utils.weekago
axion_utils.monthago / axion_utils.yearago / axion_utils.yearfrom

# Frame shorthand constants
axion_utils.d   # daily
axion_utils.w   # weekly
axion_utils.m   # monthly
axion_utils.y   # yearly

# DataFrame helpers
axion_utils.df(items)                  # Create DataFrame from list of dicts
axion_utils.pds(list_of_lists)         # Convert 2D list of dicts → list of DataFrames
axion_utils.stack(dfs)                 # Concat DataFrames vertically
axion_utils.stitch(dfs, col="time")    # Merge different data types on shared column
axion_utils.snap(dfs, names, overwrite) # Merge same-type DataFrames side-by-side
axion_utils.filter(df, col, items)     # Filter rows by column values
axion_utils.dedup(lst)                 # Remove duplicates from list
axion_utils.simmer(arr)                # Flatten 2D list to 1D
axion_utils.resample(df, "2024-01-01 2024-12-31")

# Analysis helpers
axion_utils.relativity(df, cols)       # Add pct_change columns
axion_utils.indexed(prices)            # Average a dict of price DataFrames
axion_utils.composite(dfs)             # Combine and average financials/facts
axion_utils.contrast(dfs, joins)       # Reshape for side-by-side graphing
axion_utils.compare(dfs, joins)        # Cross-DataFrame % diff comparison
axion_utils.gainers(prices, frame)     # Top gainers from price dict
axion_utils.losers(prices, frame)      # Top losers from price dict
axion_utils.overlap(dfs, col)          # Intersection of column values
axion_utils.difference(dfs, col)       # Non-overlapping values

# Concurrency
axion_utils.work(df, callback, ref)    # Threaded execution with progress bar

# Caching / Persistence
axion_utils.cache(id, fn)              # Load from cache or run function
axion_utils.save(id, obj)             # Manually save object to cache
axion_utils.read(id)                  # Read object from cache
axion_utils.scribe(df, id, cb)        # Cache + work helper combined
```

---

## ML Models (`models`)

```python
import axion.models as models

# Linear regression forecast
preds = models.linearRegression(df, x="time", target="close", n_preds=10)

# Multi-feature linear regression
preds = models.multiLinearRegression(df, x="time", target="close",
                                     features=["volume", "rsi"], n_preds=10)

# Beta relative to benchmark
b = models.beta(df, x="stock_return", y="market_return")

# LSTM deep learning forecast
preds = models.lstm(df, x="time", target="close",
                    features=["volume", "rsi"], n_preds=10)
```

---

## Date Formats & Time Frames

All API date parameters use `YYYY-MM-DD` format. Supported price frames: `daily`, `weekly`, `monthly`, `quarterly`, `yearly`.

## Error Handling

```python
try:
    data = client.stocks.prices("INVALID")
except Exception as e:
    print(f"Error: {e}")
```

Common errors: `HTTP Error`, `Connection Error`, `Timeout Error`, `Authentication Error`.

## Get Started

For detailed API documentation, support, or to obtain an API key, visit the [Axion](https://axionquant.com) website.

## License

MIT
