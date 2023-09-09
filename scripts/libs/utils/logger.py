import logging
import sys
from enum import IntEnum


class LogLevel(IntEnum):
    CRITICAL = 5
    ERROR = 4
    WARNING = 3
    INFO = 2
    DEBUG = 1
    NOTSET = 0


def get_logger(level: int = 2) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.getLevelName(LogLevel(level).name.upper()))
    if not logger.hasHandlers():
        # ログを標準出力する
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt=r"%Y-%m-%dT%H:%M:%S%z",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
