from phi.agent import Agent
import phi.api
from phi.model.google import Gemini
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import os
from dotenv import load_dotenv

import phi
from phi.playground import Playground, serve_playground_app

# Load environment variables
load_dotenv()
phi.api=os.getenv("PHI_API_KEY")
Gemini.api_key = os.getenv("GOOGLE_API_KEY")

## Web Search Agent
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for accurate and up-to-date financial information",
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[DuckDuckGo()],
    instructions=[
        "1. Perform targeted searches to find the most relevant and recent financial information.",
        "2. Always verify the credibility of sources before including them in the response.",
        "3. Summarize the information concisely and include direct links to the sources.",
        "4. If no relevant information is found, state this clearly and suggest alternative search terms.",
    ],
    show_tool_calls=True,
    markdown=True,
)

## Financial Agent
financial_agent = Agent(
    name="Finance AI Agent",
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[
        YFinanceTools(
            stock_price=True,
            stock_fundamentals=True,
            analyst_recommendations=True,
            company_news=True,
        )
    ],
    instructions=[
        "1. Use tables to display stock data for better readability.",
        "2. Always include the following details for any stock:",
        "   - Current price",
        "   - Key fundamentals (e.g., P/E ratio, market cap)",
        "   - Latest analyst recommendations (Buy/Hold/Sell)",
        "   - Recent company news (last 7 days)",
        "3. If data is unavailable, explain why and suggest alternative tools or sources.",
        "4. Keep the response concise and avoid unnecessary details.",
    ],
    show_tool_calls=True,
    markdown=True,
)


app = Playground(agents=[financial_agent, web_search_agent]).get_app()


if __name__=="__main__":
    serve_playground_app("NVDA_Stock_Analyst_Playground:app",reload=True)

