from bots import PointCapBot, SegmentCapBot, StorageCapBot, NoNoticeActBot
from utils import log, Custom_Error
from datetime import date, timedelta, datetime
import sys
from time import sleep
from botConfig import setPointCapConfig, setSegmentCapConfig, setStorageCapConfig, setNoNoticeActConfig, PIPELINES_NAMES
from playwright.sync_api import sync_playwright
import random
from utils import startStats, endStats
from azurepush import pushFiles

deltaDay = timedelta(days=1)


def caller(fromdate: date, todate: date):
    daysDiff = (todate - fromdate).days
    log(f"{daysDiff}")
    today = date.today()
    print(f"{abs((fromdate - today).days)} {abs((todate - today).days)}")
    if (abs((fromdate - today).days) > 90) or (abs((todate - today).days) > 90):
        log("cannot look back more than 90 days")
        return
    curDate = todate
    print(f"{curDate}  {fromdate}  {curDate <= fromdate}")
    while curDate >= fromdate:
        try:
            scrape(curDate, fileType="del", headLess=False)
        except Exception as e:
            log(f"something went wrong at {curDate} retrying.....")
            sleep(5)
            try:
                scrape(curDate, fileType="del", headLess=False)
            except Exception as e:
                log("failed again .. erroring")

        try:
            scrape(curDate, fileType="rec")
        except Exception as e:
            log(f"something went wrong at {curDate} retrying.....")
            sleep(5)
            try:
                scrape(curDate, fileType="rec")
            except Exception as e:
                log("failed again .. erroring")

        curDate = curDate - deltaDay


try:
    # caller(todate=date(day=8, month=2, year=2025),
    #        fromdate=date(day=8, month=2, year=2025))
    # scrape(date(day=8, month=2, year=2025), fileType="rec", headLess=False)
    # for k, val in PIPELINES_NAMES.items():

    # configuration = {
    #     "headLess": False,
    #     "targetDate": date(day=8, month=2, year=2025),
    #     "fileType": "pin",
    #     "pipeLine":  "NGPL",
    #     "cycleSelector": random.choice(["TIMELY", "EVENING", "INTRADAY 1", "INTRADAY 2", "INTRADAY 3"])
    # }

    # setSegmentCapConfig(**configuration)
    # SegmentCapBot().scrape()
    # setPointCapConfig(**configuration)
    # x = PointCapBot()
    # startStats("PointConfig", x)
    # PointCapBot().scrape()
    # setStorageCapConfig(**configuration)
    # StorageCapBot().scrape()
    # setNoNoticeActConfig(**configuration)
    # x = NoNoticeActBot()
    # startStats("NoNoticeActivity", x)
    # endStats("Failed")
    # NoNoticeActBot().scrape()
    # log("checking")
    pushFiles("stats")

except Exception as e:
    raise Custom_Error(e, sys)
