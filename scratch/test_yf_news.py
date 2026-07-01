import yfinance as yf
ticker = yf.Ticker("AAPL")
news = ticker.news
print(f"Found {len(news)} news items.")
if news:
    import json
    print(json.dumps(news[0], indent=2))
