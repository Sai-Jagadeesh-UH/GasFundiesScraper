from datetime import date, timedelta
from bots import NoNoticeActBot
from botConfig import setNoNoticeActConfig
from pages.pageVars import getPipeCode,  NO_NOTICE_PIPES
from utils import log

if __name__ == '__main__':

    log("starting Historic scrapes")

    log("scraping for NoNoticeActivity - drn ------------------")

    for i in NO_NOTICE_PIPES:
        curdate = date.today() - timedelta(days=5)
        while (curdate > (date.today() - timedelta(days=94))):
            configuration = {
                "targetDate": curdate,
                "fileType": "drn",
                "pipeLine":  getPipeCode(i)
            }
            setNoNoticeActConfig(**configuration)
            NoNoticeActBot().scrape()
            curdate = curdate - timedelta(days=1)

    log("scraping for NoNoticeActivity - pin ------------------")

    for i in NO_NOTICE_PIPES:
        curdate = date.today() - timedelta(days=5)
        while (curdate > (date.today() - timedelta(days=94))):
            configuration = {
                "targetDate": curdate,
                "fileType": "pin",
                "pipeLine":  getPipeCode(i)
            }
            setNoNoticeActConfig(**configuration)
            NoNoticeActBot().scrape()
            curdate = curdate - timedelta(days=1)
