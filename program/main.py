from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADERS
from connections import connect_dydx
from private_requests import abort_all_positions
from cointegration import store_cointegration_results
from entry_paris import open_positions
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

        
         # Store Cointegrated Pairs
        try:
            print("Storing Cointegrated pairs...")
            stores_result = store_cointegration_results(df_market_price)
            if stores_result != "saved":
                print("Error, saving cointegrated pairs")
                exit(1)
        except Exception as e:
            print("Error, saving cointegrated pairs: ", e)
            exit(1)


        

    # Place trades for opening positions
    if PLACE_TRADERS:
        try:
            print("Finding trading opportunities...")
            open_positions(client)
        except Exception as e:
            print("Error, Trading pairs: ", e)
            exit(1)