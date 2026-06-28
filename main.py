import os
from dotenv import load_dotenv
from src.graph import build_graph
from src.state import AgentState

# Load environment variables (e.g. GOOGLE_API_KEY)
load_dotenv()

def main():
    if not os.environ.get("GOOGLE_API_KEY"):
        print("WARNING: GOOGLE_API_KEY environment variable is not set.")
        print("Please set it in a .env file or export it in your terminal.")
        return

    app = build_graph()
    
    ticker = input("Enter a stock ticker (e.g., AAPL, TSLA, MSFT): ").strip().upper()
    if not ticker:
        print("Ticker cannot be empty.")
        return
        
    print(f"\n--- Starting Workflow for {ticker} ---\n")
    
    # Initial state
    inputs = {"ticker": ticker}
    
    # Run the graph
    try:
        # We use invoke which runs the graph synchronously to completion
        result = app.invoke(inputs)
        
        print("\n" + "="*50)
        print(" FINAL REPORT ")
        print("="*50 + "\n")
        print(result.get("final_report", "No report generated."))
        print("\n" + "="*50)
        
    except Exception as e:
        print(f"An error occurred during workflow execution: {e}")

if __name__ == "__main__":
    main()
