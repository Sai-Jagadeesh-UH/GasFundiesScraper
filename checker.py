from playwright.sync_api import sync_playwright
import pathlib
from time import sleep

from playwright.sync_api import sync_playwright

# url = r"https://pipeline2.kindermorgan.com/Capacity/OpAvailSegment.aspx?code=NGPL"
url = rf"https://pipeline2.kindermorgan.com/Capacity/OpAvailPoint.aspx?code=NGPL"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    page.goto(url)
    # bodytext igte_NautilusEditInContainer
    dateselector = page.locator("input.bodytext.igte_NautilusEditInContainer")
    # WebSplitter1_tmpl1_ContentPlaceHolder1_HeaderBTN1_btnDownload
    dateselector.highlight()
    dateselector.click()

    for i in "04022025":
        page.keyboard.press(f"Digit{i}")

    cycleselector = page.locator("input.igdd_NautilusValueDisplay ")
    cycleselector.highlight()
    cycleselector.dblclick()

    for i in "BEST AVAILABLE":
        page.keyboard.press("Backspace")

    page.keyboard.type("INTRADAY 2", delay=100)

    page.keyboard.press("Enter")

    fileselector = page.locator(
        "input#WebSplitter1_tmpl1_ContentPlaceHolder1_rbReceipt")

    fileselector.click()

    with page.expect_download() as download_info:
        # Perform the action that initiates download
        page.locator(
            "input#WebSplitter1_tmpl1_ContentPlaceHolder1_HeaderBTN1_btnDownload").click()
        download = download_info.value
        # Wait for the download process to complete and save the downloaded file somewhere
        filename = r"Dummy." + download.suggested_filename.split(".", 2)[-1]
        download.save_as(pathlib.Path("./downs/") / filename)
        print("File saved succcessfully")

    browser.close()
