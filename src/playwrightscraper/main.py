from taipy.gui import Gui, State, notify, Markdown
import taipy.gui.builder as tgb
from datetime import datetime, date, timedelta
from pathlib import Path
from utils import getStats
from botConfig import PATH_LIST
from pages import StatusChecker, PointCapPage, SegmentCapPage, StorageCapPage, NoNoticeActivityPage, DataPreview
from azurepush import pushFiles
# from flask import Flask
import gevent.pywsgi

df = None

# flask_app = Flask(__name__)


def on_navigate(state, page_name: str):
    if page_name == "status":
        state.df = getStats()
        with tgb.Page() as statustable:
            with tgb.part(class_name="card"):
                tgb.table(data="{df}", filter=True, sortable=True)
        # pagecontent = Markdown("<|{df}|table|>")
        state.df_status.update_content(state, statustable)
        pushFiles()
        return "status"
    # if page_name == "preview":
    #     with open(PATH_LIST["TEMP_TXT"], 'w+') as file:
    #         filename = file.read()
    #     print(filename)
    #     state.df = processFiles(Path(filename))
    #     with tgb.Page() as previewtable:
    #         with tgb.part(class_name="card"):
    #             tgb.table(data="{df}", filter=True, sortable=True)
    #     # pagecontent = Markdown("<|{df}|table|>")
    #     state.df_preview.update_content(state, previewtable)
    #     pushFiles()
    #     return "preview"
    # else:
    #     print(state.SubmitActive, page_name)
    return page_name


with tgb.Page() as homepage:
    with tgb.part(class_name="container-logo"):
        tgb.image((PATH_LIST["IMAGES_PATH"] / r"gasfundies.webp"))

    tgb.navbar(lov=[("/pointcap", "Point Capacity"),
                    ("/segmentcap", "Segment Capacity"),
                    ("/storagecap", "Storage Capacity"),
                    ("/nonoticeactivity", "No Notice Activity"),
                    ("/status", "Runs Status"),
                    # ("/preview", "Preview")
                    ])

    tgb.html("br")


pagelist = {
    "/": homepage,
    "pointcap": PointCapPage,
    "segmentcap": SegmentCapPage,
    "storagecap": StorageCapPage,
    "nonoticeactivity": NoNoticeActivityPage,
    "status": StatusChecker,
    # "preview": DataPreview
    # "/status": None
}
# #21274A
gui = Gui(pages=pagelist)
df_status = gui.add_partial(Markdown("<|{df}|table|>"))

gui_app = gui.run(title="GasFundies", debug=False,
                  port="8000", allow_unsafe_werkzeug=True, run_server=False)


app_server = gevent.pywsgi.WSGIServer(('127.0.0.1', 8088), gui_app)
app_server.serve_forever()
# # if __name__ == "__main__":
# gui.run(title="GasFundies", debug=False,
#         port="8000", allow_unsafe_werkzeug=True)
