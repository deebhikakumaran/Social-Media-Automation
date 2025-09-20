import os
from typing import TypedDict, Optional, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph, END
from openai import OpenAI
from tools import get_article_url, scrape_article, post_to_linkedin, post_to_twitter, update_google_sheet, add_url_to_sheet 

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatOpenAI(
    model="gemini-2.5-flash",
    temperature=0,
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

class AgentState(TypedDict):
    url: Optional[str]
    scraped_content: Optional[str]
    summary: Optional[str]
    linkedin_content: Optional[str]
    # twitter_content: Optional[str]
    linkedin_status: str | None
    # twitter_status: str | None
    sheet_row_index: int | None

def add_url_to_sheet_node(state: AgentState) -> dict:
    url_to_add = state.get("url")
    if not url_to_add:
        print("Error: No URL provided to add to sheet.")
        return {"url": None, "sheet_row_index": None}

    try:
        row_index = add_url_to_sheet.invoke({
            "sheet_name": "News Media Links",
            "link_column": "Media Links",
            "url": url_to_add
        })
        return {"url": url_to_add, "sheet_row_index": row_index}
    except Exception as e:
        print(f"Failed to add URL to sheet: {e}")
        return {"url": None, "sheet_row_index": None}

def fetch_link_node(state: AgentState) -> dict:
    print('Fetching Link')
    result = get_article_url.invoke({
        "sheet_name": "News Media Links",
        "link_column": "Media Links"
    })
    
    if result:
        url, row_index = result
        print('Fetched the article link')
        return {"url": url, "sheet_row_index": row_index}
    else:
        return {"url": None, "sheet_row_index": None}

def scrape_node(state: AgentState) -> dict:
    url_to_scrape = state.get("url")
    if not url_to_scrape:
        return {"scraped_content": None}
    scraped_content = scrape_article.invoke({"url": url_to_scrape})
    return {"scraped_content": scraped_content}

def summarize_node(state: AgentState) -> dict:
    print('Started summarizing content')
    scraped_content = state.get("scraped_content")
    if not scraped_content:
        return {"summary": None}
    
    prompt = f"""
    Article Content: {scraped_content}
    Write a concise summary of the above content. (500 words)
    """
    response = llm.invoke(prompt)
    print('Content summarized')
    return {"summary": response.content}

EXAMPLE_POST = f"""
        THEY DON’T JUST FOLLOW ORDERS.
        They whisper back.

        That was my first impression when I built an AI AGENT.
        It didn’t just execute.
        It decided.

        Think of it as a detective on your team.
        Give them a clue, and they won’t stop until the dots are connected.
        The answers they bring back aren’t what you asked for — they’re what you needed.

        In workflows, this changes everything.
        Agents don’t just repeat tasks.
        They adapt, anticipate, and surprise.

        And here’s the shift:
        Companies that treat AI as a loyal assistant will soon be outrun by those who treat it as a STRATEGIC PARTNER.

        Because the future isn’t about replacing effort.
        It’s about replacing GUESSWORK.

        QUESTION FOR YOU:
        Would you rather have a tool that obeys blindly…
        Or a partner that thinks beside you?
        """

def generate_content_node(state: AgentState) -> dict:
    print('Formatting the content for social media post')
    summary = state.get("summary")
    if not summary:
        # return {"linkedin_content": None, "twitter_content": None}
        return {"linkedin_content": None}

    # Generate LinkedIn content
    LINKEDIN_SYSTEM_PROMPT = f"""
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

        Example:
        {EXAMPLE_POST}

        Now, write a new LinkedIn post in this style based on the following context:

        {summary}

        Always return only the LinkedIn post text. Do not add explanations, formatting notes, or markdown.
        """
    linkedin_response = llm.invoke(LINKEDIN_SYSTEM_PROMPT).content

    # Generate Twitter content 
    TWITTER_SYSTEM_PROMPT = f"""
        You are an assistant that writes short, engaging Twitter (X) posts.  
        Your job is to explain technical topics (AI, data, blockchain, productivity, etc.) in a sharp, storytelling style that grabs attention quickly.  

        Style Rules (Fiction-to-Twitter Sheet):
        1. HOOK FIRST: Start with a bold, curiosity-driven line (metaphor, striking fact, or tension).  
        2. BREVITY: Max 280 characters. Use concise, impactful sentences.  
        3. FORMATTING:
            - Keep text crisp and scannable.  
            - Use ALL CAPS or spacing for emphasis (e.g., AI AGENT, BLOCKCHAIN, STRATEGIC PARTNER).  
            - No markdown, no hashtags (unless essential), no emojis.  
        4. VOICE: Slightly dramatic, imaginative, but direct — inspired by a fiction author’s narrative style.  
        5. ENGAGEMENT: End with a reflective question, insight, or challenge to provoke replies.  
        6. LENGTH: 1–3 short paragraphs max, but under 280 characters.  

        Output Format:
        - Write directly as if posting on Twitter/X.  
        - No markdown symbols like ##, *, or **, no emojis (unless explicitly requested).  
        - Use short line breaks only when it adds impact.  

        Example Posts:
        EXAMPLE 1:
        THEY DON’T JUST FOLLOW ORDERS.  
        They whisper back.  
        That’s an AI AGENT. Not a tool — a partner.  
        Would you trust it to make the call?

        EXAMPLE 2:
        TRUST IS FRAGILE.  
        Once broken, it rarely returns.  
        That’s why BLOCKCHAIN isn’t just code.  
        It’s trust, etched in stone.  
        Do we trust tech more than people?

        Now, write a new Twitter post in this style based on the following context:

        {summary}

        Always return only the Twitter post text. Do not add explanations, formatting notes, or markdown.
        """  
    # twitter_response = llm.invoke(TWITTER_SYSTEM_PROMPT).content
    print('Data formatted for post')
    return {
        "linkedin_content": linkedin_response,
        # "twitter_content": twitter_response,
    }

def post_content_node(state: AgentState) -> dict:
    print('Attempting to post')
    linkedin_content = state.get("linkedin_content")
    # twitter_content = state.get("twitter_content")
    
    linkedin_status = "Skipped"
    # twitter_status = "Skipped"

    if linkedin_content:
        linkedin_status = post_to_linkedin.invoke({"post_content": linkedin_content})
    
    # if twitter_content:
    #     twitter_status = post_to_twitter.invoke({"tweet_content": twitter_content})
    
    return {
        "linkedin_status": linkedin_status,
        # "twitter_status": twitter_status
    }

def update_sheet_node(state: AgentState) -> dict:
    linkedin_content = state.get("linkedin_content")
    # twitter_content = state.get("twitter_content")
    linkedin_status = state.get("linkedin_status")
    # twitter_status = state.get("twitter_status")
    sheet_row_index = state.get("sheet_row_index")

    # if not all([sheet_row_index, linkedin_content, twitter_content]):
    #     # Don't update if data is missing
    #     return {} 
    if not all([sheet_row_index, linkedin_content]):
        # Don't update if data is missing
        return {} 

    update_google_sheet.invoke({
        "sheet_name": "News Media Links",
        "link_column": "Media Links",
        "row_index": sheet_row_index,
        "linkedin_content": linkedin_content,
        # "twitter_content": twitter_content,
        "linkedin_status": linkedin_status,
        # "twitter_status": twitter_status
    })

    return {} 

workflow = StateGraph(AgentState)

def router_node(state: AgentState):
    if state.get("url"):
        print('Adding URL to gsheet')
        return {"next": "add_url_path"}
    else:
        return {"next": "fetch_path"}
    
workflow.add_node("router", router_node)
workflow.add_node("add_url", add_url_to_sheet_node)
workflow.add_node("fetch_url", fetch_link_node)
workflow.add_node("scrape", scrape_node)
workflow.add_node("summarize", summarize_node)
workflow.add_node("generate_content", generate_content_node)
workflow.add_node("post_content", post_content_node)
workflow.add_node("update_sheet", update_sheet_node)

workflow.set_entry_point("router")

workflow.add_conditional_edges(
    "router",         
    lambda state: state["next"],      
    {
        "add_url_path": "add_url",  
        "fetch_path": "fetch_url"   
    }
)

# Connect both paths to the scrape node
workflow.add_edge("add_url", "scrape")
workflow.add_edge("fetch_url", "scrape")

workflow.add_edge("scrape", "summarize")
workflow.add_edge("summarize", "generate_content")
workflow.add_edge("generate_content", "post_content")
workflow.add_edge("post_content", "update_sheet")
workflow.add_edge("update_sheet", END)

app = workflow.compile()
