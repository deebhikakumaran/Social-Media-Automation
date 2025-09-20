import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, TypedDict
import asyncio
import uuid
from generate import app as generate_content, conversation_states
from post import app as post_content
from pydantic import BaseModel
from agent import app as agent, AgentState

app = FastAPI(
    title="Social Media Automation Agent",
    description="An API to trigger the social media content generation and posting agent.",
    version="1.0.0"
)

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserRequest(BaseModel):
    user_context: str
    
class PostRequest(BaseModel):
    conversation_id: str
    final_script: str
    user_approval: bool

class AgentRequest(BaseModel):
    url: Optional[str] = None

@app.get("/")
def root():
    return {"status": "Server is up and running!"}

@app.post("/generate")
async def generate_script(query: UserRequest):
    print(f"Received request with context: {query.user_context}")
    try:
        conversation_id = str(uuid.uuid4())
        initial_state = {"user_context": query.user_context}
        final_state = generate_content.invoke(initial_state)
        conversation_states[conversation_id] = final_state

        if final_state.get("generated_script"):
            return {
                "status": "Script generated, awaiting approval",
                "result": final_state["generated_script"],
                "conversation_id": conversation_id,
            }
        else:
            return {"status": "failed", "result": "Script generation failed."}

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
@app.post("/post")
async def approve_and_post(post_data: PostRequest): 
    print("--- Received approval from UI ---")

    # Get the state from the generate step
    state = conversation_states.get(post_data.conversation_id)

    if not state:
        raise HTTPException(status_code=404, detail="Conversation not found or has expired.")

    state["generated_script"] = post_data.final_script
    
    # Check for approval. Here, the UI tells us to post.
    if post_data.user_approval is False:
        del conversation_states[post_data.conversation_id]
        return {"status": "Post cancelled by user."}

    # Run the post_agent with the updated state
    final_state = post_content.invoke(state)

    # Clean up the state
    del conversation_states[post_data.conversation_id]
    
    return {
        "status": final_state.get("final_answer", "Workflow ended without posting.")
    }

@app.post("/run-agent")
async def run_agent(request: AgentRequest):
    """
    Triggers the social media automation agent.
    Optionally accepts a URL to override the Google Sheets fetch.
    """
    try:
        # Define the initial state for the agent
        initial_state = {"url": request.url} if request.url else {"url": None}

        # Run the LangGraph agent asynchronously
        final_state = await agent.ainvoke(initial_state)

        # Return the final state as a JSON response
        return {
            "status": "success",
            "message": "Agent workflow completed.",
            "final_state": final_state
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)