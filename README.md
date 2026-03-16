# Fin.ai

Fin.ai is an AI-powered financial analysis dashboard that provides real-time insights into stock market data. The project analyzes stock prices, technical indicators, and company fundamentals to help users better understand stock performance.

The goal of this project is to combine financial data analysis with AI-powered insights to create an interactive dashboard that helps users explore market trends and make informed decisions.

## Problem

Stock market data is complex and constantly changing. Investors and analysts often need to analyze multiple factors such as price trends, technical indicators, and company fundamentals to understand stock performance.

Without proper visualization and analysis tools, it becomes difficult to quickly interpret this data and extract meaningful insights.

This project addresses this challenge by creating a dashboard that analyzes stock data and presents it in a clear and interactive format.

## Why It Matters

Understanding stock market trends can help:

* Investors make more informed investment decisions
* Analysts identify trends and patterns in financial markets
* Students and researchers learn financial data analysis

By combining financial data with visualization and AI insights, the dashboard converts raw market data into meaningful information.

## Technical Approach

The project uses Python and data visualization tools to collect, analyze, and present financial data in an interactive dashboard.

Technologies used:

* Python
* Streamlit for building the interactive dashboard
* yfinance for retrieving real-time stock market data
* Plotly for interactive charts and visualizations
* Pandas for data analysis
* Groq LLM / Agno for AI-powered financial insights

Steps followed in the project:

* Retrieve stock data using financial APIs
* Clean and process the data using Pandas
* Calculate technical indicators such as moving averages and momentum
* Visualize stock trends using interactive charts
* Generate AI-driven analysis of stock performance

## Results

The dashboard provides insights such as:

* Current stock price and price change
* 52-week high and low values
* Stock price trends over time
* Technical indicators such as moving averages
* Risk and momentum indicators
* Key company fundamentals
* AI-generated analysis of stock performance

These insights help users better understand how different factors influence stock market behavior.

## Project Structure

```
fin-ai
│
├── app.py                # Streamlit dashboard application
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
├── data/                 # Optional datasets (if used)
├── notebooks/            # Experiment notebooks (optional)
└── src/                  # Helper scripts
```

## How to Run the Project

Clone the repository

```
git clone https://github.com/surajpoddar13/Fin.ai.git
cd Fin.ai
```

Install dependencies

```
pip install -r requirements.txt
```

Run the application

```
streamlit run app.py
```

The dashboard will open in your browser where you can enter any stock name or ticker to analyze its performance.

## Future Improvements

Possible improvements include:

* Adding advanced technical indicators such as RSI and MACD
* Integrating live financial news sentiment analysis
* Adding candlestick charts and volume indicators
* Supporting portfolio tracking and comparison of multiple stocks
* Deploying the dashboard as a production financial analytics tool

