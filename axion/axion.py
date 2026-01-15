import requests
import json

BASE_URL = "http://localhost:3001"


def normalize(obj):
    if isinstance(obj, dict):
        return {k: normalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalize(v) for v in obj]
    return coerce(obj)


def coerce(value):
    if isinstance(value, str):
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            if value.lower() == 'true':
                return True
            if value.lower() == 'false':
                return False
    return value


class Axion:
    def __init__(self, api_key: str = None):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def _request(self, method: str, path: str, params: dict = None, json_data: dict = None, auth_required: bool = True):
        url = f"{self.base_url}/{path}"
        headers = self.session.headers.copy()

        if not auth_required and "Authorization" in headers:
            del headers["Authorization"]
        elif auth_required and "Authorization" not in headers:
            raise Exception("Authentication required but no API key provided to client.")

        try:
            response = self.session.request(method, url, params=params, json=json_data, headers=headers)
            response.raise_for_status()

            data = response.json()
            r = normalize(data)
            return r
        except requests.exceptions.HTTPError as e:
            try:
                error_data = e.response.json()
                raise Exception(f"HTTP Error {e.response.status_code}: {error_data.get('message', 'Unknown HTTP error')}") from e
            except json.JSONDecodeError:
                raise Exception(f"HTTP Error {e.response.status_code}: {e.response.text}") from e
        except requests.exceptions.ConnectionError as e:
            raise Exception(f"Connection Error: Could not connect to {self.base_url}") from e
        except requests.exceptions.Timeout as e:
            raise Exception(f"Timeout Error: Request to {self.base_url} timed out") from e
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request Error: {e}") from e

    # --- Credit API ---
    def search_credit(self, query: str):
        """
        Search for credit entities.
        Authentication required.
        :param query: The search term for credit entities.
        """
        params = {"query": query}
        return self._request("GET", "credit/search", params=params)

    def get_credit_ratings(self, entity_id: str):
        """
        Get ratings for a specific credit entity.
        Authentication required.
        :param entity_id: The ID of the credit entity.
        """
        return self._request("GET", f"credit/ratings/{entity_id}")

    # --- ESG API ---
    def get_esg_data(self, ticker: str):
        """
        Get ESG data for a given ticker.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"esg/{ticker}")

    # --- ETF API ---
    def get_etf_fund_data(self, ticker: str):
        """
        Get detailed fund data for an ETF.
        Authentication required.
        :param ticker: The ETF ticker symbol.
        """
        return self._request("GET", f"etfs/{ticker}/fund")

    def get_etf_holdings(self, ticker: str):
        """
        Get holdings data for an ETF.
        Authentication required.
        :param ticker: The ETF ticker symbol.
        """
        return self._request("GET", f"etfs/{ticker}/holdings")

    def get_etf_exposure(self, ticker: str):
        """
        Get exposure data for an ETF holding.
        Authentication required.
        :param ticker: The ETF holding ticker symbol.
        """
        return self._request("GET", f"etfs/{ticker}/exposure")

    # --- Supply Chain API ---
    def get_supply_chain_customers(self, ticker: str):
        """
        Get customer data for a given ticker.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"supply-chain/{ticker}/customers")

    def get_supply_chain_peers(self, ticker: str):
        """
        Get peer data for a given ticker.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"supply-chain/{ticker}/peers")

    def get_supply_chain_suppliers(self, ticker: str):
        """
        Get supplier data for a given ticker.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"supply-chain/{ticker}/suppliers")

    # --- Stocks API ---
    def get_stock_tickers(self, country: str = None, exchange: str = None):
        """
        Get all stock tickers with optional filtering.
        Authentication required. Free tier restricted to 'america' country.
        :param country: Optional country to filter by.
        :param exchange: Optional exchange to filter by.
        """
        params = {}
        if country is not None:
            params["country"] = country
        if exchange is not None:
            params["exchange"] = exchange
        return self._request("GET", "stocks/tickers", params=params)

    def get_stock_ticker_by_symbol(self, ticker: str):
        """
        Get a single stock ticker by its ticker symbol.
        Authentication required. Free tier restricted to 'america' country.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"stocks/{ticker}")

    def get_stock_prices(self, ticker: str, from_date: str = None, to_date: str = None, frame: str = 'daily'):
        """
        Get prices for a specific stock ticker.
        Authentication required. Free tier restricted to 'america' country.
        :param ticker: The stock ticker symbol.
        :param from_date: Start date for filtering (format: YYYY-MM-DD).
        :param to_date: End date for filtering (format: YYYY-MM-DD).
        :param frame: Time frame for aggregation ('daily', 'weekly', 'monthly', 'quarterly', 'yearly'). Default: 'daily'.
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if frame != 'daily':
            params["frame"] = frame
        return self._request("GET", f"stocks/{ticker}/prices", params=params)

    # --- Crypto API ---
    def get_crypto_tickers(self, type: str = None):
        """
        Get all cryptocurrency tickers with optional filtering.
        Authentication required.
        :param type: Optional type to filter by (e.g., 'coin', 'token').
        """
        params = {}
        if type is not None:
            params["type"] = type
        return self._request("GET", "crypto/tickers", params=params)

    def get_crypto_ticker_by_symbol(self, ticker: str):
        """
        Get a single cryptocurrency ticker by its ticker symbol.
        Authentication required.
        :param ticker: The cryptocurrency ticker symbol.
        """
        return self._request("GET", f"crypto/{ticker}")

    def get_crypto_prices(self, ticker: str, from_date: str = None, to_date: str = None, frame: str = 'daily'):
        """
        Get prices for a specific cryptocurrency ticker.
        Authentication required.
        :param ticker: The cryptocurrency ticker symbol.
        :param from_date: Start date for filtering (format: YYYY-MM-DD).
        :param to_date: End date for filtering (format: YYYY-MM-DD).
        :param frame: Time frame for aggregation ('daily', 'weekly', 'monthly', 'quarterly', 'yearly'). Default: 'daily'.
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if frame != 'daily':
            params["frame"] = frame
        return self._request("GET", f"crypto/{ticker}/prices", params=params)

    # --- Forex API ---
    def get_forex_tickers(self, country: str = None, exchange: str = None):
        """
        Get all forex tickers with optional filtering.
        Authentication required.
        :param country: Optional country to filter by.
        :param exchange: Optional exchange to filter by.
        """
        params = {}
        if country is not None:
            params["country"] = country
        if exchange is not None:
            params["exchange"] = exchange
        return self._request("GET", "forex/tickers", params=params)

    def get_forex_ticker_by_symbol(self, ticker: str):
        """
        Get a single forex ticker by its ticker symbol.
        Authentication required.
        :param ticker: The forex ticker symbol.
        """
        return self._request("GET", f"forex/{ticker}")

    def get_forex_prices(self, ticker: str, from_date: str = None, to_date: str = None, frame: str = 'daily'):
        """
        Get prices for a specific forex ticker.
        Authentication required.
        :param ticker: The forex ticker symbol.
        :param from_date: Start date for filtering (format: YYYY-MM-DD).
        :param to_date: End date for filtering (format: YYYY-MM-DD).
        :param frame: Time frame for aggregation ('daily', 'weekly', 'monthly', 'quarterly', 'yearly'). Default: 'daily'.
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if frame != 'daily':
            params["frame"] = frame
        return self._request("GET", f"forex/{ticker}/prices", params=params)

    # --- Futures API ---
    def get_futures_tickers(self, exchange: str = None):
        """
        Get all futures tickers with optional filtering.
        Authentication required.
        :param exchange: Optional exchange to filter by.
        """
        params = {}
        if exchange is not None:
            params["exchange"] = exchange
        return self._request("GET", "futures/tickers", params=params)

    def get_futures_ticker_by_symbol(self, ticker: str):
        """
        Get a single futures ticker by its ticker symbol.
        Authentication required.
        :param ticker: The futures ticker symbol.
        """
        return self._request("GET", f"futures/{ticker}")

    def get_futures_prices(self, ticker: str, from_date: str = None, to_date: str = None, frame: str = 'daily'):
        """
        Get prices for a specific futures ticker.
        Authentication required.
        :param ticker: The futures ticker symbol.
        :param from_date: Start date for filtering (format: YYYY-MM-DD).
        :param to_date: End date for filtering (format: YYYY-MM-DD).
        :param frame: Time frame for aggregation ('daily', 'weekly', 'monthly', 'quarterly', 'yearly'). Default: 'daily'.
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if frame != 'daily':
            params["frame"] = frame
        return self._request("GET", f"futures/{ticker}/prices", params=params)

    # --- Indices API ---
    def get_index_tickers(self, exchange: str = None):
        """
        Get all index tickers with optional filtering.
        Authentication required.
        :param exchange: Optional exchange to filter by.
        """
        params = {}
        if exchange is not None:
            params["exchange"] = exchange
        return self._request("GET", "indices/tickers", params=params)

    def get_index_ticker_by_symbol(self, ticker: str):
        """
        Get a single index ticker by its ticker symbol.
        Authentication required.
        :param ticker: The index ticker symbol.
        """
        return self._request("GET", f"indices/{ticker}")

    def get_index_prices(self, ticker: str, from_date: str = None, to_date: str = None, frame: str = 'daily'):
        """
        Get prices for a specific index ticker.
        Authentication required.
        :param ticker: The index ticker symbol.
        :param from_date: Start date for filtering (format: YYYY-MM-DD).
        :param to_date: End date for filtering (format: YYYY-MM-DD).
        :param frame: Time frame for aggregation ('daily', 'weekly', 'monthly', 'quarterly', 'yearly'). Default: 'daily'.
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if frame != 'daily':
            params["frame"] = frame
        return self._request("GET", f"indices/{ticker}/prices", params=params)

    # --- Economic API ---
    def search_econ(self, query: str):
        """
        Search for economic series.
        Authentication required.
        :param query: The search term for economic series.
        """
        params = {"query": query}
        return self._request("GET", "econ/search", params=params)

    def get_econ_dataset(self, series_id: str):
        """
        Get economic series observations (all releases).
        Authentication required.
        :param series_id: The ID of the economic series.
        """
        return self._request("GET", f"econ/dataset/{series_id}")


    def get_econ_calendar(self, from_date: str = None, to_date: str = None, country: str = None, min_importance: int = None, currency: str = None, category: str = None):
        """
        Get economic calendar data with optional filters.
        Authentication required.
        :param from_date: Start date for filtering (format: YYYY-MM-DD).
        :param to_date: End date for filtering (format: YYYY-MM-DD).
        :param country: Single country code or comma-separated list (e.g., 'US' or 'US,UK,CA').
        :param min_importance: Minimum importance level (numeric value).
        :param currency: Single currency code or comma-separated list (e.g., 'USD' or 'USD,EUR').
        :param category: Single category or comma-separated list (e.g., 'employment' or 'employment,inflation').
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if country is not None:
            params["country"] = country
        if min_importance is not None:
            params["minImportance"] = min_importance
        if currency is not None:
            params["currency"] = currency
        if category is not None:
            params["category"] = category
        return self._request("GET", "econ/calendar", params=params)

    # --- News API ---
    def get_news(self):
        """
        Get general news articles.
        Authentication required.
        """
        return self._request("GET", "news")

    def get_company_news(self, ticker: str):
        """
        Get news articles for a specific company.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"news/{ticker}")

    def get_country_news(self, country: str):
        """
        Get news articles for a specific country.
        Authentication required.
        :param country: The country code or name.
        """
        return self._request("GET", f"news/country/{country}")

    def get_category_news(self, category: str):
        """
        Get news articles for a specific category.
        Authentication required.
        :param category: The news category.
        """
        return self._request("GET", f"news/category/{category}")

    # --- Sentiment API ---
    def get_sentiment_all(self, ticker: str):
        """
        Get all sentiment data (social, news, and analyst) for a ticker.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"sentiment/{ticker}/all")

    def get_sentiment_social(self, ticker: str):
        """
        Get social sentiment data for a ticker.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"sentiment/{ticker}/social")

    def get_sentiment_news(self, ticker: str):
        """
        Get news sentiment data for a ticker.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"sentiment/{ticker}/news")

    def get_sentiment_analyst(self, ticker: str):
        """
        Get analyst sentiment data for a ticker.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"sentiment/{ticker}/analyst")

    # --- Company Profile API ---

    def get_company_asset_profile(self, ticker: str):
        """
        Get company asset profile and business summary.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/asset")

    def get_company_recommendation_trend(self, ticker: str):
        """
        Get analyst recommendation trends.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/recommendation")

    def get_company_cashflow(self, ticker: str):
        """
        Get cash flow statement history.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/cashflow")

    def get_company_index_trend(self, ticker: str):
        """
        Get index trend estimates.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/trend/index")

    def get_company_statistics(self, ticker: str):
        """
        Get key statistics and financial ratios.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/statistics")

    def get_company_income_statement(self, ticker: str):
        """
        Get income statement history.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/income")

    def get_company_fund_ownership(self, ticker: str):
        """
        Get fund ownership data.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/fund")

    def get_company_summary(self, ticker: str):
        """
        Get summary detail including prices, volumes, and market data.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/summary")

    def get_company_insider_holders(self, ticker: str):
        """
        Get insider holders and their positions.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/insiders")

    def get_company_calendar_events(self, ticker: str):
        """
        Get calendar events including earnings dates and dividends.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/calendar")

    def get_company_balance_sheet(self, ticker: str):
        """
        Get balance sheet history.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/balancesheet")

    def get_company_earnings_trend(self, ticker: str):
        """
        Get earnings trend and estimates.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/trend/earnings")

    def get_company_institution_ownership(self, ticker: str):
        """
        Get institutional ownership data.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/institution")

    def get_company_major_holders(self, ticker: str):
        """
        Get major holders breakdown.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/ownership")

    def get_company_earnings_history(self, ticker: str):
        """
        Get historical earnings data.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/earnings")

    def get_company_profile_info(self, ticker: str):
        """
        Get company profile information.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/info")

    def get_company_share_activity(self, ticker: str):
        """
        Get net share purchase activity.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/activity")

    def get_company_insider_transactions(self, ticker: str):
        """
        Get insider transactions.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/transactions")

    def get_company_financial_data(self, ticker: str):
        """
        Get comprehensive financial data.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/financials")

    def get_company_website_traffic(self, ticker: str):
        """
        Get website traffic and analytics data.
        Authentication required.
        :param ticker: The stock ticker symbol.
        """
        return self._request("GET", f"profiles/{ticker}/traffic")

