import streamlit as st
import requests


# ==============================
# API KEY
# ==============================

API_KEY = st.secrets["ALPHA_VANTAGE_API_KEY"]


# ==============================
# GET STOCK PRICE / VALIDATE SYMBOL
# ==============================

@st.cache_data(ttl=300)
def get_stock_price(symbol):

    url = (
        "https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE"
        f"&symbol={symbol}"
        f"&apikey={API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        # Check if Alpha Vantage returned a quote
        quote = data.get("Global Quote", {})

        # No quote = invalid/unavailable symbol
        if not quote:
            return None

        price = quote.get("05. price")

        if price:
            return float(price)

        return None

    except Exception:
        return None


# ==============================
# PORTFOLIO CLASS
# ==============================

class Portfolio:

    def __init__(self):
        self.holdings = {}

    # --------------------------
    # ADD STOCK
    # --------------------------

    def add_stock(self, symbol, shares, price_per_share):

        if symbol in self.holdings:

            old_shares = self.holdings[symbol]["shares"]
            old_cost = self.holdings[symbol]["cost_basis"]

            total_cost = (
                old_shares * old_cost
                + shares * price_per_share
            )

            total_shares = old_shares + shares

            self.holdings[symbol]["shares"] = total_shares

            self.holdings[symbol]["cost_basis"] = (
                total_cost / total_shares
            )

        else:

            self.holdings[symbol] = {
                "shares": shares,
                "cost_basis": price_per_share
            }

    # --------------------------
    # REMOVE STOCK
    # --------------------------

    def remove_stock(self, symbol, shares):

        if symbol in self.holdings:

            current_shares = self.holdings[symbol]["shares"]

            if shares >= current_shares:

                del self.holdings[symbol]

            else:

                self.holdings[symbol]["shares"] -= shares

    # --------------------------
    # GET CURRENT PRICE
    # --------------------------

    def get_stock_quote(self, symbol):

        return get_stock_price(symbol)


# ==============================
# STREAMLIT PAGE
# ==============================

st.set_page_config(
    page_title="Stock Portfolio Tracker",
    page_icon="📈",
    layout="centered"
)


st.title("📈 Stock Portfolio Tracker")

st.write(
    "Track your stocks, shares, purchase prices, "
    "and current market value."
)


# ==============================
# SESSION STATE
# ==============================

if "portfolio" not in st.session_state:

    st.session_state.portfolio = Portfolio()


portfolio = st.session_state.portfolio


# ==============================
# ADD STOCK
# ==============================

st.header("➕ Add Stock")


with st.form("add_stock_form"):

    symbol = st.text_input(
        "Stock Symbol",
        placeholder="Example: IBM, GOOGL, META, AAPL"
    ).strip().upper()

    shares = st.number_input(
        "Number of Shares",
        min_value=1,
        value=1,
        step=1
    )

    price = st.number_input(
        "Purchase Price Per Share ($)",
        min_value=0.01,
        value=100.00,
        step=0.01
    )

    add_button = st.form_submit_button(
        "Add Stock"
    )


if add_button:

    if symbol == "":

        st.warning(
            "Please enter a stock symbol."
        )

    else:

        # Validate stock symbol before adding
        current_price = get_stock_price(symbol)

        if current_price is None:

            st.error(
                f"❌ Invalid or unavailable stock symbol: {symbol}"
            )

            st.info(
                "Please enter a valid ticker symbol, "
                "such as AAPL, GOOGL, META, MSFT, IBM, "
                "AMZN, TSLA, or NVDA."
            )

        else:

            portfolio.add_stock(
                symbol,
                shares,
                price
            )

            st.success(
                f"✅ Added {shares} shares of "
                f"{symbol}."
            )


# ==============================
# REMOVE STOCK
# ==============================

st.header("➖ Remove Stock")


with st.form("remove_stock_form"):

    remove_symbol = st.text_input(
        "Stock Symbol",
        placeholder="Example: IBM"
    ).strip().upper()

    remove_shares = st.number_input(
        "Number of Shares to Remove",
        min_value=1,
        value=1,
        step=1
    )

    remove_button = st.form_submit_button(
        "Remove Stock"
    )


if remove_button:

    if remove_symbol == "":

        st.warning(
            "Please enter a stock symbol."
        )

    elif remove_symbol not in portfolio.holdings:

        st.warning(
            "Stock not found in your portfolio."
        )

    elif (
        remove_shares
        > portfolio.holdings[remove_symbol]["shares"]
    ):

        st.warning(
            "You cannot remove more shares "
            "than you own."
        )

    else:

        portfolio.remove_stock(
            remove_symbol,
            remove_shares
        )

        st.success(
            f"✅ Removed {remove_shares} shares "
            f"of {remove_symbol}."
        )


# ==============================
# CURRENT PORTFOLIO
# ==============================

st.header("📊 Current Portfolio")


if portfolio.holdings:

    total_portfolio_value = 0.0

    for symbol, data in portfolio.holdings.items():

        st.subheader(symbol)

        st.write(
            f"**Shares:** {data['shares']}"
        )

        st.write(
            f"**Average Cost:** "
            f"${data['cost_basis']:.2f}"
        )

        # Get current market price
        current_price = portfolio.get_stock_quote(
            symbol
        )

        if current_price is not None:

            current_value = (
                current_price
                * data["shares"]
            )

            total_portfolio_value += current_value

            st.write(
                f"**Current Price:** "
                f"${current_price:.2f}"
            )

            st.write(
                f"**Current Value:** "
                f"${current_value:,.2f}"
            )

        else:

            st.warning(
                f"⚠️ Current price unavailable "
                f"for {symbol}."
            )

        st.divider()


    # Total value

    st.subheader(
        f"💰 Total Portfolio Value: "
        f"${total_portfolio_value:,.2f}"
    )


else:

    st.info(
        "Your portfolio is empty. "
        "Add a stock to get started."
    )


# ==============================
# CLEAR PORTFOLIO
# ==============================

st.header("⚙️ Portfolio Settings")


if st.button("🔄 Clear Portfolio"):

    st.session_state.portfolio = Portfolio()

    st.success(
        "Portfolio cleared successfully."
    )

    st.rerun()
