import logging
from logging.handlers import RotatingFileHandler
import os


class Logger(object):
    success_logger = None
    error_logger = None
    api_info_logger = None

    @classmethod
    def get_api_info_logger(cls):
        if cls.api_info_logger is None:
            cls.api_info_logger = cls._create_logger("logs/api_info_logs.log")
        return cls.api_info_logger

    @classmethod
    def get_success_logger(cls):
        if cls.success_logger is None:
            cls.success_logger = cls._create_logger("logs/success_logs.log")
        return cls.success_logger

    @classmethod
    def get_error_logger(cls):
        if cls.error_logger is None:
            cls.error_logger = cls._create_logger("logs/error_logs.log")
        return cls.error_logger

    @classmethod
    def _create_logger(cls, log_file: str):
        os.makedirs("logs", exist_ok=True)
        logger = logging.getLogger(log_file)
        logger.setLevel(logging.INFO)

        handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=10)
        formatter = logging.Formatter(
            "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger