import os
from utils import log
from pathlib import Path
from datetime import datetime, time, timedelta
from .azureConnect import logsFolderclient, statsFolderclient, PointCapacityFolderclient, SegmentCapacityFolderclient, StorageCapacityFolderclient, NoNotceActivityFolderclient


foldersDict = {
    "logs": ((Path("./") / "logs"), logsFolderclient),
    "point": ((Path("./") / "downs" / "PointCapacity"), PointCapacityFolderclient),
    "segment": ((Path("./") / "downs" / "SegmentCapacity"), SegmentCapacityFolderclient),
    "storage": ((Path("./") / "downs" / "StorageCapacity"), StorageCapacityFolderclient),
    "nonotice": ((Path("./") / "downs" / "NoNoticeActivity"), NoNotceActivityFolderclient),
    "stats": ((Path("./") / "downs" / "RunStats"), statsFolderclient),
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
