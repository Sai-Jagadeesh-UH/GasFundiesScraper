from .logger import log, logError
from .exceptor import Custom_Error
from .statsUpdater import startStats, endStats, getStats
from botConfig import PATH_LIST

for i, k in PATH_LIST.items():
    if (not k.exists()):
        k.mkdir()
