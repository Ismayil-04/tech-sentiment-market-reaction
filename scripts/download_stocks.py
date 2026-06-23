import os
import pandas as pd
import yfinance as yf

stocks = ["AAPL", "MSFT", "GOOGL", "META", "NVDA"]
market = "^GSPC"

start = "2016-01-01"
end = "2026-06-01"

if not os.path.exists("data/raw"):
    os.makedirs("data/raw")

print("Downloading stocks...")
for t in stocks:
    df = yf.download(t, start=start, end=end)
    df = df.reset_index()
    df.to_csv(f"data/raw/{t}.csv", index=False)

print("Downloading S&P500...")
m_df = yf.download(market, start=start, end=end)
m_df = m_df.reset_index()
m_df.to_csv("data/raw/SP500.csv", index=False)

print("Finished data download.")