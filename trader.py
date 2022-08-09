"""
Module with all trade funcionalities
"""

from iqoptionapi.stable_api import IQ_Option

import CONSTANTS

IQ = IQ_Option(CONSTANTS.IQUSER, CONSTANTS.IQPASSWORD)


def connect_to_iq():
    IQ.connect()


def change_trade_type(trade_type):
    "PRACTICE/REAL"
    IQ.change_balance(trade_type)


def get_open_assets():
    "get only digital assets"
    open_assets = IQ.get_all_open_time()
    open_assets = open_assets['digital'].keys()
    return list(open_assets)


def get_asset_payout(asset):
    return IQ.get_digital_payout(asset)

