from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from Classes.Environment import Environment
from Classes.Logger import Corporate_Database_Builder_Logger
from selenium.webdriver.support.ui import WebDriverWait #type: ignore
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import ElementClickInterceptedException
import time
import logging
import os
import json


class Crawler:
    """
    The main web-scrapper which will scraope the data from the
    database needed.
    """
    __driver: WebDriver
    """
    Controls the ChromeDriver and allows you to drive the
    browser.
    """
    __html_tags: list[WebElement]
    """
    A list of HTML tags which are pieces of markup language
    used to indicate the beginning and end of an HTML element in
    an HTML document.
    """
    __html_tag: WebElement
    """
    An HTML tag which is pieces of markup language used to
    indicate the beginning and end of an HTML element in an HTML
    document.
    """
    __services: Service
    """
    It is responsible for controlling of chromedriver.
    """
    __options: Options
    """
    It is responsible for setting the options for the webdriver.
    """
    __target: str
    """
    The target on which the data will be taken from.
    """
    __logger: Corporate_Database_Builder_Logger
    """
    The logger that will all the action of the application.
    """
    ENV: Environment
    """
    The ENV file of the application which stores the important
    information which allows the application to operate
    smoothly.
    """
    __corporate_metadata: list[dict[str, str | None]]
    """
    The metadata of the companies that are in Mauritius.
    """
    __wait: WebDriverWait
    """
    The controller which allows the Web Driver to control its
    interactions with the components.
    """
    
    def __init__(self) -> None:
        """
        Initializing the application which will go on the target to
        scrape the data needed.
        """
        self.ENV = Environment()
        self.setLogger(Corporate_Database_Builder_Logger())
        self.getLogger().setLogger(logging.getLogger(__name__))
        self.setTarget(self.ENV.getTarget())
        self.__setServices()
        self.__setOptions()
        self.setDriver(
            webdriver.Chrome(
                self.getOptions(),
                self.getServices()
            )
        )
        self.getDriver().execute_cdp_cmd(
            "Network.setUserAgentOverride",
            {
                "userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
            }
        )
        self.getDriver().execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => false})"
        )
        self.getLogger().inform("The Crawler has been successfully initialized!")
        self.enterTarget()

    def getDriver(self) -> WebDriver:
        return self.__driver

    def setDriver(self, driver: WebDriver) -> None:
        self.__driver = driver

    def getHtmlTags(self) -> list[WebElement]:
        return self.__html_tags

    def setHtmlTags(self, html_tags: list[WebElement]) -> None:
        self.__html_tags = html_tags

    def getHtmlTag(self) -> WebElement:
        return self.__html_tag

    def setHtmlTag(self, html_tag: WebElement) -> None:
        self.__html_tag = html_tag

    def getServices(self) -> Service:
        return self.__services

    def setServices(self, services: Service) -> None:
        self.__services = services

    def getOptions(self) -> Options:
        return self.__options

    def setOptions(self, options: Options) -> None:
        self.__options = options

    def getTarget(self) -> str:
        return self.__target
    
    def setTarget(self, target: str) -> None:
        self.__target = target

    def getLogger(self) -> Corporate_Database_Builder_Logger:
        return self.__logger
    
    def setLogger(self, logger: Corporate_Database_Builder_Logger) -> None:
        self.__logger = logger

    def getCorporateMetadata(self) -> list[dict[str, str | None]]:
        return self.__corporate_metadata
    
    def setCorporateMetadata(self, corporate_metadata: list[dict[str, str | None]]) -> None:
        self.__corporate_metadata = corporate_metadata

    def getWait(self) -> WebDriverWait:
        return self.__wait
    
    def setWait(self, wait: WebDriverWait) -> None:
        self.__wait = wait

    def __setServices(self) -> None:
        """
        Setting the services for the ChromeDriver.

        Return:
            (void)
        """
        self.setServices(
            Service(
                ChromeDriverManager().install()
            )
        )
        self.getLogger().inform("The Web Driver has been succesfully installed!")

    def __setOptions(self) -> None:
        """
        Setting the options for the ChromeDriver.

        Return:
            (void)
        """
        self.setOptions(Options())
        self.getOptions().add_argument('--no-sandbox')
        self.getOptions().add_argument('--disable-dev-shm-usage')
        self.getOptions().add_argument('--disable-blink-features=AutomationControlled')
        self.getOptions().add_experimental_option("excludeSwitches", ["enable-automation"])
        self.getOptions().add_experimental_option('useAutomationExtension', False)
        self.getOptions().add_argument("start-maximized")
        self.getLogger().inform("The Crawler has been correctly configured!")

    def enterTarget(self) -> None:
        """
        Entering the target.

        Return:
            (void)
        """
        delay = self.ENV.calculateDelay(self.getTarget())
        self.getLogger().inform(
            f"Entering the target.\nDelay: {delay}s\nTarget: {self.getTarget()}"
        )
        self.getDriver().get(self.getTarget())
        time.sleep(delay)

    def retrieveCorporateMetadata(self, date_from: str, date_to: str) -> dict[str, int]:
        """
        Retrieving corporate metadata about the companies that
        operate in Mauritius.

        Parameters:
            date_from:  (str):  The start date of the search.
            date_to:    (str):  The end date of the search

        Return:
            (object)
        """
        delay: float = (self.ENV.calculateDelay(date_from) + self.ENV.calculateDelay(date_to)) / 2
        amount: int
        response: dict = {}
        print(f"Delay: {delay}s")
        self.setHtmlTag(
            self.getDriver().find_element(
                By.XPATH,
                f"{self.ENV.getTargetApplicationRootXpath()}/cbris-header/div/div/form/div/div[2]/div[2]/div[1]/input"
            )
        )
        self.getHtmlTag().send_keys(date_from)
        time.sleep(delay)
        self.setHtmlTag(
            self.getDriver().find_element(
                By.XPATH,
                f"{self.ENV.getTargetApplicationRootXpath()}/cbris-header/div/div/form/div/div[2]/div[2]/div[2]/input"
            )
        )
        self.getHtmlTag().send_keys(date_to)
        time.sleep(delay)
        self.setHtmlTag(
            self.getDriver().find_element(
                By.XPATH,
                f"{self.ENV.getTargetApplicationRootXpath()}/cbris-header/div/div/form/div/div[2]/div[3]/div[2]/button"
            )
        )
        self.getHtmlTag().click()
        wait_delay = delay * (1.1 ** 0)
        print(f"Wait Delay: {wait_delay}s")
        time.sleep(wait_delay)
        self.setWait(
            WebDriverWait(
                self.getDriver(),
                wait_delay
            )
        )
        self.getWait().until(
            expected_conditions.presence_of_element_located(
                (
                    By.XPATH,
                    f"{self.ENV.getTargetApplicationRootXpath()}/cbris-search-results/lib-mns-universal-table/div/div[2]/mat-paginator/div/div/div[2]/div"
                )
            )
        )
        data_amount = self.getDriver().find_element(
            By.XPATH,
            f"{self.ENV.getTargetApplicationRootXpath()}/cbris-search-results/lib-mns-universal-table/div/div[2]/mat-paginator/div/div/div[2]/div"
        ).text.replace("1 – 10 of ", "")
        amount = int(data_amount)
        self.getLogger().inform(
            f"Search completed for corporate metadata between {date_from} and {date_to}\nDate From: {date_from}\nDate To: {date_to}\nAmount: {amount}"
        )
        self.setHtmlTag(
            self.getDriver().find_element(
                By.XPATH,
                f"{self.ENV.getTargetApplicationRootXpath()}/cbris-search-results/lib-mns-universal-table/div/div[1]/table/tbody"
            )
        )
        table_body = self.getHtmlTag()
        self.interceptCookie()
        self.setHtmlTag(table_body)
        self.readCache()
        amount_data_found = len(self.getCorporateMetadata())
        self.scrapeMetadata(amount_data_found, 10, amount, delay)
        response = {
            "status": 200,
            "amount": amount
        }
        self.getLogger().inform(
            f"The metadata has been retrieved and stored in the cache database.\nStatus: {response['status']}\nAmount: {response['amount']}"
        )
        return response

    def scrapeMetadata(self, amount_data_found: int, amount_data_per_page: int, amount: int, delay: float) -> dict:
        """
        Scraping the metadata from the target's application.

        Parameters:
            amount_data_found:      (int):      The amount of data that the crawler has found.
            amount_data_per_page:   (int):      The amount of data per page.
            amount:                 (int):      The total amount of data.
            delay:                  (float):    The amount of time in seconds that the crawler will wait to not get caught by the bot detection.

        Return:
            (object)
        """
        response = {}
        self.setCorporateMetadata([])
        data_amount = amount
        amount_page = int(amount / amount_data_per_page)
        table_body = self.getHtmlTag()
        wait_delay = delay * (1.1 ** 0)
        print(f"Scrape Delay: {wait_delay}s")
        for index in range(0, amount_page, 1):
            self.readCache()
            self.setHtmlTags(
                table_body.find_elements(
                    By.TAG_NAME,
                    "tr"
                )
            )
            amount = data_amount
            self.getPageTableData(amount_data_found, amount)
            amount_data_found += amount_data_per_page
            done = (amount_data_found / amount) * 100
            self.getLogger().debug(
                f"The extraction of corporate metadata is in progress.\nAmount of data found: {amount_data_found}\nIteration: {index}\nDone: {done}%"
            )
            self.writeCache()
            self.nextPage(wait_delay)
            self.setHtmlTag(
                self.getDriver().find_element(
                    By.XPATH,
                    self.ENV.getTargetApplicationRootXpath()
                )
            )
        return response

    def nextPage(self, delay: float) -> None:
        """
        Going to the next page.

        Parameters:
            delay:  (float):    The amount of time for the application to wait before execution.

        Return:
            (void)
        """
        try:
            time.sleep(delay)
            self.setHtmlTag(
                self.getDriver().find_element(
                    By.XPATH,
                    f"{self.ENV.getTargetApplicationRootXpath()}/cbris-search-results/lib-mns-universal-table/div/div[2]/mat-paginator/div/div/div[2]/button[3]"
                )
            )
            self.getHtmlTag().click()
        except ElementClickInterceptedException:
            exception_delay = delay * 1.1
            self.setHtmlTag(
                self.getDriver().find_element(
                    By.TAG_NAME,
                    "cbris-spinner"
                )
            )
            self.getDriver().execute_script(
                "arguments[0].style.display = 'none';",
                self.getHtmlTag()
            )
            self.nextPage(delay)

    def writeCache(self) -> None:
        """
        Writing data to the cache directory.

        Return:
            (void)
        """
        file_name = f"{time.time()}.json"
        file = open(
            f"{self.ENV.getDirectory()}/Cache/{file_name}",
            "w"
        )
        file.write(json.dumps(self.getCorporateMetadata(), indent=4))
        file.close()
        self.getLogger().inform("The data has been written to the cache.")

    
    def readCache(self) -> None:
        """
        Reading data from the cache directory.

        Return:
            (void)
        """
        files = os.listdir(
            f"{self.ENV.getDirectory()}/Cache"
        )
        if len(files) > 0:
            file = open(
                f"{self.ENV.getDirectory()}/Cache/{max(files)}",
                "r"
            )
            self.setCorporateMetadata(json.load(file))
            file.close()
        else:
            self.setCorporateMetadata([])
        self.getLogger().inform("The data has been read from the cache!")
    
    def interceptCookie(self) -> None:
        """
        Intercepting the cookie in order not to be recognize as a
        bot.

        Return:
            (void)
        """
        self.setHtmlTag(
            self.getDriver().find_element(
                By.XPATH,
                f"{self.ENV.getTargetApplicationRootXpath()}/cbris-policy/div/div/button[1]"
            )
        )
        self.getHtmlTag().click()
        self.getLogger().inform("The cookie has been intercepted!")
    
    def getPageTableData(self, amount_data_found: int, amount: int) -> None:
        """
        Retrieving the corporate metadata that is in the table which
        is generally displayed in a way order.

        Parameters:
            amount_data_found:      (int):      The amount of data that the crawler has found.
            amount:                 (int):      The total amount of data.

        Return:
            (void)
        """
        rows = self.getHtmlTags()
        for index in range(0, len(rows), 1):
            self.setHtmlTags(
                rows[index].find_elements(
                    By.TAG_NAME,
                    "td"
                )
            )
            name = self.getHtmlTags()[1].text
            file_number = self.getHtmlTags()[2].text
            category = self.getHtmlTags()[3].text
            date_incorporation = self.getHtmlTags()[4].text
            nature = self.getHtmlTags()[5].text
            status = self.getHtmlTags()[6].text
            data: dict[str, str | None] = {
                "business_registration_number": None,
                "name": name,
                "file_number": file_number,
                "category": category,
                "date_incorporation": date_incorporation,
                "nature": nature,
                "status": status,
            }
            amount_data_found += self.checkCorporateMetadata(name, data)
            done = (amount_data_found / amount) * 100
            self.getLogger().inform(
                f"Retrieving corporate metadata.\nPercentage Done: {done}%\nBRN: {data['business_registration_number']}\nName: {data['name']}\nFile Number: {data['file_number']}\nCategory: {data['category']}\nDate of Incorporation: {data['date_incorporation']}\nNature: {data['nature']}\nStatus: {data['status']}"
            )
    
    def checkCorporateMetadata(self, name: str, data: dict[str, str | None]) -> int:
        """
        Checking the corporate metadata against the corporate
        metadata from the cache.

        Parameters:
            name:   (string):   The name of the company.
            data:   (object):   The corporate metadata of a company.

        Return:
            (int)
        """
        if any(name in data.values() for data in self.getCorporateMetadata()):
            return 1
        else:
            self.getCorporateMetadata().append(data)
            return 1