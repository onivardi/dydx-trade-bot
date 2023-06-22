from constants import ZSCORE_THRESH, USD_PER_TRADE, USD_MIN_COLLATERAL
from utils import format_number
from public_requests import get_candles_recent
from cointegration import calculate_zscore
from private_requests import is_open_positions
from bot_agent import BotAgent
import pandas as pd
import json

from pprint import pprint

# Open positions
def open_positions(client):

    """
        Manage finding triggers for trade entry
        Store trades managing later on exit function
    """

    # Load cointegrated pairs
    df = pd.read_csv("cointegrated_pairs.csv")

    # Get markets from referencing of min order size, tick size etc 
    markets = client.public.get_markets().data

    # Initialize container for BotAgent results
    bot_agents = []

    # Find ZScore triggers
    for index, row in df.iterrows():

        # Extract variables
        base_market = row["base_market"]
        quote_market = row["quote_market"]
        hedge_ratio = row["hedge_ratio"]
        half_life = row["half_life"]

        # Get prices
        series_1 = get_candles_recent(client, base_market)
        series_2 = get_candles_recent(client, quote_market)

        # Get ZScore
        if len(series_1) > 0 and len(series_1) == len(series_2):
            spread = series_1 - (hedge_ratio * series_2)
            z_score = calculate_zscore(spread).values.tolist()[-1]
            
            # Establish if potential trade
            if abs(z_score) >= ZSCORE_THRESH:

                # Ensure like-for-like not already open (diversify trading)
                is_base_open = is_open_positions(client, base_market)
                is_quote_open = is_open_positions(client, base_market)

                # Place trade
                if not is_base_open and not is_quote_open:

                    # Determine side
                    base_side = "BUY" if z_score < 0 else "SELL"
                    quote_side = "BUY" if z_score > 0 else "SELL"

                    # Get acceptable price in string format with correct number of decimals
                    base_price = series_1[-1]
                    quote_price = series_2[-1]
                    accept_base_price = float(base_price) * 1.01 if z_score < 0 else float(base_price) * 0.99
                    accept_quote_price = float(quote_price) * 1.01 if z_score > 0 else float(quote_price) * 0.99
                    failsafe_base_price = float(base_price) * 0.05 if z_score > 0 else float(base_price) * 1.7
                    base_tick_size = markets["markets"][base_market]["tickSize"]
                    quote_tick_size = markets["markets"][quote_market]["tickSize"]

                    # Format prices
                    accept_base_price = format_number(accept_base_price, base_tick_size)
                    accept_quote_price = format_number(accept_quote_price, quote_tick_size)
                    accept_failsafe_base_price = format_number(failsafe_base_price, base_tick_size)

                    # Get size
                    base_quantity = 1 / base_price * USD_PER_TRADE
                    quote_quantity = 1 / quote_price * USD_PER_TRADE
                    base_step_size = markets["markets"][base_market]["stepSize"]
                    quote_step_size = markets["markets"][quote_market]["stepSize"]

                    # Format sizes
                    base_size = format_number(base_quantity, base_step_size)
                    quote_size = format_number(quote_quantity, quote_step_size)

                    # Ensure size
                    base_min_order_size = markets["markets"][base_market]["minOrderSize"]
                    quote_min_order_size = markets["markets"][quote_market]["minOrderSize"]
                    check_base = float(base_quantity) > float(base_min_order_size)
                    check_quote = float(quote_quantity) > float(quote_min_order_size)

                    # if Check pass, place trades
                    if check_base and check_quote:

                        # Check account balance
                        account = client.private.get_account()
                        free_collateral = float(account.data["account"]["freeCollateral"])
                        print(f"Balance: {free_collateral} and minimum at {USD_MIN_COLLATERAL}")

                        # Guard: Ensure collateral
                        if free_collateral < USD_MIN_COLLATERAL:
                            break

                        # Create Bot 
                        print(base_market, base_side, base_size, accept_base_price)
                        print(quote_market, quote_side, quote_size, accept_quote_price)
                        exit(1)


