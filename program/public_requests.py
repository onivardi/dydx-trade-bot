from constants import RESOLUTION
from utils import get_ISO_times
import pandas as pd
import numpy as np
from pprint import pprint


# Get relevant time periods for ISO from and to
ISO_TIMES = get_ISO_times()

def get_candles_historical(client, market):
    
    # Define output
    close_prices = []

    # Extract historical price data for each timeframe
    for timeframe in ISO_TIMES.keys():

        # Confirm times needed
        tf_obj = ISO_TIMES[timeframe]
        from_iso = tf_obj["from_iso"]
        to_iso = tf_obj["to_iso"]

        # Protect API
        time.sleep(0.2)

        # Get data
        candles = client.public.get_candles(
            market=market,
            resolution=RESOLUTION,
            from_iso=from_iso,
            to_iso=to_iso,
            limit=100
        )

        # Structure data
        for candle in candles.data["candles"]:
            close_prices.append({ "datetime": candle["startedAt"], market: candle["close"] })

        # Construct and return DataFrame
        close_prices.reverse()
        return close_prices

# Construct market prices
def construct_market_prices(client):
    pass