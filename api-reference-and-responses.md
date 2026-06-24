# Axion API Reference

All endpoints use `GET` method and return JSON. Base path prefix applies per asset class. All time-series endpoints accept `from` and `to` query parameters for date filtering.

---

## Market Data APIs

### 1. Stocks API

#### Get Stock Ticker Details
```
GET /stocks/:ticker
```
**Path Params:** `ticker` (string, required) – Stock symbol.

**Response Fields:** `id`, `ticker`, `symbol` (with exchange prefix), `exchange`, `country`.

**Sample Response:**
```json
{
  "id": 6723,
  "ticker": "MSFT",
  "symbol": "NASDAQ:MSFT",
  "exchange": "NASDAQ",
  "country": "america"
}
```

#### Get Historical Stock Price Data
```
GET /stocks/:ticker/prices
```
**Path Params:** `ticker` (string, required).

**Query Params:** `from` (date), `to` (date), `frame` (string: daily/weekly/monthly/quarterly/yearly), `page` (int), `size` (int).

**Response Fields:** `time` (ISO 8601), `ticker`, `open`, `high`, `low`, `close`, `volume` (all returned as strings to preserve decimal precision).

**Sample Response:**
```json
[
  {
    "time": "2025-12-19T19:03:05.000Z",
    "ticker": "AAPL",
    "open": "272.1400",
    "high": "272.9200",
    "low": "270.2700",
    "close": "270.6700",
    "volume": "43267805"
  },
  {
    "time": "2025-12-18T14:30:00.000Z",
    "ticker": "AAPL",
    "open": "273.6100",
    "high": "273.6300",
    "low": "266.9500",
    "close": "272.1900",
    "volume": "51600000"
  }
]
```

#### Get All Stock Tickers
```
GET /stocks/tickers
```
**Query Params:** `exchange` (string), `country` (string), `page` (int), `size` (int).

**Response Fields:** `id`, `ticker`, `symbol`, `exchange`, `country`.

**Sample Response:**
```json
[
  {
    "id": 1,
    "ticker": "MTST",
    "symbol": "OTC:MTST",
    "exchange": "OTC",
    "country": "america"
  },
  {
    "id": 2,
    "ticker": "LGHT",
    "symbol": "AMEX:LGHT",
    "exchange": "AMEX",
    "country": "america"
  },
  {
    "id": 6723,
    "ticker": "MSFT",
    "symbol": "NASDAQ:MSFT",
    "exchange": "NASDAQ",
    "country": "america"
  }
]
```

---

### 2. Indices API

#### Get Index Ticker Details
```
GET /indices/:ticker
```
**Path Params:** `ticker` (string, required).

**Response Fields:** `id`, `ticker`, `name`, `exchange`.

**Sample Response:**
```json
{
  "id": 48,
  "ticker": "GRNWATERLEURX",
  "name": "NASDAQ OMX Global Water EUR Tot",
  "exchange": "NIM"
}
```

#### Get Historical Index Data
```
GET /indices/:ticker/prices
```
**Query Params:** `from`, `to`, `period`, `page`, `size`.

**Response:** Array of `{ time, ticker, open, high, low, close, volume }`.

**Sample Response:**
```json
[
  {
    "time": "2025-12-19T16:31:46.000Z",
    "ticker": "GVZ",
    "open": "21.2600",
    "high": "21.3900",
    "low": "20.8100",
    "close": "21.0600",
    "volume": "0"
  },
  {
    "time": "2025-12-18T14:30:00.000Z",
    "ticker": "GVZ",
    "open": "20.6500",
    "high": "21.5100",
    "low": "20.0500",
    "close": "21.3100",
    "volume": "0"
  }
]
```

#### Get All Index Tickers
```
GET /indices/tickers
```
**Query Params:** `exchange` (string).

**Response:** Array of index ticker objects.

**Sample Response:**
```json
[
  {
    "id": 1,
    "ticker": "AXJO",
    "name": "S&P/ASX 200",
    "exchange": "ASX"
  },
  {
    "id": 2,
    "ticker": "AEX",
    "name": "AEX-Index",
    "exchange": "AMS"
  },
  {
    "id": 48,
    "ticker": "GRNWATERLEURX",
    "name": "NASDAQ OMX Global Water EUR Tot",
    "exchange": "NIM"
  }
]
```

---

### 3. Futures API

#### Get Specific Futures Ticker
```
GET /futures/:ticker
```
**Path Params:** `ticker` (string, required).

**Response Fields:** `id`, `ticker`, `name`, `exchange`.

**Sample Response:**
```json
{
  "id": 1,
  "ticker": "ALI",
  "name": "Aluminum Futures,Feb-2026",
  "exchange": "CMX"
}
```

#### Get Historical Price Data
```
GET /futures/:ticker/prices
```
**Query Params:** `from`, `to`, `period`, `page`, `size`.

**Response:** Array of `{ time, ticker, open, high, low, close, volume }`.

**Sample Response:**
```json
[
  {
    "time": "2025-12-19T16:02:30.000Z",
    "ticker": "ALI",
    "open": "2920.2500",
    "high": "2965.2500",
    "low": "2914.0000",
    "close": "2964.0000",
    "volume": "327"
  },
  {
    "time": "2025-12-18T05:00:00.000Z",
    "ticker": "ALI",
    "open": "2823.7500",
    "high": "2823.7500",
    "low": "2823.7500",
    "close": "2823.7500",
    "volume": "0"
  }
]
```

#### Get All Futures Tickers
```
GET /futures/tickers
```
**Query Params:** `exchange` (string), `type` (string), `page`, `size`.

**Response:** Array of futures ticker objects.

**Sample Response:**
```json
[
  {
    "id": 1,
    "ticker": "ALI",
    "name": "Aluminum Futures,Feb-2026",
    "exchange": "CMX"
  },
  {
    "id": 2,
    "ticker": "M6A",
    "name": "Micro AUD/USD Futures,Mar-2026",
    "exchange": "CME"
  },
  {
    "id": 3,
    "ticker": "BTC",
    "name": "Bitcoin Futures,Dec-2025",
    "exchange": "CME"
  }
]
```

---

### 4. Forex API

#### Get Forex Ticker Details
```
GET /forex/:ticker
```
**Path Params:** `ticker` (string, required – e.g. EURUSD).

**Response Fields:** `id`, `ticker`, `detail`, `exchange`, `country`.

