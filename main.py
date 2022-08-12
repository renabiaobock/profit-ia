import logging
import time
import schedule

import CONSTANTS
import trader
import strategy


def check_connection_and_update_open_assets():
    "check conection"
    if not trader.IQ.check_connect:
        trader.connect_to_iq()
    if trader.IQ.check_connect():
        "update open assets"
        open_assets = trader.get_open_assets()
        for asset in open_assets:
            trader.subscribe_to_candle_stream(asset, CONSTANTS.TIMEFRAME, 200)


#1: Conect to IQ account and update open assets"
trader.connect_to_iq()
open_assets = trader.get_open_assets()
for asset in open_assets:
    trader.subscribe_to_candle_stream(asset, CONSTANTS.TIMEFRAME, 200)

#2: Change trade type
trader.change_trade_type(CONSTANTS.TRADETYPE)

#3: Create scheduler to check conection and update open assets every 1 minute
schedule.every().minute.at(':10').do(check_connection_and_update_open_assets)

#4: Start trading loop
while True:
    schedule.run_pending()
    for asset in open_assets:
        direction = strategy.check_entry_BOLLINGER_BANDS_EMA(asset, CONSTANTS.TIMEFRAME,
                                                             CONSTANTS.BB_PERIOD,
                                                             CONSTANTS.BB_DEV_UP,
                                                             CONSTANTS.BB_DEV_DOWN,
                                                             CONSTANTS.EMA)
        if direction and asset not in trader.trading_assets:
            trader.trading_assets.append(asset)
            stake = trader.get_stake_by_percentage_of_balance(CONSTANTS.STAKE_PERCENTAGE)
            trader.buy_and_wait_for_result_as_thread(asset, CONSTANTS.TIMEFRAME, stake, direction)
    time.sleep(0.2)

