from taipy.gui import Gui, State, notify
import taipy.gui.builder as tgb
from datetime import datetime, date, timedelta

ondate = date.today()
mindate = date.today() - timedelta(days=2)
maxdate = date.today() + timedelta(days=2)

with tgb.Page() as dummyPage:
    with tgb.part(class_name="card"):
        with tgb.part(class_name="card"):
            tgb.text("### On", mode="md", class_name="on-run")
            tgb.date(date="{ondate}", min="{mindate}",
                     max="{maxdate}", propagate=True)
