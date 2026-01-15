# Axion Python SDK

A comprehensive Python client for accessing financial market data, economic indicators, company profiles, and more through the Axion API.

## Installation

```bash
pip install axion-sdk
```

## Quick Start

```python
from axion import Axion

# Initialize the client with your API key
client = Axion(api_key="your_api_key_here")

# Get stock prices
prices = client.get_stock_prices("AAPL", from_date="2024-01-01", to_date="2024-12-31")

# Search for economic data
econ_data = client.search_econ("unemployment rate")

# Get company news
news = client.get_company_news("TSLA")
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
tickers = client.get_stock_tickers(country="america")

# Get specific ticker information
ticker_info = client.get_stock_ticker_by_symbol("AAPL")

# Get historical prices
prices = client.get_stock_prices(
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
profile = client.get_company_asset_profile("AAPL")

# Financial statements
income_statement = client.get_company_income_statement("AAPL")
balance_sheet = client.get_company_balance_sheet("AAPL")
cashflow = client.get_company_cashflow("AAPL")

# Key statistics and ratios
stats = client.get_company_statistics("AAPL")

# Earnings data
earnings = client.get_company_earnings_history("AAPL")
earnings_trend = client.get_company_earnings_trend("AAPL")

# Ownership information
insiders = client.get_company_insider_holders("AAPL")
institutions = client.get_company_institution_ownership("AAPL")
major_holders = client.get_company_major_holders("AAPL")

# Analyst data
recommendations = client.get_company_recommendation_trend("AAPL")

# Other data
calendar = client.get_company_calendar_events("AAPL")
traffic = client.get_company_website_traffic("AAPL")
```

### Cryptocurrency API

Access cryptocurrency ticker data and historical prices.

```python
# Get all crypto tickers
crypto_tickers = client.get_crypto_tickers(type="coin")

# Get specific crypto information
btc_info = client.get_crypto_ticker_by_symbol("BTC")

# Get crypto prices
btc_prices = client.get_crypto_prices(
    ticker="BTC",
    from_date="2024-01-01",
    frame="daily"
)
```

### Forex API

Access foreign exchange rates and historical data.

```python
# Get forex tickers
forex_tickers = client.get_forex_tickers()

# Get specific forex pair
pair_info = client.get_forex_ticker_by_symbol("EURUSD")

# Get forex prices
prices = client.get_forex_prices("EURUSD", from_date="2024-01-01")
```

### Futures API

Access futures contract data and prices.

```python
# Get futures tickers
futures = client.get_futures_tickers(exchange="CME")

# Get specific futures contract
contract = client.get_futures_ticker_by_symbol("ES")

# Get futures prices
prices = client.get_futures_prices("ES", from_date="2024-01-01")
```

### Indices API

Access market index data and historical performance.

```python
# Get index tickers
indices = client.get_index_tickers()

# Get specific index
index_info = client.get_index_ticker_by_symbol("SPX")

# Get index prices
prices = client.get_index_prices("SPX", from_date="2024-01-01")
```

### Economic Data API

Search and retrieve economic indicators and calendar events.

```python
# Search for economic series
results = client.search_econ("GDP")

# Get economic dataset
dataset = client.get_econ_dataset("UNRATE")

# Get economic calendar with filters
calendar = client.get_econ_calendar(
    from_date="2024-01-01",
    to_date="2024-12-31",
    country="US,UK,CA",
    min_importance=3,
    currency="USD",
    category="employment,inflation"
)
```

### ETF API

Access ETF fund data, holdings, and exposure information.

```python
# Get ETF fund details
fund_data = client.get_etf_fund_data("SPY")

# Get ETF holdings
holdings = client.get_etf_holdings("SPY")

# Get exposure data
exposure = client.get_etf_exposure("SPY")
```

### News API

Access financial news articles by company, country, or category.

```python
# Get general news
news = client.get_news()

# Get company-specific news
company_news = client.get_company_news("AAPL")

# Get country news
country_news = client.get_country_news("US")

# Get category news
category_news = client.get_category_news("technology")
```

### Sentiment API

Analyze market sentiment from social media, news, and analyst ratings.

```python
# Get all sentiment data
all_sentiment = client.get_sentiment_all("AAPL")

# Get specific sentiment types
social = client.get_sentiment_social("AAPL")
news = client.get_sentiment_news("AAPL")
analyst = client.get_sentiment_analyst("AAPL")
```

### ESG API

Access Environmental, Social, and Governance data.

```python
esg_data = client.get_esg_data("AAPL")
```

### Credit Ratings API

Search for credit entities and retrieve credit ratings.

```python
# Search for credit entities
results = client.search_credit("Apple Inc")

# Get credit ratings
ratings = client.get_credit_ratings("entity_id_here")
```

### Supply Chain API

Analyze company supply chain relationships.

```python
# Get customers
customers = client.get_supply_chain_customers("AAPL")

# Get suppliers
suppliers = client.get_supply_chain_suppliers("AAPL")

# Get peers
peers = client.get_supply_chain_peers("AAPL")
```

## Error Handling

The SDK provides detailed error messages for various failure scenarios:

```python
try:
    data = client.get_stock_prices("INVALID")
except Exception as e:
    print(f"Error: {e}")
```

Common errors include:
- **HTTP Error**: API returned an error status code
- **Connection Error**: Unable to connect to the API
- **Timeout Error**: Request took too long to complete
- **Authentication Error**: Missing or invalid API key

## Free Tier Limitations

The free tier has some restrictions:
- Stock API: Limited to 'america' country
- Rate limits may apply to certain endpoints

## Date Formats

All date parameters should be in `YYYY-MM-DD` format:

```python
data = client.get_stock_prices("AAPL", from_date="2024-01-01", to_date="2024-12-31")
```

## Time Frames

Price endpoints support various time frames:
- `daily` (default)
- `weekly`
- `monthly`
- `quarterly`
- `yearly`

```python
prices = client.get_stock_prices("AAPL", frame="monthly")
```

## Support

For API documentation, support, or to obtain an API key, visit the Axion API website.

## License

See LICENSE file for details.
