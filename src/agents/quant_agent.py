import pandas as pd
import yfinance as yf
from src.state import AgentState

def quant_agent_node(state: AgentState) -> AgentState:
    ticker = state["ticker"]
    print(f"[Quant Agent] Analyzing historical data for {ticker}...")
    
    # We use yfinance to simulate a large CSV of historical data
    # In a real scenario, this could be pd.read_csv("large_kaggle_dataset.csv")
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    
    if hist.empty:
        return {"quant_data": "No historical data found."}
    
    # Calculate some basic technical indicators
    hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
    hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
    
    latest_close = hist['Close'].iloc[-1]
    latest_sma20 = hist['SMA_20'].iloc[-1]
    latest_sma50 = hist['SMA_50'].iloc[-1]
    
    # Simple logic
    trend = "Bullish" if latest_sma20 > latest_sma50 else "Bearish"
    
    quant_report = (
        f"Quant Analysis for {ticker}:\n"
        f"- Latest Close Price: ${latest_close:.2f}\n"
        f"- 20-Day SMA: ${latest_sma20:.2f}\n"
        f"- 50-Day SMA: ${latest_sma50:.2f}\n"
        f"- Overall Technical Trend: {trend}\n"
    )
    
    print(f"[Quant Agent] Analysis complete for {ticker}.")
    return {"quant_data": quant_report}
