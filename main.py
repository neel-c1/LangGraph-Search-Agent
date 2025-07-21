from langgraph.graph import StateGraph
from tools import scope_node, research_node, write_node

builder = StateGraph(dict)

# Register LangGraph nodes
builder.add_node("scope", scope_node)
builder.add_node("research", research_node)
builder.add_node("write", write_node)

builder.set_entry_point("scope")
builder.add_edge("scope", "research")
builder.add_edge("research", "write")
builder.set_finish_point("write")

app = builder.compile()

if __name__ == "__main__":
    while True:
        input_text = input("Research Query: ")
        result = app.invoke({"input": input_text})
        print("\nFinal Report:\n")
        print(result["output"])
        print("\n" + "-" * 60 + "\n")

