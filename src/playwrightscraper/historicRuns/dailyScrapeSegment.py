from datetime import date, timedelta
from bots import SegmentCapBot
from botConfig import setSegmentCapConfig
from pages.pageVars import getPipeCode, SEGMENT_PIPES
from utils import log


def segmentDaily():

    log("scraping for Segment capacity ------------------")

    for i in SEGMENT_PIPES:
        curdate = date.today()
        while (curdate >= (date.today() - timedelta(days=1))):
            configuration = {
                "targetDate": curdate,
                "fileType": "del",
                "pipeLine":  getPipeCode(i),
                "cycleSelector": 'INTRADAY 3'
            }
            setSegmentCapConfig(**configuration)
            SegmentCapBot().scrape()
            curdate = curdate - timedelta(days=1)
