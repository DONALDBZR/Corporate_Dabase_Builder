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
from Data.CompanyDetails import CompanyDetails
from Environment import Environment
from Models.Logger import Corporate_Database_Builder_Logger
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
from typing import List, Dict, Union, Tuple
from selenium.webdriver.common.action_chains import ActionChains
from Models.CompanyDetails import Company_Details
from datetime import datetime
import time
import logging
import os
import json
import random
import base64


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
    __company_details: Company_Details
    """
    The model which will interact exclusively with the Company
    Details.
    """

    def __init__(self) -> None:
        """
        Initializing the application which will go on the target to
        scrape the data needed.
        """
        self.ENV = Environment()
        self.setCompanyDetails(Company_Details())
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

    def getCompanyDetails(self) -> Company_Details:
        return self.__company_details

    def setCompanyDetails(self, company_details: Company_Details) -> None:
        self.__company_details = company_details

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
        maximum_delay: float = delay * 1.1
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

    def retrieveCorporateDocumentFile(self, company_details: CompanyDetails, coefficient: int) -> Dict[str, Union[int, Dict[str, Union[str, None, int]], bytes, None]]:
        """
        Retrieving the corporate document files based on the
        corporate metadata that are filled as parameters.

        Parameters:
            company_details: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}: The list of corporate metadata to be used for retrieving the corporate document files.
            coeffcient: float: This coefficient changes depending the handlers.

        Returns:
            {status: int, CompanyDetails: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}, DocumentFiles: bytes|null}
        """
        delay: float = self.__randomDelay(self.ENV.calculateDelay(company_details.name) * (1.1 ** coefficient))
        self.setHtmlTag(
            self.getDriver().find_element(
                By.XPATH,
                f"{self.ENV.getTargetApplicationRootXpath()}/cbris-header/div/div/form/div/div[1]/div[2]/div/input"
            )
        )
        self.__moveMouse(self.getHtmlTag())
        self.getHtmlTag().send_keys(company_details.name)
        time.sleep(delay)
        self.getLogger().inform(
            f"The payload has been injected.\nCompany Name: {company_details.name}\nDelay: {delay} s"
        )
        self.setHtmlTag(
            self.getDriver().find_element(
                By.XPATH,
                f"{self.ENV.getTargetApplicationRootXpath()}/cbris-header/div/div/form/div/div[2]/div[3]/div[2]/button"
            )
        )
        self.__moveMouse(self.getHtmlTag())
        self.handleSearch()
        time.sleep(delay)
        payload_amount = self.getDataAmountRetrieveCorporateDocumentFile(delay, coefficient)
        self.getLogger().inform(
            f"Search completed for the payload.\nCompany Name: {company_details.name}\nAmount: {payload_amount}"
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
        return self.handleCrawlerResponseRetrieveCorporateDocumentFile(
            self.scrapeDocumentFile(delay, company_details),
            company_details
        )

    def handleCrawlerResponseRetrieveCorporateDocumentFile(self, crawler: Dict[str, Union[int, Dict[str, Union[str, None, int]], bytes, None]], company_detail: CompanyDetails) -> Dict[str, Union[int, Dict[str, Union[str, None, int]], bytes, None]]:
        """
        Handling the response returned by the crawler and doing any
        data manipulation required on the data.

        Parameters:
            crawler: {status: int, CompanyDetails: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}, DocumentFiles: bytes | null}: The response from the crawler.
            company_detail: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}: The metadata of the company that is used as payload.

        Returns:
            {status: int, CompanyDetails: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}, DocumentFiles: bytes|null}
        """
        response: Dict[str, Union[int, Dict[str, Union[str, None, int]], bytes, None]]
        if crawler["status"] == 200:
            response = {
                "status": crawler["status"],
                "CompanyDetails": crawler["CompanyDetails"],
                "DocumentFiles": crawler["DocumentFiles"]
            }
        else:
            response = {
                "status": 404, 
                "CompanyDetails": {
                    "identifier": company_detail.identifier,
                    "business_registration_number": company_detail.business_registration_number,
                    "name": company_detail.name,
                    "file_number": company_detail.file_number,
                    "category": company_detail.category,
                    "date_incorporation": company_detail.date_incorporation,
                    "nature": company_detail.nature,
                    "status": company_detail.status,
                    "date_verified": int(time.time())
                },
                "DocumentFiles": None
            }
        self.getLogger().inform(
            f"The crawler has tried to retrieve the corporate document file!\nStatus: {response['status']}\nName: {company_detail.name}" # type: ignore
        )
        return response

    def getDataAmountRetrieveCorporateDocumentFile(self, delay: float, coefficient: int) -> int:
        """
        Retrieving the amount of data that the targeted application
        currently has.

        Parameters:
            delay: float: The amount of time that the application has to wait in seconds.
            coeffcient: int: This coefficient changes depending the handlers.

        Returns:
            int
        """
        search_button: WebElement = self.getDriver().find_element(
            By.XPATH,
            f"{self.ENV.getTargetApplicationRootXpath()}/cbris-header/div/div/form/div/div[2]/div[3]/div[2]/button"
        )
        loading_icon: WebElement
        table_body: WebElement = self.getDriver().find_element(
            By.XPATH,
            f"{self.ENV.getTargetApplicationRootXpath()}/cbris-search-results/lib-mns-universal-table/div/div[1]/table/tbody"
        )
        table_rows: List[WebElement] = table_body.find_elements(
            By.TAG_NAME,
            "tr"
        )
        if len(table_rows) > 0:
            self.getLogger().inform(
                f"Search in progress!\nDataset Amount: {len(table_rows)}\nDelay: {delay} s\nCo-efficient: {coefficient}"
            )
            return len(table_rows)
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
            return self.getDataAmountRetrieveCorporateDocumentFile(delay, coefficient)

    def getFileNumbers(self, file_numbers: List[str] = []) -> List[str]:
        """
        Retrieving the list of the file numbers from the result set
        of the corporate metadata.

        Parameters:
            file_numbers: [string]: The list of the file numbers to be used as initializer.

        Returns:
            [string]
        """
        for index in range(0, len(self.getHtmlTags()), 1):
            cells: List[WebElement] = self.getHtmlTags()[index].find_elements(
                By.TAG_NAME,
                "td"
            )
            file_number: str = cells[2].text
            file_numbers.append(file_number)
        return file_numbers

    def _addDifferentCorporateMetadata(self, identifier: int, file_number_identifier: int) -> None:
        """
        Verifying that the index of the corporate metadata is not
        equal to the index of the company needed for inserting the
        data correctly into the relational database server.

        Parameters:
            identifier: int: The index of the corporate metadata.
            file_number_identfier: int: The index of the file number.

        Returns:
            void
        """
        if identifier != file_number_identifier:
            cells: List[WebElement] = self.getHtmlTags()[identifier].find_elements(
                By.TAG_NAME,
                "td"
            )
            data: Dict[str, Union[str, None]] = {
                "business_registration_number": None,
                "name": str(cells[1].text),
                "file_number": str(cells[2].text),
                "category": str(cells[3].text),
                "date_incorporation": str(cells[4].text),
                "nature": str(cells[5].text),
                "status": str(cells[6].text)
            }
            corporate_metadata: Tuple[str, str, str, int, str, str] = (
                str(data["name"]),
                str(data["file_number"]),
                str(data["category"]),
                int(
                    datetime.strptime(
                        str(data["date_incorporation"]),
                        "%d/%m/%Y"
                    ).timestamp()
                ),
                str(data["nature"]),
                str(data["status"])
            )
            self.getCompanyDetails().addCompany(corporate_metadata) # type: ignore

    def addDifferentCorporateMetadata(self, file_number_identifier: int) -> None:
        """
        Adding the different corporate metadata into the relational
        database server.

        Parameters:
            file_number_identifier: int: The identifier of the file number.

        Returns:
            void
        """
        for index in range(0, len(self.getHtmlTags()), 1):
            self._addDifferentCorporateMetadata(index, file_number_identifier)

    def _scrapeDocumentFileFoundResultSetsByFileNumber(self, delay: float, company_detail: CompanyDetails, file_number_amount: int, file_numbers: List[str]) -> Dict[str, Union[int, Dict[str, Union[str, None, int]], bytes, None]]:
        """
        Scraping the corporate document file from the target's
        application specifically when there are results that are
        returned by the target's application by comparing the file
        numbers of the returned result set.

        Parameters:
            delay: float: The delay that the application will take to halt the operations of the application before resuming to the same way as a human being would to.
            company_detail: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}: The metadata of the company that is used as payload.
            file_number_amount: int: The amount of file numbers.
            file_numbers: [string]: The list of the file numbers.

        Returns:
            {status: int, CompanyDetails: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}, DocumentFiles: bytes | null}
        """
        if file_number_amount == 1:
            self.setHtmlTags(
                self.getHtmlTags()[0].find_elements(
                    By.TAG_NAME,
                    "td"
                )
            )
            return self.__scrapeDocumentFileFoundResultSets(delay, company_detail)
        else:
            file_number_identifier: int = file_numbers.index(company_detail.file_number)
            self.addDifferentCorporateMetadata(file_number_identifier)
            self.setHtmlTags(
                self.getHtmlTags()[file_number_identifier].find_elements(
                    By.TAG_NAME,
                    "td"
                )
            )
            return self.__scrapeDocumentFileFoundResultSets(delay, company_detail)

    def _scrapeDocumentFileFoundResultSets(self, delay: float, company_detail: CompanyDetails) -> Dict[str, Union[int, Dict[str, Union[str, None, int]], bytes, None]]:
        """
        Scraping the corporate document file from the target's
        application specifically when there are result sets that are
        returned by the target's application.

        Parameters:
            delay: float: The delay that the application will take to halt the operations of the application before resuming to the same way as a human being would to.
            company_detail: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}: The metadata of the company that is used as payload.

        Returns:
            {status: int, CompanyDetails: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}, DocumentFiles: bytes | null}
        """
        table_rows: List[WebElement] = self.getHtmlTags()
        if len(self.getHtmlTags()) > 1:
            table_data: List[str] = self.getFileNumbers()
            refined_table_data_length: int = len(list(set(table_data)))
            return self._scrapeDocumentFileFoundResultSetsByFileNumber(delay, company_detail, refined_table_data_length, table_data)
        else:
            self.setHtmlTags(
                table_rows[0].find_elements(
                    By.TAG_NAME,
                    "td"
                )
            )
            return self.__scrapeDocumentFileFoundResultSets(delay, company_detail)

    def __scrapeDocumentFileFoundResultSets(self, delay: float, company_detail: CompanyDetails) -> Dict[str, Union[int, Dict[str, Union[str, None, int]], bytes, None]]:
        """
        Verifying the amount the cells that are in the row to ensure
        that the crawler scrape the data correctly.

        Parameters:
            delay: float: The delay that the application will take to halt the operations of the application before resuming to the same way as a human being would to.
            company_detail: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}: The metadata of the company that is used as payload.

        Returns:
            {status: int, CompanyDetails: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}, DocumentFiles: bytes | null}
        """
        if len(self.getHtmlTags()) > 1:
            buttons_cell: WebElement = self.getHtmlTags()[7].find_element(
                By.TAG_NAME,
                "div"
            )
            print_button: WebElement = buttons_cell.find_elements(
                By.TAG_NAME,
                "fa-icon"
            )[1]
            self.__moveMouse(print_button)
            time.sleep(delay)
            print_button.click()
            time.sleep(delay)
            self.getDriver().switch_to.window(
                self.getDriver().window_handles[-1]
            )
            time.sleep(delay)
            file_downloader_response = self.downloadFile()
            return self.handleDocumentFileFoundIndividualRecord(file_downloader_response, company_detail) # type: ignore
        else:
            return {
                "status": 404,
                "CompanyDetails": {
                    "identifier": company_detail.identifier,
                    "business_registration_number": company_detail.business_registration_number,
                    "name": company_detail.name,
                    "file_number": company_detail.file_number,
                    "category": company_detail.category,
                    "date_incorporation": company_detail.date_incorporation,
                    "nature": company_detail.nature,
                    "status": company_detail.status,
                    "date_verified": company_detail.date_verified
                },
                "DocumentFiles": None
            }

    def handleDocumentFileFoundIndividualRecord(self, file_downloader: Dict[str, Union[int, bytes, None]], company_detail: CompanyDetails) -> Union[Dict[str, Union[int, Dict[str, Union[str, None, int]], bytes]], None]:
        """
        Handling the response given by the File downloader of the
        application.

        Parameters:
            file_downloader: {status: int, file: bytes|null}: The response from the file downloader.
            company_detail: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}: The metadata of the company that is used as payload.

        Returns:
            {status: int, CompanyDetails: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}, DocumentFiles: bytes} | void
        """
        if int(file_downloader["status"]) == 200: # type: ignore
            return {
                "status": int(file_downloader["status"]), # type: ignore
                "CompanyDetails": {
                    "identifier": company_detail.identifier,
                    "business_registration_number": company_detail.business_registration_number,
                    "name": company_detail.name,
                    "file_number": company_detail.file_number,
                    "category": company_detail.category,
                    "date_incorporation": company_detail.date_incorporation,
                    "nature": company_detail.nature,
                    "status": company_detail.status,
                    "date_verified": int(time.time())
                },
                "DocumentFiles": bytes(file_downloader["file"]) # type: ignore
            }
        else:
            return {
                "status": int(file_downloader["status"]), # type: ignore
                "CompanyDetails": {
                    "identifier": company_detail.identifier,
                    "business_registration_number": company_detail.business_registration_number,
                    "name": company_detail.name,
                    "file_number": company_detail.file_number,
                    "category": company_detail.category,
                    "date_incorporation": company_detail.date_incorporation,
                    "nature": company_detail.nature,
                    "status": company_detail.status,
                    "date_verified": int(time.time())
                },
                "DocumentFiles": None
            }

    def downloadFile(self) -> Dict[str, Union[int, bytes, None]]:
        """
        Downloading the file from the targeted application in order
        to store it into the relational database server.

        Returns:
            {status: int, file: bytes|null}
        """
        response: Dict[str, Union[int, bytes, None]]
        target_response: Union[int, str] = self.getDriver().execute_async_script(
            "var uri = arguments[0]; var callback = arguments[1]; var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'.charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder('ascii').decode(a)}; var xhr = new XMLHttpRequest(); xhr.responseType = 'arraybuffer'; xhr.onload = function(){ callback(toBase64(xhr.response)) }; xhr.onerror = function(){ callback(xhr.status) }; xhr.open('GET', uri); xhr.send();",
            self.getDriver().current_url
        )
        if type(target_response) == int:
            self.getLogger().error(f"The corporate document file cannot be downloaded for the moment.\nStatus: {target_response}")
            response = {
                "status": target_response,
                "file": None,
            }
        else:
            self.getLogger().inform(f"The corporate document file has been successfullly downloaded.\nStatus: 200")
            response = {
                "status": 200,
                "file": base64.b64decode(str(target_response))
            }
        return response

    def scrapeDocumentFile(self, delay: float, company_detail: CompanyDetails) -> Dict[str, Union[int, Dict[str, Union[str, None, int]], bytes, None]]:
        """
        Scraping the corporate document file from the target's
        application.

        Parameters:
            delay: float: The amount of time in seconds that the crawler will wait to not get caught by the bot detection.
            company_detail: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}: The metadata of the company that is used as payload.

        Returns:
            {status: int, CompanyDetails: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}, DocumentFiles: bytes | null}
        """
        self.setHtmlTags(
            self.getHtmlTag().find_elements(
                By.TAG_NAME,
                "tr"
            )
        )
        return self._scrapeDocumentFileFoundResultSets(delay, company_detail)

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
        data_amount: str = self.getDataAmountRetrieveCorporateMetadata(delay, coefficient)
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
        self.readCacheCorporateDataCollection()
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

    def getDataAmountRetrieveCorporateMetadata(self, delay: float, coefficient: int) -> str:
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
            return self.getDataAmountRetrieveCorporateMetadata(delay, coefficient)

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
            self.readCacheCorporateDataCollection()
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
            self.writeCacheCorporateDataCollection()
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
            self.scrollIntoViewport()
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

    def writeCacheCorporateDataCollection(self) -> None:
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

    def readCacheCorporateDataCollection(self) -> None:
        """
        Reading data from the cache directory.

        Returns:
            void
        """
        files: List[str] = os.listdir(f"{self.ENV.getDirectory()}/Cache/CorporateDataCollection")
        if len(files) > 0:
            file = open(f"{self.ENV.getDirectory()}/Cache/CorporateDataCollection/{max(files)}", "r")
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
        except ElementClickInterceptedException:
            self.getLogger().error("The cookie cannot be intercepted yet but the application will retry to intercept it!")
            delay: float = self.__randomDelay(10.00)
            loading_icon = self.getDriver().find_element(
                By.TAG_NAME,
                "cbris-spinner"
            )
            self.setHtmlTag(loading_icon)
            self.getDriver().execute_script(
                "arguments[0].style.display = 'none';",
                self.getHtmlTag()
            )
            time.sleep(delay)
            self.interceptCookie()


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
