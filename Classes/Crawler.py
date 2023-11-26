from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from Classes.Environment import Environment
from Classes.Logger import Corporate_Database_Builder_Logger
import time
import logging


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

    def retrieveCorporateMetadata(self, date_from: str, date_to: str) -> dict:
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
        time.sleep(delay)
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
        self.scrapeMetadata(0, 10, amount, delay)
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
        return response