**Sample Response:**
```json
{
  "id": 1,
  "ticker": "AEDAUD",
  "detail": "U.A.E. DIRHAM / AUSTRALIAN DOLLAR",
  "exchange": "IDC",
  "country": "AE"
}
```

#### Get Historical Exchange Rate Data
```
GET /forex/:ticker/prices
```
**Query Params:** `from`, `to`, `period`, `page`, `size`.

**Response:** Array of `{ time, ticker, open, high, low, close, volume }`.

**Sample Response:**
```json
[
  {
    "time": "2025-12-19T00:00:00.000Z",
    "ticker": "AEDAUD",
    "open": "0.4100",
    "high": "0.4100",
    "low": "0.4100",
    "close": "0.4100",
    "volume": "0"
  },
  {
    "time": "2025-12-18T00:00:00.000Z",
    "ticker": "AEDAUD",
    "open": "0.4100",
    "high": "0.4100",
    "low": "0.4100",
    "close": "0.4100",
    "volume": "0"
  }
]
```

#### Get All Forex Tickers
```
GET /forex/tickers
```
**Query Params:** `country` (string), `exchange` (string).

**Response:** Array of forex ticker objects.

**Sample Response:**
```json
[
  {
    "id": 1,
    "ticker": "AEDAUD",
    "detail": "U.A.E. DIRHAM / AUSTRALIAN DOLLAR",
    "exchange": "IDC",
    "country": "AE"
  },
  {
    "id": 2,
    "ticker": "AFNUSD",
    "detail": "AFGHAN AFGHANI / US DOLLAR",
    "exchange": "IDC",
    "country": "AF"
  }
]
```

---

### 5. Crypto API

#### Get Cryptocurrency Ticker Details
```
GET /crypto/:ticker
```
**Path Params:** `ticker` (string, required – e.g. BTC).

**Response Fields:** `id`, `ticker`, `name`, `type` (coin/token).

**Sample Response:**
```json
{
  "id": 1,
  "ticker": "BTC",
  "name": "Bitcoin",
  "type": "spot"
}
```

#### Get Historical Price Data
```
GET /crypto/:ticker/prices
```
**Query Params:** `from`, `to`, `period` (1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M), `page`, `size`.

**Response:** Array of `{ time, ticker, open, high, low, close, volume }`.

**Sample Response:**
```json
[
  {
    "time": "2025-12-19T12:43:00.000Z",
    "ticker": "BTC",
    "open": "85463.3000",
    "high": "88292.5500",
    "low": "85134.0600",
    "close": "87981.6800",
    "volume": "59129171968"
  },
  {
    "time": "2025-12-18T00:00:00.000Z",
    "ticker": "BTC",
    "open": "86144.3700",
    "high": "89412.6600",
    "low": "84436.3100",
    "close": "85462.5100",
    "volume": "52667115348"
  }
]
```

#### Get All Cryptocurrency Tickers
```
GET /crypto/tickers
```
**Query Params:** `type` (coin/token).

**Response:** Array of crypto ticker objects.

**Sample Response:**
```json
[
  {
    "id": 1,
    "ticker": "BTC",
    "name": "Bitcoin",
    "type": "spot"
  },
  {
    "id": 2,
    "ticker": "ETH",
    "name": "Ethereum",
    "type": "spot"
  },
  {
    "id": 3,
    "ticker": "SOL",
    "name": "Solana",
    "type": "spot"
  }
]
```

---

### 6. ETFs API

#### Get Fund Information
```
GET /etfs/:ticker/fund
```
**Path Params:** `ticker` (string, required).

**Response Fields:** Comprehensive ETF metadata including classification, ratings, efficiency scores, tradability, and trading metrics.

**Sample Response:**
```json
{
  "ticker": "SPY",
  "fund": "SPDR S&P 500 ETF Trust",
  "assetclass": "Equity",
  "category": "Size and Style",
  "focus": "Large Cap",
  "niche": "Broad-based",
  "region": "North America",
  "geography": "U.S.",
  "segment": "Equity: U.S.  -  Large Cap",
  "segmentid": 261,
  "efficiencyscore": 99.69286,
  "tradabilityscore": 99.679609,
  "overallratingscore": "A ",
  "medianspreadpct45day": 0.000029,
  "primaryexchange": "NYSEArca"
}
```

#### Get Sector & Region Weights
```
GET /etfs/:ticker/weights
```
**Path Params:** `ticker` (string, required).

**Response:** `sector` (array of `{ name, weight, rawWeight }`), `regions` (array of `{ name, weight, benchmarkWeight, rawWeight }`).

**Sample Response:**
```json
{
  "sector": [
    {
      "name": "Technology Services",
      "weight": "21.08%",
      "rawWeight": 0.21079285342758
    },
    {
      "name": "Commercial Services",
      "weight": "2.90%",
      "rawWeight": 0.0289666913939312
    }
  ],
  "regions": [
    {
      "name": "United States",
      "weight": "100.00%",
      "benchmarkWeight": "99.89%",
      "rawWeight": 1
    },
    {
      "name": "Canada",
      "weight": "--",
      "benchmarkWeight": "0.11%",
      "rawWeight": "--"
    }
  ]
}
```

#### Get Top Holdings
```
GET /etfs/:ticker/holdings
```
**Path Params:** `ticker` (string, required).

**Response:** Array of `{ ticker, name, weight, shares, market_value, rawWeight }`.

**Sample Response:**
```json
[
  {
    "ticker": "NVDA",
    "name": "NVIDIA Corporation",
    "weight": "7.17%",
    "shares": 305156465,
    "market_value": 44519276678.85,
    "rawWeight": 0.0716544211188534
  },
  {
    "ticker": "AAPL",
    "name": "Apple Inc.",
    "weight": "6.95%",
    "shares": 188603226,
    "market_value": 43190138754,
    "rawWeight": 0.0695151543630329
  }
]
```

#### Get ETF Exposure Analysis
```
GET /etfs/:ticker/exposure
```
**Path Params:** `ticker` (string, required – stock ticker, not ETF).

**Response:** Array of ETFs holding the stock.

**Sample Response:**
```json
[
  {
    "ticker": "XLK",
    "fundName": "Technology Select Sector SPDR Fund",
    "segment": "Equity: U.S. Information Technology",
    "allocation": "24.17%",
    "marketValue": "$10.46B",
    "rawAllocation": 0.2417,
    "rawMarketValue": 10460000000
  },
  {
    "ticker": "FTEC",
    "fundName": "Fidelity MSCI Information Technology Index ETF",
    "segment": "Equity: U.S. Information Technology",
    "allocation": "23.75%",
    "marketValue": "$1.45B",
    "rawAllocation": 0.2375,
    "rawMarketValue": 1450000000
  }
]
```

