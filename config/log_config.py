import logging
from logging.handlers import RotatingFileHandler
import os


class Logger(object):
    logger = None
   

    @classmethod
    def get_logger(cls):
        if cls.logger is None:
            path = os.makedirs("logs", exist_ok= True)
            cls.logger = logging.getLogger()
            cls.logger.setLevel(logging.INFO)

            handler = RotatingFileHandler(
                "logs/app_logs.log", maxBytes=1024 * 1024, backupCount=1
            )
            formatter = logging.Formatter(
                "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            cls.logger.addHandler(handler)

        return cls.logger
