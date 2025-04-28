from datetime import datetime
import pyodbc
import pandas as pd
connectionString = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:sqlgfpipeprod.database.windows.net,1433;Database=sqldbgfpipeprod;Uid=PythonAppUser;Pwd={bIpvif-vabqub-benga3};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"


def pushSegmentCap(df: pd.DataFrame):
    conn = pyodbc.connect(connectionString)
    with conn.cursor() as cursor:
        sqlcommand = """INSERT INTO RAW.SegmentCapacity_KM
        ( EffGasDayTime, PipelineName, CycleDesc, LocSegment, LocNameSegment, LocZn, DesignCapacity, OperatingCapacity, TotalScheduledQuantity, OperationallyAvailableCapacity, IT, FlowInd, AllQtyAvail, QtyReason, Timestamp)
        values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        for _, row in df.iterrows():
            cursor.execute(sqlcommand, *list(row.to_dict().values()),
                           datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        conn.commit()


def pushStorageCap(df: pd.DataFrame):
    conn = pyodbc.connect(connectionString)
    with conn.cursor() as cursor:
        sqlcommand = """INSERT INTO RAW.StorageCapacity_KM
        (EffGasDayTime, PipelineName, CycleDesc, Loc, LocName, LocQTIDesc, DesignCapacity, OperatingCapacity, TotalScheduledQuantity, OperationallyAvailableCapacity, IT, FlowInd, AllQtyAvail, QtyReason, Timestamp)
        values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        for _, row in df.iterrows():
            cursor.execute(sqlcommand, *list(row.to_dict().values()),
                           datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        conn.commit()


def pushNoNoticeAct(df: pd.DataFrame):
    conn = pyodbc.connect(connectionString)
    with conn.cursor() as cursor:
        sqlcommand = """INSERT INTO RAW.NoNoticeActivity_KM
        (GasFlowDate, PipelineName, LocationCode, LocationID, LocationName, NoNoticeQuantityDth, Timestamp)
        values (?,?,?,?,?,?,?)"""
        for _, row in df.iterrows():
            cursor.execute(sqlcommand, *list(row.to_dict().values()),
                           datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        conn.commit()


def pushPointDELCap(df: pd.DataFrame):
    conn = pyodbc.connect(connectionString)
    with conn.cursor() as cursor:
        sqlcommand = """INSERT INTO RAW.PointCapacityDelivery_KM
        ( EffGasDayTime, PipelineName, CycleDesc, LocPurpDesc, Loc, LocName, LocZn, LocSegment, DesignCapacity, OperatingCapacity, TotalScheduledQuantity, OperationallyAvailableCapacity, IT, FlowInd, AllQtyAvail, QtyReason, Timestamp)
        values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        for _, row in df.iterrows():
            cursor.execute(sqlcommand, *list(row.to_dict().values()),
                           datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        conn.commit()


def pushPointRECCap(df: pd.DataFrame):
    conn = pyodbc.connect(connectionString)
    with conn.cursor() as cursor:
        sqlcommand = """INSERT INTO RAW.PointCapacityReceipt_KM
        ( EffGasDayTime, PipelineName, CycleDesc, LocPurpDesc, Loc, LocName, LocZn, LocSegment, DesignCapacity, OperatingCapacity, TotalScheduledQuantity, OperationallyAvailableCapacity, IT, FlowInd, AllQtyAvail, QtyReason, Timestamp)
        values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        for _, row in df.iterrows():
            cursor.execute(sqlcommand, *list(row.to_dict().values()),
                           datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        conn.commit()