---

## Alternative Data APIs

### 7. Supply Chain API

#### Get Key Suppliers
```
GET /supply-chain/:ticker/suppliers
```
**Path Params:** `ticker` (string, required).

**Response:** Array of `{ ticker, name }`.

**Sample Response:**
```json
[
  { "ticker": "AMD", "name": "Advanced Micro Devices Inc" },
  { "ticker": "INTC", "name": "Intel Corporation" },
  { "ticker": "TSM", "name": "Taiwan Semiconductor Manufacturing Company Limited" },
  { "ticker": "AVGO", "name": "Broadcom Inc" },
  { "ticker": "QCOM", "name": "Qualcomm Inc" },
  { "ticker": "MU", "name": "Micron Technology Inc" },
  { "ticker": "TXN", "name": "Texas Instruments Incorporated" },
  { "ticker": "SONY", "name": "Sony Group Corporation" }
]
```

#### Get Competitors (Peers)
```
GET /supply-chain/:ticker/peers
```
**Path Params:** `ticker` (string, required).

**Response:** Array of `{ ticker, name }`.

**Sample Response:**
```json
[
  { "ticker": "DELL", "name": "Dell Technologies Inc" },
  { "ticker": "IBM", "name": "International Business Machines Corporation" },
  { "ticker": "HPQ", "name": "Hp Inc" },
  { "ticker": "MSFT", "name": "Microsoft Corporation" },
  { "ticker": "GOOG", "name": "Alphabet Inc" },
  { "ticker": "META", "name": "Meta Platforms Inc" },
  { "ticker": "QCOM", "name": "Qualcomm Inc" }
]
```

#### Get Major Customers
```
GET /supply-chain/:ticker/customers
```
**Path Params:** `ticker` (string, required).

**Response:** Array of `{ ticker, name }`.

**Sample Response:**
```json
[
  { "ticker": "BBY", "name": "Best Buy Co Inc" },
  { "ticker": "TGT", "name": "Target Corporation" },
  { "ticker": "WMT", "name": "Walmart Inc" },
  { "ticker": "AMZN", "name": "Amazon com Inc" },
  { "ticker": "VZ", "name": "Verizon Communications Inc" },
  { "ticker": "T", "name": "At and t Inc" },
  { "ticker": "TMUS", "name": "T mobile Us Inc" },
  { "ticker": "AVGO", "name": "Broadcom Inc" }
]
```

---

### 8. Sentiment API

#### Get Social Media Sentiment
```
GET /sentiment/:ticker/social
```
**Path Params:** `ticker` (string, required).

**Response Fields:** `label`, `score`, `breakdown` with `positive` and `negative` counts and avg scores.

**Sample Response:**
```json
{
  "label": "NEGATIVE",
  "score": 0.99506558974584,
  "breakdown": {
    "positive": {
      "count": 145,
      "avgScore": 0.93158021569252
    },
    "negative": {
      "count": 436,
      "avgScore": 0.99506558974584
    }
  }
}
```

#### Get News Sentiment
```
GET /sentiment/:ticker/news
```
**Path Params:** `ticker` (string, required).

**Response Fields:** `label`, `score`, `breakdown` with `positive` and `negative` counts and avg scores.

**Sample Response:**
```json
{
  "label": "NEGATIVE",
  "score": 0.982357367873192,
  "breakdown": {
    "positive": {
      "count": 231,
      "avgScore": 0.903340172767639
    },
    "negative": {
      "count": 1292,
      "avgScore": 0.982357367873192
    }
  }
}
```

#### Get Analyst Sentiment
```
GET /sentiment/:ticker/analyst
```
**Path Params:** `ticker` (string, required).

**Response Fields:** `sentiment` (string), `score` (number).

**Sample Response:**
```json
{
  "sentiment": "NEGATIVE",
  "score": 0.31
}
```

#### Get All Sentiment Data
```
GET /sentiment/:ticker/all
```
**Path Params:** `ticker` (string, required).

**Response:** Aggregate of social, news, and analyst sentiment.

**Sample Response:**
```json
{
  "socialSentiment": {
    "label": "NEGATIVE",
    "score": 0.979367434978485,
    "breakdown": {
      "positive": { "count": 0, "avgScore": 0 },
      "negative": { "count": 100, "avgScore": 0.979367434978485 }
    }
  },
  "newsSentiment": {
    "label": "NEGATIVE",
    "score": 0.952301025390625,
    "breakdown": {
      "positive": { "count": 10, "avgScore": 0.875148761272431 },
      "negative": { "count": 16, "avgScore": 0.952301025390625 }
    }
  },
  "analystSentiment": {
    "sentiment": "POSITIVE",
    "score": 0.66
  }
}
```

---

### 9. ESG API

#### Get ESG Scores by Ticker
```
GET /esg/:ticker
```
**Path Params:** `ticker` (string, required).

**Response Fields:** Array of `{ category, score, grade, id }` covering esg, environment, social, governance, and controversy categories.

**Sample Response:**
```json
[
  {
    "category": "esg",
    "score": 42.86,
    "grade": "BB",
    "id": "1"
  },
  {
    "category": "social",
    "score": 40,
    "grade": "BB",
    "id": "5"
  },
  {
    "category": "governance",
    "score": 31,
    "grade": "BB",
    "id": "6"
  },
  {
    "category": "controversy",
    "score": 20,
    "grade": "B",
    "id": "3"
  },
  {
    "category": "environment",
    "score": 57,
    "grade": "BBB",
    "id": "4"
  }
]
```

---

### 10. Company Web Traffic API

#### Get Website Traffic
```
GET /stocks/:ticker/traffic
```
**Path Params:** `ticker` (string, required).

**Response Fields:** `ranks` (global/country/category), `metrics` (visits, pagesPerVisit, avgVisitDuration, bounceRate), `global` (traffic by country), `deviceSplit`, `peers`, `seo` (keywords, backlinks), `traffic` (sources/destinations), `site`, `date`.

