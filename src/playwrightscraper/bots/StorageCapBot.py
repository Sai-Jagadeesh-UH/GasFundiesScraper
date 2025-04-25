from playwright.sync_api import sync_playwright
import pathlib
from datetime import date
from time import sleep
from utils import log
from botConfig import StorageCapConfig, PATH_LIST
from utils import Custom_Error, startStats, endStats
import sys
from azurepush import pushFiles


class StorageCapBot:

    def __init__(self):
        config = StorageCapConfig()

        # log(f"""setting Config \n{config}""")
        for key, val in config.items():
            setattr(self, key, val)

        self.downDir = PATH_LIST[self.downDir]

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
        self.url = rf"https://pipeline2.kindermorgan.com/Capacity/OpAvailStorage.aspx?code={self.pipeLine}"

    def scrape(self):
        isSuccess = "Success"
        if (self.pipeLine not in self.pipeGroups):
            log(f"{self.pipeLine} does not have Storage Capacity Data")
            return

        try:
            startStats("StorageCapacity", self)
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
                        log(f"Bot run {isSuccess}")
        endStats(isSuccess)
        pushFiles("storage")

    def scrapeIndividual(self):
        scrapeday = self.targetDate.strftime(r'%m%d%Y')
        downDir = pathlib.Path(self.downDir)

        log(f"scraping Storage Capacity for {scrapeday}")
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=self.headLess, slow_mo=10)
            page = browser.new_page()
            page.goto(self.url)
            print("please dont quit.....")
            sleep(5)
            dateselector = page.locator(
                "input.bodytext.igte_NautilusEditInContainer")
            # bodytext igte_NautilusEditInContainer
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
                # WebSplitter1_tmpl1_ContentPlaceHolder1_HeaderBTN1_btnDownload
                page.locator(
                    "input#WebSplitter1_tmpl1_ContentPlaceHolder1_HeaderBTN1_btnDownload").click()
                download = download_info.value
                # Wait for the download process to complete and save the downloaded file somewhere
                filename = self.pipeLine + r"_" + scrapeday + "StorageCapacity" + rf"_{self.cycleSelector.replace(' ','')}" + r"." + \
                    download.suggested_filename.split(".", 2)[-1]
                download.save_as(downDir / filename)
                log(filename + " saved")

            browser.close()
