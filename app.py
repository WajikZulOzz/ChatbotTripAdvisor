import os
import uuid
from typing import Dict, List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai
from google.genai import types

from server_utils import get_weather, search_places, SYSTEM_INSTRUCTION

load_dotenv()

app = FastAPI()

# Global client instance
client: Optional[genai.Client] = None

# Store active chat sessions
chat_sessions: Dict[str, object] = {}

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

def get_gemini_client():
    # Use global client or initialize it
    global client
    if client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY not set")
        client = genai.Client(api_key=api_key)
    return client

def create_new_chat():
    try:
        # Get the persistent client
        current_client = get_gemini_client()
        
        tools = [get_weather, search_places]
        # Create chat using the persistent client
        chat = current_client.chats.create(
            model="gemini-3-flash-preview",
            config=types.GenerateContentConfig(
                temperature=0.8,
                tools=tools,
                system_instruction=SYSTEM_INSTRUCTION,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
            )
        )
        return chat
    except Exception as e:
        print(f"Error creating chat: {e}")
        # If client issue, maybe reset it?
        global client
        client = None 
        raise HTTPException(status_code=500, detail=f"Failed to initialize chat: {str(e)}")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    session_id = request.session_id
    
    # helper to getting or creating chat
    if not session_id or session_id not in chat_sessions:
        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = create_new_chat()
    
    chat = chat_sessions[session_id]
    
    try:
        response = chat.send_message(request.message)
        response_text = response.text if response.text else "(Thinking...)"
        return ChatResponse(response=response_text, session_id=session_id)
    except Exception as e:
        print(f"Error during chat: {e}")
        # If we hit an error (like client closed), try to recreate the session once
        if "client has been closed" in str(e).lower():
             print("Attempting to recover session...")
             chat_sessions[session_id] = create_new_chat()
             chat = chat_sessions[session_id]
             try:
                response = chat.send_message(request.message)
                response_text = response.text if response.text else "(Thinking...)"
                return ChatResponse(response=response_text, session_id=session_id)
             except Exception as retry_e:
                 raise HTTPException(status_code=500, detail=str(retry_e))
        
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files (we will create these next)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
