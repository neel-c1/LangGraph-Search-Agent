from langchain_community.utilities import SerpAPIWrapper
from langchain_community.tools import Tool

search = SerpAPIWrapper()

# Search Tool
search_tool = Tool(
    name="Google Search",
    func=search.run,
    description="Use for real-time info, current events, or web lookup."
)