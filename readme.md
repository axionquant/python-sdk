# Axion Python SDK

A comprehensive Python client for accessing financial market data, economic indicators, company profiles, and more through the Axion API.

## Installation

```bash
pip install axionquant-sdk
```

## Quick Start

```python
from axion import Axion

# Initialize the client with your API key
client = Axion(api_key="your_api_key_here")

# Get stock prices
prices = client.stocks.prices("AAPL", from_date="2024-01-01", to_date="2024-12-31")

# Search for economic data
econ_data = client.econ.search("unemployment rate")

# Get company news
news = client.news.company("TSLA")
```

## Authentication

Most endpoints require authentication. Initialize the client with your API key:

```python
client = Axion(api_key="your_api_key_here")
```

## Features

### Stocks API

Get stock ticker information, prices, and historical data.

```python
# Get all stock tickers (filtered by country/exchange)
tickers = client.stocks.tickers(country="america")

# Get specific ticker information
ticker_info = client.stocks.quote("AAPL")

# Get historical prices
prices = client.stocks.prices(
    ticker="AAPL",
    from_date="2024-01-01",
    to_date="2024-12-31",
    frame="daily"  # Options: daily, weekly, monthly, quarterly, yearly
)
```

### Company Profiles API

Access comprehensive company information and financial statements.

```python
# Company overview and business summary
profile = client.profiles.asset("AAPL")

# Company information
info = client.profiles.info("AAPL")

# Financial statements
income_statement = client.profiles.income("AAPL")
balance_sheet = client.profiles.balancesheet("AAPL")
cashflow = client.profiles.cashflow("AAPL")
financials = client.profiles.financials("AAPL")

# Key statistics and ratios
stats = client.profiles.statistics("AAPL")
summary = client.profiles.summary("AAPL")

# Earnings data
earnings = client.profiles.earnings("AAPL")
earnings_trend = client.profiles.earnings_trend("AAPL")

# Ownership information
insiders = client.profiles.insiders("AAPL")
institutions = client.profiles.institution_ownership("AAPL")
fund_ownership = client.profiles.fund_ownership("AAPL")
major_holders = client.profiles.ownership("AAPL")

# Insider activity
transactions = client.profiles.transactions("AAPL")
activity = client.profiles.activity("AAPL")

# Analyst data
recommendations = client.profiles.recommendation("AAPL")

# Trends and estimates
index_trend = client.profiles.index_trend("AAPL")

# Other data
calendar = client.profiles.calendar("AAPL")
traffic = client.profiles.traffic("AAPL")
```

### Cryptocurrency API

Access cryptocurrency ticker data and historical prices.

```python
# Get all crypto tickers
crypto_tickers = client.crypto.tickers(type="coin")

# Get specific crypto information
btc_info = client.crypto.quote("BTC")

# Get crypto prices
btc_prices = client.crypto.prices(
    ticker="BTC",
    from_date="2024-01-01",
    frame="daily"
)
```

### Forex API

Access foreign exchange rates and historical data.

```python
# Get forex tickers
forex_tickers = client.forex.tickers()

# Get specific forex pair
pair_info = client.forex.quote("EURUSD")

# Get forex prices
prices = client.forex.prices("EURUSD", from_date="2024-01-01")
```

### Futures API

Access futures contract data and prices.

```python
# Get futures tickers
futures = client.futures.tickers(exchange="CME")

# Get specific futures contract
contract = client.futures.quote("ES")

# Get futures prices
prices = client.futures.prices("ES", from_date="2024-01-01")
```

### Indices API

Access market index data and historical performance.

```python
# Get index tickers
indices = client.indices.tickers()

# Get specific index
index_info = client.indices.quote("SPX")

# Get index prices
prices = client.indices.prices("SPX", from_date="2024-01-01")
```

### Economic Data API

Search and retrieve economic indicators and calendar events.

```python
# Search for economic series
results = client.econ.search("GDP")

# Get economic dataset
dataset = client.econ.dataset("UNRATE")

# Get economic calendar with filters
calendar = client.econ.calendar(
    from_date="2024-01-01",
    to_date="2024-12-31",
    country="US",
    min_importance=3,
    currency="USD",
    category="employment"
)
```

### ETF API

Access ETF fund data, holdings, and exposure information.

```python
# Get ETF fund details
fund_data = client.etfs.fund("SPY")

# Get ETF holdings
holdings = client.etfs.holdings("SPY")

# Get exposure data
exposure = client.etfs.exposure("SPY")
```

### News API

Access financial news articles by company, country, or category.

```python
# Get general news
news = client.news.general()

# Get company-specific news
company_news = client.news.company("AAPL")

# Get country news
country_news = client.news.country("US")

# Get category news
category_news = client.news.category("technology")
```

### Sentiment API

Analyze market sentiment from social media, news, and analyst ratings.

```python
# Get all sentiment data
all_sentiment = client.sentiment.all("AAPL")

# Get specific sentiment types
social = client.sentiment.social("AAPL")
news_sentiment = client.sentiment.news("AAPL")
analyst = client.sentiment.analyst("AAPL")
```

### ESG API

Access Environmental, Social, and Governance data.

```python
esg_data = client.esg.data("AAPL")
```

### Credit Ratings API

Search for credit entities and retrieve credit ratings.

```python
# Search for credit entities
results = client.credit.search("Apple Inc")

# Get credit ratings
ratings = client.credit.ratings("entity_id_here")
```

### Supply Chain API

Analyze company supply chain relationships.

```python
# Get customers
customers = client.supply_chain.customers("AAPL")

# Get suppliers
suppliers = client.supply_chain.suppliers("AAPL")

# Get peers
peers = client.supply_chain.peers("AAPL")
```

## Error Handling

The SDK provides detailed error messages for various failure scenarios:

```python
try:
    data = client.stocks.prices("INVALID")
except Exception as e:
    print(f"Error: {e}")
```

Common errors include:
- **HTTP Error**: API returned an error status code
- **Connection Error**: Unable to connect to the API
- **Timeout Error**: Request took too long to complete
- **Authentication Error**: Missing or invalid API key

## Data Normalization

The SDK automatically normalizes all API responses by converting string numbers to integers or floats, and string booleans to actual boolean values. This ensures consistent data types across all responses.

## Date Formats

All date parameters should be in `YYYY-MM-DD` format:

```python
data = client.stocks.prices("AAPL", from_date="2024-01-01", to_date="2024-12-31")
```

## Time Frames

Price endpoints support various time frames:
- `daily` (default)
- `weekly`
- `monthly`
- `quarterly`
- `yearly`

```python
prices = client.stocks.prices("AAPL", frame="monthly")
```

## API Structure

The SDK is organized into the following modules:

- `client.stocks` - Stock market data
- `client.crypto` - Cryptocurrency data
- `client.forex` - Foreign exchange data
- `client.futures` - Futures contracts data
- `client.indices` - Market indices data
- `client.profiles` - Company profiles and financials
- `client.econ` - Economic data and calendar
- `client.etfs` - ETF data and holdings
- `client.news` - Financial news
- `client.sentiment` - Market sentiment analysis
- `client.esg` - ESG ratings
- `client.credit` - Credit ratings
- `client.supply_chain` - Supply chain relationships

## Support

For API documentation, support, or to obtain an API key, visit the Axion API website.

## License

See LICENSE file for details.
