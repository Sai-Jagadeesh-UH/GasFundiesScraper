import os
import yaml
from azure.storage.filedatalake import (
    DataLakeServiceClient,
    DataLakeDirectoryClient,
    FileSystemClient,
    FileProperties
)
from azure.identity import DefaultAzureCredential
from pathlib import Path
from botConfig import PATH_LIST

AZUREKEY_FILE = PATH_LIST["AZUREKEY_FILE"]


def getKey():
    with open(AZUREKEY_FILE) as file:
        temp = yaml.safe_load(file)
        return temp["key"], temp["account_url"]


key, url = getKey()

service_client = DataLakeServiceClient(url, credential=key)

appdataFileSystemClient = service_client.get_file_system_client(
    file_system="appdata")

rawdataFileSystemClient = service_client.get_file_system_client(
    file_system="rawdata")

logsFolderclient = appdataFileSystemClient.get_directory_client(
    directory="logs")

statsFolderclient = appdataFileSystemClient.get_directory_client(
    directory="RunStats")

configsFolderclient = appdataFileSystemClient.get_directory_client(
    directory="Conifgs")

PointCapacityFolderclient = rawdataFileSystemClient.get_directory_client(
    directory="PointCapacity")

SegmentCapacityFolderclient = rawdataFileSystemClient.get_directory_client(
    directory="SegmentCapacity")

StorageCapacityFolderclient = rawdataFileSystemClient.get_directory_client(
    directory="StorageCapacity")

NoNotceActivityFolderclient = rawdataFileSystemClient.get_directory_client(
    directory="NoNotceActivity")
