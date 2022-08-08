from iqoptionapi.stable_api import IQ_Option
import logging


logging.disable(level=(logging.DEBUG))

IQ = IQ_Option('aquila.mitra@gmail.com', 'Renancosta2@')
check, reason = IQ.connect()

