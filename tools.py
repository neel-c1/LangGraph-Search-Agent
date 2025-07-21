import os
import re
from dotenv import load_dotenv
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.tools import Tool
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from prompts import get_prompt

load_dotenv()

# === Search Tool ===
search = SerpAPIWrapper(
    serpapi_api_key=os.environ.get("SERPAPI_API_KEY"),
    params={"gl": "us", "hl": "en", "tbm": "nws"}
)

search_tool = Tool(
    name="Google News Search",
    func=search.run,
    description="Use this tool for real-time news, current events, or live web lookup."
)

# === LLM and Memory ===
llm = ChatOpenAI(model="gpt-4", temperature=0.7)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# === Node: Scope ===
def scope_node(state: dict) -> dict:
    user_input = state["input"]
    memory.chat_memory.messages = state.get("chat_history", [])
    prompt = get_prompt("scope", user_input=user_input)
    research_brief = llm.invoke(prompt).content
    memory.save_context({"input": user_input}, {"output": research_brief})
    return {
        "input": user_input,
        "research_brief": research_brief,
        "chat_history": memory.chat_memory.messages
    }

# === Helper: Extract Subquestions ===
def extract_subquestions(research_brief: str) -> list[str]:
    pattern = r"(?:-|\*|\d+\.)\s*(.+)"
    matches = re.findall(pattern, research_brief)
    return [q.strip() for q in matches if len(q.strip()) > 5]

# === Helper: Run Search & Summarize ===
def run_search_and_summarize(sub_q: str) -> dict:
    try:
        search_result = search_tool.run(sub_q)
        snippet = search_result[:1000]
        summary_prompt = f"""You're an AI assistant helping synthesize research.

Search snippet:
{snippet}

Question:
{sub_q}

Summarize the relevant answer and cite any sources."""
        summary = llm.invoke(summary_prompt).content
    except Exception as e:
        summary = f"Failed to get results: {str(e)}"
        snippet = ""
    
    return {
        "sub_question": sub_q,
        "search_snippet": snippet,
        "summary": summary
    }

# === Node: Research ===
def research_node(state: dict) -> dict:
    research_brief = state["research_brief"]
    subquestions = extract_subquestions(research_brief)
    if not subquestions:
        subquestions = [research_brief]

    results = []
    for sub_q in subquestions:
        print(f"Searching for: {sub_q}")
        result = run_search_and_summarize(sub_q)
        results.append(result)

    findings = "\n\n".join(
        f"### {item['sub_question']}\n"
        f"Snippet:\n{item['search_snippet']}\n\n"
        f"Summary:\n{item['summary']}"
        for item in results
    )

    return {
        "input": state["input"],
        "research_brief": research_brief,
        "research_findings": findings,
        "chat_history": state["chat_history"]
    }

# === Node: Write ===
def write_node(state: dict) -> dict:
    findings = state["research_findings"]
    prompt = get_prompt("write", research_findings=findings)
    response = llm.invoke(prompt).content
    memory.save_context({"input": state["input"]}, {"output": response})
    return {
        "input": state["input"],
        "output": response,
        "chat_history": memory.chat_memory.messages
    }

