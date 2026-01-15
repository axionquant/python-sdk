#!/usr/bin/env python3
"""
Example usage of Axion Financial Data SDK

This script demonstrates various API endpoints available through the Axion SDK.
Make sure to set your API key as an environment variable or pass it directly.

Usage:
    export AXION_API_KEY="your_api_key_here"
    python example.py
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv  # Optional: for loading from .env file

# Import the Axion SDK (assuming it's in axion.py in the same directory)
try:
    from axion import Axion
except ImportError:
    # If axion.py is not in the same directory, adjust the import path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from axion import Axion

# Load environment variables from .env file (optional)
load_dotenv()


class AxionExample:
    def __init__(self, api_key: str = None):
        """Initialize the Axion client"""
        if not api_key:
            api_key = os.getenv("AXION_API_KEY")
            if not api_key:
                raise ValueError(
                    "API key is required. Set AXION_API_KEY environment variable or pass it directly."
                )

        self.client = Axion(api_key=api_key)
        print(f"✓ Axion client initialized successfully")
        print("-" * 50)

    def run_all_examples(self):
        """Run a selection of API examples"""
        print("Running Axion SDK Examples")
        print("=" * 50)

        try:
            # 1. Stocks Examples
            self.stock_examples()

            # 2. Company Profile Examples
            self.company_examples()

            # 3. ETF Examples
            self.etf_examples()

            # 4. Crypto Examples
            self.crypto_examples()

            # 5. Economic Data Examples
            self.economic_examples()

            # 6. News and Sentiment Examples
            self.news_sentiment_examples()

            # 7. Credit and ESG Examples
            self.credit_esg_examples()

            # 8. Supply Chain Examples
            self.supply_chain_examples()

            # 9. Other Asset Classes
            self.other_assets_examples()

        except Exception as e:
            print(f"Error: {e}")
            print("Make sure your API key is valid and you have access to the requested endpoints.")

    def stock_examples(self):
        """Examples for stock data endpoints"""
        print("\n1. STOCK DATA EXAMPLES")
        print("-" * 30)

        # Get stock tickers (limited to America for free tier)
        print("\nGetting US stock tickers...")
        try:
            tickers = self.client.get_stock_tickers(country="america", exchange="NASDAQ")
            print(f"Found {len(tickers) if isinstance(tickers, list) else 'multiple'} tickers")
        except Exception as e:
            print(f"Note: {e}")

        # Get specific stock data
        print("\nGetting Apple (AAPL) data...")
        try:
            apple_data = self.client.get_stock_ticker_by_symbol("AAPL")
            print(f"AAPL: {apple_data.get('name', 'Unknown')}")
            print(f"Market Cap: {apple_data.get('market_cap', 'N/A')}")
        except Exception as e:
            print(f"Error getting AAPL data: {e}")

        # Get stock prices with date range
        print("\nGetting AAPL prices for last 30 days...")
        try:
            to_date = datetime.now().strftime("%Y-%m-%d")
            from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

            prices = self.client.get_stock_prices(
                ticker="AAPL",
                from_date=from_date,
                to_date=to_date,
                frame="daily"
            )

            if isinstance(prices, list) and len(prices) > 0:
                print(f"Got {len(prices)} price points")
                latest = prices[-1] if isinstance(prices[-1], dict) else prices[-1]
                print(f"Latest close: {latest.get('close', 'N/A')}")
        except Exception as e:
            print(f"Error getting prices: {e}")

    def company_examples(self):
        """Examples for company profile data"""
        print("\n\n2. COMPANY PROFILE EXAMPLES")
        print("-" * 30)

        print("\nGetting Microsoft (MSFT) company profile...")
        try:
            # Get basic company info
            profile = self.client.get_company_profile_info("MSFT")
            print(f"Company: {profile.get('name', 'N/A')}")
            print(f"Sector: {profile.get('sector', 'N/A')}")
            print(f"Industry: {profile.get('industry', 'N/A')}")

            # Get financial data
            financials = self.client.get_company_financial_data("MSFT")
            if financials:
                print(f"Financial data available: {len(financials) if isinstance(financials, list) else 'Yes'}")

            # Get earnings data
            earnings = self.client.get_company_earnings_history("MSFT")
            if earnings and isinstance(earnings, list):
                print(f"Earnings history: {len(earnings)} periods")

        except Exception as e:
            print(f"Error: {e}")

    def etf_examples(self):
        """Examples for ETF data"""
        print("\n\n3. ETF EXAMPLES")
        print("-" * 30)

        print("\nGetting SPY ETF data...")
        try:
            # Get ETF fund data
            spy_data = self.client.get_etf_fund_data("SPY")
            print(f"ETF: {spy_data.get('name', 'N/A')}")
            print(f"Assets: {spy_data.get('total_assets', 'N/A')}")

            # Get holdings
            holdings = self.client.get_etf_holdings("SPY")
            if holdings and isinstance(holdings, list) and len(holdings) > 0:
                print(f"Top holdings: {len(holdings)} positions")
                for i, holding in enumerate(holdings[:3]):  # Show first 3
                    if isinstance(holding, dict):
                        print(f"  {i+1}. {holding.get('ticker', 'N/A')}: {holding.get('weight', 'N/A')}%")

        except Exception as e:
            print(f"Error: {e}")

    def crypto_examples(self):
        """Examples for cryptocurrency data"""
        print("\n\n4. CRYPTOCURRENCY EXAMPLES")
        print("-" * 30)

        print("\nGetting cryptocurrency tickers...")
        try:
            crypto_tickers = self.client.get_crypto_tickers(type="coin")
            print(f"Found {len(crypto_tickers) if isinstance(crypto_tickers, list) else 'multiple'} crypto coins")

            # Get Bitcoin data
            btc_data = self.client.get_crypto_ticker_by_symbol("BTC")
            print(f"\nBitcoin (BTC):")
            print(f"Price: ${btc_data.get('price', 'N/A')}")
            print(f"Market Cap: ${btc_data.get('market_cap', 'N/A')}")

            # Get Bitcoin prices
            btc_prices = self.client.get_crypto_prices(
                ticker="BTC",
                from_date="2024-01-01",
                to_date="2024-01-07",
                frame="daily"
            )
            if btc_prices and isinstance(btc_prices, list):
                print(f"BTC price data points: {len(btc_prices)}")

        except Exception as e:
            print(f"Error: {e}")

    def economic_examples(self):
        """Examples for economic data"""
        print("\n\n5. ECONOMIC DATA EXAMPLES")
        print("-" * 30)

        print("\nGetting economic calendar for next week...")
        try:
            from_date = datetime.now().strftime("%Y-%m-%d")
            to_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

            calendar = self.client.get_econ_calendar(
                from_date=from_date,
                to_date=to_date,
                country="US",
                min_importance=2
            )

            if calendar and isinstance(calendar, list):
                print(f"Economic events: {len(calendar)}")
                for event in calendar[:3]:  # Show first 3 events
                    if isinstance(event, dict):
                        print(f"  • {event.get('title', 'N/A')} - {event.get('date', 'N/A')}")

        except Exception as e:
            print(f"Error: {e}")

    def news_sentiment_examples(self):
        """Examples for news and sentiment data"""
        print("\n\n6. NEWS & SENTIMENT EXAMPLES")
        print("-" * 30)

        print("\nGetting general news...")
        try:
            news = self.client.get_news()
            if news and isinstance(news, list):
                print(f"Recent news articles: {len(news)}")
                for article in news[:2]:  # Show first 2 articles
                    if isinstance(article, dict):
                        print(f"  • {article.get('title', 'N/A')}")

            # Get sentiment for a stock
            sentiment = self.client.get_sentiment_all("AAPL")
            if sentiment:
                print(f"\nAAPL sentiment data available")
                if isinstance(sentiment, dict):
                    for key in sentiment:
                        print(f"  {key}: {sentiment[key]}")

        except Exception as e:
            print(f"Error: {e}")

    def credit_esg_examples(self):
        """Examples for credit and ESG data"""
        print("\n\n7. CREDIT & ESG EXAMPLES")
        print("-" * 30)

        print("\nGetting ESG data for Microsoft...")
        try:
            esg_data = self.client.get_esg_data("MSFT")
            if esg_data:
                print("ESG data retrieved")
                if isinstance(esg_data, dict):
                    print(f"ESG Score: {esg_data.get('esg_score', 'N/A')}")
                    print(f"Environment Score: {esg_data.get('environment_score', 'N/A')}")

            # Search for credit entities
            credit_search = self.client.search_credit("Apple")
            if credit_search and isinstance(credit_search, list):
                print(f"\nCredit search results: {len(credit_search)}")

        except Exception as e:
            print(f"Error: {e}")

    def supply_chain_examples(self):
        """Examples for supply chain data"""
        print("\n\n8. SUPPLY CHAIN EXAMPLES")
        print("-" * 30)

        print("\nGetting supply chain data for Apple...")
        try:
            # Get suppliers
            suppliers = self.client.get_supply_chain_suppliers("AAPL")
            if suppliers and isinstance(suppliers, list):
                print(f"Suppliers: {len(suppliers)} companies")

            # Get customers
            customers = self.client.get_supply_chain_customers("AAPL")
            if customers and isinstance(customers, list):
                print(f"Customers: {len(customers)} companies")

        except Exception as e:
            print(f"Error: {e}")

    def other_assets_examples(self):
        """Examples for other asset classes"""
        print("\n\n9. OTHER ASSET CLASSES")
        print("-" * 30)

        print("\nGetting forex data...")
        try:
            forex_tickers = self.client.get_forex_tickers()
            if forex_tickers:
                print(f"Forex pairs available: {len(forex_tickers) if isinstance(forex_tickers, list) else 'Multiple'}")

            # Get indices
            indices = self.client.get_index_tickers()
            if indices:
                print(f"Market indices: {len(indices) if isinstance(indices, list) else 'Multiple'}")

        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main function to run examples"""
    print("\n" + "="*60)
    print("AXION FINANCIAL DATA SDK - EXAMPLE USAGE")
    print("="*60)

    # Initialize with API key (from env var or prompt)
    api_key = os.getenv("AXION_API_KEY")

    if not api_key:
        print("\n⚠  API key not found in environment variables.")
        print("You can:")
        print("  1. Set AXION_API_KEY environment variable")
        print("  2. Enter your API key now")
        print("  3. Create a .env file with AXION_API_KEY=your_key")

        choice = input("\nEnter choice (1-3) or press Enter to skip: ").strip()

        if choice == "2":
            api_key = input("Enter your Axion API key: ").strip()
        elif choice == "3":
            # Try to load from .env
            load_dotenv()
            api_key = os.getenv("AXION_API_KEY")

    if not api_key:
        print("\n❌ No API key provided. Exiting.")
        print("\nTo get an API key, visit: https://axion.com/api")
        return

    try:
        # Create example instance and run all examples
        example = AxionExample(api_key=api_key)
        example.run_all_examples()

        print("\n" + "="*60)
        print("EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nFor more information and full API documentation:")
        print("Visit: https://docs.axion.com")

    except Exception as e:
        print(f"\n❌ Failed to initialize or run examples: {e}")
        print("Please check your API key and internet connection.")


if __name__ == "__main__":
    main()
