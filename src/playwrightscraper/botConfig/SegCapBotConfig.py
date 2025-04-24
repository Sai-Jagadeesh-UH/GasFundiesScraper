from typing import Literal
import yaml
from .configVars import BASE_FILE_PATH, TEMP_FILE


def setSegmentCapConfig(**kwargs) -> dict:

    with open(BASE_FILE_PATH) as file:
        baseconfig = yaml.safe_load(file)

    CapConfig = baseconfig['SegmentCapacity'] | kwargs
    with open(TEMP_FILE, 'w+') as yaml_file:
        yaml.dump(CapConfig, yaml_file, default_flow_style=False)


def SegmentCapConfig(filePath=TEMP_FILE):
    with open(TEMP_FILE) as file:
        return yaml.safe_load(file)
