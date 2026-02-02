## Social Media Automation Agent

This project is a powerful social media automation agent built with **LangChain** and **LangGraph**. It is designed to automatically fetch the latest news link from a Google Sheet, scrape and summarize the article, generate platform-specific content, and post it to LinkedIn and Twitter. The entire process is exposed via a **FastAPI** server, allowing the agent to be triggered by an API call.

## Workflow Overview

The agent operates in a sequential, stateful workflow orchestrated by **LangGraph**. Each step is a dedicated "node" that passes information to the next, ensuring a clean and reliable process.

1.  **UI Trigger**: The workflow begins when a user submits a URL via the web-based UI.
2.  **Fetch or Add URL**: The agent either fetches the latest URL from a Google Sheet or adds a manually provided URL to the sheet.
3.  **Scrape Content**: The URL is passed to a web scraping tool (Firecrawl) that extracts the main content of the article, removing ads and other noise.
4.  **Summarize Content**: An LLM (Google Gemini) summarizes the scraped content into a concise, professional summary.
5.  **Generate Content**: Based on the summary, the LLM generates tailored social media posts for each platform (e.g., a professional post for LinkedIn and a short, engaging tweet for Twitter).
6.  **Post to Social Media**: The agent uses dedicated tools to post the generated content to LinkedIn and Twitter. It handles potential API errors and records the outcome.
7.  **Update Google Sheet**: Finally, the agent updates the original Google Sheet with the generated content for each platform and the status of each post (e.g., "Post successful" or "Post failed").

## Technologies Used

  * **LangChain & LangGraph**: The core frameworks for building the agent's logic and orchestrating the workflow.
  * **FastAPI**: A web framework for creating a server and API endpoint.
  * **Google Sheets API & `gspread`**: For reading data and writing back to Google Sheets.
  * **Firecrawl**: A web scraping API that provides clean, LLM-ready content.
  * **Google Gemini API**: The large language model used for summarization and content generation.
  * **LinkedIn API & `requests`**: For programmatic posting to LinkedIn.
  * **Twitter (X) API & `tweepy`**: For programmatic posting to Twitter.

## Getting Started

### Prerequisites

  * Python 3.8+
  * Git

### Installation

1.  **Clone the repository:**

    ```
    git clone https://github.com/deebhikakumaran/SocialMediaAutomation.git
    cd SocialMediaAutomation
    ```

2.  **Install dependencies:**

    ```
    pip install -r requirements.txt
    ```

### Setup

1.  **API Keys**: Obtain API keys for Firecrawl, Google Gemini, LinkedIn, and Twitter (X).
2.  **Google Sheets**: Set up a Google Cloud Project, enable the Sheets and Drive APIs, and download the `credentials.json` file. Share your target Google Sheet with the service account email.
3.  **Environment Variables**: Create a `.env` file in the root directory with the following variables:

    ```
    FIRECRAWL_API_KEY=your_firecrawl_api_key
    GOOGLE_API_KEY=your_google_api_key
    LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token
    LINKEDIN_PERSON_URN=your_linkedin_person_urn
    TWITTER_CONSUMER_KEY=your_twitter_consumer_key
    TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret
    TWITTER_ACCESS_TOKEN=your_twitter_access_token
    TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
    ```
4.  **Google Sheet Columns**: Ensure your Google Sheet has at least the following column headers: `Media Links`, `LinkedIn Content`, `LinkedIn Status`, `Twitter Content`, and `Twitter Status`.

## UI and Demonstration

This project includes a simple web-based UI to demonstrate the agent's functionality. The UI acts as a client, sending API requests to the FastAPI server.

**Client-Server Running:**

To start the API server, run the following command in your terminal:

```bash
uvicorn main:app --reload
```

The server will be available at `http://127.0.0.1:8000`. You can then open the index.html file in your browser to access the UI.

**How It Works:**

1. Enter URL: You enter a URL into the text box and click 'Run Agent'.
2. Client Request: The browser sends a POST request to the server's /run-agent endpoint with your provided URL.
3. Server-Side Execution: The FastAPI server takes your URL, and triggers the workflow.

## API Endpoint

You can trigger the agent by sending a POST request to the `/run-agent` endpoint.

### Request

```
POST http://127.0.0.1:8000/run-agent
Content-Type: application/json

{
  "url": "https://example.com/your-article"
}
```

### Response

The API will return a JSON object with the final state of the agent's run, including the generated content and the status of each post.

```json
{
  "status": "success",
  "message": "Agent workflow completed.",
  "final_state": {
    "url": "...",
    "scraped_content": "...",
    "summary": "...",
    "linkedin_content": "...",
    "twitter_content": "...",
    "linkedin_status": "Post successful.",
    "twitter_status": "Post failed: 403 Forbidden",
    "sheet_row_index": 5
  }
}
```

## License

This project is part of an AI Demos Hackathon submission.