**Sample Response:**
```json
{
  "ranks": {
    "globalRank": { "target": "Worldwide", "rank": 46 },
    "countryRank": { "target": "United States", "rank": 35 },
    "categoryRank": null
  },
  "metrics": {
    "visits": "717.09M",
    "pagesPerVisit": "3.13",
    "avgVisitDuration": "07:40",
    "bounceRate": "59.76%",
    "totalVisitsLast3Months": [
      { "month": "Nov", "value": "717.09M" },
      { "month": "Oct", "value": "807.63M" },
      { "month": "Sep", "value": "875.79M" }
    ]
  },
  "global": [
    { "country": "United States", "contribution": "33.56%", "count": "240.63M", "desktopSplit": "37.46%", "mobileSplit": "62.54%" },
    { "country": "India", "contribution": "6.79%", "count": "48.69M", "desktopSplit": "19.76%", "mobileSplit": "80.24%" },
    { "country": "United Kingdom", "contribution": "6.79%", "count": "48.67M", "desktopSplit": "28.85%", "mobileSplit": "71.15%" }
  ],
  "deviceSplit": { "desktop": "40.51%", "mobile": "59.49%" },
  "peers": [
    { "site": "google.com", "visits": "99.41B" },
    { "site": "spotify.com", "visits": "731.6M" },
    { "site": "imdb.com", "visits": "653.63M" }
  ],
  "seo": {
    "organic": "834.7M",
    "paid": "3.97M",
    "keywords": [
      { "keyword": "apple", "position": "1", "volume": "4,090,000", "cpc": 0.27, "traffic": 1.96 }
    ],
    "backlinks": {
      "authority": "100",
      "referringDomains": "5.89M",
      "backlinks": "5.95B"
    }
  },
  "traffic": {
    "topSources": [
      { "source": "Direct", "contribution": "43.71%" },
      { "source": "Google organic\u2022google.com", "contribution": "30.12%" }
    ],
    "topDestinations": [
      { "destination": "Google.com", "contribution": "9.24%" },
      { "destination": "Chatgpt.com", "contribution": "8.5%" }
    ]
  },
  "site": "apple.com",
  "date": "2026-01-09T02:27:20.806Z"
}
```

---

## Fundamentals APIs

### 11. Financials API

#### Revenue
```
GET /financials/:ticker/revenue
```
**Path Params:** `ticker` (string, required). **Query Params:** `periods` (int, default 1).

**Response:** Array of annual revenue values.

**Sample Response:**
```json
[
  143756000000,
  416161000000,
  313695000000,
  94036000000
]
```

#### Net Income
```
GET /financials/:ticker/netincome
```
**Path Params:** `ticker` (string, required). **Query Params:** `periods` (int).

**Response:** Array of annual net income values.

**Sample Response:**
```json
[
  42097000000,
  112010000000,
  84544000000,
  23434000000
]
```

#### Total Assets
```
GET /financials/:ticker/total/assets
```
**Path Params:** `ticker` (string, required). **Query Params:** `periods` (int).

**Response:** Array of annual total asset values.

**Sample Response:**
```json
[
  379297000000,
  359241000000,
  359241000000,
  331495000000
]
```

#### Total Liabilities
```
GET /financials/:ticker/total/liabilities
```
**Path Params:** `ticker` (string, required). **Query Params:** `periods` (int).

**Response:** Array of annual total liability values.

**Sample Response:**
```json
[
  291107000000,
  285508000000,
  285508000000,
  265665000000
]
```

#### Stockholders' Equity
```
GET /financials/:ticker/stockholdersequity
```
**Path Params:** `ticker` (string, required). **Query Params:** `periods` (int).

**Response:** Array of annual equity values.

**Sample Response:**
```json
[
  88190000000,
  73733000000,
  73733000000,
  65830000000
]
```

#### Operating Cash Flow
```
GET /financials/:ticker/cashflow/operating
```
**Path Params:** `ticker` (string, required). **Query Params:** `periods` (int).

**Response:** Array of annual operating cash flow values.

**Sample Response:**
```json
[
  53925000000,
  111482000000,
  81754000000,
  53887000000
]
```

#### Basic Shares Outstanding
```
GET /financials/:ticker/sharesoutstanding/basic
```
**Path Params:** `ticker` (string, required). **Query Params:** `periods` (int).

**Response:** Array of annual shares outstanding (weighted-average basic).

**Sample Response:**
```json
[
  14748158000,
  14948500000,
  14992898000,
  14902886000
]
```

#### Financial Metrics (Composite)
```
GET /financials/:ticker/metrics
```
**Path Params:** `ticker` (string, required).

**Response Fields:** Comprehensive financial metrics including revenue, netIncome, totalAssets, totalLiabilities, stockholdersEquity, current ratios, cash flow metrics, shares outstanding.

**Sample Response:**
```json
{
  "revenue": 143756000000,
  "netIncome": 42097000000,
  "totalAssets": 379297000000,
  "totalLiabilities": 291107000000,
  "stockholdersEquity": 88190000000,
  "currentAssets": 158104000000,
  "currentLiabilities": 162367000000,
  "operatingCashFlow": 53925000000,
  "capitalExpenditures": 2373000000,
  "freeCashFlow": 51552000000,
  "sharesOutstandingBasic": 14748158000,
  "sharesOutstandingDiluted": 14810356000,
  "currentRatio": 0.973744664864166,
  "debtToAssets": 0.76749091081659
}
```

#### Financial Snapshot
```
GET /financials/:ticker/snapshot
```
**Path Params:** `ticker` (string, required).

**Response Fields:** Real-time price, analyst targets, valuation metrics, profitability ratios, market data.

**Sample Response:**
```json
{
  "currentPrice": 272.19,
  "targetHighPrice": 350,
  "targetLowPrice": 215,
  "targetMeanPrice": 287.70682,
  "targetMedianPrice": 300,
  "recommendationMean": 2,
  "recommendationKey": "buy",
  "numberOfAnalystOpinions": 41,
  "totalCash": 54697000960,
  "totalCashPerShare": 3.702,
  "ebitda": 144748003328,
  "totalDebt": 112377004032,
  "quickRatio": 0.771,
  "currentRatio": 0.893,
  "totalRevenue": 416161005568,
  "debtToEquity": 152.411,
  "revenuePerShare": 27.84,
  "returnOnAssets": 0.22964,
  "returnOnEquity": 1.7142199,
  "grossProfits": 195201007616,
  "freeCashflow": 78862254080,
  "operatingCashflow": 111482003456,
  "earningsGrowth": 0.912,
  "revenueGrowth": 0.079,
  "grossMargins": 0.46905,
  "ebitdaMargins": 0.34782,
  "operatingMargins": 0.31647,
  "profitMargins": 0.26915002,
  "financialCurrency": "USD"
}
```

---

