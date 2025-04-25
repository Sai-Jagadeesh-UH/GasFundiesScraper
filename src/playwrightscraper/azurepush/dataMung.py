import pandas as pd
from datetime import datetime
from botConfig import PATH_LIST


def mungPointFiles(filename):
    df = pd.read_excel(filename, nrows=2)
    effDate = df.loc[0, 'Eff Gas Day/Eff Time']
    cycDesc = df.loc[0, 'CycleDesc']
    pipeName = df.loc[0, 'TSP Name']
    purpose = df.loc[0, 'Loc Purp Desc']
    df = pd.read_excel(filename, header=3)
    df.dropna(subset=df.columns[1:], how="all", inplace=True)
    collist = df.columns.to_list()
    df["TSP Name"] = pipeName
    df["Eff Gas Day/Eff Time"] = effDate
    df["CycleDesc"] = cycDesc
    df["Loc Purp Desc"] = purpose
    df["TimeStamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = df[["Eff Gas Day/Eff Time", "TSP Name",
             "CycleDesc", "Loc Purp Desc", *collist, "TimeStamp"]]
    if (len(df) > 0):
        df.to_csv(PATH_LIST["TEMP_CSV"])


def mungSegStorFiles(filename):
    df = pd.read_excel(filename, nrows=2)
    effDate = df.loc[0, 'Eff Gas Day/Eff Time']
    cycDesc = df.loc[0, 'CycleDesc']
    pipeName = df.loc[0, 'TSP Name']
    df = pd.read_excel(filename, header=3)
    df.dropna(subset=df.columns[1:], how="all", inplace=True)
    collist = df.columns.to_list()
    df["TSP Name"] = pipeName
    df["Eff Gas Day/Eff Time"] = effDate
    df["CycleDesc"] = cycDesc
    df["TimeStamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = df[["Eff Gas Day/Eff Time", "TSP Name",
             "CycleDesc", *collist, "TimeStamp"]]

    if (len(df) > 0):
        df.to_csv(PATH_LIST["TEMP_CSV"])


def mungNoNoticeFiles(filename):
    df = pd.read_excel(filename, nrows=2)
    effDate = df.loc[0, 'Gas Flow Date']
    location = df.loc[0, 'Location']
    pipeName = df.loc[0, 'TSP Name']
    df = pd.read_excel(filename, header=3, usecols=[
                       'Location', 'Location Name', 'No Notice Quantity (Dth)'])
    df.dropna(subset=df.columns[1:], how="all", inplace=True)
    collist = df.columns.to_list()
    df["TSP Name"] = pipeName
    df["Gas Flow Date"] = effDate
    df["Location TYPE"] = location
    df["TimeStamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = df[["Gas Flow Date", "TSP Name", "Location TYPE", *collist, "TimeStamp"]]
    if (len(df) > 0):
        df.to_csv(PATH_LIST["TEMP_CSV"])


def processFiles(filename):
    if ("DEL" in filename.name or "REC" in filename.name):
        mungPointFiles(filename)
    elif ("Segment" in filename.name or "Storage" in filename.name):
        mungSegStorFiles(filename)
    else:
        mungNoNoticeFiles(filename)
