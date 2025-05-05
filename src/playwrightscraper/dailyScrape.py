from historicRuns import nonoticeDaily, segmentDaily, storageDaily, pointDaily
from utils import log
from datetime import date
from azurepush import wipeFiles

if __name__ == '__main__':
    log(f"starting daily Scheduled scrapes for {date.today()}")
    pointDaily()
    segmentDaily()
    storageDaily()
    nonoticeDaily()
    wipeFiles("point")
    wipeFiles("segment")
    wipeFiles("storage")
    wipeFiles("nonotice")
    wipeFiles("logs")
    wipeFiles("stats")
    log("Scheduled scrapes completed, all files are pushed to cloud")
