import logging
import time

import CONSTANTS
import trader
import strategy


logging.disable(level=(logging.DEBUG))

"1: Conect to IQ account"
trader.connect_to_iq()

"2: Change trade type"
trader.change_trade_type(CONSTANTS.TRADETYPE)

timeframe = 5
open_assets = trader.get_open_assets()


for asset in open_assets:
    trader.subscribe_to_candle_stream(asset, timeframe, 200)
while True:
    for asset in open_assets:
        direction = strategy.check_entry_BOLLINGER_BANDS_EMA(asset, timeframe,
                                                             CONSTANTS.BB_PERIOD,
                                                             CONSTANTS.BB_DEV_UP,
                                                             CONSTANTS.BB_DEV_DOWN,
                                                             EMA_time_period)
        if direction and asset not in trader.trading_assets:
            trader.trading_assets.append(asset)
            trader.buy_and_wait_for_result_as_thread(asset, timeframe, 10, direction)
    time.sleep(0.2)

