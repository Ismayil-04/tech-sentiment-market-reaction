import os
import pandas as pd

tickers = ["AAPL", "MSFT", "GOOGL", "META", "NVDA"]

if not os.path.exists("data/processed"):
    os.makedirs("data/processed")

print("Processing market baseline...")
sp500 = pd.read_csv("data/raw/SP500.csv")
sp500["Date"] = pd.to_datetime(sp500["Date"])
sp500 = sp500.sort_values("Date")

sp500["Close"] = pd.to_numeric(sp500["Close"], errors='coerce')
sp500["Market_Return"] = sp500["Close"].pct_change()
m_returns = sp500[["Date", "Market_Return"]]

combined_stocks = []

print("Processing stocks...")
for t in tickers:
    df = pd.read_csv(f"data/raw/{t}.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    
    df["Close"] = pd.to_numeric(df["Close"], errors='coerce')
    df["Stock_Return"] = df["Close"].pct_change()
    df["Ticker"] = t
    
    combined_stocks.append(df[["Date", "Ticker", "Stock_Return"]])

final_df = pd.concat(combined_stocks, ignore_index=True)
final_df = pd.merge(final_df, m_returns, on="Date", how="left")

news_file = "data/raw/news_events.csv"
if os.path.exists(news_file):
    print("Merging news data...")
    news_df = pd.read_csv(news_file)
    
    if "date" in news_df.columns:
        news_df = news_df.rename(columns={"date": "Date"})
    news_df["Date"] = pd.to_datetime(news_df["Date"])
    
    if "Ticker" not in news_df.columns:
        news_df["Ticker"] = "AAPL"
        if "title" in news_df.columns:
            for t in tickers:
                news_df.loc[news_df["title"].str.contains(t, case=False, na=False), "Ticker"] = t

    master_data = pd.merge(final_df, news_df, on=["Date", "Ticker"], how="left")
    
    if "sentiment_cat" in master_data.columns:
        master_data["Is_Negative"] = (master_data["sentiment_cat"] == "negative").astype(int)
        master_data["Is_Positive"] = (master_data["sentiment_cat"] == "positive").astype(int)
            
    master_data.to_csv("data/processed/master_regression_data.csv", index=False)
    print("Master dataset saved to data/processed/")
else:
    final_df.to_csv("data/processed/stock_returns_base.csv", index=False)
    print("Saved baseline returns.")