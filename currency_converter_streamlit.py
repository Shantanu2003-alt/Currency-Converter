import streamlit as st
import requests
import datetime
import matplotlib.pyplot as plt

# ---------------------------- CONFIG ----------------------------
st.set_page_config(page_title="💱 Currency Converter with Trend Chart")

API_URL = "https://api.exchangerate.host"


# ---------------------------- API FUNCTIONS ----------------------------

@st.cache_data(ttl=600)
def get_symbols():
    url = f"{API_URL}/symbols"
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"Failed to fetch currency symbols. Status code: {response.status_code}")
        return {}

    data = response.json()
    if "symbols" not in data:
        st.error(f"Unexpected response from API: {data}")
        return {}

    return data["symbols"]

@st.cache_data(ttl=600)
def get_conversion(from_currency, to_currency, amount):
    url = f"{API_URL}/convert"
    params = {"from": from_currency, "to": to_currency, "amount": amount}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        st.error(f"Conversion failed. Status: {response.status_code}")
        return None

    data = response.json()
    return data.get("result", None)

@st.cache_data(ttl=600)
def get_historical_rates(from_currency, to_currency, days=30):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days)
    url = f"{API_URL}/timeseries"
    params = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "base": from_currency,
        "symbols": to_currency
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        st.error(f"Failed to fetch historical data. Status: {response.status_code}")
        return {}

    data = response.json()
    if "rates" not in data:
        st.error(f"Unexpected format for historical data: {data}")
        return {}

    return data["rates"]


# ---------------------------- APP UI ----------------------------

st.title("💱 Currency Converter with Trend Chart")
st.markdown("Convert currencies using live exchange rates and visualize trends over time.")

symbols = get_symbols()
if not symbols:
    st.stop()

symbol_names = [f"{code} - {symbols[code]['description']}" for code in symbols]
code_map = {f"{code} - {symbols[code]['description']}": code for code in symbols}

col1, col2 = st.columns(2)
with col1:
    from_display = st.selectbox("From Currency", symbol_names, index=symbol_names.index("USD - United States Dollar"))
with col2:
    to_display = st.selectbox("To Currency", symbol_names, index=symbol_names.index("INR - Indian Rupee"))

from_currency = code_map[from_display]
to_currency = code_map[to_display]

amount = st.number_input("Amount", min_value=0.0, value=100.0, step=1.0)

# Conversion
if st.button("Convert"):
    result = get_conversion(from_currency, to_currency, amount)
    if result is not None:
        st.success(f"**{amount:,.2f} {from_currency} = {result:,.2f} {to_currency}**")
    else:
        st.error("Conversion failed.")

# Chart
st.subheader("📈 Historical Exchange Rate Trend")
days = st.slider("Select number of past days", min_value=7, max_value=90, value=30)

historical = get_historical_rates(from_currency, to_currency, days)

if historical:
    dates = sorted(historical.keys())
    rates = [historical[date][to_currency] for date in dates]

    plt.figure(figsize=(10, 4))
    plt.plot(dates, rates, marker='o')
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel(f"Rate ({from_currency} → {to_currency})")
    plt.title("Exchange Rate Trend")
    st.pyplot(plt)
