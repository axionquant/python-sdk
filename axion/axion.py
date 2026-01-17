import requests
import json

BASE_URL = "https://api.axionquant.com"


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


class BaseAPI:
    def __init__(self, client):
        self.client = client

    def _request(self, method: str, path: str, params: dict = None, json_data: dict = None, auth_required: bool = True):
        return self.client._request(method, path, params, json_data, auth_required)


class CreditAPI(BaseAPI):
    def search(self, query: str):
        """Search for credit entities."""
        params = {"query": query}
        return self._request("GET", "credit/search", params=params)

    def ratings(self, entity_id: str):
        """Get ratings for a specific credit entity."""
        return self._request("GET", f"credit/ratings/{entity_id}")


class ESGAPI(BaseAPI):
    def data(self, ticker: str):
        """Get ESG data for a given ticker."""
        return self._request("GET", f"esg/{ticker}")


class ETFAPI(BaseAPI):
    def fund(self, ticker: str):
        """Get detailed fund data for an ETF."""
        return self._request("GET", f"etfs/{ticker}/fund")

    def holdings(self, ticker: str):
        """Get holdings data for an ETF."""
        return self._request("GET", f"etfs/{ticker}/holdings")

    def exposure(self, ticker: str):
        """Get exposure data for an ETF holding."""
        return self._request("GET", f"etfs/{ticker}/exposure")


class SupplyChainAPI(BaseAPI):
    def customers(self, ticker: str):
        """Get customer data for a given ticker."""
        return self._request("GET", f"supply-chain/{ticker}/customers")

    def peers(self, ticker: str):
        """Get peer data for a given ticker."""
        return self._request("GET", f"supply-chain/{ticker}/peers")

    def suppliers(self, ticker: str):
        """Get supplier data for a given ticker."""
        return self._request("GET", f"supply-chain/{ticker}/suppliers")


class StocksAPI(BaseAPI):
    def tickers(self, country: str = None, exchange: str = None):
        """Get all stock tickers with optional filtering."""
        params = {}
        if country is not None:
            params["country"] = country
        if exchange is not None:
            params["exchange"] = exchange
        return self._request("GET", "stocks/tickers", params=params)

    def quote(self, ticker: str):
        """Get a single stock ticker by its ticker symbol."""
        return self._request("GET", f"stocks/{ticker}")

    def prices(self, ticker: str, from_date: str = None, to_date: str = None, frame: str = 'daily'):
        """Get prices for a specific stock ticker."""
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if frame != 'daily':
            params["frame"] = frame
        return self._request("GET", f"stocks/{ticker}/prices", params=params)


class CryptoAPI(BaseAPI):
    def tickers(self, type: str = None):
        """Get all cryptocurrency tickers with optional filtering."""
        params = {}
        if type is not None:
            params["type"] = type
        return self._request("GET", "crypto/tickers", params=params)

    def quote(self, ticker: str):
        """Get a single cryptocurrency ticker by its ticker symbol."""
        return self._request("GET", f"crypto/{ticker}")

    def prices(self, ticker: str, from_date: str = None, to_date: str = None, frame: str = 'daily'):
        """Get prices for a specific cryptocurrency ticker."""
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if frame != 'daily':
            params["frame"] = frame
        return self._request("GET", f"crypto/{ticker}/prices", params=params)


class ForexAPI(BaseAPI):
    def tickers(self, country: str = None, exchange: str = None):
        """Get all forex tickers with optional filtering."""
        params = {}
        if country is not None:
            params["country"] = country
        if exchange is not None:
            params["exchange"] = exchange
        return self._request("GET", "forex/tickers", params=params)

    def quote(self, ticker: str):
        """Get a single forex ticker by its ticker symbol."""
        return self._request("GET", f"forex/{ticker}")

    def prices(self, ticker: str, from_date: str = None, to_date: str = None, frame: str = 'daily'):
        """Get prices for a specific forex ticker."""
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if frame != 'daily':
            params["frame"] = frame
        return self._request("GET", f"forex/{ticker}/prices", params=params)


class FuturesAPI(BaseAPI):
    def tickers(self, exchange: str = None):
        """Get all futures tickers with optional filtering."""
        params = {}
        if exchange is not None:
            params["exchange"] = exchange
        return self._request("GET", "futures/tickers", params=params)

    def quote(self, ticker: str):
        """Get a single futures ticker by its ticker symbol."""
        return self._request("GET", f"futures/{ticker}")

    def prices(self, ticker: str, from_date: str = None, to_date: str = None, frame: str = 'daily'):
        """Get prices for a specific futures ticker."""
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if frame != 'daily':
            params["frame"] = frame
        return self._request("GET", f"futures/{ticker}/prices", params=params)


class IndicesAPI(BaseAPI):
    def tickers(self, exchange: str = None):
        """Get all index tickers with optional filtering."""
        params = {}
        if exchange is not None:
            params["exchange"] = exchange
        return self._request("GET", "indices/tickers", params=params)

    def quote(self, ticker: str):
        """Get a single index ticker by its ticker symbol."""
        return self._request("GET", f"indices/{ticker}")

    def prices(self, ticker: str, from_date: str = None, to_date: str = None, frame: str = 'daily'):
        """Get prices for a specific index ticker."""
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if frame != 'daily':
            params["frame"] = frame
        return self._request("GET", f"indices/{ticker}/prices", params=params)


