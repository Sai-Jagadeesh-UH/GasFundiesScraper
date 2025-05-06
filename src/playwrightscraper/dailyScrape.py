from historicRuns import nonoticeDaily, segmentDaily, storageDaily, pointDaily
from utils import log
from datetime import date, datetime
from azurepush import wipeFiles, pushFiles
from botConfig import PATH_LIST

if __name__ == '__main__':
    log(f"starting daily Scheduled scrapes for {date.today()}")
    wipeFiles("stats")
    pointDaily()
    segmentDaily()
    storageDaily()
    nonoticeDaily()
    wipeFiles("point")
    wipeFiles("segment")
    wipeFiles("storage")
    wipeFiles("nonotice")
    pushFiles("stats")
    with open(PATH_LIST["LOGS_PATH"] / f"CRONLOG_{datetime.now().strftime('%b')}.txt", 'r') as file:
        file.write(
            f"CRON run for {date.today()} is completed at {datetime.now().strftime('%H:%M:%S')}")
    wipeFiles("logs")
    log("Scheduled scrapes completed, all files are pushed to cloud")
