from datetime import date
from pages.pageVars import CYCLES
from bots import PointCapBot
from botConfig import setPointCapConfig


if __name__ == '__main__':
    configuration = {
        "targetDate": date.today(),
        "fileType": "del",
        "pipeLine":  "MOPC",
        "cycleSelector": CYCLES[0]
    }
    setPointCapConfig(**configuration)
    PointCapBot().scrape()
