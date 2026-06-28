from langgraph.graph import StateGraph, START, END
from src.state import AgentState
from src.agents.quant_agent import quant_agent_node
from src.agents.news_agent import news_agent_node
from src.agents.report_agent import report_agent_node

def build_graph():
    # Initialize the graph with our TypedDict state
    workflow = StateGraph(AgentState)
    
    # Add the nodes
    workflow.add_node("quant_agent", quant_agent_node)
    workflow.add_node("news_agent", news_agent_node)
    workflow.add_node("report_agent", report_agent_node)
    
    # Build the edges (Parallel Execution)
    # Both quant and news agents start at the same time
    workflow.add_edge(START, "quant_agent")
    workflow.add_edge(START, "news_agent")
    
    # Both feed into the report agent
    workflow.add_edge("quant_agent", "report_agent")
    workflow.add_edge("news_agent", "report_agent")
    
    # Report agent goes to END
    workflow.add_edge("report_agent", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app
