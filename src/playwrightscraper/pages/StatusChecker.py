from taipy.gui import Gui, State, notify
import taipy.gui.builder as tgb
from datetime import datetime, date, timedelta
import pandas as pd
from utils import getStats


# df = getStats()
# print(df)


with tgb.Page() as StatusChecker:
    # tgb.text(r"# RunStatus ", mode="md")
    # tgb.button(label="Refresh", on_action=clickRefresh)
    with tgb.part(class_name="card"):
        tgb.part(partial="{df_status}")