### 12. Profile API (Corp. Intelligence)

#### Get Company Profile
```
GET /profile/:ticker
```
**Path Params:** `ticker` (string, required).

**Response Fields:** Company info, business summary, sector/industry, employees, contact, executives, governance scores.

**Sample Response:**
```json
{
  "address1": "One Apple Park Way",
  "city": "Cupertino",
  "state": "CA",
  "zip": "95014",
  "country": "United States",
  "website": "https://www.apple.com",
  "industry": "Consumer Electronics",
  "sector": "Technology",
  "longBusinessSummary": "Apple Inc. designs, manufactures, and markets smartphones...",
  "fullTimeEmployees": 166000,
  "companyOfficers": [
    {
      "name": "Mr. Timothy D. Cook",
      "age": 63,
      "title": "CEO & Director",
      "totalPay": 16520856
    }
  ],
  "overallRisk": 1,
  "auditRisk": 7,
  "boardRisk": 1,
  "compensationRisk": 3,
  "shareHolderRightsRisk": 1
}
```

#### Get Company Info
```
GET /profile/:ticker/info
```
**Path Params:** `ticker` (string, required).

**Response Fields:** Light version – address, sector, industry, business description, employee count, phone, website.

**Sample Response:**
```json
{
  "address1": "One Apple Park Way",
  "city": "Cupertino",
  "state": "CA",
  "zip": "95014",
  "country": "United States",
  "phone": "(408) 996-1010",
  "website": "https://www.apple.com",
  "industry": "Consumer Electronics",
  "sector": "Technology",
  "longBusinessSummary": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide...",
  "fullTimeEmployees": 166000
}
```

#### Get Performance Summary
```
GET /profile/:ticker/summary
```
**Path Params:** `ticker` (string, required).

**Response Fields:** Current price, day range, 52w range, volume, avg volume, market cap, PE, EPS, dividend yield, beta.

**Sample Response:**
```json
{
  "previousClose": 271.84,
  "open": 273.605,
  "dayLow": 266.96,
  "dayHigh": 273.62,
  "volume": 51509672,
  "averageVolume": 46958041,
  "marketCap": 4039405731840,
  "trailingPE": 36.49,
  "forwardPE": 29.84,
  "dividendRate": 1.04,
  "dividendYield": 0.0038,
  "exDividendDate": "2025-11-10T00:00:00.000Z",
  "fiftyTwoWeekLow": 169.21,
  "fiftyTwoWeekHigh": 288.62,
  "beta": 1.107
}
```

#### Get Key Statistics
```
GET /profile/:ticker/statistics
```
**Path Params:** `ticker` (string, required).

**Response Fields:** Enterprise value, shares outstanding, short interest, insider ownership %, institutional ownership %, valuation ratios.

**Sample Response:**
```json
{
  "enterpriseValue": 4079655583744,
  "forwardPE": 29.84,
  "profitMargins": 0.269,
  "floatShares": 14750642146,
  "sharesOutstanding": 14776353000,
  "sharesShort": 129458559,
  "shortRatio": 2.64,
  "shortPercentOfFloat": 0.0088,
  "heldPercentInsiders": 0.01697,
  "heldPercentInstitutions": 0.64406,
  "beta": 1.107,
  "bookValue": 4.991,
  "priceToBook": 54.54,
  "lastSplitFactor": "4:1",
  "lastSplitDate": 1598832000
}
```

#### Get Calendar Events
```
GET /profile/:ticker/calendar
```
**Path Params:** `ticker` (string, required).

**Response Fields:** Next earnings date, earnings call date, ex-div date, dividend pay date, consensus EPS estimate, consensus revenue estimate.

**Sample Response:**
```json
{
  "earnings": {
    "earningsDate": ["2026-01-29T21:00:00.000Z"],
    "earningsCallDate": ["2025-10-30T21:00:00.000Z"],
    "isEarningsDateEstimate": true,
    "earningsAverage": 2.6647,
    "earningsLow": 2.51,
    "earningsHigh": 2.76,
    "revenueAverage": 138253076640,
    "revenueLow": 136679500000,
    "revenueHigh": 142741000000
  },
  "exDividendDate": "2025-11-10T00:00:00.000Z",
  "dividendDate": "2025-11-13T00:00:00.000Z"
}
```

#### Get Recommendation Trends
```
GET /profile/:ticker/recommendation
```
**Path Params:** `ticker` (string, required).

**Response Fields:** `period` (array of time periods), each with `strongBuy`, `buy`, `hold`, `sell`, `strongSell` counts.

**Sample Response:**
```json
[
  {
    "period": "0m",
    "strongBuy": 5,
    "buy": 24,
    "hold": 15,
    "sell": 1,
    "strongSell": 3
  },
  {
    "period": "-1m",
    "strongBuy": 5,
    "buy": 24,
    "hold": 15,
    "sell": 1,
    "strongSell": 3
  },
  {
    "period": "-2m",
    "strongBuy": 5,
    "buy": 24,
    "hold": 15,
    "sell": 1,
    "strongSell": 3
  },
  {
    "period": "-3m",
    "strongBuy": 5,
    "buy": 23,
    "hold": 15,
    "sell": 1,
    "strongSell": 3
  }
]
```

---

### 13. Insiders & Ownership API

#### Get Fund Ownership
```
GET /insiders/:ticker/funds
```
**Path Params:** `ticker` (string, required).

**Response:** Array of `{ reportDate, organization, pctHeld, position, value, pctChange }`.

**Sample Response:**
```json
[
  {
    "reportDate": "2025-09-30T00:00:00.000Z",
    "organization": "VANGUARD INDEX FUNDS-Vanguard Total Stock Market Index Fund",
    "pctHeld": 0.031600002,
    "position": 467135722,
    "value": 127149673311,
    "pctChange": -0.0274
  },
  {
    "reportDate": "2025-09-30T00:00:00.000Z",
    "organization": "VANGUARD INDEX FUNDS-Vanguard 500 Index Fund",
    "pctHeld": 0.0248,
    "position": 366145920,
    "value": 99661258858,
    "pctChange": -0.1363
  }
]
```

#### Get Individual Insider Holders
```
GET /insiders/:ticker/individuals
```
**Path Params:** `ticker` (string, required).

**Response:** Array of `{ name, relation, transactionDescription, latestTransDate, positionDirect, positionDirectDate }`.

