import time
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import os

load_dotenv()

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="Fin.ai",
    page_icon="📈",
    layout="wide"
)

# ------------------------------------------------
# STYLE
# ------------------------------------------------

st.markdown("""
<style>

.block-container{
padding-top:0.5rem;
}

.stApp{
background:white;
}

h1{
text-align:center;
color:#4285f4;
font-size:60px;
margin-bottom:10px;
}

.metric-card{
background:#34a853;
padding:20px;
border-radius:12px;
text-align:center;
height:140px;
}

.metric-title{
color:white;
font-weight:bold;
font-size:18px;
}

.metric-value{
color:white;
font-size:32px;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.markdown("<h1>Fin.ai</h1>", unsafe_allow_html=True)

query = st.text_input(
    "Enter Stock or Company (Example: NVDA, Nvidia, Tesla)",
    ""
)

# ------------------------------------------------
# GLOBAL TICKER DETECTION (UPDATED 🔥)
# ------------------------------------------------

def detect_ticker(user_input):

    user_input = user_input.strip()

    # 1️⃣ Try direct ticker
    try:
        test = yf.Ticker(user_input.upper())
        data = test.history(period="1d")

        if not data.empty:
            return user_input.upper()
    except:
        pass

    # 2️⃣ Yahoo global search
    try:
        search = yf.Search(user_input, max_results=5)
        quotes = search.quotes

        if quotes:
            return quotes[0]["symbol"]
    except:
        pass

    # 3️⃣ Try multiple exchanges
    exchanges = [".NS", ".BO", ".L", ".TO", ".AX", ".HK", ".KS"]

    for ex in exchanges:
        try:
            test = yf.Ticker(user_input.upper() + ex)
            data = test.history(period="1d")

            if not data.empty:
                return user_input.upper() + ex
        except:
            continue

    return None


ticker = None

if query:
    ticker = detect_ticker(query)

# ------------------------------------------------
# AI AGENT
# ------------------------------------------------

agent = Agent(
    name="Finance Assistant",

    model=OpenAIChat(
        id="llama-3.3-70b-versatile",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    ),

    instructions=[
        "You are a financial analyst.",
        "Explain stock performance clearly.",
        "Use bullet points."
    ],

    markdown=True
)

# ------------------------------------------------
# STOCK DATA
# ------------------------------------------------

@st.cache_data(ttl=3600)
def get_stock_data(ticker):

    try:

        stock = yf.Ticker(ticker)

        data = None

        for _ in range(3):

            try:
                data = stock.history(period="6mo")

                if not data.empty:
                    break

            except:
                time.sleep(2)

        return data

    except:
        return None

# ------------------------------------------------
# MAIN APP
# ------------------------------------------------

if ticker:

    data = get_stock_data(ticker)

    if data is None or data.empty:

        st.error("Unable to fetch stock data. Try again later.")

    else:

        current = round(data["Close"].iloc[-1],2)
        prev = round(data["Close"].iloc[-2],2)

        change = round(current-prev,2)
        percent = round((change/prev)*100,2)

        high = round(data["High"].max(),2)
        low = round(data["Low"].min(),2)

        # ------------------------------------------------
        # METRICS
        # ------------------------------------------------

        col1,col2,col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
            <div class="metric-title">Current Price</div>
            <div class="metric-value">${current}</div>
            <div style="color:white">{change} ({percent}%)</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
            <div class="metric-title">52 Week High</div>
            <div class="metric-value">${high}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
            <div class="metric-title">52 Week Low</div>
            <div class="metric-value">${low}</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        # ------------------------------------------------
        # CHART
        # ------------------------------------------------

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            line=dict(color="#fbbc05", width=3)
        ))

        fig.update_traces(
            fill="tozeroy",
            fillcolor="rgba(66,133,244,0.35)"
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="black"),
            title=f"{ticker} Price Chart"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ------------------------------------------------
        # INSIGHTS
        # ------------------------------------------------

        st.subheader("📊 Stock Insights")

        ma50 = data["Close"].rolling(50).mean().iloc[-1]
        ma200 = data["Close"].rolling(200).mean().iloc[-1]

        volatility = data["Close"].pct_change().std()*100

        momentum = (data["Close"].iloc[-1] - data["Close"].iloc[-30]) / data["Close"].iloc[-30] *100

        col1,col2 = st.columns(2)

        with col1:

            signal = "Bullish 📈" if ma50 > ma200 else "Bearish 📉"

            st.table(pd.DataFrame({
                "Metric":[
                    "50 Day MA",
                    "200 Day MA",
                    "Signal"
                ],
                "Value":[
                    round(ma50,2),
                    round(ma200,2),
                    signal
                ]
            }))

        with col2:

            st.table(pd.DataFrame({
                "Metric":[
                    "Volatility",
                    "30 Day Momentum"
                ],
                "Value":[
                    f"{round(volatility,2)} %",
                    f"{round(momentum,2)} %"
                ]
            }))

        # ------------------------------------------------
        # AI ANALYSIS
        # ------------------------------------------------

        st.subheader("🤖 AI Stock Analysis")

        if st.button("Generate Analysis"):

            prompt = f"""
            Analyze stock {ticker}

            Current price ${current}

            Provide:
            - company overview
            - growth potential
            - risks
            """

            response = agent.run(prompt)

            st.markdown(response.content)

elif query:

    st.error("Stock not recognized. Try Tesla, Nvidia, Tata, Reliance, etc.")