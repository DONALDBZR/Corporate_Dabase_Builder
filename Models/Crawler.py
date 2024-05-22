"""
The crawler of the application which will scrape the
Corporate and Business Registration Department application
of Mauritius Network Services to retrieve all of the data
that it has on the corporate that exists in Mauritius.

Authors:
    Andy Ewen Gaspard
"""


from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from Environment import Environment
from Models.Logger import Corporate_Database_Builder_Logger
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
from typing import List, Dict, Union
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging
import os
import json
import random


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
    __html_tags: List[WebElement]
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
    __corporate_metadata: List[Dict[str, Union[str, None]]]
    """
    The metadata of the companies that are in Mauritius.
    """
    __action_chains: ActionChains
    """
    ActionChains are a way to automate low level interactions
    such as mouse movements, mouse button actions, key press,
    and context menu interactions.  This is useful for doing
    more complex actions like hover over and drag and drop.
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
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
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

    def getHtmlTags(self) -> List[WebElement]:
        return self.__html_tags

    def setHtmlTags(self, html_tags: List[WebElement]) -> None:
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

    def getCorporateMetadata(self) -> List[Dict[str, Union[str, None]]]:
        return self.__corporate_metadata

    def setCorporateMetadata(self, corporate_metadata: List[Dict[str, Union[str, None]]]) -> None:
        self.__corporate_metadata = corporate_metadata

    def getActionChains(self) -> ActionChains:
        return self.__action_chains

    def setActionChains(self, action_chains: ActionChains) -> None:
        self.__action_chains = action_chains

    def __setServices(self) -> None:
        """
        Setting the services for the ChromeDriver.

        Returns:
            void
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

        Returns:
            void
        """
        self.setOptions(Options())
        self.getOptions().add_argument('--no-sandbox')
        self.getOptions().add_argument('--disable-dev-shm-usage')
        self.getOptions().add_argument('--disable-blink-features=AutomationControlled')
        self.getOptions().add_experimental_option(
            "excludeSwitches",
            ["enable-automation"]
        )
        self.getOptions().add_experimental_option('useAutomationExtension', False)
        self.getOptions().add_argument("start-maximized")
        self.getLogger().inform("The Crawler has been correctly configured!")

    def __randomDelay(self, delay: float) -> float:
        """
        Generating a random delay based on the delay that has been
        calculated by the application.

        Parameters:
            delay: float: The delay that has been calculated by the application.

        Returns:
            float
        """
        minimum_delay: float = delay
        maximum_delay: float = delay * 4
        return random.uniform(minimum_delay, maximum_delay)

    def __moveMouse(self, element: WebElement) -> None:
        """
        Replicating the way the a human being will navigate by using
        a mouse.

        Parameters:
            element: WebElement: The DOM Element

        Returns:
            void
        """
        range_limit: int = random.randint(8, 16)
        delay: float = self.__randomDelay(
            random.random() * 2
        )
        self.setActionChains(ActionChains(self.getDriver()))
        self.getActionChains().move_to_element(element)
        for index in range(range_limit):
            horizontal_offset: int = random.randint(-5, 5)
            vertical_offset: int = random.randint(-5, 5)
            self.getActionChains().move_by_offset(horizontal_offset, vertical_offset)
        self.getActionChains().move_to_element(element).perform()
        time.sleep(delay)

    def __typeCharacters(self, element: WebElement, payload: str) -> None:
        """
        Typing the characters from the payload given the same as a
        human being would have done it.

        Parameters:
            element: WebElement: The DOM element
            payload: string: The payload to be injected

        Returns:
            void
        """
        for index in range(0, len(payload), 1):
            delay: float = 60 / 200
            delay = self.__randomDelay(delay)
            element.send_keys(payload[index])
            time.sleep(delay)

    def enterTarget(self) -> None:
        """
        Entering the target.

        Returns:
            void
        """
        delay: float = self.__randomDelay(
            self.ENV.calculateDelay(
                self.getTarget()
            )
        )
        self.getLogger().inform(
            f"Entering the target.\nDelay: {delay}s\nTarget: {self.getTarget()}"
        )
        self.getDriver().get(self.getTarget())
        time.sleep(delay)

    def retrieveCorporateMetadata(self, date_from: str, date_to: str, coefficient: int) -> Dict[str, int]:
        """
        Retrieving corporate metadata about the companies that
        operate in Mauritius.

        Parameters:
            date_from: str: The start date of the search.
            date_to: str: The end date of the search.
            coeffcient: float: This coefficient changes depending the handlers.

        Returns:
            {status: int, amount: int}
        """
        delay: float = (
            (
                self.ENV.calculateDelay(date_from) +
                self.ENV.calculateDelay(date_to)
            ) / 2
        ) * (
            1.1 ** coefficient
        )
        delay = self.__randomDelay(
            delay
        )
        amount: int
        response: Dict[str, int] = {}
        self.setHtmlTag(
            self.getDriver().find_element(
                By.XPATH,
                f"{self.ENV.getTargetApplicationRootXpath()}/cbris-header/div/div/form/div/div[2]/div[2]/div[1]/input"
            )
        )
        self.__moveMouse(
            self.getHtmlTag()
        )
        self.getHtmlTag().send_keys(date_from)
        time.sleep(delay)
        self.getLogger().inform(
            f"The start date has been injected.\nDate From: {date_from}\nDelay: {delay} s"
        )
        self.setHtmlTag(
            self.getDriver().find_element(
                By.XPATH,
                f"{self.ENV.getTargetApplicationRootXpath()}/cbris-header/div/div/form/div/div[2]/div[2]/div[2]/input"
            )
        )
        self.__moveMouse(
            self.getHtmlTag()
        )
        self.getHtmlTag().send_keys(date_to)
        time.sleep(delay)
        self.getLogger().inform(
            f"The end date has been injected.\nDate To: {date_to}\nDelay: {delay} s"
        )
        self.setHtmlTag(
            self.getDriver().find_element(
                By.XPATH,
                f"{self.ENV.getTargetApplicationRootXpath()}/cbris-header/div/div/form/div/div[2]/div[3]/div[2]/button"
            )
        )
        self.__moveMouse(
            self.getHtmlTag()
        )
        self.handleSearch()
        time.sleep(delay)
        data_amount: str = self.getDataAmount(delay, coefficient)
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

    def getDataAmount(self, delay: float, coefficient: int) -> str:
        """
        Retrieving the amount of data that the targeted application
        currently has.

        Parameters:
            delay: float: The amount of time that the application has to wait in seconds.
            coeffcient: int: This coefficient changes depending the handlers.

        Returns:
            string
        """
        data_amount_element: WebElement = self.getDriver().find_element(
            By.XPATH,
            f"{self.ENV.getTargetApplicationRootXpath()}/cbris-search-results/lib-mns-universal-table/div/div[2]/mat-paginator/div/div/div[2]/div"
        )
        search_button: WebElement = self.getDriver().find_element(
            By.XPATH,
            f"{self.ENV.getTargetApplicationRootXpath()}/cbris-header/div/div/form/div/div[2]/div[3]/div[2]/button"
        )
        dataset: str = data_amount_element.text
        loading_icon: WebElement
        if "1 – 10 of " in dataset:
            self.getLogger().inform(
                f"Search in progress!\nDataset Amount: {dataset.replace('1 – 10 of ', '')}\nDelay: {delay} s\nCo-efficient: {coefficient}"
            )
            return dataset.replace("1 – 10 of ", "")
        else:
            coefficient += 1
            delay = delay * (1.1 ** coefficient)
            self.getLogger().error(
                f"The search has failed and the dataset amount cannot be recovered!  The application will try again.\nDelay: {delay} s\nCo-efficient: {coefficient}"
            )
            loading_icon = self.getDriver().find_element(
                By.TAG_NAME,
                "cbris-spinner"
            )
            self.setHtmlTag(loading_icon)
            self.getDriver().execute_script(
                "arguments[0].style.display = 'none';",
                self.getHtmlTag()
            )
            self.interceptCookie()
            self.setHtmlTag(search_button)
            self.handleSearch()
            time.sleep(delay)
            return self.getDataAmount(delay, coefficient)

    def scrapeMetadata(self, amount_data_found: int, amount_data_per_page: int, amount: int, delay: float) -> None:
        """
        Scraping the metadata from the target's application.

        Parameters:
            amount_data_found: int: The amount of data that the crawler has found.
            amount_data_per_page: int: The amount of data per page.
            amount: int: The total amount of data.
            delay: float: The amount of time in seconds that the crawler will wait to not get caught by the bot detection.

        Returns:
            void
        """
        self.setCorporateMetadata([])
        data_amount: int = amount
        amount_page: int = int(amount / amount_data_per_page)
        table_body = self.getHtmlTag()
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
            done: float = (amount_data_found / amount) * 100
            self.getLogger().debug(
                f"The extraction of corporate metadata is in progress.\nAmount of data found: {amount_data_found}\nIteration: {index}\nDone: {done}%"
            )
            self.writeCache()
            self.nextPage(delay)
            self.setHtmlTag(
                self.getDriver().find_element(
                    By.XPATH,
                    self.ENV.getTargetApplicationRootXpath()
                )
            )

    def elementInViewport(self) -> bool:
        """
        Verifying that the element is in the viewport.

        Returns:
            boolean
        """
        viewport_height: int = int(
            self.getDriver().execute_script("return window.innerHeight;")
        )
        element_top: int = int(
            self.getDriver().execute_script(
                "return arguments[0].getBoundingClientRect().top;",
                self.getHtmlTag()
            )
        )
        element_bottom: int = int(
            self.getDriver().execute_script(
                "return arguments[0].getBoundingClientRect().bottom;",
                self.getHtmlTag()
            )
        )
        return (0 <= element_top <= viewport_height) and (0 <= element_bottom <= viewport_height)

    def scrollIntoViewport(self) -> None:
        """
        Scrolling into viewport.

        Returns:
            void
        """
        if not self.elementInViewport():
            self.getDriver().execute_script(
                "arguments[0].scrollIntoView(true);",
                self.getHtmlTag()
            )
        else:
            return None

    def nextPage(self, delay: float) -> None:
        """
        Going to the next page.

        Parameters:
            delay: float: The amount of time for the application to wait before execution.

        Returns:
            void
        """
        try:
            time.sleep(delay)
            self.setHtmlTag(
                self.getDriver().find_element(
                    By.XPATH,
                    f"{self.ENV.getTargetApplicationRootXpath()}/cbris-search-results/lib-mns-universal-table/div/div[2]/mat-paginator/div/div/div[2]/button[3]"
                )
            )
            self.__moveMouse(
                self.getHtmlTag()
            )
            self.getHtmlTag().click()
        except ElementClickInterceptedException:
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

        Returns:
            void
        """
        file_name: str = f"{time.time()}.json"
        file = open(
            f"{self.ENV.getDirectory()}/Cache/CorporateDataCollection/{file_name}",
            "w"
        )
        file.write(
            json.dumps(self.getCorporateMetadata(), indent=4)
        )
        file.close()
        self.getLogger().inform("The data has been written to the cache.")

    def readCache(self) -> None:
        """
        Reading data from the cache directory.

        Returns:
            void
        """
        files = os.listdir(
            f"{self.ENV.getDirectory()}/Cache/CorporateDataCollection"
        )
        if len(files) > 0:
            file = open(
                f"{self.ENV.getDirectory()}/Cache/CorporateDataCollection/{max(files)}",
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

        Returns:
            void
        """
        try:
            self.setHtmlTag(
                self.getDriver().find_element(
                    By.XPATH,
                    f"{self.ENV.getTargetApplicationRootXpath()}/cbris-policy/div/div/button[1]"
                )
            )
            self.__moveMouse(
                self.getHtmlTag()
            )
            self.getHtmlTag().click()
            self.getLogger().inform("The cookie has been intercepted!")
        except NoSuchElementException:
            self.getLogger().error("The cookie has already been intercepted!")

    def getPageTableData(self, amount_data_found: int, amount: int) -> None:
        """
        Retrieving the corporate metadata that is in the table which
        is generally displayed in a way order.

        Parameters:
            amount_data_found: int: The amount of data that the crawler has found.
            amount: int: The total amount of data.

        Returns:
            void
        """
        rows: List[WebElement] = self.getHtmlTags()
        for index in range(0, len(rows), 1):
            self.setHtmlTags(
                rows[index].find_elements(
                    By.TAG_NAME,
                    "td"
                )
            )
            data: Dict[str, Union[str, None]] = {
                "business_registration_number": None,
                "name": self.getHtmlTags()[1].text,
                "file_number": self.getHtmlTags()[2].text,
                "category": self.getHtmlTags()[3].text,
                "date_incorporation": self.getHtmlTags()[4].text,
                "nature": self.getHtmlTags()[5].text,
                "status": self.getHtmlTags()[6].text,
            }
            amount_data_found += self.checkCorporateMetadata(data)
            done: float = (amount_data_found / amount) * 100
            self.getLogger().inform(
                f"Retrieving corporate metadata.\nPercentage Done: {done}%\nBRN: {data['business_registration_number']}\nName: {data['name']}\nFile Number: {data['file_number']}\nCategory: {data['category']}\nDate of Incorporation: {data['date_incorporation']}\nNature: {data['nature']}\nStatus: {data['status']}"
            )

    def checkCorporateMetadata(self, data: Dict[str, Union[str, None]]) -> int:
        """
        Checking the corporate metadata against the corporate
        metadata from the cache.

        Parameters:
            data: {business_registration_number: null, name: string, file_number: string, category: string, date_incorporation: string, nature: string, status: string}: The corporate metadata of a company.

        Returns:
            int
        """
        company_names: List[str] = []
        for index in range(0, len(self.getCorporateMetadata()), 1):
            company_names.append(
                str(self.getCorporateMetadata()[index]["name"])
            )
        if data["name"] in company_names:
            return 1
        else:
            self.getCorporateMetadata().append(data)
            return 1

    def handleSearch(self) -> None:
        """
        Verifying the component before injecting the correct
        component.

        Returns:
            void
        """
        try:
            self.getHtmlTag().click()
        except ElementClickInterceptedException:
            self.getLogger().error(
                f"The search button cannot be clicked!  Injecting the component needed!\nStatus: 401\nX-Path: {self.ENV.getTargetApplicationRootXpath()}/cbris-header/div/div/form/div/div[2]/div[3]/div[2]/button"
            )
            self.getDriver().execute_script(
                "arguments[0].removeAttribute('disabled');",
                self.getHtmlTag()
            )
            self.handleSearch()
