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
    "digital mode only"
    open_assets = IQ.get_all_open_time()
    open_assets = open_assets['digital'].keys()
    return list(open_assets)

