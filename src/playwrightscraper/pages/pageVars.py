import yaml
from botConfig import PATH_LIST

with open(PATH_LIST["CONFIGS_PATH"] / r"pipes.yml") as file:
    PIPES = yaml.safe_load(file)["PIPELINE_NAMES"]

with open(PATH_LIST["CONFIGS_PATH"] / r"pipeScrapes.yml") as file:
    PIPE_SCRAPES = yaml.safe_load(file)


POINT_PIPES = PIPE_SCRAPES["POINT_CAPACITY"]

SEGMENT_PIPES = PIPE_SCRAPES["SEGMENT_CAPACITY"]

STORAGE_PIPES = PIPE_SCRAPES["STORAGE_CAPACITY"]

NO_NOTICE_PIPES = PIPE_SCRAPES["NO_NOTICE_ACTIVITY"]

CYCLES = PIPE_SCRAPES["CYCLES"]


def getPipeCode(pipename: str) -> str:
    return PIPES.get(pipename, "error")
