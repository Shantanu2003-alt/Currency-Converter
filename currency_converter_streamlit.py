import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# ----------------------------
# Title
# ----------------------------
st.set_page_config(page_title="Currency Converter", layout="centered")
st.title("💱 Currency Converter with Trend Chart")

# ----------------------------
# Theme toggle
# ----------------------------
dark_mode = st.toggle("🌙 Dark Mode", value=False)
if dark_mode:
    st.markdown(
        """
        <style>
            body { background-color: #0e1117; color: white; }
            .stApp { background-color: #0e1117; color: white; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ----------------------------
# Helper functions
# ----------------------------
@st.cache_data(ttl=3600)
def get_symbols():
    url = "https://api.exchangerate.host/symbols"
    response = requests.get(url)
    return response.json()["symbols"]

@st.cache_data(ttl=600)
def get_conversion(from_currency, to_currency, amount):
    url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
    response = requests.get(url)
    return response.json()

@st.cache_data(ttl=3600)
def get_historical_data(from_currency, to_currency, days=30):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    url = f"https://api.exchangerate.host/timeseries?start_date={start_date}&end_date={end_date}&base={from_currency}&symbols={to_currency}"
    response = requests.get(url)
    data = response.json()["rates"]
    df = pd.DataFrame(data).T
    df.index = pd.to_datetime(df.index)
    df.columns = [to_currency]
    return df

# ----------------------------
# Currency Selection
# ----------------------------
symbols = get_symbols()
symbol_names = [f"{code} - {symbols[code]['description']}" for code in symbols]
code_map = {f"{code} - {symbols[code]['description']}": code for code in symbols}

from_selection = st.selectbox("From Currency", symbol_names, index=symbol_names.index("USD - United States Dollar"))
to_selection = st.selectbox("To Currency", symbol_names, index=symbol_names.index("INR - Indian Rupee"))
from_currency = code_map[from_selection]
to_currency = code_map[to_selection]

amount = st.number_input("Enter amount to convert", min_value=0.0, value=1.0, step=0.1)

# ----------------------------
# Perform Conversion
# ----------------------------
if st.button("Convert"):
    result = get_conversion(from_currency, to_currency, amount)
    converted_amount = result["result"]
    rate = result["info"]["rate"]
    st.success(f"{amount} {from_currency} = {converted_amount:.4f} {to_currency}")
    st.caption(f"Exchange Rate: 1 {from_currency} = {rate:.4f} {to_currency}")

    # ----------------------------
    # Show Historical Trend
    # ----------------------------
    with st.spinner("Fetching 30-day historical data..."):
        hist_df = get_historical_data(from_currency, to_currency)
        fig = px.line(hist_df, y=to_currency, title=f"30-Day Exchange Rate: {from_currency} → {to_currency}")
        st.plotly_chart(fig, use_container_width=True)

