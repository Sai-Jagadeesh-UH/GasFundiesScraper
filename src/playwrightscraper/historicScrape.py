from datetime import date, timedelta
from pages.pageVars import CYCLES
from bots import PointCapBot, SegmentCapBot, StorageCapBot, NoNoticeActBot
from botConfig import setPointCapConfig, setSegmentCapConfig, setStorageCapConfig, setNoNoticeActConfig
from pages.pageVars import getPipeCode, POINT_PIPES, SEGMENT_PIPES, STORAGE_PIPES, NO_NOTICE_PIPES
from utils import log

if __name__ == '__main__':

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
