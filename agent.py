from langchain.messages import SystemMessage, HumanMessage
from langchain.tools import tool
from models import llm
from tools import search_web
from pydantic import BaseModel, Field
import logging

logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s  | %(levelname)s  | %(message)s"
)

SUBAGENT1_SYSTEM_PROMPT = """You are SubAgent1, an expert researcher on wedding venues, locations, and styling aesthetics.
Based strictly on the provided web search results, summarize the top 2-3 venue recommendations in concise, informative bullet points.
Highlight their unique vibe, location in Cairo/Egypt, and capacity if available."""

SUBAGENT2_SYSTEM_PROMPT = """You are SubAgent2, an expert researcher on wedding budgets, catering costs, and vendor pricing in Egypt.
Based strictly on the provided web search results, summarize realistic pricing benchmarks, cost per guest, and budget allocations in concise bullet points."""

class DelegateInput(BaseModel):
    query: str = Field(default="", description="Search keywords or specific topic to research")

    model_config = {"extra": "allow"}

def invoke_subagent_research(system_prompt: str, query: str, default_query: str) -> str:
    effective_q = query.strip() or default_query
    logging.info(f"SubAgent executing web search for: '{effective_q}'")
    
    # 1. Direct web search
    search_results = search_web.invoke({"query": effective_q})
    
    # 2. LLM synthesis
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Research Request: {effective_q}\n\nWeb Search Results:\n{search_results}")
    ]
    response = llm.invoke(messages)
    return response.content

@tool(args_schema=DelegateInput)
def delegate_to_subagent1(query: str = "", **kwargs) -> str:
    """Delegate venue, location, and aesthetic research to SubAgent1."""
    q = query.strip() or kwargs.get("topic", "") or kwargs.get("keywords", "") or "wedding venues in Cairo"
    logging.info(f"Delegating query '{q}' to SubAgent1 (Venues)")
    return invoke_subagent_research(SUBAGENT1_SYSTEM_PROMPT, q, "best wedding venues Cairo Egypt")

@tool(args_schema=DelegateInput)
def delegate_to_subagent2(query: str = "", **kwargs) -> str:
    """Delegate budget, pricing, catering, and vendor research to SubAgent2."""
    q = query.strip() or kwargs.get("topic", "") or kwargs.get("keywords", "") or "wedding budget and catering costs Cairo"
    logging.info(f"Delegating query '{q}' to SubAgent2 (Budget & Vendors)")
    return invoke_subagent_research(SUBAGENT2_SYSTEM_PROMPT, q, "Cairo wedding catering costs and vendor prices")

# Aliases for backwards compatibility
sub_agent1 = delegate_to_subagent1
sub_agent2 = delegate_to_subagent2
