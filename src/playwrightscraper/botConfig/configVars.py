from pathlib import Path

TOP_PATH = Path(__file__).parent.parent.parent

LOGS_PATH = TOP_PATH.parent / r"logs"

CONFIGS_PATH = TOP_PATH / r"configs"

BASE_FILE_PATH = CONFIGS_PATH / r"baseconfig.yml"

TEMP_FILE = CONFIGS_PATH / r"CapTemp.yml"

AZUREKEY_FILE = CONFIGS_PATH / r"azureConnection.yml"

IMAGES_PATH = TOP_PATH / r"images"

DOWNS_PATH = TOP_PATH / r"downs"

POINTCAPACITY_PATH = DOWNS_PATH / r"PointCapacity"

SEGMENTCAPACITY_PATH = DOWNS_PATH / r"SegmentCapacity"

STORAGECAPACITY_PATH = DOWNS_PATH / r"StorageCapacity"

RUNSTATS_PATH = DOWNS_PATH / r"RunStats"

NONOTICEACTIVITY_PATH = DOWNS_PATH / r"NoNoticeActivity"

PATH_LIST = {
    "CONFIGS_PATH": CONFIGS_PATH,
    "BASE_FILE_PATH": BASE_FILE_PATH,
    "TEMP_FILE": TEMP_FILE,
    "IMAGES_PATH": IMAGES_PATH,
    "DOWNS_PATH": DOWNS_PATH,
    "POINTCAPACITY_PATH": POINTCAPACITY_PATH,
    "SEGMENTCAPACITY_PATH": SEGMENTCAPACITY_PATH,
    "STORAGECAPACITY_PATH": STORAGECAPACITY_PATH,
    "RUNSTATS_PATH": RUNSTATS_PATH,
    "NONOTICEACTIVITY_PATH": NONOTICEACTIVITY_PATH,
    "AZUREKEY_FILE": AZUREKEY_FILE,
    "LOGS_PATH": LOGS_PATH
}

PIPELINES_NAMES = {
    'Arlington Storage': "ARLS",
    'Cheyenne Plains': "CP",  # NO Storage
    'Colorado Interstate Gas': "CIG",
    'Elba Express': "EEC",  # NO Storage
    'El Paso Natural Gas': "EPNG",  # NO Storage
    'Horizon Pipeline': "HORZ",  # NO Storage
    'KM Illinois Pipeline': 'KMIL',  # NO Storage
    'KM Louisiana Pipeline': 'KMLP',  # NO Storage
    'Midcontinent Express': 'MEP',  # NO Storage
    'Mojave Pipeline': 'MOPC',  # NO Storage
    'Natural Gas Pipeline': 'NGPL',
    'Sierrita Gas Pipeline': 'SGP',  # NO Storage
    'Southern LNG': 'SLNG',  # No Segment
    'Southern Natural Gas': 'SNG',
    'Stagecoach Pipeline and Storage': 'STAG',
    'Tennessee Gas Pipeline': 'TGPD',
    'TransColorado Gas Transmission': 'TCP',  # NO Storage
    'Wyoming Interstate': 'WIC',  # NO Storage
    'Young Gas Storage': 'YGS',  # NO Segment
    # 'Keystone Gas Storage': 'KGS', # Not Available
    # 'Twin Tier Pipeline': 'TTP', # Not Available
    # 'Banquete Hub': 'BANH',  # Not Available
    # 'Camino Real': 'CRGS',
    # 'Copano Pipelines': 'COP', # Not avaialable
    # 'Kinderhawk Field Services': 'KHFS',
    # 'KM Border Pipeline': 'KMBP',
    # 'Eagle Ford Gathering': 'EFGS',
    # 'Eagle Ford Midstream, LLC': 'KMEF',
    # 'Gulf Coast Express Pipeline': 'GCX',
    # 'KM Mexico Pipeline': 'KMMX', # Not Available
    # 'KM North Texas Pipeline': 'KMNT',
    # 'Permian Highway Pipeline': 'PHP',
    # 'KM Tejas Pipeline': 'KMTJ',
    # 'KM Texas Pipeline': 'KMTP',
    # 'NET Mexico Pipeline Partners, LLC': 'NETM'
}
