import streamlit as st
import requests

API_KEY = st.secrets["ALPHA_VANTAGE_API_KEY"]


class Portfolio:
    def __init__(self):
        self.holdings = {}

    def add_stock(self, symbol, shares, price_per_share):
        if symbol in self.holdings:
            old_shares = self.holdings[symbol]["shares"]
            old_cost = self.holdings[symbol]["cost_basis"]

            total_cost = (old_shares * old_cost) + (shares * price_per_share)
            total_shares = old_shares + shares

            self.holdings[symbol]["shares"] = total_shares
            self.holdings[symbol]["cost_basis"] = total_cost / total_shares

        else:
            self.holdings[symbol] = {
                "shares": shares,
                "cost_basis": price_per_share
            }

    def remove_stock(self, symbol, shares):
        if symbol in self.holdings:
            if shares >= self.holdings[symbol]["shares"]:
                del self.holdings[symbol]
            else:
                self.holdings[symbol]["shares"] -= shares

    def get_stock_quote(self, symbol):
        url = (
            "https://www.alphavantage.co/query"
            f"?function=GLOBAL_QUOTE"
            f"&symbol={symbol}"
            f"&apikey={API_KEY}"
        )

        try:
            response = requests.get(url, timeout=10)
            data = response.json()

            quote = data.get("Global Quote", {})
            price = quote.get("05. price")

            if price:
                return float(price)

            return None

        except Exception:
            return None


# Page configuration
st.set_page_config(
    page_title="Stock Portfolio Tracker",
    page_icon="📈"
)

st.title("📈 Stock Portfolio Tracker")
st.write("Track your stocks and calculate your portfolio value.")


# Store portfolio during the session
if "portfolio" not in st.session_state:
    st.session_state.portfolio = Portfolio()

portfolio = st.session_state.portfolio


# Add stock
st.header("➕ Add Stock")

symbol = st.text_input(
    "Stock Symbol",
    placeholder="Example: IBM"
).upper()

shares = st.number_input(
    "Number of Shares",
    min_value=1,
    step=1
)

price = st.number_input(
    "Purchase Price Per Share ($)",
    min_value=0.01,
    step=0.01
)

if st.button("Add Stock"):
    if symbol == "":
        st.warning("Please enter a stock symbol.")
    else:
        portfolio.add_stock(symbol, shares, price)
        st.success(
            f"Added {shares} shares of {symbol}."
        )


# Remove stock
st.header("➖ Remove Stock")

remove_symbol = st.text_input(
    "Stock Symbol to Remove",
    placeholder="Example: IBM"
).upper()

remove_shares = st.number_input(
    "Number of Shares to Remove",
    min_value=1,
    step=1
)

if st.button("Remove Stock"):
    if remove_symbol not in portfolio.holdings:
        st.warning("Stock not found in your portfolio.")

    elif remove_shares > portfolio.holdings[remove_symbol]["shares"]:
        st.warning("You cannot remove more shares than you own.")

    else:
        portfolio.remove_stock(remove_symbol, remove_shares)
        st.success(
            f"Removed {remove_shares} shares of {remove_symbol}."
        )


# View portfolio
st.header("📊 Current Portfolio")

if portfolio.holdings:

    for symbol, data in portfolio.holdings.items():

        current_price = portfolio.get_stock_quote(symbol)

        if current_price is not None:
            current_value = current_price * data["shares"]

            st.write(f"### {symbol}")
            st.write(f"Shares: {data['shares']}")
            st.write(
                f"Average Cost: ${data['cost_basis']:.2f}"
            )
            st.write(
                f"Current Price: ${current_price:.2f}"
            )
            st.write(
                f"Current Value: ${current_value:.2f}"
            )

            st.divider()

        else:
            st.warning(
                f"Could not fetch the current price for {symbol}."
            )

else:
    st.info("Your portfolio is empty. Add a stock to get started.")


# Clear portfolio
if st.button("🔄 Clear Portfolio"):
    st.session_state.portfolio = Portfolio()
    st.rerun()

                
        
           

        
