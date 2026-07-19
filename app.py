import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
from openai import OpenAI
import time
import signal_generator
import hashlib
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="📈 AI Investment Bot + Chat", layout="wide")
st.title("📈 AI Investment Bot with Signals & Chat")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    try:
        prices = pd.read_csv("stock_prices.csv", index_col=0, parse_dates=True)
    except FileNotFoundError:
        st.error("❌ stock_prices.csv not found. Run data_pipeline.py first.")
        st.stop()
    try:
        fundamentals = pd.read_csv("fundamental_data.csv")
    except FileNotFoundError:
        st.error("❌ fundamental_data.csv not found. Run fundamental_analyzer.py first.")
        st.stop()
    return prices, fundamentals

prices, fundamentals = load_data()

# HF Token

os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")


# Check if DB exists and CSV hasn't changed
csv_hash = hashlib.md5(open("stock_prices.csv", "rb").read()).hexdigest()
db_path = f"./stock_chat_db_{csv_hash[:8]}"


# Sidebar
st.sidebar.header("⚙️ Controls")
tickers = [col for col in prices.columns if col != 'Date']
selected_ticker = st.sidebar.selectbox("Select Stock", tickers)

# ---------- MAIN CONTENT ----------
col1, col2 = st.columns([2, 1])

with col1:
    # --- Signal Display ---
    signal, score, reasoning = signal_generator.get_signal(selected_ticker, prices, fundamentals)
    
    # Color coding
    if signal == "BUY":
        color = "green"
    elif signal == "SELL":
        color = "red"
    else:
        color = "orange"
    
    st.markdown(f"## 📊 Signal: :{color}[{signal}] (Score: {score}/4)")
    with st.expander("📝 Reasoning"):
        for point in reasoning:
            st.write(f"- {point}")
    
    # --- Price Chart ---
    st.subheader(f"📈 {selected_ticker} – Price History")
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(prices[selected_ticker], label=selected_ticker, color='blue', linewidth=2)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    st.pyplot(fig)

with col2:
    # --- Quick Stats ---
    current_price = prices[selected_ticker].iloc[-1]
    returns = prices[selected_ticker].pct_change().dropna()
    st.metric("💰 Current Price", f"${current_price:.2f}")
    st.metric("📈 Avg Return (Daily)", f"{returns.mean()*100:.2f}%")
    st.metric("📉 Volatility", f"{returns.std()*100:.2f}%")
    
    # --- Fundamentals ---
    st.subheader("📋 Fundamentals")
    fund_row = fundamentals[fundamentals['Ticker'] == selected_ticker]
    if not fund_row.empty:
        st.dataframe(fund_row.T, use_container_width=True)
    else:
        st.info("No fundamental data available. Run fundamental_analyzer.py.")

# ---------- AI CHATBOT (Instant, No RAG) ----------
st.divider()
st.subheader("🤖 AI Assistant (Ask about stocks)")

@st.cache_resource
def get_llm():
    return OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),  # <-- REPLACE WITH YOUR KEY
        base_url="https://api.deepseek.com/v1"
    )

llm = get_llm()

user_q = st.text_input("💬 Ask a question about these stocks (e.g., 'Which stock performed best in the last 30 days?'):")

if user_q:
    with st.spinner("Analyzing data..."):
        # Load price data (only last 100 days for speed)
        df = pd.read_csv("stock_prices.csv", index_col=0, parse_dates=True).tail(100)
        # Generate a summary for the LLM to work from
        summary = df.describe().round(2).to_string()
        
        prompt = f"""You are a stock analyst. Answer the user's question based ONLY on the data summary below.

Data summary (last 100 days):
{summary}

Question: {user_q}
Answer:"""
        
        resp = llm.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}]
        )
        st.success(resp.choices[0].message.content)

st.caption("💡 Tip: The signal is based on technical (RSI, SMA) + fundamental (P/E, Profit Margin) scoring.")