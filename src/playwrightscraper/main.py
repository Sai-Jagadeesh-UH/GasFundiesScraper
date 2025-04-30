from taipy.gui import Gui, Markdown
import taipy.gui.builder as tgb
from utils import getStats
from botConfig import PATH_LIST
from pages import StatusChecker, PointCapPage, SegmentCapPage, StorageCapPage, NoNoticeActivityPage, DataPreview
from azurepush import pushFiles
# from flask import Flask

df = None


def on_navigate(state, page_name: str):
    if page_name == "status":
        state.df = getStats()
        with tgb.Page() as statustable:
            with tgb.part(class_name="card"):
                tgb.table(data="{df}", filter=True, sortable=True)
        state.df_status.update_content(state, statustable)
        pushFiles()
        return "status"
    return page_name


with tgb.Page() as homepage:
    with tgb.part(class_name="container-logo"):
        tgb.image((PATH_LIST["IMAGES_PATH"] / r"gasfundies.webp"))

    tgb.navbar(lov=[("/pointcap", "Point Capacity"),
                    ("/segmentcap", "Segment Capacity"),
                    ("/storagecap", "Storage Capacity"),
                    ("/nonoticeactivity", "No Notice Activity"),
                    ("/status", "Runs Status")
                    ])

    tgb.html("br")

pagelist = {
    "/": homepage,
    "pointcap": PointCapPage,
    "segmentcap": SegmentCapPage,
    "storagecap": StorageCapPage,
    "nonoticeactivity": NoNoticeActivityPage,
    "status": StatusChecker
}

# app = Flask(__name__)

gui = Gui(pages=pagelist)
df_status = gui.add_partial(Markdown("<|{df}|table|>"))


# gui.run(title="GasFundies", debug=False,
#         allow_unsafe_werkzeug=True, run_server=False)

if __name__ == '__main__':
    # app.run(debug=False, threaded=True,  port=5000)
    gui.run(title="GasFundies", debug=False, port=5000)
