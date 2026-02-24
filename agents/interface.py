from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

router_llm = ChatGroq(
    temperature=0, 
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    max_tokens=10
)



def interface_llm(state):
    
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
    
    
    user_msg = state["messages"][-1].content
    
    
    response = chain.invoke({"issue": user_msg})
    
    
    return {"messages": state["messages"] + [response]}


def router_decision(state):
    
    classification = state["messages"][-1].content.lower().strip()
    
    if "billing" in classification:
        return "billing_node"
        
    elif "technical" in classification:
        return "technical_node"
        
    elif "feedback" in classification:
        return "feedback_node"
        
    else:
        return "feedback_node"