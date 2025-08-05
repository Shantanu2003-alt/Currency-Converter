# Currency-Converter
A real-time Currency Converter that lets you instantly convert between global currencies using live exchange rates. Simple, fast and smart - Get accurate conversions with symbols and style in a single click!
Try it out here: https://currency-converter0.streamlit.app/

A modern, minimal, and responsive Currency Converter app built using Streamlit.
Supports 100+ world currencies and features a cool Light/Dark theme toggle.

# Features
Real-time currency exchange rates via ExchangeRate-API
Convert between 100+ currencies
Toggle between Light and Dark modes
Responsive web UI powered by Streamlit
Caching for faster response and less API calls

# Tech Stack
Python 3.10+
Streamlit
Requests
HTML/CSS for custom styling

# How Currency Conversion works here
Behind the scenes, the app:
Fetches live exchange rates from ExchangeRate-API
Converts the entered amount from the source currency to the base (the USD here)
Then converts from USD to the target currency using real-time rates
This ensures accurate conversion using the most up-to-date market data.

# Live API Used
Fetches real-time exchange rates using a selected base currency.

# License
This project is licensed under the MIT License.
