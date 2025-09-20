from typing import TypedDict
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
import requests

load_dotenv()

class GraphState(TypedDict):
    """
    Represents the state of our graph.
    """
    user_context: str
    retrieved_snippets: list
    generated_script: str
    final_answer: str | None

def post_node(state: GraphState):
    """Posts the approved script to Linkedin."""
    print("---POSTING TO LINKEDIN---")
    final_script = state["generated_script"]
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    company_id = os.getenv("LINKEDIN_COMPANY_ID")

    if not access_token or not company_id:
        print("Error: LinkedIn credentials (access token or company ID) not found. Please set your .env file.")
        return {"final_answer": "Post failed: Missing credentials."}
    
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    payload = {
        "author": "urn:li:person:-Zwn3471ec",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": final_script
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        id = response.json().get("id", "N/A")
        print(f"Post ID: {id}")
        
        print("Post successful!")
        return {"final_answer": "Post successful."}
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        print(f"Response: {response.text}")
        return {"final_answer": f"Post failed: {err}"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"final_answer": f"Post failed: {e}"}
    
# Build the LangGraph workflow
workflow = StateGraph(GraphState)
workflow.add_node("post", post_node)
workflow.set_entry_point("post")
workflow.add_edge("post", END) 

# Compile the graph
app = workflow.compile()