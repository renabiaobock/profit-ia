import logging

import trader


logging.disable(level=(logging.DEBUG))

"Conect to IQ account"
trader.connect_to_iq()

"Change trade type"
trader.change_trade_type('PRACTICE')

