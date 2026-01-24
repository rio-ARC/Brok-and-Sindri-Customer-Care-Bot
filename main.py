from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
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
        result = graph.invoke(graph_input)
        final_response = result["messages"][-1].content
        
        return {
            "response": final_response,
            "status": "success"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
