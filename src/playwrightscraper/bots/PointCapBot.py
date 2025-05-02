from playwright.sync_api import sync_playwright
import pathlib
from datetime import date
from time import sleep
from utils import log
from botConfig import PointCapConfig, PATH_LIST
from utils import Custom_Error, startStats, endStats
import sys
from azurepush import pushFiles, processFiles


class PointCapBot:

    def __init__(self):
        config = PointCapConfig()
        # log(f"""setting Config \n{config}""")
        for key, val in config.items():
            setattr(self, key, val)

        self.downDir = PATH_LIST[self.downDir]

        if (not hasattr(self, "fileType")):
            log(f"fileType missing setting it to {None}")
            self.fileType = None

        if (not hasattr(self, "cycleSelector")):
            if (self.targetDate < date.today()):
                log(f"Cycle Selector is missing setting it to INTRADAY 3")
                self.cycleSelector = "INTRADAY 3"
            else:
                log(f"Cycle Selector is missing setting it to EVENING")
                self.cycleSelector = "EVENING"

        pathlib.Path(self.downDir).mkdir(exist_ok=True)
        self.url = rf"https://pipeline2.kindermorgan.com/Capacity/OpAvailPoint.aspx?code={self.pipeLine}"

    def scrape(self):
        isSuccess = "Success"
        if (self.fileType is None):
            self.fileType = "del"
            try:
                startStats("PointCapacity", self)
                self.scrapeIndividual()
            except Exception:
                log(
                    f"something went wrong at {self.targetDate} {self.fileType} retrying[1].....")
                sleep(5)
                try:
                    self.scrapeIndividual()
                except Exception:
                    log(
                        f"something went wrong at {self.targetDate} {self.fileType} retrying[2].....")
                    sleep(5)
                    try:
                        self.scrapeIndividual()
                    except Exception:
                        log(
                            f"something went wrong at {self.targetDate} {self.fileType} retrying[3].....")
                        sleep(5)
                        try:
                            self.scrapeIndividual()
                        except Exception as e:
                            log(
                                f"something went wrong at {self.targetDate} {self.fileType} Errored " + "x"*30)
                            isSuccess = "Failed"
                            raise Custom_Error(e, sys)
                        finally:
                            log(f"Bot run {isSuccess}")
        # pushing files to adls
            endStats(isSuccess)
            if (isSuccess != "Failed"):
                pushFiles("point")

            sleep(7)

            self.fileType = "rec"
            try:
                startStats("PointCapacity", self)
                self.scrapeIndividual()
            except Exception:
                log(
                    f"something went wrong at {self.targetDate} {self.fileType} retrying[1].....")
                sleep(5)
                try:
                    self.scrapeIndividual()
                except Exception:
                    log(
                        f"something went wrong at {self.targetDate} {self.fileType} retrying[2].....")
                    sleep(5)
                    try:
                        self.scrapeIndividual()
                    except Exception:
                        log(
                            f"something went wrong at {self.targetDate} {self.fileType} retrying[3].....")
                        sleep(5)
                        try:
                            self.scrapeIndividual()
                        except Exception as e:
                            log(
                                f"something went wrong at {self.targetDate} {self.fileType} Errored " + "x"*30)
                            isSuccess = "Failed"
                            raise Custom_Error(e, sys)
                        finally:
                            log(f"Bot run {isSuccess}")
        # pushing files to adls
            endStats(isSuccess)
            if (isSuccess != "Failed"):
                pushFiles("point")

        else:
            try:
                startStats("PointCapacity", self)
                self.scrapeIndividual()
            except Exception:
                log(
                    f"something went wrong at {self.targetDate} {self.fileType} retrying[1].....")
                sleep(5)
                try:
                    self.scrapeIndividual()
                except Exception:
                    log(
                        f"something went wrong at {self.targetDate} {self.fileType} retrying[2].....")
                    sleep(5)
                    try:
                        self.scrapeIndividual()
                    except Exception:
                        log(
                            f"something went wrong at {self.targetDate} {self.fileType} retrying[3].....")
                        sleep(5)
                        try:
                            self.scrapeIndividual()
                        except Exception as e:
                            log(
                                f"something went wrong at {self.targetDate} {self.fileType} Errored " + "x"*30)
                            isSuccess = "Failed"
                            raise Custom_Error(e, sys)
                        finally:
                            log(f"Bot run {isSuccess}")
            endStats(isSuccess)
            if (isSuccess != "Failed"):
                pushFiles("point")

    def scrapeIndividual(self):
        scrapeday = self.targetDate.strftime(r'%m%d%Y')
        fileType = self.fileType
        downDir = pathlib.Path(self.downDir)

        log(f"scraping Point Capacity {fileType} file for {scrapeday}")
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

            if (fileType == "rec"):
                fileselector = page.locator(
                    "input#WebSplitter1_tmpl1_ContentPlaceHolder1_rbReceipt")
            else:
                fileselector = page.locator(
                    "input#WebSplitter1_tmpl1_ContentPlaceHolder1_rbDelivery")

            fileselector.click()

            # page.keyboard.press("Enter")
            # Start waiting for the download
            with page.expect_download() as download_info:
                # Perform the action that initiates download
                page.locator(
                    "input#WebSplitter1_tmpl1_ContentPlaceHolder1_HeaderBTN1_btnDownload").click()
                download = download_info.value
                # Wait for the download process to complete and save the downloaded file somewhere
                filename = self.pipeLine + r"_" + scrapeday + fileType.upper() + rf"_{self.cycleSelector.replace(' ', '')}" + r"." + \
                    download.suggested_filename.split(".", 2)[-1]
                download.save_as(downDir / filename)
                log(filename + " saved, pushing to blob")

            browser.close()
