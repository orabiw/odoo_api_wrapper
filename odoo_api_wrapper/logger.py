""" Logger """
import logging

from config import LOG_LEVEL

FORMAT = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'


def get_logger(name: str = __name__) -> logging.Logger:
    """ create a logger object """
    formatter = logging.Formatter(FORMAT, datefmt='%Y-%m-%d %H:%M:%S %z')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(LOG_LEVEL)
    logger.propagate = 0

    return logger
