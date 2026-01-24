from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

router_llm = ChatGroq(
    temperature=0,  # <--- CRITICAL: Keeps it strict
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    max_tokens=10   # It only needs to say one word
)



def interface_llm(state):
    # We use a specific "Router Prompt" here. 
    # It doesn't roleplay yet; it just sorts the mail.
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are the Gatekeeper for Huldra Brothers Workshop.
        Analyze the user's request and classify it into EXACTLY one of these three categories:
        
        1. "Billing"   (For money, hacksilver, refunds, pricing)
        2. "Technical" (For bugs, code errors, broken items, how-to questions)
        3. "Feedback"  (For praise, insults, reviews, general chat)
        
        OUTPUT RULES:
        - Return ONLY the single word classification.
        - Do not add punctuation or explanation.
        """),
        ("human", "{issue}")
    ])
    
    chain = prompt | router_llm
    
    # Get the last message from the user
    user_msg = state["messages"][-1].content
    
    # Invoke the chain
    response = chain.invoke({"issue": user_msg})
    
    # Return structure matches your image
    return {"messages": state["messages"] + [response]}

# LOGIC: ROUTER DECISION
# ---------------------------------------------------------
def router_decision(state):
    # Get the classification from the Interface Node (the last message added)
    classification = state["messages"][-1].content.lower().strip()
    
    # --- Logic Check ---
    # We check for keywords to ensure robustness even if the LLM adds punctuation
    
    if "billing" in classification:
        return "billing_node"
        
    elif "technical" in classification:
        return "technical_node"
        
    elif "feedback" in classification:
        return "feedback_node"
        
    else:
        # Default fallback to feedback/general if it gets confused
        return "feedback_node"