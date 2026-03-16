import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import pandas as pd
import os
from yahooquery import search

def get_ticker_from_query(query):

    try:
        result = search(query)

        quotes = result.get("quotes")

        if quotes:
            return quotes[0]["symbol"]

    except:
        pass

    return None

load_dotenv()

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Finance Dashboard",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>

/* Reduce top padding of the whole page */
.block-container{
    padding-top:0.5rem !important;
}

/* Remove extra margin above title */
h1{
    margin-top:0px !important;
}

/* Reduce space between title and input */
#product-title{
    margin-bottom:5px !important;
}

</style>
""", unsafe_allow_html=True)
# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp{
background:white;
}

h1{
color:#4285f4;
}

h2,h3{
color:#673ab7;
}

p,div,span{
color:black;
}

input{
color:black !important;
border:2px solid #4285f4 !important;
border-radius:6px !important;
}

.stButton > button{
background:#ea4335;
color:white;
border-radius:6px;
font-weight:bold;
}

.metric-card{
background:#34a853;
padding:25px;
border-radius:12px;
text-align:center;
height:150px;
}

.metric-title{
font-size:18px;
font-weight:bold;
color:white;
}

.metric-value{
font-size:32px;
font-weight:bold;
color:white;
}

.card{
border-radius:10px;
padding:20px;
border:2px solid #4285f4;
background:white;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# AI AGENT
# --------------------------------------------------

agent = Agent(
    name="Finance Assistant",
    model=OpenAIChat(
        id="llama-3.3-70b-versatile",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    ),
    instructions=[
        "You are a financial analyst.",
        "Explain stock insights clearly.",
        "Use bullet points."
    ],
    markdown=True
)


# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def format_market_cap(value):

    if value is None:
        return "N/A"

    if value >= 1_000_000_000_000:
        return f"${round(value/1_000_000_000_000,2)} Trillion"

    if value >= 1_000_000_000:
        return f"${round(value/1_000_000_000,2)} Billion"

    return value


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
"""
<h1 id="product-title" style="
text-align:center;
font-size:60px;
font-weight:bold;
color:#4285f4;
toppadding:1px;
">
Fin.ai
</h1>
""",
unsafe_allow_html=True
)
query = st.text_input("Enter Stock (Example: NVDA, TSLA, AAPL)")

ticker=None

if query:
    ticker = get_ticker_from_query(query)

# --------------------------------------------------
# STOCK DATA
# --------------------------------------------------

if ticker:

    stock=yf.Ticker(ticker)
    data=stock.history(period="1y")

    if not data.empty:

        current=round(data["Close"].iloc[-1],2)
        prev=round(data["Close"].iloc[-2],2)

        change=round(current-prev,2)
        percent=round((change/prev)*100,2)

        high=round(data["High"].max(),2)
        low=round(data["Low"].min(),2)

        # --------------------------------------------------
        # METRIC CARDS
        # --------------------------------------------------

        col1,col2,col3=st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
            <div class="metric-title">Current Price</div>
            <div class="metric-value">${current}</div>
            <div>{change} ({percent}%)</div>
            </div>
            """,unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
            <div class="metric-title">52 Week High</div>
            <div class="metric-value">${high}</div>
            </div>
            """,unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
            <div class="metric-title">52 Week Low</div>
            <div class="metric-value">${low}</div>
            </div>
            """,unsafe_allow_html=True)

        st.write("")

        # --------------------------------------------------
        # PRICE CHART
        # --------------------------------------------------

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

            title=dict(
                text=f"{ticker} Price Chart",
                font=dict(color="#4285f4",size=22)
            ),

            xaxis=dict(
                tickfont=dict(color="black")
            ),

            yaxis=dict(
                tickfont=dict(color="black")
            )
        )

        st.plotly_chart(fig,use_container_width=True)

        # --------------------------------------------------
        # TECHNICAL INDICATORS
        # --------------------------------------------------

        data["MA50"]=data["Close"].rolling(50).mean()
        data["MA200"]=data["Close"].rolling(200).mean()

        ma50=round(data["MA50"].iloc[-1],2)
        ma200=round(data["MA200"].iloc[-1],2)

        signal="Bullish 📈" if ma50>ma200 else "Bearish 📉"

        volatility=round(data["Close"].pct_change().std()*100,2)

        momentum=round((current-data["Close"].iloc[-30])/data["Close"].iloc[-30]*100,2)

        score=0

        if percent>0:
            score+=1
        if momentum>0:
            score+=1
        if ma50>ma200:
            score+=1

        recommendation="Bullish Outlook 📈" if score>=2 else "Neutral / Bearish 📉"

        # --------------------------------------------------
        # INSIGHT CARDS
        # --------------------------------------------------

        st.subheader("📊 Stock Insights")

        c1,c2=st.columns(2)

        with c1:
            st.markdown(f"""
            <div class="card">
            <h4>Technical Trend</h4>
            <table>
            <tr><td>50 Day MA</td><td>{ma50}</td></tr>
            <tr><td>200 Day MA</td><td>{ma200}</td></tr>
            <tr><td>Signal</td><td>{signal}</td></tr>
            </table>
            </div>
            """,unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="card">
            <h4>Risk Indicator</h4>
            <p>Volatility: {volatility}%</p>
            <p>Higher volatility means higher potential return but also higher risk.</p>
            </div>
            """,unsafe_allow_html=True)

        c3,c4=st.columns(2)

        with c3:
            st.markdown(f"""
            <div class="card">
            <h4>Momentum (30 Day)</h4>
            <p>Performance: {momentum}%</p>
            </div>
            """,unsafe_allow_html=True)

        with c4:
            st.markdown(f"""
            <div class="card">
            <h4>Technical Recommendation</h4>
            <p style="font-size:20px;"><b>{recommendation}</b></p>
            </div>
            """,unsafe_allow_html=True)

        # --------------------------------------------------
        # FUNDAMENTALS TABLE
        # --------------------------------------------------

        info=stock.info

        st.subheader("📊 Key Fundamentals")

        fundamentals=pd.DataFrame({
        "Metric":[
        "Market Cap",
        "P/E Ratio",
        "Dividend Yield"
        ],

        "Value":[
        format_market_cap(info.get("marketCap")),
        info.get("trailingPE","N/A"),
        info.get("dividendYield","N/A")
        ]
        })

        st.dataframe(fundamentals,use_container_width=True,hide_index=True)

        # --------------------------------------------------
        # AI ANALYSIS
        # --------------------------------------------------

        st.subheader("🤖 AI Stock Analysis")

        if st.button("Generate AI Insights"):

            prompt=f"""
Analyze stock {ticker}

Price: {current}
52 week high: {high}
52 week low: {low}

Provide:

• Key insight
• Investment outlook
• Major risks
• Interesting fact
"""

            response=agent.run(prompt)

            st.markdown(response.content)

    else:
        st.error("Stock not found")