import streamlit as st
import pandas as pd
import requests
import datetime
import plotly.express as px

st.set_page_config(page_title="GIZA Token Dashboard", layout="wide")
st.title("📊 GIZA Token Economy Dashboard")

@st.cache_data(ttl=3600)
def fetch_giza_data():
    url = "https://api.coingecko.com/api/v3/coins/giza"
    res = requests.get(url).json()
    market_data = res["market_data"]
    
    data = {
        "Price (USD)": market_data["current_price"]["usd"],
        "Market Cap (USD)": market_data["market_cap"]["usd"],
        "Volume 24h (USD)": market_data["total_volume"]["usd"],
        "Circulating Supply": market_data["circulating_supply"],
        "Total Supply": market_data["total_supply"],
        "Max Supply": market_data.get("max_supply", "N/A"),
        "Volume / Market Cap": round(market_data["total_volume"]["usd"] / market_data["market_cap"]["usd"], 4)
    }
    return data, res["market_data"]

with st.spinner("Fetching GIZA data..."):
    giza_data, _ = fetch_giza_data()

st.subheader("💡 Key Token Metrics")
st.dataframe(pd.DataFrame(giza_data.items(), columns=["Metric", "Value"]))

# Historical chart
def fetch_price_chart(days=90):
    url = f"https://api.coingecko.com/api/v3/coins/giza/market_chart?vs_currency=usd&days={days}"
    res = requests.get(url).json()
    prices = res["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

st.subheader("📈 Historical Price (90 Days)")
price_df = fetch_price_chart()
fig = px.line(price_df, x="date", y="price", title="GIZA Price in USD")
st.plotly_chart(fig, use_container_width=True)

st.subheader("🧬 Token Distribution (Top Holders)")
st.markdown("[View on Etherscan](https://etherscan.io/token/0xYourTokenAddress)")  # replace with real address
