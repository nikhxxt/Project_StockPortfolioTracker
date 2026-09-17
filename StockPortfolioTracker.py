import streamlit as st

API_KEY = st.secrets["ALPHA_VANTAGE_API_KEY"]

class Portfolio:
    def __init__(self):
      self.holdings = {}
    
    def add_stock(self, symbol, shares, price_per_share):
        if symbol in self.holdings:
            self.holdings[symbol]['shares'] += shares
            self.update_cost_basis(symbol, price_per_share)
        else:
             self.holdings[symbol] = {'shares' : shares, 'cost_basis' : price_per_share}
                                      
    def remove_stock(self, symbol, shares):
          if symbol in self.holdings:
              if shares >= self.holdings[symbol]['shares']:
                  del self.holdings[symbol]
              else:
                  self.holdings[symbol]['shares'] -=shares

    def update_cost_basis(self, symbol, price):
          if symbol in self.holdings:
              current_shares = self.holdings[symbol]['shares']
              current_cost = self.holdings[symbol]['cost_basis'] * current_shares
              new_cost = current_cost + (price * current_shares)
              self.holdings[symbol]['cost_basis'] = new_cost / current_shares

    def portfolio_value(self):
       total_value = 0.0
       for symbol, data in self.holdings.items():
           price = self.get_stock_quote(symbol)
           total_value += price * data['shares']
       return total_value

    def get_stock_quote(self, symbol):
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
        try:
            response = requests.get(url)
            data = response.json()
            return float(data['Global Quote']['05. price'])
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return 0.0

    def print_portfolio(self):
        print("\n=== Current Portfolio ===")
        for symbol, data in self.holdings.items():
            price = self.get_stock_quote(symbol)
            current_value = price *data['shares']
            print(f"{symbol}: Shares={data['shares']}, Cost Basis=${data['cost_basis']:.2f}, Cureent price=${price:.2f}, Cureent Value=${current_value:.2f}")
        total_value = self.portfolio_value()
        print(f"Total Portfolio Value: ${total_value:.2f}")


def main():
    portfolio = Portfolio()

    while True:
        print("\nMenu:")
        print("1. Add stock")
        print("2. Remove stock")
        print("3. View portfolio")
        print("4. Exit")
        
        choice = input("Enter your choice:")
        
        if choice == '1':
            symbol    = input("Enter stock symbol:").upper()
            shares = int(input("Enter number of shares: "))
            price = float(input("Enter price per share: "))
            portfolio.add_stock(symbol, shares, price)
            print(f"Added {shares} share of {symbol} at ${price:.2f} each.")

        elif choice == '2':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares to remove: "))
            portfolio.remove_stock(symbol, shares)
            print(f"Removed {shares} shares of {symbol}.")

        elif choice == '3':
             portfolio.print_portfolio()

        elif choice == '4':
           print("Exiting.")
           break

        else:
              print("invalid choice. Please enter a number between 1 and 4.")
             
if __name__ =="__main__":
    main()

                
        
           

        
