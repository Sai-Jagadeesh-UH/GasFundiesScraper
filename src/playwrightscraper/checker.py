from taipy import Gui
import taipy.gui.builder as tgb

with tgb.Page() as root_page:
    tgb.text("# Multi-page application", mode="md")

with tgb.Page() as home_page:
    tgb.text("# Home", mode="md")

with tgb.Page() as about_page:
    tgb.text("# About", mode="md")

pages = {
    "/": root_page,
    "home": home_page,
    "about": about_page
}

Gui(pages=pages).run()