class EconAPI(BaseAPI):
    def search(self, query: str):
        """Search for economic series."""
        params = {"query": query}
        return self._request("GET", "econ/search", params=params)

    def dataset(self, series_id: str):
        """Get economic series observations (all releases)."""
        return self._request("GET", f"econ/dataset/{series_id}")

    def calendar(self, from_date: str = None, to_date: str = None, country: str = None,
                 min_importance: int = None, currency: str = None, category: str = None):
        """Get economic calendar data with optional filters."""
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


class NewsAPI(BaseAPI):
    def general(self):
        """Get general news articles."""
        return self._request("GET", "news")

    def company(self, ticker: str):
        """Get news articles for a specific company."""
        return self._request("GET", f"news/{ticker}")

    def country(self, country: str):
        """Get news articles for a specific country."""
        return self._request("GET", f"news/country/{country}")

    def category(self, category: str):
        """Get news articles for a specific category."""
        return self._request("GET", f"news/category/{category}")


class SentimentAPI(BaseAPI):
    def all(self, ticker: str):
        """Get all sentiment data (social, news, and analyst) for a ticker."""
        return self._request("GET", f"sentiment/{ticker}/all")

    def social(self, ticker: str):
        """Get social sentiment data for a ticker."""
        return self._request("GET", f"sentiment/{ticker}/social")

    def news(self, ticker: str):
        """Get news sentiment data for a ticker."""
        return self._request("GET", f"sentiment/{ticker}/news")

    def analyst(self, ticker: str):
        """Get analyst sentiment data for a ticker."""
        return self._request("GET", f"sentiment/{ticker}/analyst")


class ProfilesAPI(BaseAPI):
    def asset(self, ticker: str):
        """Get company asset profile and business summary."""
        return self._request("GET", f"profiles/{ticker}/asset")

    def recommendation(self, ticker: str):
        """Get analyst recommendation trends."""
        return self._request("GET", f"profiles/{ticker}/recommendation")

    def cashflow(self, ticker: str):
        """Get cash flow statement history."""
        return self._request("GET", f"profiles/{ticker}/cashflow")

    def index_trend(self, ticker: str):
        """Get index trend estimates."""
        return self._request("GET", f"profiles/{ticker}/trend/index")

    def statistics(self, ticker: str):
        """Get key statistics and financial ratios."""
        return self._request("GET", f"profiles/{ticker}/statistics")

    def income(self, ticker: str):
        """Get income statement history."""
        return self._request("GET", f"profiles/{ticker}/income")

    def fund_ownership(self, ticker: str):
        """Get fund ownership data."""
        return self._request("GET", f"profiles/{ticker}/fund")

    def summary(self, ticker: str):
        """Get summary detail including prices, volumes, and market data."""
        return self._request("GET", f"profiles/{ticker}/summary")

    def insiders(self, ticker: str):
        """Get insider holders and their positions."""
        return self._request("GET", f"profiles/{ticker}/insiders")

    def calendar(self, ticker: str):
        """Get calendar events including earnings dates and dividends."""
        return self._request("GET", f"profiles/{ticker}/calendar")

    def balancesheet(self, ticker: str):
        """Get balance sheet history."""
        return self._request("GET", f"profiles/{ticker}/balancesheet")

    def earnings_trend(self, ticker: str):
        """Get earnings trend and estimates."""
        return self._request("GET", f"profiles/{ticker}/trend/earnings")

    def institution_ownership(self, ticker: str):
        """Get institutional ownership data."""
        return self._request("GET", f"profiles/{ticker}/institution")

    def ownership(self, ticker: str):
        """Get major holders breakdown."""
        return self._request("GET", f"profiles/{ticker}/ownership")

    def earnings(self, ticker: str):
        """Get historical earnings data."""
        return self._request("GET", f"profiles/{ticker}/earnings")

    def info(self, ticker: str):
        """Get company profile information."""
        return self._request("GET", f"profiles/{ticker}/info")

    def activity(self, ticker: str):
        """Get net share purchase activity."""
        return self._request("GET", f"profiles/{ticker}/activity")

    def transactions(self, ticker: str):
        """Get insider transactions."""
        return self._request("GET", f"profiles/{ticker}/transactions")

    def financials(self, ticker: str):
        """Get comprehensive financial data."""
        return self._request("GET", f"profiles/{ticker}/financials")

    def traffic(self, ticker: str):
        """Get website traffic and analytics data."""
        return self._request("GET", f"profiles/{ticker}/traffic")


class Axion:
    def __init__(self, api_key: str = None):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

        # Initialize nested API classes
        self.credit = CreditAPI(self)
        self.esg = ESGAPI(self)
        self.etfs = ETFAPI(self)
        self.supply_chain = SupplyChainAPI(self)
        self.stocks = StocksAPI(self)
        self.crypto = CryptoAPI(self)
        self.forex = ForexAPI(self)
        self.futures = FuturesAPI(self)
        self.indices = IndicesAPI(self)
        self.econ = EconAPI(self)
        self.news = NewsAPI(self)
        self.sentiment = SentimentAPI(self)
        self.profiles = ProfilesAPI(self)

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
