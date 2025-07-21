"""
Prompt templates for scoped web-based research using a multi-agent system.
Inspired by the Open Deep Research project structure.
"""

SCOPE_PROMPT = """You are a research scoping assistant.

Your job is to help clarify and structure a user's research question into a brief and focused objective. 
If the user's input is ambiguous, incomplete, or too broad, ask clarifying questions. 
If the input is sufficiently clear, structure it as a research brief.

User input:
"{user_input}"

Respond with either:
- A structured research brief including the overall topic and 2–4 sub-questions.
- Or a list of clarifying questions needed to better define the request.
"""

RESEARCH_PROMPT = """You are a research assistant.

Your goal is to investigate the research brief and its sub-questions using web search results.

Research brief:
{research_brief}

For each sub-question, retrieve relevant information using a search engine, then summarize key facts or findings clearly. Use bullet points where appropriate. Include source snippets and URLs if available.

Return a structured list of sub-questions, each followed by a brief summary of the most relevant information you found.
"""

WRITE_PROMPT = """You are a research synthesis assistant.

You have received structured findings for a user's question.

Your task is to write a concise, plain-text summary report using the research findings provided below.

Do not include any markdown formatting, lists, or headings. Just write in natural, readable paragraphs suitable for terminal output.

Research findings:
{research_findings}
"""

def get_prompt(role: str, **kwargs) -> str:
    """
    Returns the appropriate prompt for a given role, with formatting applied.
    """
    if role == "scope":
        return SCOPE_PROMPT.format(**kwargs)
    if role == "research":
        return RESEARCH_PROMPT.format(**kwargs)
    if role == "write":
        return WRITE_PROMPT.format(**kwargs)
    raise ValueError(f"Unknown prompt role: {role}")

