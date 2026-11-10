import logging
from langchain.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s  | %(levelname)s  | %(message)s"
)

load_dotenv()
tavily_client = TavilyClient()

class SearchInput(BaseModel):
    query: str = Field(default="", description="Search query keywords, e.g. 'wedding venues Cairo'")
    cursor: int | None = Field(default=None)
    id: str | None = Field(default=None)
    url: str | None = Field(default=None)

    model_config = {"extra": "allow"}

@tool(args_schema=SearchInput)
def search_web(query: str = "", **kwargs) -> str:
    """Search the web for concise information matching the query."""
    search_term = query.strip()
    if not search_term:
        for key in ("q", "keywords", "topic", "url", "id"):
            val = kwargs.get(key)
            if val and isinstance(val, str) and len(val) > 2:
                search_term = val.strip()
                break
    if not search_term:
        return "Search completed. Use the available context to summarize."

    logging.info(f"search_web tool called with query: {search_term}")
    try:
        response = tavily_client.search(query=search_term, max_results=2)
        results = response.get("results", [])
        if not results:
            return "No relevant results found."
        
        summaries = []
        for r in results:
            title = r.get("title", "")
            content = r.get("content", "")[:300]
            url = r.get("url", "")
            summaries.append(f"- Title: {title}\n  URL: {url}\n  Summary: {content}")
        return "\n\n".join(summaries)
    except Exception as e:
        return f"Error performing search: {str(e)}"

@tool
def open_url(url: str = "", **kwargs) -> str:
    """Open a web link or URL to read details."""
    target = url.strip() or kwargs.get("id", "") or kwargs.get("query", "")
    return search_web.invoke({"query": target})
