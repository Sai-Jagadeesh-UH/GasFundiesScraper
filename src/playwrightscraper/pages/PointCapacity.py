from taipy.gui import notify
import taipy.gui.builder as tgb
from datetime import date, timedelta
from .pageVars import getPipeCode, POINT_PIPES, CYCLES
from bots import PointCapBot
from botConfig import setPointCapConfig
from azurepush import pushFiles


def on_page_load(state):
    state.singleOpen = True
    state.rangeOpen = False

    Today = date.today()
    days90 = timedelta(days=90)

    state.mindate = Today - days90
    state.maxdate = Today

    state.fromdate = Today - timedelta(days=2)
    state.todate = Today - timedelta(days=1)
    state.ondate = Today

    state.Location = "Delivery"
    state.Pipeline = "Natural Gas Pipeline"
    state.Cycle = "INTRADAY 3"


def onSubmit(state):
    LocationDict = {"Delivery": "del", "Receipt": "rec"}
    configuration = {
        # "headLess": True,
        "targetDate": state.ondate,
        "fileType": LocationDict.get(state.Location, "error"),
        "pipeLine":  getPipeCode(state.Pipeline),
        "cycleSelector": state.Cycle
    }
    print(configuration)
    if configuration["fileType"] == "error":
        notify(state, notification_type="error",
               message="Please check Location")
        return
    if configuration["pipeLine"] == "error":
        notify(state, notification_type="error",
               message="Please check pipeLine")
        return
    if configuration["cycleSelector"] is None:
        notify(state, notification_type="error",
               message="Please check Cycle")
        return
    notify(state, notification_type="info",
           message=f"Bot is running for {configuration['targetDate']} please wait...")
    state.SubmitActive = False
    setPointCapConfig(**configuration)
    PointCapBot().scrape()
    state.SubmitActive = True
    notify(state, notification_type="info",
           message=f'Scrape for {configuration["cycleSelector"]} {configuration["pipeLine"]} pipeline {state.Location} on {configuration["targetDate"]} is complete')
    pushFiles()


def onRangeSubmit(state):

    LocationDict = {"Delivery": "del", "Receipt": "rec"}
    if state.todate <= state.fromdate:
        notify(state, notification_type="warning",
               message="todate should be greater than fromdate")
        return
    currentdate = state.fromdate
    while (currentdate <= state.todate):
        configuration = {
            "headLess": False,
            "targetDate": currentdate,
            "fileType": LocationDict.get(state.Location, "error"),
            "pipeLine":  getPipeCode(state.Pipeline),
            "cycleSelector": state.Cycle
        }
        print(configuration)
        if configuration["fileType"] == "error":
            notify(state, notification_type="error",
                   message="Please check Location")
            return
        if configuration["pipeLine"] == "error":
            notify(state, notification_type="error",
                   message="Please check pipeLine")
            return
        if configuration["cycleSelector"] is None:
            notify(state, notification_type="error",
                   message="Please check Cycle")
            return
        notify(state, notification_type="info",
               message=f"Bot is running for {configuration['targetDate']} please wait...")
        state.SubmitActive = False
        setPointCapConfig(**configuration)
        PointCapBot().scrape()
        state.SubmitActive = True
        notify(state, notification_type="info",
               message=f'Scrape for {configuration["cycleSelector"]} {configuration["pipeLine"]} pipeline {state.Location} on {configuration["targetDate"]} is complete')
        currentdate = currentdate + timedelta(days=1)
        pushFiles()


singleOpen = True
rangeOpen = False
SubmitActive = True


Today = date.today()
days90 = timedelta(days=90)


mindate = Today - days90
maxdate = Today

fromdate = Today - timedelta(days=2)
todate = Today - timedelta(days=1)
ondate = Today


Location = "Delivery"
Pipeline = "Natural Gas Pipeline"
Cycle = "INTRADAY 3"


def onDateChnage(state,):
    if (state.todate <= state.fromdate):
        notify(state, notification_type="warning",
               message="todate should be greater than fromdate")


def singleOpenFun(state):
    if (state.singleOpen):
        state.rangeOpen = False
    else:
        state.rangeOpen = True


def rangeOpenFun(state):
    if (state.rangeOpen):
        state.singleOpen = False
    else:
        state.singleOpen = True


with tgb.Page() as PointCapPage:

    with tgb.part(class_name="card"):
        with tgb.expandable(title="Run for a date", expanded="{singleOpen}", on_change=singleOpenFun):
            with tgb.layout("2 1"):
                with tgb.part(class_name="card"):
                    tgb.text("Pipeline")
                    tgb.selector(
                        dropdown=True, value="{Pipeline}", lov=POINT_PIPES, filter=True, width=r"100%")
                    tgb.html("br")
                    with tgb.layout("1 1"):
                        with tgb.part():
                            tgb.text("Cycle")
                            tgb.selector(
                                dropdown=True, value="{Cycle}", lov=CYCLES, filter=True, width=r"98%")
                        with tgb.part():
                            tgb.text("Location Point")
                            tgb.selector(
                                dropdown=True, value="{Location}", lov=["Delivery", "Receipt"], filter=True, width=r"100%")

                with tgb.part(class_name="card"):
                    tgb.text("### On", mode="md", class_name="on-run")
                    tgb.date(date="{ondate}", min="{mindate}",
                             max="{maxdate}", propagate=True)
                    tgb.html("br")
                    tgb.button(label="Submit",
                               class_name="plain apply_button", on_action=onSubmit, active="{SubmitActive}")

    with tgb.part(class_name="card"):
        with tgb.expandable(title="Run for a period", expanded="{rangeOpen}", on_change=rangeOpenFun):
            with tgb.layout("1 3 1"):
                with tgb.part(class_name="card"):
                    tgb.text("### From", mode="md")
                    tgb.date(date="{fromdate}",
                             min="{mindate}", max="{maxdate}", on_change=onDateChnage, propagate=True)

                with tgb.part(class_name="card"):
                    with tgb.part():
                        tgb.text("Pipeline")
                        tgb.selector(
                            dropdown=True, value="{Pipeline}", lov=POINT_PIPES, filter=True, width=r"100%")
                        tgb.html("br")
                        with tgb.layout("1 1"):
                            with tgb.part():
                                tgb.text("Cycle")
                                tgb.selector(
                                    dropdown=True, value="{Cycle}", lov=CYCLES, filter=True, width=r"98%")
                            with tgb.part():
                                tgb.text("Location Point")
                                tgb.selector(
                                    dropdown=True, value="{Location}", lov=["Delivery", "Receipt"], filter=True, width=r"100%")

                with tgb.part(class_name="card"):
                    tgb.text("### To", mode="md")
                    tgb.date(date="{todate}",
                             min="{mindate}", max="{maxdate}", on_change=onDateChnage, propagate=True)

            tgb.html("br")

            with tgb.layout("1 3 1"):
                with tgb.part():
                    pass
                with tgb.part(class_name="text-center"):
                    tgb.button(
                        label="Submit", class_name="plain apply_button", active="{SubmitActive}", on_action=onRangeSubmit)
                with tgb.part():
                    pass
