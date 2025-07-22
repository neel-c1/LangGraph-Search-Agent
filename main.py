from langgraph.graph import StateGraph
import sys
import gradio as gr

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

def cli_mode():
    while True:
        input_text = input("\Search Query: ")
        result = app.invoke({"input": input_text})
        print("\n" + "-" * 60)
        print("\nFinal Report:\n")
        print(result["output"])
        print("\n" + "-" * 60 + "\n")

def gui_mode():
    def run_agent(query: str) -> str:
        try:
            result = app.invoke({"input": query})
            return result["output"]
        except Exception as e:
            return f"Error: {str(e)}"

    with gr.Blocks(title="Search Agent") as demo:
        gr.Markdown("# 🔍 Search Assistant")
        gr.Markdown("Enter a search topic or question. The agent will run scoped web research and generate a report.")

        with gr.Row():
            query_box = gr.Textbox(label="Enter your search query", lines=3, placeholder="e.g., Impact of climate change on agriculture")
            submit_btn = gr.Button("Create Report")

        output_box = gr.Markdown(label="Agent Report")

        submit_btn.click(fn=run_agent, inputs=[query_box], outputs=[output_box])

    demo.launch()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "gui":
        gui_mode()
    else:
        cli_mode()