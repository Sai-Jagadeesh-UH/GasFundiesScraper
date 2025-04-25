import os
from utils import log
from pathlib import Path
from datetime import datetime, time, timedelta
from .azureConnect import logsFolderclient, statsFolderclient, PointCapacityFolderclient, SegmentCapacityFolderclient, StorageCapacityFolderclient, NoNotceActivityFolderclient
from botConfig import PATH_LIST

foldersDict = {
    "logs": (PATH_LIST["LOGS_PATH"], logsFolderclient),
    "point": (PATH_LIST["POINTCAPACITY_PATH"], PointCapacityFolderclient),
    "segment": (PATH_LIST["SEGMENTCAPACITY_PATH"], SegmentCapacityFolderclient),
    "storage": (PATH_LIST["STORAGECAPACITY_PATH"], StorageCapacityFolderclient),
    "nonotice": (PATH_LIST["NONOTICEACTIVITY_PATH"], NoNotceActivityFolderclient),
    "stats": (PATH_LIST["RUNSTATS_PATH"], statsFolderclient),
}


def pushFiles(key: str = "logs"):
    folpath, folclient = foldersDict[key]
    # if (datetime.now().hour > 9):
    if (datetime.now().hour):
        filelist = [(f, os.path.getctime(f))
                    for f in folpath.iterdir()]
        filelist.sort(key=lambda item: item[1], reverse=True)
        fileclient = folclient.get_file_client(
            filelist[0][0].name)
        with open(file=filelist[0][0], mode=r"rb") as data:
            fileclient.upload_data(data=data, overwrite=True)
        log(f"{filelist[0][0].name} pushed to blob successfully")
    # else:
    #     for i in folpath.iterdir():
    #         fileclient = folclient.get_file_client(i.name)
    #         with open(file=i, mode=r"rb") as data:
    #             fileclient.upload_data(data=data, overwrite=True)
    #         log(f"{i.name} pushed to blob successfully")
    #         if (datetime.now().hour < 9):
    #             i.unlink(missing_ok=True)
