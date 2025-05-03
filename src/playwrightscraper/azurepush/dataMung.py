from utils import log
from .tablePush import pushSegmentCap, pushStorageCap, pushNoNoticeAct, pushPointDELCap, pushPointRECCap
import pandas as pd
import warnings


def mungPointFiles(filename):
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)
        df = pd.read_excel(filename, nrows=2)
        effDate = df.loc[0, 'Eff Gas Day/Eff Time']
        cycDesc = df.loc[0, 'CycleDesc']
        pipeName = df.loc[0, 'TSP Name']
        locPrpDesc = df.loc[0, 'Loc Purp Desc']
        df = pd.read_excel(filename, header=3)
        df.dropna(subset=df.columns[1:], how="all", inplace=True)
        df[['Design Capacity', 'Operating Capacity', 'Total Scheduled Quantity', 'Operationally Available Capacity']] = df[[
            'Design Capacity', 'Operating Capacity', 'Total Scheduled Quantity', 'Operationally Available Capacity']].fillna(0)
        df['Design Capacity'] = df['Design Capacity'].apply(
            lambda x:  int(float(str(x).replace(',', ''))))
        df['Operating Capacity'] = df['Operating Capacity'].apply(
            lambda x:  int(float(str(x).replace(',', ''))))
        df['Total Scheduled Quantity'] = df['Total Scheduled Quantity'].apply(
            lambda x:  int(float(str(x).replace(',', ''))))
        df['Operationally Available Capacity'] = df['Operationally Available Capacity'].apply(
            lambda x:  int(float(str(x).replace(',', ''))))
        df.fillna('', inplace=True)
        collist = df.columns.to_list()
        df["TSP Name"] = pipeName
        df["Eff Gas Day/Eff Time"] = effDate
        df["CycleDesc"] = cycDesc
        df["Loc Purp Desc"] = locPrpDesc
        # df["TimeStamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df = df[["Eff Gas Day/Eff Time", "TSP Name",
                "CycleDesc", "Loc Purp Desc", *collist]]
        # return df
        if (len(df) > 0):
            if ("DEL" in filename.name):
                pushPointDELCap(df)
            elif ("REC" in filename.name):
                pushPointRECCap(df)
            log(filename.name + " is pushed into table")
        else:
            log(filename.name + " is empty nothing to push")


def mungSegmentFile(filename):
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)
        df = pd.read_excel(filename, nrows=2)
        effDate = df.loc[0, 'Eff Gas Day/Eff Time']
        cycDesc = df.loc[0, 'CycleDesc']
        pipeName = df.loc[0, 'TSP Name']
        df = pd.read_excel(filename, header=3)
        df.dropna(subset=df.columns[1:], how="all", inplace=True)
        df[['Design Capacity', 'Operating Capacity', 'Total Scheduled Quantity', 'Operationally Available Capacity']] = df[[
            'Design Capacity', 'Operating Capacity', 'Total Scheduled Quantity', 'Operationally Available Capacity']].fillna(0)
        df['Design Capacity'] = df['Design Capacity'].apply(
            lambda x:  int(float(str(x).replace(',', ''))))
        df['Operating Capacity'] = df['Operating Capacity'].apply(
            lambda x:  int(float(str(x).replace(',', ''))))
        df['Total Scheduled Quantity'] = df['Total Scheduled Quantity'].apply(
            lambda x:  int(float(str(x).replace(',', ''))))
        df['Operationally Available Capacity'] = df['Operationally Available Capacity'].apply(
            lambda x:  int(float(str(x).replace(',', ''))))
        df.fillna('', inplace=True)
        collist = df.columns.to_list()
        df["TSP Name"] = pipeName
        df["Eff Gas Day/Eff Time"] = effDate
        df["CycleDesc"] = cycDesc
        # df["TimeStamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df = df[["Eff Gas Day/Eff Time", "TSP Name",
                "CycleDesc", *collist]]
        if (len(df) > 0):
            pushSegmentCap(df)
            log(filename.name + " is pushed into table")
        else:
            log(filename.name + " is empty nothing to push")


def mungStorageFiles(filename):
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)
        df = pd.read_excel(filename, nrows=2)
        effDate = df.loc[0, 'Eff Gas Day/Eff Time']
        cycDesc = df.loc[0, 'CycleDesc']
        pipeName = df.loc[0, 'TSP Name']
        df = pd.read_excel(filename, header=3)
        df.dropna(subset=df.columns[1:], how="all", inplace=True)
        df[['Design Capacity', 'Operating Capacity', 'Total Scheduled Quantity', 'Operationally Available Capacity']] = df[[
            'Design Capacity', 'Operating Capacity', 'Total Scheduled Quantity', 'Operationally Available Capacity']].fillna(0)
        df['Design Capacity'] = df['Design Capacity'].apply(
            lambda x:  int(float(str(x).replace(',', ''))))
        df['Operating Capacity'] = df['Operating Capacity'].apply(
            lambda x:  int(float(str(x).replace(',', ''))))
        df['Total Scheduled Quantity'] = df['Total Scheduled Quantity'].apply(
            lambda x:  int(float(str(x).replace(',', ''))))
        df['Operationally Available Capacity'] = df['Operationally Available Capacity'].apply(
            lambda x:  int(float(str(x).replace(',', ''))))
        df.fillna('', inplace=True)
        collist = df.columns.to_list()
        df["TSP Name"] = pipeName
        df["Eff Gas Day/Eff Time"] = effDate
        df["CycleDesc"] = cycDesc
        # df["TimeStamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df = df[["Eff Gas Day/Eff Time", "TSP Name",
                "CycleDesc", *collist]]
        if (len(df) > 0):
            pushStorageCap(df)
            log(filename.name + " is pushed into table")
        else:
            log(filename.name + " is empty nothing to push")


def mungNoNoticeFiles(filename):
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)
        df = pd.read_excel(filename, nrows=2)
        effDate = df.loc[0, 'Gas Flow Date']
        locationCode = df.loc[0, 'Location']
        pipeName = df.loc[0, 'TSP Name']
        df = pd.read_excel(filename, header=3, usecols=[0, 1, 2])
        df.dropna(subset=df.columns[1:], how="all", inplace=True)
        df['No Notice Quantity (Dth)'] = df['No Notice Quantity (Dth)'].apply(
            lambda x:  int(float(str(x).replace(',', ''))))
        df.fillna('', inplace=True)
        collist = df.columns.to_list()
        df["TSP Name"] = pipeName
        df["Gas Flow Date"] = effDate
        df["Location Code"] = locationCode
        # df["TimeStamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df = df[["Gas Flow Date", "TSP Name",
                "Location Code", *collist]]
        if (len(df) > 0):
            pushNoNoticeAct(df)
            log(filename.name + " is pushed into table")
        else:
            log(filename.name + " is empty nothing to push")


def processFiles(filename):
    if ("DEL" in filename.name or "REC" in filename.name):
        mungPointFiles(filename)
    elif ("Segment" in filename.name):
        mungSegmentFile(filename)
    elif ("Storage" in filename.name):
        mungStorageFiles(filename)
    elif ("DRN" in filename.name or "PIN" in filename.name):
        mungNoNoticeFiles(filename)
