from langchain.agents import Tool, initialize_agent, AgentType
from langchain.agents.agent_toolkits import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langgraph.graph import StateGraph, END

# 1. Define tools
search = SerpAPIWrapper()  # This wraps Google search via SerpAPI
search_tool = Tool(
    name="Google Search",
    func=search.run,
    description="Useful for answering questions about current events or factual queries."
)

# 2. Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 3. Language model (GPT-4)
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# 4. Agent setup
tools = [search_tool]
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# 5. LangGraph State (Optional - to expand with complex workflows)
class AgentState:
    def __init__(self):
        self.input = None
        self.output = None

def run_agent(state: AgentState) -> AgentState:
    print(f"Running agent on input: {state.input}")
    response = agent.run(state.input)
    state.output = response
    return state

# 6. LangGraph graph setup
graph = StateGraph(AgentState)
graph.add_node("run_agent", run_agent)
graph.set_entry_point("run_agent")
graph.set_finish_point("run_agent", END)

app = graph.compile()

# 7. Use the agent
if __name__ == "__main__":
    state = AgentState()
    state.input = "What's the latest news on the AI regulations in the EU?"
    result = app.invoke(state)
    print("Agent response:", result.output)

