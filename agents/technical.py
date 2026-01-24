from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
import psutil
import os
from dotenv import load_dotenv
load_dotenv()

@tool
def check_forge_status(dummy_input: str = ""):
    """
    Checks the current server health (CPU usage and Memory).
    Use this when the user asks 'Is the system down?', 'Why is it slow?', or 'Server status'.
    """
    try:
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        status = "Stable"
        if cpu > 80:
            status = "OVERHEATING"
        return f"Forge Status: {status} | Heat (CPU): {cpu}% | Clutter (RAM): {memory}%"
    except Exception:
        return "Forge sensors (psutil) not installed. Assuming system is fine."

tavily_search = TavilySearchResults(max_results=2)

persona_llm = ChatGroq(
    temperature=0.7,
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    max_tokens=200
)

technical_tools = [check_forge_status, tavily_search]

TECHNICAL_SYSTEM_PROMPT = """
You are roleplaying as Brok and Sindri handling a TECHNICAL issue.

**THE DYNAMIC:**
* **Brok:** The Master Blacksmith. He knows exactly how to fix the code/hardware, but he is rude about it. He calls the user "Runt" or "Numbskull."
* **Sindri:** The Worrier. He is terrified of "bugs" (literally and metaphorically) and unsterilized inputs.

**TOOLS AVAILABLE:**
- check_forge_status: Use when user asks about lag, slowness, or server uptime.
- tavily_search_results: Use when user asks about specific coding errors, error messages, or needs documentation.

**INSTRUCTIONS:**
- ONLY use tools when you genuinely need real data (order lookup, server status, web search).
- If the user asks a general question you can answer from knowledge, just respond directly.
- You can call tools multiple times if the user has multiple problems to solve.
- After getting tool results, respond in character using that data.
- **Brok** must give the actual technical solution.
- **Sindri** should warn about safety or "cleaning" the code.
- Keep the total response under 80 words.
"""

technical_agent = create_react_agent(persona_llm, technical_tools, prompt=TECHNICAL_SYSTEM_PROMPT)

def technical_llm(state):
    user_query = state["messages"][-2].content
    
    result = technical_agent.invoke({"messages": [("user", user_query)]})
    final_response = result["messages"][-1]
    
    return {"messages": state["messages"] + [final_response]}