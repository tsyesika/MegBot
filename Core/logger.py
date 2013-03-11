import sys
import logging
from traceback import format_exception

def log_uncaught_exceptions(*args):
    # stackoverflow 6234405
    error = "".join(format_exception(*args))
    logger.error("Unhandled exception: %s", error)

logging.basicConfig(format='<%(asctime)s, %(threadName)s, %(levelname)s> %(message)s', level=logging.DEBUG)
logging.captureWarnings(True)
sys.excepthook = log_uncaught_exceptions
