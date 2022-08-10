import logging

import CONSTANTS
import trader
import indicators


logging.disable(level=(logging.DEBUG))

"Conect to IQ account"
trader.connect_to_iq()

"Change trade type"
trader.change_trade_type(CONSTANTS.TRADETYPE)

