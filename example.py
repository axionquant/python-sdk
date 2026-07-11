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

try:
    from axion import Axion
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from axion import Axion


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
        print("Axion client initialized successfully")
        print("-" * 50)

    def run_all_examples(self):
        """Run a selection of API examples"""
        print("Running Axion SDK Examples")
        print("=" * 50)

        try:
            self.stock_examples()
            self.company_examples()
            self.etf_examples()
            self.crypto_examples()
            self.economic_examples()
            self.news_sentiment_examples()
            self.credit_esg_examples()
            self.supply_chain_examples()
            self.other_assets_examples()
        except Exception as e:
            print(f"Error: {e}")
            print("Make sure your API key is valid and you have access to the requested endpoints.")

    def stock_examples(self):
        """Examples for stock data endpoints"""
        print("\n1. STOCK DATA EXAMPLES")
        print("-" * 30)

        print("\nGetting US stock tickers...")
        try:
            tickers = self.client.stocks.tickers(country="america", exchange="NASDAQ")
            print(f"Found {len(tickers) if isinstance(tickers, list) else 'multiple'} tickers")
        except Exception as e:
            print(f"Note: {e}")

        print("\nGetting Apple (AAPL) data...")
        try:
            apple_data = self.client.stocks.ticker("AAPL")
            if isinstance(apple_data, dict):
                print(f"AAPL: {apple_data.get('name', 'Unknown')}")
                print(f"Exchange: {apple_data.get('exchange', 'N/A')}")
        except Exception as e:
            print(f"Error getting AAPL data: {e}")

        print("\nGetting AAPL stock quote...")
        try:
            quote = self.client.stocks.quote("AAPL")
            if isinstance(quote, dict):
                print(f"AAPL Price: {quote.get('price', 'N/A')}")
        except Exception as e:
            print(f"Error getting quote: {e}")

        print("\nGetting AAPL prices...")
        try:
            prices = self.client.stocks.prices(
                ticker="AAPL",
                from_date="2024-01-01",
                to_date="2024-01-31",
                frame="daily"
            )
            if isinstance(prices, list) and len(prices) > 0:
                print(f"Got {len(prices)} price points")
                latest = prices[-1]
                print(f"Latest close: {latest.get('close', 'N/A')}")
        except Exception as e:
            print(f"Error getting prices: {e}")

    def company_examples(self):
        """Examples for company profile data"""
        print("\n\n2. COMPANY PROFILE EXAMPLES")
        print("-" * 30)

        print("\nGetting Microsoft (MSFT) company profile...")
        try:
            profile = self.client.profiles.info("MSFT")
            if isinstance(profile, dict):
                print(f"Company: {profile.get('name', 'N/A')}")
                print(f"Sector: {profile.get('sector', 'N/A')}")
                print(f"Industry: {profile.get('industry', 'N/A')}")

            financials = self.client.financials.metrics("MSFT")
            if financials:
                print(f"Financial data available: {'Yes' if isinstance(financials, dict) else 'Yes'}")

            earnings = self.client.earnings.history("MSFT")
            if isinstance(earnings, list):
                print(f"Earnings history: {len(earnings)} periods")
        except Exception as e:
            print(f"Error: {e}")

    def etf_examples(self):
        """Examples for ETF data"""
        print("\n\n3. ETF EXAMPLES")
        print("-" * 30)

        print("\nGetting SPY ETF data...")
        try:
            spy_data = self.client.etfs.fund("SPY")
            if isinstance(spy_data, dict):
                print(f"ETF: {spy_data.get('fund', 'N/A')}")

            holdings = self.client.etfs.holdings("SPY")
            if isinstance(holdings, list) and len(holdings) > 0:
                print(f"Top holdings: {len(holdings)} positions")
                for i, holding in enumerate(holdings[:3]):
                    if isinstance(holding, dict):
                        print(f"  {i+1}. {holding.get('ticker', 'N/A')}: {holding.get('weight', 'N/A')}")
        except Exception as e:
            print(f"Error: {e}")

    def crypto_examples(self):
        """Examples for cryptocurrency data"""
        print("\n\n4. CRYPTOCURRENCY EXAMPLES")
        print("-" * 30)

        print("\nGetting cryptocurrency tickers...")
        try:
            crypto_tickers = self.client.crypto.tickers(type="coin")
            print(f"Found {len(crypto_tickers) if isinstance(crypto_tickers, list) else 'multiple'} crypto coins")

            btc_data = self.client.crypto.ticker("BTC")
            if isinstance(btc_data, dict):
                print(f"\nBitcoin (BTC):")
                print(f"Name: {btc_data.get('name', 'N/A')}")

            btc_prices = self.client.crypto.prices(
                ticker="BTC",
                from_date="2024-01-01",
                to_date="2024-01-07",
                frame="daily"
            )
            if isinstance(btc_prices, list):
                print(f"BTC price data points: {len(btc_prices)}")
        except Exception as e:
            print(f"Error: {e}")

    def economic_examples(self):
        """Examples for economic data"""
        print("\n\n5. ECONOMIC DATA EXAMPLES")
        print("-" * 30)

        print("\nGetting economic calendar...")
        try:
            calendar = self.client.econ.calendar(
                from_date="2024-01-01",
                to_date="2024-01-07",
                country="US",
                min_importance=2
            )
            if isinstance(calendar, list):
                print(f"Economic events: {len(calendar)}")
                for event in calendar[:3]:
                    if isinstance(event, dict):
                        print(f"  - {event.get('title', 'N/A')} - {event.get('date', 'N/A')}")
        except Exception as e:
            print(f"Error: {e}")

        print("\nSearching economic datasets with AI...")
        try:
            results = self.client.econ.find("unemployment rate")
            if isinstance(results, list):
                print(f"Found {len(results)} datasets")
        except Exception as e:
            print(f"Error: {e}")

    def news_sentiment_examples(self):
        """Examples for news and sentiment data"""
        print("\n\n6. NEWS & SENTIMENT EXAMPLES")
        print("-" * 30)

        print("\nGetting general news...")
        try:
            news = self.client.news.general()
            if isinstance(news, list):
                print(f"Recent news articles: {len(news)}")
                for article in news[:2]:
                    if isinstance(article, dict):
                        print(f"  - {article.get('title', 'N/A')}")

            sentiment = self.client.sentiment.all("AAPL")
            if isinstance(sentiment, dict):
                print(f"\nAAPL sentiment data available")
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
            esg_data = self.client.esg.data("MSFT")
            if isinstance(esg_data, list):
                print("ESG data retrieved")
                for entry in esg_data:
                    if isinstance(entry, dict):
                        print(f"  {entry.get('category', 'N/A')}: {entry.get('score', 'N/A')} ({entry.get('grade', 'N/A')})")

            credit_search = self.client.credit.search("Apple")
            if isinstance(credit_search, list):
                print(f"\nCredit search results: {len(credit_search)}")
        except Exception as e:
            print(f"Error: {e}")

    def supply_chain_examples(self):
        """Examples for supply chain data"""
        print("\n\n8. SUPPLY CHAIN EXAMPLES")
        print("-" * 30)

        print("\nGetting supply chain data for Apple...")
        try:
            suppliers = self.client.supply_chain.suppliers("AAPL")
            if isinstance(suppliers, list):
                print(f"Suppliers: {len(suppliers)} companies")

            customers = self.client.supply_chain.customers("AAPL")
            if isinstance(customers, list):
                print(f"Customers: {len(customers)} companies")
        except Exception as e:
            print(f"Error: {e}")

    def other_assets_examples(self):
        """Examples for other asset classes"""
        print("\n\n9. OTHER ASSET CLASSES")
        print("-" * 30)

        print("\nGetting forex data...")
        try:
            forex_tickers = self.client.forex.tickers()
            if isinstance(forex_tickers, list):
                print(f"Forex pairs available: {len(forex_tickers)}")

            indices = self.client.indices.tickers()
            if isinstance(indices, list):
                print(f"Market indices: {len(indices)}")
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main function to run examples"""
    print("\n" + "=" * 60)
    print("AXION FINANCIAL DATA SDK - EXAMPLE USAGE")
    print("=" * 60)

    api_key = os.getenv("AXION_API_KEY")

    if not api_key:
        print("\nAPI key not found in environment variables.")
        print("You can:")
        print("  1. Set AXION_API_KEY environment variable")
        print("  2. Enter your API key now")
        print("  3. Create a .env file with AXION_API_KEY=your_key")

        choice = input("\nEnter choice (1-3) or press Enter to skip: ").strip()

        if choice == "2":
            api_key = input("Enter your Axion API key: ").strip()

    if not api_key:
        print("\nNo API key provided. Exiting.")
        print("\nTo get an API key, visit: https://axionquant.com/dashboard/api-keys")
        return

    try:
        example = AxionExample(api_key=api_key)
        example.run_all_examples()

        print("\n" + "=" * 60)
        print("EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nFor more information and full API documentation:")
        print("Visit: https://axionquant.com")

    except Exception as e:
        print(f"\nFailed to initialize or run examples: {e}")
        print("Please check your API key and internet connection.")


if __name__ == "__main__":
    main()
