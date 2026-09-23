# 📈 Stock Portfolio Tracker

A **Streamlit-based stock portfolio tracking application** that allows users to manage holdings, calculate cost basis, and retrieve current market prices through the Alpha Vantage API.

## ✨ Features

* Add and remove stock holdings
* Track shares and purchase prices
* Calculate average cost basis
* Validate stock ticker symbols
* Fetch current market prices
* Calculate individual holding values
* Calculate total portfolio value
* Interactive web interface using Streamlit

## 🛠️ Tech Stack

**Python · Streamlit · Requests · Alpha Vantage API**

## 🔄 How It Works

```text
User
  │
  ▼
Streamlit Interface
  │
  ├── Add / Remove Holdings
  ├── Track Shares & Purchase Price
  └── Calculate Portfolio Metrics
          │
          ▼
    Alpha Vantage API
          │
          ▼
    Current Market Price
```

The application combines user-entered portfolio data with market prices retrieved from Alpha Vantage to calculate current portfolio values.

## 🌐 Live Demo

**Try the application:**
https://projectstockportfoliotracker-womclutid84ovm9yb6cappj.streamlit.app/

## 🚀 Run Locally

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run StockPortfolioTracker.py
```

The application will open in your browser at the local Streamlit address.

## 📁 Project Structure

```text
stock-portfolio-tracker/
├── StockPortfolioTracker.py
├── requirements.txt
├── output with code.jpeg
└── README.md
```

## ⚙️ API Configuration

The application uses the **Alpha Vantage API** to retrieve market data.

Store the API key securely rather than committing it directly to the repository.

Example:

```text
ALPHA_VANTAGE_API_KEY=your_api_key
```

