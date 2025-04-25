from playwright.sync_api import sync_playwright
from pathlib import Path
from datetime import date, timedelta
from time import sleep
from utils import log
from botConfig import NoNoticeActConfig, PATH_LIST
from utils import Custom_Error, startStats, endStats
import sys
from azurepush import pushFiles


class NoNoticeActBot:

    def __init__(self):

        config = NoNoticeActConfig()

        # log(f"""setting Config \n{config}""")
        for key, val in config.items():
            setattr(self, key, val)

        self.downDir = PATH_LIST[self.downDir]

        if (not hasattr(self, "targetDate")):
            log(f"targetDate missing setting it to {date.today()}")
            self.targetDate = date.today() - timedelta(days=4)

        if (not hasattr(self, "fileType")):
            log(f"fileType missing setting it to {None}")
            self.fileType = None

        Path(self.downDir).mkdir(exist_ok=True)
        self.url = rf"https://pipeline2.kindermorgan.com/Capacity/NoNotice.aspx?code={self.pipeLine}"

    def scrape(self):
        isSuccess = "Success"

        if (self.targetDate > date.today() - timedelta(days=4)):
            log("targetDate is not allowed")
            return

        if (self.fileType is None):
            self.fileType = "drn"
            try:
                startStats("NoNoticeActivity", self)
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
            pushFiles("nonotice")
            sleep(7)

            self.fileType = "pin"
            try:
                startStats("NoNoticeActivity", self)
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
            pushFiles("nonotice")
        else:
            try:
                startStats("NoNoticeActivity", self)
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
            pushFiles("nonotice")

    def scrapeIndividual(self):
        if (self.targetDate > date.today() - timedelta(days=4)):
            log(f"{self.targetDate} is not available, retrieving latest available file")
            self.targetDate = date.today() - timedelta(days=4)
        scrapeday = self.targetDate.strftime(r'%m%d%Y')
        fileType = self.fileType
        downDir = Path(self.downDir)

        log(f"scraping No Notice Activity {fileType} file for {scrapeday}")
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=self.headLess, slow_mo=10)
            page = browser.new_page()
            page.goto(self.url)
            print("please dont quit.....")
            sleep(5)

            # select the radio buttons first
            if (fileType == "drn"):
                # WebSplitter1_tmpl1_ContentPlaceHolder1_rbDRN
                fileselector = page.locator(
                    "input#WebSplitter1_tmpl1_ContentPlaceHolder1_rbDRN")
            else:
                # WebSplitter1_tmpl1_ContentPlaceHolder1_rbPIN
                fileselector = page.locator(
                    "input#WebSplitter1_tmpl1_ContentPlaceHolder1_rbPIN")

            fileselector.click()

            # bodytext igte_NautilusEditInContainer
            dateselector = page.locator(
                "input.bodytext.igte_NautilusEditInContainer")
            dateselector.click()

            for i in scrapeday:
                page.keyboard.press(f"Digit{i}")

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
                filename = self.pipeLine + r"_" + scrapeday + fileType.upper() + r"." + \
                    download.suggested_filename.split(".", 2)[-1]
                download.save_as(downDir / filename)
                log(filename + " saved")

            browser.close()
