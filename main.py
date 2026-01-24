from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from graph import graph

load_dotenv()

app = FastAPI(title="Huldra Brothers Support Bot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str
    user_id: str = "default_user"


@app.get("/")
def root():
    return {
        "status": "online",
        "bot": "Huldra Brothers Workshop",
        "message": "Brok and Sindri are ready to help (or yell at you)."
    }


@app.post("/chat")
def chat(request: MessageRequest):
    try:
        graph_input = {"messages": [("user", request.message)]}
        config = {"configurable": {"thread_id": request.user_id}}
        
        result = graph.invoke(graph_input, config)
        final_response = result["messages"][-1].content
        
        return {
            "response": final_response,
            "user_id": request.user_id,
            "status": "success"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/history/{user_id}")
def get_history(user_id: str):
    try:
        config = {"configurable": {"thread_id": user_id}}
        state = graph.get_state(config)
        
        if state.values:
            messages = []
            for msg in state.values.get("messages", []):
                messages.append({
                    "role": getattr(msg, "type", "unknown"),
                    "content": msg.content if hasattr(msg, "content") else str(msg)
                })
            return {"user_id": user_id, "messages": messages}
        
        return {"user_id": user_id, "messages": []}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")