**Sample Response:**
```json
[
  {
    "name": "ADAMS KATHERINE L",
    "relation": "General Counsel",
    "transactionDescription": "Stock Gift",
    "latestTransDate": "2025-11-12T00:00:00.000Z",
    "positionDirect": 175408,
    "positionDirectDate": "2025-11-12T00:00:00.000Z"
  },
  {
    "name": "COOK TIMOTHY D",
    "relation": "Chief Executive Officer",
    "transactionDescription": "Sale",
    "latestTransDate": "2025-10-02T00:00:00.000Z",
    "positionDirect": 3280300,
    "positionDirectDate": "2025-10-02T00:00:00.000Z"
  }
]
```

#### Get Institutional Ownership
```
GET /insiders/:ticker/institutions
```
**Path Params:** `ticker` (string, required).

**Response:** Array of `{ reportDate, organization, pctHeld, position, value, pctChange }`.

**Sample Response:**
```json
[
  {
    "reportDate": "2025-09-30T00:00:00.000Z",
    "organization": "Vanguard Group Inc",
    "pctHeld": 0.0947,
    "position": 1399427162,
    "value": 380910082641,
    "pctChange": -0.0117
  },
  {
    "reportDate": "2025-09-30T00:00:00.000Z",
    "organization": "Blackrock Inc.",
    "pctHeld": 0.0776,
    "position": 1146332274,
    "value": 312020184458,
    "pctChange": -0.0022
  }
]
```

#### Get Major Holders Breakdown
```
GET /insiders/:ticker/ownership
```
**Path Params:** `ticker` (string, required).

**Response Fields:** `insidersPercentHeld`, `institutionsPercentHeld`, `institutionsFloatPercentHeld`, `institutionsCount`.

**Sample Response:**
```json
{
  "insidersPercentHeld": 0.016970001,
  "institutionsPercentHeld": 0.64405996,
  "institutionsFloatPercentHeld": 0.65518,
  "institutionsCount": 7072
}
```

#### Get Insider Transactions
```
GET /insiders/:ticker/transactions
```
**Path Params:** `ticker` (string, required). **Query Params:** `page`, `size`.

**Response:** Array of `{ shares, value, filerName, filerRelation, transactionText, startDate, ownership }`.

**Sample Response:**
```json
[
  {
    "shares": 3750,
    "value": 0,
    "filerName": "ADAMS KATHERINE L",
    "filerRelation": "General Counsel",
    "transactionText": "Stock Gift at price 0.00 per share.",
    "startDate": "2025-11-12T00:00:00.000Z",
    "ownership": "D"
  },
  {
    "shares": 3752,
    "value": 1017655,
    "filerName": "KONDO CHRISTOPHER",
    "filerRelation": "Officer",
    "transactionText": "Sale at price 271.23 per share.",
    "startDate": "2025-11-07T00:00:00.000Z",
    "ownership": "D"
  }
]
```

#### Get Net Share Purchase Activity
```
GET /insiders/:ticker/activity
```
**Path Params:** `ticker` (string, required).

**Response Fields:** 6-month summary with buy/sell info counts, shares, and net activity.

**Sample Response:**
```json
{
  "period": "6m",
  "buyInfoCount": 8,
  "buyInfoShares": 582428,
  "buyPercentInsiderShares": 0.002,
  "sellInfoCount": 7,
  "sellInfoShares": 352873,
  "sellPercentInsiderShares": 0.001,
  "netInfoCount": 15,
  "netInfoShares": 229555,
  "netPercentInsiderShares": 0.001,
  "totalInsiderShares": 250754720
}
```

---

### 14. SEC Filings API

#### List Available Form Types
```
GET /filings/desc/forms
```
**Response:** Object with `commonForms` and `fundForms` arrays containing form types with descriptions.

**Sample Response:**
```json
{
  "commonForms": [
    { "form": "10-K", "description": "Form 10-K: Annual report for public companies" },
    { "form": "10-Q", "description": "Form 10-Q: Quarterly report for public companies" },
    { "form": "8-K", "description": "Form 8-K: Current report" },
    { "form": "4", "description": "Form 4: Statement of changes in beneficial ownership" },
    { "form": "3", "description": "Form 3: Initial statement of beneficial ownership" },
    { "form": "S-1", "description": "Form S-1: Securities registration" },
    { "form": "S-3", "description": "Form S-3: Simplified securities registration" },
    { "form": "DEF 14A", "description": "Form DEF 14A: Definitive proxy statement" },
    { "form": "13F-HR", "description": "Form 13F-HR: Initial quarterly holdings report by institutional managers" },
    { "form": "SC 13G", "description": "Form SC 13G: Beneficial ownership" },
    { "form": "SC 13D", "description": "Form SC 13D: Ownership for control disclosure" },
    { "form": "144", "description": "Form 144: Notice of proposed sale" }
  ],
  "fundForms": [ "NPORT-P", "NPORT-EX" ]
}
```

#### Search Filings by Year and Quarter
```
GET /filings/search
```
**Query Params:** `year` (int, required), `quarter` (int 1-4, required), `formType` (string), `ticker` (string), `page`, `size`.

**Response:** `filings` (array of filing objects), `count`.

**Sample Response:**
```json
{
  "year": 2024,
  "quarter": 1,
  "form": "4",
  "ticker": "AAPL",
  "count": 15,
  "filings": [
    {
      "company": "Apple Inc.",
      "form": "4",
      "filingDate": "2024-01-15T00:00:00.000Z",
      "reportDate": "2024-01-14T00:00:00.000Z",
      "accessionNumber": "000032019324000015",
      "url": "https://www.sec.gov/Archives/edgar/data/320193/000032019324000015-index.html"
    }
  ]
}
```

#### Get Recent Filings
```
GET /filings/:ticker
```
**Path Params:** `ticker` (string, required). **Query Params:** `formType` (string), `page`, `size`.

**Response:** `company` (object with `name`, `cik`), `filings` (array of filing objects).

**Sample Response:**
```json
{
  "company": {
    "name": "Apple Inc.",
    "cik": 320193,
    "ticker": "AAPL"
  },
  "filings": [
    {
      "form": "4",
      "filingDate": "2026-01-15T00:00:00.000Z",
      "reportDate": "2026-01-14T00:00:00.000Z",
      "accessionNumber": "000032019326000015",
      "url": "https://www.sec.gov/Archives/edgar/data/320193/000032019326000015-index.html"
    },
    {
      "form": "10-Q",
      "filingDate": "2026-01-12T00:00:00.000Z",
      "reportDate": "2025-12-27T00:00:00.000Z",
      "accessionNumber": "000032019326000006",
      "url": "https://www.sec.gov/Archives/edgar/data/320193/000032019326000006/aapl-20251227.htm"
    }
  ]
}
```

