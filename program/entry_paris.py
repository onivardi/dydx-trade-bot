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

    print(df)