import logging
import os
from datetime import datetime
import pathlib
from botConfig import PATH_LIST

INFOFILE_NAME = datetime.now().strftime(r"%Y_%m_%d_%H")+"INFO.log"
ERRORFILE_NAME = datetime.now().strftime(r"%Y_%m_%d_%H")+"ERROR.log"


INFOFILE_PATH = PATH_LIST["LOGS_PATH"] / INFOFILE_NAME
ERRORFILE_PATH = PATH_LIST["LOGS_PATH"] / ERRORFILE_NAME

INFOFILE_PATH.parent.mkdir(exist_ok=True, parents=True)

info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')

info_logger.setLevel(logging.WARN)
error_logger.setLevel(logging.WARN)

info_file_handler = logging.FileHandler(INFOFILE_PATH)
error_file_handler = logging.FileHandler(ERRORFILE_PATH)

formatter = logging.Formatter(
    '%(asctime)s, %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')
info_file_handler.setFormatter(formatter)
error_file_handler.setFormatter(formatter)

# Add handlers to loggers
info_logger.addHandler(info_file_handler)
error_logger.addHandler(error_file_handler)


def log(msg: str):
    print(msg)
    info_logger.warning(msg)


def logError(msg: str):
    print(msg)
    error_logger.error(msg)


if __name__ == "__main__":
    info_logger.warning('Logging Successful')
