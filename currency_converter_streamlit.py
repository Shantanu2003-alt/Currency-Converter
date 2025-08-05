import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="Currency Converter", layout="centered")

# Theme toggle
theme = st.radio("Choose Theme", ["Light", "Dark"], horizontal=True)

# Custom CSS based on selected theme
def set_theme(theme):
    if theme == "Dark":
        st.markdown("""
            <style>
                body {
                    background-color: #0e1117;
                    color: #ffffff;
                }
                .stApp {
                    background-color: #0e1117;
                }
                .stRadio > div {
                    background-color: #262730;
                    color: white;
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                body {
                    background-color: #ffffff;
                    color: #000000;
                }
                .stApp {
                    background-color: #ffffff;
                }
                .stRadio > div {
                    background-color: #f0f2f6;
                    color: black;
                }
            </style>
        """, unsafe_allow_html=True)

set_theme(theme)

# Title
st.title("💱 Currency Converter")

# Helper function to fetch exchange rates
@st.cache_data
def get_exchange_rates(base):
    url = f"https://api.exchangerate-api.com/v4/latest/{base}"
    response = requests.get(url)
    return response.json()

# Input section
base_currency = st.selectbox("From Currency", ["USD", "EUR", "GBP", "INR", "JPY", "CNY", "AUD", "CAD"])
target_currency = st.selectbox("To Currency", ["USD", "EUR", "GBP", "INR", "JPY", "CNY", "AUD", "CAD"])
amount = st.number_input("Amount", min_value=0.0, value=1.0, step=0.01)

# Fetch and convert
if st.button("Convert"):
    data = get_exchange_rates(base_currency)
    if target_currency in data['rates']:
        rate = data['rates'][target_currency]
        converted = rate * amount
        st.success(f"{amount:.2f} {base_currency} = {converted:.2f} {target_currency}")
    else:
        st.error("Currency not supported.")
