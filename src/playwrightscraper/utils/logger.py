import logging
import os
from datetime import datetime
import pathlib
from botConfig import PATH_LIST

FILE_NAME = datetime.now().strftime(r"%Y_%m_%d_%H")+".log"

FILE_PATH = PATH_LIST["LOGS_PATH"] / FILE_NAME

FILE_PATH.parent.mkdir(exist_ok=True, parents=True)

logging.basicConfig(filename=str(FILE_PATH),
                    filemode='a', format='%(asctime)s, %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')


def log(msg: str):
    print(msg)
    logging.info(msg)


if __name__ == "__main__":
    logging.info('Logging Successful')
