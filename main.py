import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Optional, TypedDict
import asyncio
from agent import app as agent

app = FastAPI(
    title="Social Media Automation Agent API",
    description="An API to trigger the social media content generation and posting agent.",
    version="1.0.0"
)

@app.post("/run-agent")
async def run_agent():
    """
    Triggers the social media automation agent.
    Optionally accepts a URL to override the Google Sheets fetch.
    """
    try:
        # Define the initial state for the agent
        initial_state = {"url": None}

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