from datetime import date, timedelta
from bots import PointCapBot
from botConfig import setPointCapConfig
from pages.pageVars import getPipeCode, POINT_PIPES
from utils import log


def pointHistoric():

    log("starting Historic scrapes")

    log("scraping for Point capacity - del ------------------")

    for i in POINT_PIPES:
        curdate = date.today()
        while (curdate > (date.today() - timedelta(days=90))):
            configuration = {
                "targetDate": curdate,
                "fileType": "del",
                "pipeLine":  getPipeCode(i),
                "cycleSelector": 'INTRADAY 3'
            }
            setPointCapConfig(**configuration)
            PointCapBot().scrape()
            curdate = curdate - timedelta(days=1)

    log("scraping for Point capacity - rec ------------------")

    for i in POINT_PIPES:
        curdate = date.today()
        while (curdate > (date.today() - timedelta(days=90))):
            configuration = {
                "targetDate": curdate,
                "fileType": "rec",
                "pipeLine":  getPipeCode(i),
                "cycleSelector": 'INTRADAY 3'
            }
            setPointCapConfig(**configuration)
            PointCapBot().scrape()
            curdate = curdate - timedelta(days=1)
