from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

from tools import search_tool
from prompts import BASE_PROMPT

load_dotenv()

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
        context = search_result
    else:
        context = ""

    prompt = BASE_PROMPT.format(user_input=user_input, context=context)

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
