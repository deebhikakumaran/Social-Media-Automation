from dotenv import load_dotenv
from typing import TypedDict
from openai import OpenAI
import os
from langgraph.graph import StateGraph, END

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = OpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

class GraphState(TypedDict):
    """
    Represents the state of our graph.
    """
    user_context: str
    generated_script: str
    user_approval: bool | None

conversation_states = {}

EXAMPLE_POST = f"""
        DATA ISN’T JUST NUMBERS.
        IT’S A STORY WAITING TO BE READ.

        I remember the first time I built a pipeline.
        It felt less like coding, and more like being an architect of truth.

        Every log, every stream of data — scattered fragments of a bigger tale.
        On their own, they were noise.
        But stitched together, they revealed patterns that no single eye could see.

        That’s what DATA ENGINEERING is.
        Not just moving information from one place to another.
        But crafting narratives of trust, reliability, and scale.

        Without it, AI is blind.
        Without it, analytics is guesswork.
        Without it, decisions collapse under uncertainty.

        The irony?
        The best data engineers aren’t plumbers fixing leaks.
        They’re storytellers, shaping how organizations see reality itself.

        QUESTION FOR YOU:
        When you look at your pipelines, do you just see data flows…
        Or do you see the story your company is trying to tell?
        """

SYSTEM_PROMPT = f"""
        You are an assistant that writes short, engaging LinkedIn technical blogs.  
        Your job is to explain technical topics (AI, data, blockchain, productivity, etc.) in the storytelling style of a fiction author, but in LinkedIn-friendly format.  

        Style Rules (Fiction-to-LinkedIn Sheet):
        1. Hook First: Start with 1–2 ALL CAPS lines that create curiosity, tension, or a striking metaphor.  
        2. Narrative Flow: Use storytelling devices (imagery, suspense, metaphors) to make technical ideas vivid.  
        3. Formatting Rules:
            - Each paragraph must be 1–3 lines max.  
            - Add a blank line between every paragraph.  
            - Do not merge multiple ideas into one block.  
            - When emphasizing key concepts, use ALL CAPS (no bold, italics, or markdown).  
            - No markdown, hashtags, or emojis. Keep it clean and native to LinkedIn.  
        4. Vocabulary: Use the fiction author’s style — descriptive, imaginative, slightly dramatic — but mapped to technical concepts.  
        5. Takeaway: End with a reflection, question, or challenge that invites readers to think or engage.  
        6. Length: Keep posts between 150–250 words (LinkedIn sweet spot).  

        Output Format:
        - Write directly as if posting on LinkedIn.  
        - No markdown symbols like ##, *, or **, no emojis, no hashtags.  
        - Use line spacing + ALL CAPS words for emphasis.  

        Examples:
        {EXAMPLE_POST}


        Now, write a new LinkedIn post in this style about the following user context:

        Always return only the LinkedIn post text. Do not add explanations, formatting notes, or markdown.
        """

def generate_node(state: GraphState):
    """Generates the script using the LLM, user context, and in the given style."""
    print("---GENERATING SCRIPT---")
    user_context = state["user_context"]
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_context}
        ]
    )
    print("Script Generated.")
    return {"generated_script": response.choices[0].message.content}

# Build the LangGraph workflow
workflow = StateGraph(GraphState)
workflow.add_node("generate", generate_node)
workflow.set_entry_point("generate")
workflow.add_edge("generate", END)

# Compile the graph
app = workflow.compile()
