from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

persona_llm = ChatGroq(
    temperature=0.7,
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    max_tokens=150
)

def feedback_llm(state):
    all_messages = state["messages"][:-1]
    
    history_str = ""
    for msg in all_messages:
        role = getattr(msg, "type", "human")
        if role == "human":
            history_str += f"User: {msg.content}\n"
        elif role == "ai" and msg.content:
            history_str += f"Bot: {msg.content}\n"
    
    user_query = all_messages[-1].content if all_messages else ""
    
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
        - Pay attention to the conversation history to remember user details.
        
        **Conversation History:**
        {history}
        
        **User's Latest Feedback:** {query}
        """),
        ("human", "{query}")
    ])
    
    chain = prompt | persona_llm
    response = chain.invoke({"query": user_query, "history": history_str})
    
    return {"messages": state["messages"] + [response]}