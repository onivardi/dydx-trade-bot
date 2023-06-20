from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED
from connections import connect_dydx
from private_requests import abort_all_positions
from public_requests import construct_market_prices

if __name__ == "__main__":
    
    # Connect to client
    try:
        print("Connection to Client...")
        client = connect_dydx()
    except Exception as e:
        print("Error, connection to client: ", e)
        exit(1)

    # Abort all open positions
    if ABORT_ALL_POSITIONS:
        try:
            print("Closing all position...")
            close_orders = abort_all_positions(client)
        except Exception as e:
            print("Error, closing all positions: ", e)
            exit(1)
    
    # Find Cointegrated Pairs
    if FIND_COINTEGRATED:

        # Construct Market Prices
        try:
            print("Fetching market prices, please allow 3 mins...")
            df_market_price = construct_market_prices(client)
        except Exception as e:
            print("Error, constructing market prices: ", e)
            exit(1)