from historicRuns import nonoticeHistoric, segmentHistoric, storageHistoric, pointHistoric
from utils import log

if __name__ == '__main__':
    log("starting Historic scrapes")
    pointHistoric()
    segmentHistoric()
    storageHistoric()
    nonoticeHistoric()
    log("historic scraping completed")
