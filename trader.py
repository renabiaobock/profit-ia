"""
Module with all trade funcionalities
"""
from time import sleep
from datetime import datetime
from threading import Thread

from iqoptionapi.stable_api import IQ_Option

import CONSTANTS
import database

IQ = IQ_Option(CONSTANTS.IQUSER, CONSTANTS.IQPASSWORD)


asset_trade_count = {}


def connect_to_iq():
    IQ.connect()


def change_trade_type(trade_type):
    "PRACTICE/REAL"
    IQ.change_balance(trade_type)


def get_open_assets():
    "get only digital assets"
    assets_info = IQ.get_all_open_time()
    digital_assets_info = assets_info['digital']
    open_assets = []
    for asset in digital_assets_info:
        if digital_assets_info[asset]['open']:
            open_assets.append(asset)
    return open_assets


def get_asset_payout(asset):
    return IQ.get_digital_payout(asset)


def get_account_balance():
    return IQ.get_balance()


def get_stake_by_percentage_of_balance(percentage):
    return round((percentage/100) * get_account_balance(), 2)


def increase_asset_trade_count(asset):
    asset_trade_count[asset] = asset_trade_count[asset] + 1


def decrease_asset_trade_count(asset):
    asset_trade_count[asset] = asset_trade_count[asset] - 1


def reached_limit_of_simultaneous_trades(max_simultaneous_trades, asset):
    if not asset in asset_trade_count:
        asset_trade_count[asset] = 0
    if asset_trade_count[asset] >= max_simultaneous_trades:
        return True
    else:
        return False


def buy(asset, timeframe_in_minutes, stake, action):
    if not reached_limit_of_simultaneous_trades(1, asset):
        check, entry_id = IQ.buy_digital_spot(asset, stake, action, timeframe_in_minutes)
        if check:
            increase_asset_trade_count(asset)
            date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            payout = get_asset_payout(asset)
            database.insert_new_entry_on_database(str(entry_id), date_time, CONSTANTS.TRADETYPE, asset, payout, stake)
    else:
        check, entry_id = False, 0
    return check, entry_id


def get_trade_result(entry_id):
    return IQ.check_win_digital_v2(entry_id)


def buy_and_wait_for_result(asset, timeframe_in_minutes, stake, action):
    check, entry_id = buy(asset, timeframe_in_minutes, stake, action)
    if check:
        while not get_trade_result(entry_id)[0]:
            sleep(1)
        profit = round(get_trade_result(entry_id)[1], 2)
        decrease_asset_trade_count(asset)
        if profit < 0:
            result = 'loss'
        elif profit > 0:
            result = 'win'
        elif profit == 0:
            result = 'tie'
        database.update_entry_result_and_profit(entry_id, result, profit)
    else:
        result, profit = None, None
    return result, profit


def buy_and_wait_for_result_as_thread(asset, timeframe_in_minutes, stake, action):
    buy_thread = Thread(target=buy_and_wait_for_result, args=(asset, timeframe_in_minutes, stake, action))
    buy_thread.start()


def subscribe_to_candle_stream(asset, timeframe_in_minutes, n_candles):
    timeframe_in_seconds = timeframe_in_minutes * 60
    IQ.start_candles_stream(asset, timeframe_in_seconds, n_candles)


def get_real_time_candles(asset, timeframe_in_minutes):
    "get real time candles need an active subscription to the candle stream"
    timeframe_in_seconds = timeframe_in_minutes * 60
    return IQ.get_realtime_candles(asset, timeframe_in_seconds)

