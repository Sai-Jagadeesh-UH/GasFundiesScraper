from pathlib import Path
from botConfig import PATH_LIST

for i, k in PATH_LIST.items():
    if (not k.exists()):
        k.mkdir()
