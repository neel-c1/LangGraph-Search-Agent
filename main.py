from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.tools import Tool
from langchain.memory import ConversationBufferMemory
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

load_dotenv()

search = SerpAPIWrapper()
search_tool = Tool(
    name="Google Search",
    func=search.run,
    description="Use for real-time info, current events, or web lookup."
)

llm = ChatOpenAI(model="gpt-4", temperature=0.7)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

def agent_node(state: dict) -> dict:
    memory.chat_memory.messages = state.get("chat_history", [])

    user_input = state["input"]

    if "news" in user_input.lower() or "regulations" in user_input.lower():
        search_result = search_tool.run(user_input)
        prompt = f"User asked: {user_input}\n\nSearch result:\n{search_result}\n\nPlease summarize or respond."
    else:
        prompt = user_input

    response = llm.invoke(prompt)
    memory.save_context({"input": user_input}, {"output": response.content})

    return {
        "input": user_input,
        "output": response.content,
        "chat_history": memory.chat_memory.messages,
    }

builder = StateGraph(dict)
builder.add_node("agent_node", agent_node)
builder.set_entry_point("agent_node")
builder.set_finish_point("agent_node")
app = builder.compile()

if __name__ == "__main__":
    while True:
        input_text = input("Search: ")
        result = app.invoke({"input": input_text})
        print(f"\n💬 Agent response: {result["output"]}\n")
