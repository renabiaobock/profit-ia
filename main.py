import logging

import CONSTANTS
import trader


logging.disable(level=(logging.DEBUG))

"1: Conect to IQ account"
trader.connect_to_iq()

"2: Change trade type"
trader.change_trade_type(CONSTANTS.TRADETYPE)

