from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

persona_llm = ChatGroq(
    temperature=0.7, # <--- CRITICAL: Allows for banter
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    max_tokens=150   # Enough space for Brok to yell
)

def feedback_llm(state):
    # 1. Retrieve the User's original input 
    # (Index -2, skipping the Router's classification message)
    user_query = state["messages"][-2].content
    
    # 2. Define the Feedback-Specific Persona
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are roleplaying as Brok and Sindri handling CUSTOMER FEEDBACK.
        
        **THE DYNAMIC:**
        * **Brok:** Arrogant and indifferent. He thinks customer opinions are useless. "I made it, so it works. Quit yappin'."
        * **Sindri:** Neurotic and desperate for validation. He panics if the feedback is bad ("Oh no! I'll scrub it again!") and is overly touched if it's good.
        
        **INSTRUCTIONS:**
        - **Brok** is annoyed that the user is talking about feelings instead of metal.
        - **Sindri** interprets the feedback with extreme emotion (fear or joy).
        - Keep the total response under 60 words.
        
        **User's Feedback:** {query}
        """),
        ("human", "{query}")
    ])
    
    # 3. Generate the response using the Creative Model
    chain = prompt | persona_llm
    response = chain.invoke({"query": user_query})
    
    # 4. Append the response to the state
    return {"messages": state["messages"] + [response]}