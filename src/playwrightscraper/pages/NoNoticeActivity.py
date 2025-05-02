from taipy.gui import notify, navigate
import taipy.gui.builder as tgb
from datetime import date, timedelta
from .pageVars import getPipeCode, NO_NOTICE_PIPES
from bots import NoNoticeActBot
from botConfig import setNoNoticeActConfig
from azurepush import pushFiles


def isActive(x: bool, state):
    for i in ["pointcap", "segmentcap", "storagecap", "nonoticeactivity"]:
        state[i].SubmitActive = x


def on_page_load(state):
    state.singleOpen = True
    state.rangeOpen = False

    Today = date.today()
    days90 = timedelta(days=94)

    state.mindate = Today - days90
    state.maxdate = Today - timedelta(days=5)

    state.fromdate = Today - timedelta(days=6)
    state.todate = Today - timedelta(days=5)
    state.ondate = Today - timedelta(days=5)

    state.Location = "DRN"
    state.Pipeline = "Natural Gas Pipeline"


def onSubmit(state):
    LocationDict = {"DRN": "drn", "PIN": "pin"}
    configuration = {
        # "headLess": False,
        "targetDate": state.ondate,
        "fileType": LocationDict.get(state.Location, "error"),
        "pipeLine":  getPipeCode(state.Pipeline),
    }
    print(configuration)
    if configuration["fileType"] == "error":
        notify(state, notification_type="error",
               message="Please check Location")
        # state.SubmitActive = False
        isActive(False, state)
        return
    if configuration["pipeLine"] == "error":
        notify(state, notification_type="error",
               message="Please check pipeLine")
        return

    notify(state, notification_type="info",
           message=f"Bot is running for {configuration['targetDate']} please wait...")
    # state.SubmitActive = False
    isActive(False, state)
    setNoNoticeActConfig(**configuration)
    NoNoticeActBot().scrape()
    # state.SubmitActive = True
    isActive(True, state)
    notify(state, notification_type="info",
           message=f'Scrape for {configuration["pipeLine"]} pipeline {state.Location} on {configuration["targetDate"]} is complete')
    # pushFiles()
    # navigate(state, "preview")


def onRangeSubmit(state):

    LocationDict = {"DRN": "drn", "PIN": "pin"}
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

        }
        print(configuration)
        if configuration["fileType"] == "error":
            notify(state, notification_type="error",
                   message="Please check Location")
            # state.SubmitActive = False
            isActive(False, state)
            return
        if configuration["pipeLine"] == "error":
            notify(state, notification_type="error",
                   message="Please check pipeLine")
            return

        notify(state, notification_type="info",
               message=f"Bot is running for {configuration['targetDate']} please wait...")
        # state.SubmitActive = False
        isActive(False, state)
        setNoNoticeActConfig(**configuration)
        NoNoticeActBot().scrape()
        # state.SubmitActive = True
        isActive(True, state)
        notify(state, notification_type="info",
               message=f'Scrape for {configuration["pipeLine"]} pipeline {state.Location} on {configuration["targetDate"]} is complete')
        currentdate = currentdate + timedelta(days=1)
        # pushFiles()
        # navigate(state, "preview")


singleOpen = True
rangeOpen = False
SubmitActive = True

Today = date.today()
days90 = timedelta(days=94)


mindate = Today - days90
maxdate = Today - timedelta(days=5)

fromdate = Today - timedelta(days=6)
todate = Today - timedelta(days=5)
ondate = Today - timedelta(days=5)


Location = "DRN"
Pipeline = "Natural Gas Pipeline"


def onDateChnage(state):
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


with tgb.Page() as NoNoticeActivityPage:

    with tgb.part(class_name="card"):
        with tgb.expandable(title="Run for a date", expanded="{singleOpen}", on_change=singleOpenFun):
            with tgb.layout("2 1"):
                with tgb.part(class_name="card"):
                    tgb.text("Pipeline")
                    tgb.selector(
                        dropdown=True, value="{Pipeline}", lov=NO_NOTICE_PIPES, filter=True, width="100%",)
                    tgb.html("br")
                    tgb.text("Location Point")
                    tgb.selector(
                        dropdown=True, value="{Location}", lov=["DRN", "PIN"], filter=True, width=r"60%")

                with tgb.part(class_name="card"):
                    tgb.text("### On", mode="md")
                    tgb.date(date="{ondate}", min="{mindate}",
                             max="{maxdate}")
                    tgb.html("br")
                    tgb.button(label="Submit",
                               class_name="plain apply_button", on_action=onSubmit, active="{SubmitActive}")

    with tgb.part(class_name="card"):
        with tgb.expandable(title="Run for a period", expanded="{rangeOpen}", on_change=rangeOpenFun):
            with tgb.layout("1 3 1"):
                with tgb.part(class_name="card"):
                    tgb.text("### From", mode="md")
                    tgb.date(date="{fromdate}",
                             min="{mindate}", max="{maxdate}", on_change=onDateChnage)

                with tgb.part(class_name="card"):
                    tgb.text("Pipeline")
                    tgb.selector(
                        dropdown=True, value="{Pipeline}", lov=NO_NOTICE_PIPES, filter=True, width=r"100%")
                    tgb.html("br")
                    tgb.text("Location Point")
                    tgb.selector(
                        dropdown=True, value="{Location}", lov=["DRN", "PIN"], filter=True, width=r"60%")

                with tgb.part(class_name="card"):
                    tgb.text("### To", mode="md")
                    tgb.date(date="{todate}",
                             min="{mindate}", max="{maxdate}", on_change=onDateChnage)

            tgb.html("br")

            with tgb.layout("1 3 1"):
                with tgb.part():
                    pass
                with tgb.part(class_name="text-center"):
                    tgb.button(
                        label="Submit", class_name="plain apply_button", on_action=onRangeSubmit, active="{SubmitActive}")
                with tgb.part():
                    pass
