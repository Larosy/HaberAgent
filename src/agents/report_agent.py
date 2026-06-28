from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.state import AgentState

def report_agent_node(state: AgentState) -> AgentState:
    ticker = state["ticker"]
    quant_data = state.get("quant_data", "No quant data.")
    news_data = state.get("news_data", "No news data.")
    
    print(f"[Report Agent] Synthesizing final report for {ticker}...")
    
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a professional financial analyst. You will be provided with quantitative technical analysis data and qualitative news sentiment data for a given stock. Your job is to synthesize these into a concise, professional investment summary report. Do not invent new data; rely only on what is provided."),
            ("user", "Stock: {ticker}\n\n=== Quantitative Data ===\n{quant}\n\n=== Qualitative News Data ===\n{news}\n\nPlease write the final synthesized report.")
        ])
        
        chain = prompt | llm
        response = chain.invoke({"ticker": ticker, "quant": quant_data, "news": news_data})
        final_report = response.content
    except Exception as e:
        final_report = f"Error generating report: {e}"
        
    print(f"[Report Agent] Final report generated for {ticker}.")
    return {"final_report": final_report}
