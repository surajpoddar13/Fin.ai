from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import os
import yfinance as yf

load_dotenv()

agent = Agent(
    name="Finance Agent",

    model=OpenAIChat(
        id="llama-3.3-70b-versatile",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    ),

    instructions=[
        "You are an AI finance assistant.",
        "Explain financial information clearly.",
        "Use bullet points when helpful."
    ],

    markdown=True
)

# Company name to ticker mapping
company_to_ticker = {
    "NVIDIA": "NVDA",
    "TESLA": "TSLA",
    "APPLE": "AAPL",
    "MICROSOFT": "MSFT",
    "GOOGLE": "GOOGL",
    "AMAZON": "AMZN",
    "META": "META"
}


def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")

    if data.empty:
        return None

    return round(data["Close"].iloc[-1], 2)


if __name__ == "__main__":
    print("📈 Finance Agent Ready")
    print("Type 'exit' to quit\n")

    while True:
        query = input("Ask about stocks: ")

        if query.lower() == "exit":
            print("Goodbye 👋")
            break

        # Let the LLM handle news or comparisons
        if "news" in query.lower() or "compare" in query.lower():
            response = agent.run(query)
            print("\n", response.content, "\n")
            continue

        words = query.upper().split()
        ticker = None

        # If user typed ticker directly
        for w in words:
            if w in company_to_ticker.values():
                ticker = w
                break

        # If user typed company name
        if not ticker:
            for w in words:
                if w in company_to_ticker:
                    ticker = company_to_ticker[w]
                    break

        if ticker:
            price = get_stock_price(ticker)

            if price:
                prompt = f"The current stock price of {ticker} is ${price}. Explain briefly."
                response = agent.run(prompt)
                print("\n", response.content, "\n")
            else:
                print("❌ Could not find stock data.\n")

        else:
            response = agent.run(query)
            print("\n", response.content, "\n")