---

### 15. Earnings API

#### Get Earnings History
```
GET /earnings/:ticker/history
```
**Path Params:** `ticker` (string, required). **Query Params:** `periods` (int, default 4), `from`, `to`.

**Response:** Array of earnings objects with `epsActual`, `epsEstimate`, `epsDifference`, `surprisePercent`, `quarter`, `currency`, `period`.

**Sample Response:**
```json
[
  {
    "epsActual": 2.4,
    "epsEstimate": 2.34102,
    "epsDifference": 0.06,
    "surprisePercent": 0.0252,
    "quarter": "2024-12-31T00:00:00.000Z",
    "currency": "USD",
    "period": "-4q"
  },
  {
    "epsActual": 1.65,
    "epsEstimate": 1.62253,
    "epsDifference": 0.03,
    "surprisePercent": 0.016900001,
    "quarter": "2025-03-31T00:00:00.000Z",
    "currency": "USD",
    "period": "-3q"
  }
]
```

#### Get Earnings Report (8-K Tables)
```
GET /earnings/:ticker/report/:period
```
**Path Params:** `ticker` (string, required), `period` (string – e.g. "Q3-2024", required).

**Response:** Extracted financial tables from the 8-K filing including income statement, balance sheet, cash flow, segment data.

**Sample Response:**
```json
[
  {
    "dataframe": [
      { "label": "ASSETS:", "values": [] },
      { "label": "Current assets:", "values": [] },
      { "label": "Cash and cash equivalents", "values": ["$", 40760, "$", 29965] },
      { "label": "Marketable securities", "values": [32340, 31590] },
      { "label": "Total current assets", "values": [143692, 143566] },
      { "label": "Total assets", "values": ["$", 353514, "$", 352583] }
    ],
    "scale": 1000000000,
    "title": null,
    "statementType": "balance_sheet",
    "periods": ["Period 1"],
    "rawIndex": 5
  },
  {
    "dataframe": [
      { "label": "Three Months Ended", "values": [] },
      { "label": "Cash generated by operating activities", "values": [39895, 34005] },
      { "label": "Cash generated by/(used in) investing activities", "values": [1927, -1445] },
      { "label": "Cash used in financing activities", "values": [-30585, -35563] }
    ],
    "scale": 1000000000,
    "statementType": "cash_flow",
    "rawIndex": 6
  }
]
```

#### Get Earnings Trend
```
GET /earnings/:ticker/history
```
Alias of the earnings history endpoint. Returns the same quarterly data.

**Sample Response:**
```json
[
  {
    "period": "0q",
    "endDate": "2025-12-31T00:00:00.000Z",
    "growth": 0.1103,
    "earningsEstimate": {
      "avg": 2.66574,
      "low": 2.51,
      "high": 2.8,
      "yearAgoEps": 2.4,
      "numberOfAnalysts": 29,
      "growth": 0.1107
    },
    "revenueEstimate": {
      "avg": 138253076640,
      "low": 136679500000,
      "high": 142741000000,
      "numberOfAnalysts": 29,
      "yearAgoRevenue": 124300000000,
      "growth": 0.1123
    },
    "epsTrend": {
      "current": 2.66574,
      "7daysAgo": 2.66367,
      "30daysAgo": 2.66153,
      "60daysAgo": 2.48232,
      "90daysAgo": 2.492
    },
    "epsRevisions": {
      "upLast7days": 1,
      "upLast30days": 1,
      "downLast30days": 0,
      "downLast7Days": 0
    }
  }
]
```

---

### 16. Credit Ratings API

#### Search Organizations
```
GET /credit/search
```
**Query Params:** `q` (string, required – name search), `page`, `size`.

**Response:** Array of `{ id, name, sectorCode, country, state }`.

**Sample Response:**
```json
[
  {
    "id": "689595",
    "name": "Apple Bidco, LLC",
    "sectorCode": "CORP",
    "country": "USA",
    "state": "Texas"
  },
  {
    "id": "112354",
    "name": "Apple Inc.",
    "sectorCode": "CORP",
    "country": "USA",
    "state": "California"
  }
]
```

#### Get Credit Ratings
```
GET /credit/ratings/:id
```
**Path Params:** `id` (string, required – organization ID from search).

**Response:** Array of rating objects with `orgDebtTypeDesc`, `rating`, `currentCwOl`, `ratingDate`, `lastReviewDate`, `ratingTypeCode`, `ratingTypeCodeDesc`.

**Sample Response:**
```json
[
  {
    "orgDebtTypeDesc": "Issuer Credit Rating",
    "rating": "B",
    "ratingDate": "06-Jul-2021",
    "currentCwOl": "Stable",
    "lastReviewDate": "11-Jun-2025",
    "ratingTypeCode": "STDLONG",
    "ratingTypeCodeDesc": "Local Currency LT",
    "id": 1
  },
  {
    "orgDebtTypeDesc": "Issuer Credit Rating",
    "rating": "B",
    "ratingDate": "06-Jul-2021",
    "currentCwOl": "Stable",
    "lastReviewDate": "11-Jun-2025",
    "ratingTypeCode": "FCLONG",
    "ratingTypeCodeDesc": "Foreign Currency LT",
    "id": 2
  }
]
```

---

## Macros & Signals APIs

### 17. Economic Data API

#### Search Economic Series
```
GET /econ/search
```
**Query Params:** `q` (string, required – keyword search), `page`, `size`.

**Response:** Array of `{ id, title, observationStart, observationEnd, frequency, units, seasonalAdjustment, lastUpdated, popularity, notes }`.

**Sample Response:**
```json
[
  {
    "id": "PMAIZMTUSDM",
    "title": "Global price of Corn",
    "observationStart": "1990-01-01",
    "observationEnd": "2025-06-01",
    "frequency": "Monthly",
    "frequencyShort": "M",
    "units": "U.S. Dollars per Metric Ton",
    "unitsShort": "U.S. $ per Metric Ton",
    "seasonalAdjustment": "Not Seasonally Adjusted",
    "seasonalAdjustmentShort": "NSA",
    "lastUpdated": "2025-07-18 09:37:11-05",
    "popularity": "54"
  },
  {
    "id": "PMAIZMTUSDA",
    "title": "Global price of Corn",
    "observationStart": "1990-01-01",
    "observationEnd": "2024-01-01",
    "frequency": "Annual",
    "frequencyShort": "A",
    "units": "U.S. Dollars per Metric Ton",
    "seasonalAdjustment": "Not Seasonally Adjusted",
    "lastUpdated": "2025-01-27 13:31:17-06",
    "popularity": "24"
  }
]
```

