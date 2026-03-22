from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Import our custom RAG engine from Day 4!
from rag_engine import generate_shopping_advice

# 1. Initialize the API Gateway
app = FastAPI(
    title="AI-Mart Gateway",
    description="The core API gateway for the AI-Mart e-commerce system.",
    version="1.0.0"
)

# 2. Define Data Models (Strict Typing for absolute safety)
class ChatRequest(BaseModel):
    user_query: str

class ChatResponse(BaseModel):
    reply: str
    status: str

# 3. Create the API Endpoint (The Routing Logic)
@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    print(f"\n[API GATEWAY] Received request: {request.user_query}")
    
    try:
        # Hand off the query to our RAG Engine
        # In a fully async production app, this would be an 'await' call, 
        # but our current RAG engine is synchronous, which is fine for the MVP.
        ai_reply = generate_shopping_advice(request.user_query)
        
        return ChatResponse(
            reply=ai_reply,
            status="success"
        )
    except Exception as e:
        print(f"[API GATEWAY ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail="Internal AI Engine Error")

# 4. Run the Server
if __name__ == "__main__":
    print("="*50)
    print("🚀 Starting AI-Mart Uvicorn Server on Port 8000...")
    print("="*50)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)