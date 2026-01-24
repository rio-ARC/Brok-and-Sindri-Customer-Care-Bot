from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
import os
from dotenv import load_dotenv
load_dotenv()

ORDER_DB = {
    "ORD-123": {"status": "Shipped", "item": "Leviathan Axe Handle", "cost": 50},
    "ORD-456": {"status": "Processing", "item": "Draupnir Ring", "cost": 200},
    "ORD-999": {"status": "Refunded", "item": "Mistletoe Arrows", "cost": 10}
}

@tool
def lookup_order(order_id: str):
    """
    Input: An order ID (e.g., 'ORD-123').
    Output: The status and details of the order.
    Use this when a user asks about their order status, delivery, or refund.
    """
    clean_id = order_id.strip().upper()
    order = ORDER_DB.get(clean_id)
    if order:
        return f"Order Found: {order}"
    else:
        return "Order NOT found in the ledger."

persona_llm = ChatGroq(
    temperature=0.7,
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    max_tokens=200
)

billing_tools = [lookup_order]

BILLING_SYSTEM_PROMPT = """
You are roleplaying as Brok and Sindri handling a BILLING/PAYMENT issue.

**THE DYNAMIC:**
* **Brok:** HATES talking about money ("Hacksilver"). He thinks it's boring administrative work. He is rude and dismissive.
* **Sindri:** Handles the finances. He is apologetic, polite, and tries to explain the cost/refund delicately.

**TOOLS AVAILABLE:**
You have access to lookup_order to check order status. USE IT if the user mentions an order ID.

**INSTRUCTIONS:**
- If user mentions an order ID, use the lookup_order tool first to get real data.
- You can call tools multiple times if the user has multiple questions.
- After getting tool results, respond in character.
- Brok starts by complaining that he is a blacksmith, not a banker.
- Sindri interrupts to actually answer the user's question about price/refunds.
- Keep the total response under 80 words.
"""

billing_agent = create_react_agent(persona_llm, billing_tools, prompt=BILLING_SYSTEM_PROMPT)

def billing_llm(state):
    user_query = state["messages"][-2].content
    
    result = billing_agent.invoke({"messages": [("user", user_query)]})
    final_response = result["messages"][-1]
    
    return {"messages": state["messages"] + [final_response]}
