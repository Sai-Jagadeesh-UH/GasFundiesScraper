from typing import Literal
import yaml
from .configVars import BASE_FILE_PATH, TEMP_FILE


def setNoNoticeActConfig(**kwargs) -> dict:

    with open(BASE_FILE_PATH) as file:
        baseconfig = yaml.safe_load(file)

    CapConfig = baseconfig['NoNoticeActivity'] | kwargs
    with open(TEMP_FILE, 'w+') as yaml_file:
        yaml.dump(CapConfig, yaml_file, default_flow_style=False)


def NoNoticeActConfig(filePath=TEMP_FILE):
    with open(TEMP_FILE) as file:
        return yaml.safe_load(file)
