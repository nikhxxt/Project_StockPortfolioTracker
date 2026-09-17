# 📈 Stock Portfolio Tracker

A simple and interactive **Stock Portfolio Tracker** built using **Python and Streamlit**.

The application allows users to add and remove stocks, track the number of shares, record purchase prices, and view current market prices and portfolio values using the **Alpha Vantage API**.

## 🌐 Live Demo

👉 [Stock Portfolio Tracker · Streamlit](https://projectstockportfoliotracker-womclutid84ovm9yb6cappj.streamlit.app/)

## ✨ Features

- 📈 Add stocks to your portfolio
- ➖ Remove stocks from your portfolio
- 🔢 Track the number of shares
- 💰 Record purchase price per share
- 📊 Calculate average cost basis
- 💵 Fetch current stock prices using Alpha Vantage
- ✅ Validate stock ticker symbols before adding them
- ❌ Display an error for invalid or unavailable symbols
- 📋 View current portfolio details
- 🔄 Clear the portfolio and start again
- 🌐 Interactive Streamlit web interface

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **Requests**
- **Alpha Vantage API**

## 🧠 How It Works

1. Enter a valid stock ticker symbol, such as `AAPL`, `GOOGL`, `META`, or `IBM`.
2. Enter the number of shares.
3. Enter the purchase price per share.
4. Click **Add Stock**.
5. The application validates the stock symbol using Alpha Vantage.
6. Valid stocks are added to the portfolio.
7. The application retrieves the current market price.
8. The current value of each holding is calculated.
9. Users can remove shares or clear the entire portfolio.

## 📊 Portfolio Information

For each stock, the application displays:

- **Stock Symbol**
- **Number of Shares**
- **Average Cost**
- **Current Market Price**
- **Current Holding Value**

The total portfolio value is also calculated from the current market prices.

## 🔍 Stock Symbol Validation

The application checks whether the entered ticker symbol is recognized by the Alpha Vantage API before adding it to the portfolio.

For example:

```text
GOOGL → Valid
META  → Valid
AAPL  → Valid
IBM   → Valid
GOOGLE → Invalid ticker symbol
