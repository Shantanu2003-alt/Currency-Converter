import requests
import streamlit as st

# -------------------- Currency Symbols Dictionary --------------------
currency_symbols = {
    'USD': '$',
    'INR': '₹',
    'EUR': '€',
    'GBP': '£',
    'JPY': '¥',
    'AUD': 'A$',
    'CAD': 'C$',
    'CNY': '¥',
    'CHF': 'CHF',
    'SEK': 'kr',
    'NZD': 'NZ$'
}

# -------------------- Function to Get Exchange Rates --------------------
@st.cache_data
def get_exchange_rates():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    if response.status_code != 200:
        st.error("Error fetching data from API.")
        return None
    return response.json()

# -------------------- Function to Convert Currency --------------------
def convert_currency(amount, from_currency, to_currency, rates):
    if from_currency == to_currency:
        return amount

    base_amount = amount / rates['rates'][from_currency]
    converted_amount = base_amount * rates['rates'][to_currency]
    return converted_amount

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="Currency Converter", page_icon="💱", layout="centered")
st.title("💱 Currency Converter")
st.markdown("Convert from one currency to another using live exchange rates.")

# Get rates
rates = get_exchange_rates()
if not rates:
    st.stop()

currency_list = list(rates['rates'].keys())

# Input fields
amount = st.number_input("Amount", min_value=0.0, value=100.0, step=1.0)
from_currency = st.selectbox("From Currency", currency_list, index=currency_list.index("USD"))
to_currency = st.selectbox("To Currency", currency_list, index=currency_list.index("INR"))

# Convert button
if st.button("Convert"):
    try:
        result = convert_currency(amount, from_currency, to_currency, rates)
        from_symbol = currency_symbols.get(from_currency, '')
        to_symbol = currency_symbols.get(to_currency, '')

        st.success(
            f"{from_symbol}{amount:,.2f} {from_currency} = {to_symbol}{result:,.2f} {to_currency}"
        )
    except KeyError:
        st.error("Invalid currency code.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
