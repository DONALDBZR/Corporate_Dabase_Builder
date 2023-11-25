from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from Classes.Environment import Environment


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
    
    def __init__(self) -> None:
        """
        Initializing the application which will go on the target to
        scrape the data needed.
        """
        ENV = Environment()
        self.setTarget(ENV.getTarget())
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

    def __setServices(self) -> None:
        """
        Setting the services for the ChromeDriver.

        Return:
            (void)
        """
        self.setServices(Service(ChromeDriverManager().install()))

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