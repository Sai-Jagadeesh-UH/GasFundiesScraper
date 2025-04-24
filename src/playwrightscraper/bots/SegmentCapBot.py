from playwright.sync_api import sync_playwright
import pathlib
from datetime import date
from time import sleep
from utils import log
from botConfig import SegmentCapConfig
from utils import Custom_Error, startStats, endStats
import sys
from azurepush import pushFiles


class SegmentCapBot:

    def __init__(self):
        config = SegmentCapConfig()

        # log(f"""setting Config \n{config}""")
        for key, val in config.items():
            setattr(self, key, val)

        if (not hasattr(self, "basePath")):
            log("basepath missing setting it")
            self.basePath = pathlib.Path(r"./")
            self.downDir = self.basePath / pathlib.Path(r"/downs/")

        if (not hasattr(self, "targetDate")):
            log(f"targetDate missing setting it to {date.today()}")
            self.targetDate = date.today()

        if (not hasattr(self, "cycleSelector")):
            if (self.targetDate < date.today()):
                log(f"Cycle Selector is missing setting it to INTRADAY 3")
                self.cycleSelector = "INTRADAY 3"
            else:
                log(f"Cycle Selector is missing setting it to EVENING")
                self.cycleSelector = "EVENING"

        pathlib.Path(self.downDir).mkdir(exist_ok=True)
        self.url = rf"https://pipeline2.kindermorgan.com/Capacity/OpAvailSegment.aspx?code={self.pipeLine}"

    def scrape(self):
        isSuccess = "Success"
        if (self.pipeLine not in self.pipeGroups):
            log(f"{self.pipeLine} does not have Segment Capacity Data")
            return

        try:
            startStats("SegmentCapacity", self)
            self.scrapeIndividual()
        except Exception:
            log(
                f"something went wrong at {self.targetDate} retrying[1].....")
            sleep(5)
            try:
                self.scrapeIndividual()
            except Exception:
                log(
                    f"something went wrong at {self.targetDate} retrying[2].....")
                sleep(5)
                try:
                    self.scrapeIndividual()
                except Exception:
                    log(
                        f"something went wrong at {self.targetDate} retrying[3].....")
                    sleep(5)
                    try:
                        self.scrapeIndividual()
                    except Exception as e:
                        log(
                            f"something went wrong at {self.targetDate} Errored " + "x"*30)
                        isSuccess = "Failed"
                        raise Custom_Error(e, sys)
                    finally:
                        pass
        endStats(isSuccess)
        pushFiles("segment")

    def scrapeIndividual(self):
        scrapeday = self.targetDate.strftime(r'%m%d%Y')
        downDir = pathlib.Path(self.downDir)

        log(f"scraping Segment Capacity for {scrapeday}")
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=self.headLess, slow_mo=10)
            page = browser.new_page()
            page.goto(self.url)
            print("please dont quit.....")
            sleep(5)
            dateselector = page.locator(
                "input.bodytext.igte_NautilusEditInContainer")
            dateselector.click()

            for i in scrapeday:
                page.keyboard.press(f"Digit{i}")

            cycleselector = page.locator("input.igdd_NautilusValueDisplay ")
            cycleselector.dblclick()

            for i in "BEST AVAILABLE":
                page.keyboard.press("Backspace")

            page.keyboard.type(self.cycleSelector, delay=100)

            page.keyboard.press("Enter")

            # page.keyboard.press("Enter")
            # Start waiting for the download
            with page.expect_download() as download_info:
                # Perform the action that initiates download
                page.locator(
                    "input#WebSplitter1_tmpl1_ContentPlaceHolder1_HeaderBTN1_btnDownload").click()
                download = download_info.value
                # Wait for the download process to complete and save the downloaded file somewhere
                filename = self.pipeLine + r"_" + scrapeday + "SegmentCapacity" + rf"_{self.cycleSelector.replace(' ','')}" + r"." + \
                    download.suggested_filename.split(".", 2)[-1]
                download.save_as(downDir / filename)
                log(filename + " saved")

            browser.close()
