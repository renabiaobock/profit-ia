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

open_assets = trader.get_open_assets()


for asset in open_assets:
    trader.subscribe_to_candle_stream(asset, CONSTANTS.TIMEFRAME, 200)

while True:
    for asset in open_assets:
        direction = strategy.check_entry_BOLLINGER_BANDS_EMA(asset, CONSTANTS.TIMEFRAME,
                                                             CONSTANTS.BB_PERIOD,
                                                             CONSTANTS.BB_DEV_UP,
                                                             CONSTANTS.BB_DEV_DOWN,
                                                             CONSTANTS.EMA)
        if direction and asset not in trader.trading_assets:
            trader.trading_assets.append(asset)
            stake = trader.get_stake_by_percentage_of_balance(1)
            trader.buy_and_wait_for_result_as_thread(asset, CONSTANTS.TIMEFRAME, stake, direction)
    time.sleep(0.2)

