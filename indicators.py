"""
Module that calculate indicators from candle data
"""

import time
import numpy as np
from talib.abstract import (EMA)

import trader


def generate_candle_data_from_candle_stream(asset, timeframe_in_minutes):
    candles=trader.get_real_time_candles(asset, timeframe_in_minutes)

    candle_data = {
        'open': np.array([]),
        'high': np.array([]),
        'low': np.array([]),
        'close': np.array([]),
        'volume': np.array([])
    }

    for timestamp in candles:
        candle_data["open"] = np.append(candle_data["open"], candles[timestamp]["open"])
        candle_data["high"] = np.append(candle_data["high"], candles[timestamp]["max"])
        candle_data["low"] = np.append(candle_data["low"], candles[timestamp]["min"])
        candle_data["close"] = np.append(candle_data["close"], candles[timestamp]["close"])
        candle_data["volume"] = np.append(candle_data["volume"], candles[timestamp]["volume"])
    return candle_data


def calculate_EMA(candle_data, EMA_time_period):
    return EMA(candle_data, timeperiod=EMA_time_period)


def calculate_asset_EMA(asset, timeframe_in_minutes, EMA_time_period):
    candle_data = generate_candle_data_from_candle_stream(asset, timeframe_in_minutes)
    return calculate_EMA(candle_data, EMA_time_period)

