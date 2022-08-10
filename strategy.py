"""
Module that check for entries based on some strategy
"""

import indicators

def check_entry_BOLLINGER_BANDS_EMA(asset, timeframe_in_minutes,
                                    BB_time_period, BB_dev_up, BB_dev_down):
    price = indicators.generate_candle_data_from_candle_stream(asset, timeframe_in_minutes)['close'][-1]
    #Bollinger
    bollinger_bands = indicators.calculate_asset_BB(asset, timeframe_in_minutes,
                                                    BB_time_period, BB_dev_up, BB_dev_down)
    bollinger_bands_last_upper = bollinger_bands['upper'][-1]
    bollinger_bands_last_lower = bollinger_bands['lower'][-2]
    # Strategy logic
    if price > bollinger_bands_last_upper:
        return 'put'
    elif price < bollinger_bands_last_lower:
        return 'call'
    else:
        return None