#### Get Dataset by ID
```
GET /econ/dataset/:id
```
**Path Params:** `id` (string, required – series ID from search).

**Query Params:** `from`, `to`, `page`, `size`.

**Response:** Array of `{ realtimeStart, date, value }` observations.

**Sample Response:**
```json
[
  {
    "realtimeStart": "2015-03-13T00:00:00.000Z",
    "date": "1971-01-01T00:00:00.000Z",
    "value": 63.4
  },
  {
    "realtimeStart": "2015-03-13T00:00:00.000Z",
    "date": "1971-02-01T00:00:00.000Z",
    "value": 63.6
  },
  {
    "realtimeStart": "2015-03-13T00:00:00.000Z",
    "date": "1971-03-01T00:00:00.000Z",
    "value": 62
  },
  {
    "realtimeStart": "2015-03-13T00:00:00.000Z",
    "date": "1971-04-01T00:00:00.000Z",
    "value": 60.8
  }
]
```

#### Economic Calendar
```
GET /econ/calendar
```
**Query Params:** `from` (date), `to` (date), `country`, `importance` (1-3), `currency`, `category`, `page`, `size`.

**Response:** Array of `{ id, title, country, indicator, category, actual, previous, forecast, currency, importance, date }`.

**Sample Response:**
```json
[
  {
    "id": "366961",
    "title": "New Year's Day",
    "country": "AR",
    "indicator": "Holidays",
    "category": "gov",
    "actual": null,
    "previous": null,
    "forecast": null,
    "currency": "ARS",
    "importance": -1,
    "date": "2025-01-01T00:00:00.000Z"
  },
  {
    "id": "366963",
    "title": "New Year's Day",
    "country": "AU",
    "indicator": "Holidays",
    "category": "gov",
    "actual": null,
    "previous": null,
    "forecast": null,
    "currency": "AUD",
    "importance": -1,
    "date": "2025-01-01T00:00:00.000Z"
  }
]
```

---

### 18. News API

#### Get Company News
```
GET /news/:ticker
```
**Path Params:** `ticker` (string, required). **Query Params:** `from`, `to`, `page`, `size`.

**Response:** Array of `{ title, link, summary, published }`.

**Sample Response:**
```json
[
  {
    "title": "Apple spent 2025 setting itself up for the future - and its biggest moves weren't about AI - Yahoo Finance",
    "link": "https://api.axionquant.com/news/article/...",
    "summary": "Apple spent 2025 setting itself up for the future - and its biggest moves weren't about AI  Yahoo Finance",
    "published": "Wed, 24 Dec 2025 09:05:43 GMT"
  },
  {
    "title": "Apple Just Released a New AI Model. Should You Buy AAPL Stock Here? - Barchart.com",
    "link": "https://api.axionquant.com/news/article/...",
    "summary": "Apple Just Released a New AI Model. Should You Buy AAPL Stock Here?  Barchart.com",
    "published": "Tue, 23 Dec 2025 16:00:03 GMT"
  }
]
```

#### Get News by Category
```
GET /news/category/:category
```
**Path Params:** `category` (string, required). **Query Params:** `page`, `size`.

**Response:** Same structure as Company News.

**Sample Response:**
```json
[
  {
    "title": "Markets Rally as Fed Holds Rates Steady - Bloomberg",
    "link": "https://api.axionquant.com/news/article/...",
    "summary": "Markets Rally as Fed Holds Rates Steady  Bloomberg",
    "published": "Wed, 24 Dec 2025 14:00:00 GMT"
  },
  {
    "title": "Tech Stocks Surge on AI Optimism - Reuters",
    "link": "https://api.axionquant.com/news/article/...",
    "summary": "Tech Stocks Surge on AI Optimism  Reuters",
    "published": "Wed, 24 Dec 2025 13:30:00 GMT"
  }
]
```

#### Get News by Country
```
GET /news/country/:country
```
**Path Params:** `country` (string, required – 2-letter code). **Query Params:** `page`, `size`.

**Response:** Same structure as Company News.

**Sample Response:**
```json
[
  {
    "title": "Trump Live Updates: DOJ Says It Has Found 1 Million More Epstein Files - The New York Times",
    "link": "https://api.axionquant.com/news/article/...",
    "summary": "Trump Live Updates: DOJ Says It Has Found 1 Million More Epstein Files  The New York Times",
    "published": "Wed, 24 Dec 2025 21:31:18 GMT"
  }
]
```

#### Get General News
```
GET /news
```
**Query Params:** `page`, `size`.

**Response:** Same structure as Company News.

**Sample Response:**
```json
[
  {
    "title": "Trump Live Updates: DOJ Says It Has Found 1 Million More Epstein Files - The New York Times",
    "link": "https://api.axionquant.com/news/article/...",
    "summary": "Trump Live Updates: DOJ Says It Has Found 1 Million More Epstein Files  The New York Times",
    "published": "Wed, 24 Dec 2025 21:31:18 GMT"
  },
  {
    "title": "Powerful winter storm arrives in Southern California for Christmas holiday",
    "link": "https://api.axionquant.com/news/article/...",
    "summary": "Powerful winter storm arrives in Southern California for Christmas holiday. Here's what to know.  CBS News",
    "published": "Wed, 24 Dec 2025 14:52:00 GMT"
  }
]
```

---

### 19. Corporate Events (Calendar)

#### Get Corporate Events
```
GET /profile/:ticker/calendar
```
**Path Params:** `ticker` (string, required).

**Response:** Upcoming earnings dates, call dates, dividend calendar, EPS and revenue consensus estimates.

**Sample Response:**
```json
{
  "earnings": {
    "earningsDate": ["2026-01-29T21:00:00.000Z"],
    "earningsCallDate": ["2025-10-30T21:00:00.000Z"],
    "isEarningsDateEstimate": true,
    "earningsAverage": 2.6647,
    "earningsLow": 2.51,
    "earningsHigh": 2.76,
    "revenueAverage": 138253076640,
    "revenueLow": 136679500000,
    "revenueHigh": 142741000000
  },
  "exDividendDate": "2025-11-10T00:00:00.000Z",
  "dividendDate": "2025-11-13T00:00:00.000Z"
}
```
