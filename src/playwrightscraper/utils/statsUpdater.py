import pandas as pd
from datetime import datetime
import os
from botConfig import PATH_LIST

RUNSTATS_PATH = PATH_LIST["RUNSTATS_PATH"]


# # Create an empty DataFrame with the defined schema
# df = pd.DataFrame(columns=['Rundate', 'ScrapeType', 'Pipeline',
#                            'Cycle', 'TargetDate',  'StartTime', 'EndTime', 'status', 'Arguments'])


def startStats(scrapetype: str, configs):

    file_name = (RUNSTATS_PATH /
                 rf"{datetime.now().strftime(r'%Y_%m_%d')}.csv")
    if (file_name.exists()):
        df = pd.read_csv(file_name)
    else:
        df = pd.DataFrame(columns=['Rundate', 'ScrapeType', 'Pipeline',
                                   'Cycle', 'TargetDate',  'StartTime', 'EndTime', 'status', 'Arguments'])
        df.to_csv(file_name, index=False)

    new_row = {
        'Rundate': datetime.now().strftime(r"%m/%d/%Y"),
        'ScrapeType': scrapetype,
        'Pipeline': configs.pipeLine,
        'Cycle': None,
        'TargetDate': configs.targetDate.strftime(r'%m/%d/%Y'),
        'StartTime': datetime.now().strftime(r"%H:%M:%S"),
        'EndTime': None,
        'status': "Processing",
        'Arguments': None
    }

    if hasattr(configs, "cycleSelector"):
        new_row['Cycle'] = configs.cycleSelector

    if hasattr(configs, "fileType"):
        new_row['Arguments'] = {"fileType": configs.fileType}

    df.loc[len(df)] = new_row
    # print(df.loc[len(df) - 1])
    df.to_csv(file_name, index=False)


def endStats(status: str):

    filelist = [(f, os.path.getctime(f))
                for f in RUNSTATS_PATH.iterdir()]
    filelist.sort(key=lambda item: item[1], reverse=True)

    df = pd.read_csv(filelist[0][0])

    df.loc[len(df) - 1, 'status'] = status
    df.loc[len(df) - 1, 'EndTime'] = datetime.now().strftime(r"%H:%M:%S")
    # print(df.loc[len(df) - 1])
    df.to_csv(filelist[0][0], index=False)


def getStats():
    filelist = [(f, os.path.getctime(f))
                for f in RUNSTATS_PATH.iterdir()]
    filelist.sort(key=lambda item: item[1], reverse=True)

    return pd.read_csv(filelist[0][0])
