from iqoptionapi.stable_api import IQ_Option
import logging
import CONSTANTS


logging.disable(level=(logging.DEBUG))

IQ = IQ_Option(CONSTANTS.IQUSER, CONSTANTS.IQPASSWORD)
check, reason = IQ.connect()

