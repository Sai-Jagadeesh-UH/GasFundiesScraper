from datetime import date, timedelta
from bots import StorageCapBot
from botConfig import setStorageCapConfig
from pages.pageVars import getPipeCode, STORAGE_PIPES
from utils import log


def storageDaily():

    log("scraping for Storage capacity ------------------")

    for i in STORAGE_PIPES:
        curdate = date.today()
        while (curdate >= (date.today() - timedelta(days=1))):
            configuration = {
                "targetDate": curdate,
                "fileType": "del",
                "pipeLine":  getPipeCode(i),
                "cycleSelector": 'INTRADAY 3'
            }
            setStorageCapConfig(**configuration)
            StorageCapBot().scrape()
            curdate = curdate - timedelta(days=1)
