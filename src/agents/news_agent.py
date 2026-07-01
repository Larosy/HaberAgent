import yfinance as yf
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.state import AgentState

def news_agent_node(state: AgentState) -> AgentState:
    ticker = state["ticker"]
    print(f"[News Agent] Fetching and analyzing news for {ticker}...")
    
    # Fetch news using yfinance
    try:
        stock = yf.Ticker(ticker)
        raw_news = stock.news
        results = []
        for n in raw_news[:5]:
            content = n.get("content", n)
            title = content.get("title", "No Title")
            summary = content.get("summary", "")
            results.append({"title": title, "body": summary})
    except Exception as e:
        results = []
        print(f"[News Agent] Error fetching news: {e}")
        
    if not results:
        return {"news_data": "No recent news found or error fetching news."}
        
    news_texts = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
    
    # Use LLM for sentiment analysis
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a financial news sentiment analyzer. Read the provided news headlines and summaries for a stock and provide a brief overall sentiment summary (Positive, Negative, or Neutral) with a short explanation."),
            ("user", "Here are the recent news for {ticker}:\n\n{news}")
        ])
        
        chain = prompt | llm
        response = chain.invoke({"ticker": ticker, "news": news_texts})
        sentiment_report = response.content
    except Exception as e:
        sentiment_report = f"Failed to perform sentiment analysis. Error: {e}\nRaw news:\n{news_texts}"
        
    print(f"[News Agent] News analysis complete for {ticker}.")
    return {"news_data": sentiment_report}
