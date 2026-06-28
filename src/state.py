from typing import TypedDict, Optional

class AgentState(TypedDict):
    ticker: str
    quant_data: Optional[str]
    news_data: Optional[str]
    final_report: Optional[str]
