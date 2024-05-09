"""
The module which will have the main corporate database
builder.

Authors:
    Andy Ewen Gaspard
"""


from Models.Crawler import Crawler
from Models.DatabaseHandler import Database_Handler
from Models.Logger import Corporate_Database_Builder_Logger
from Models.FinancialCalendar import Financial_Calendar
from datetime import datetime
from datetime import timedelta
from Environment import Environment
from typing import List, Tuple, Union, Dict
from mysql.connector.types import RowType
import logging
import os


class Builder:
    """
    The builder which will build the database.
    """
    __crawler: Crawler
    """
    The main web-scrapper which will scrape the data from the
    database needed.
    """
    __Database_Handler: Database_Handler
    """
    The database handler that will communicate with the database
    server.
    """
    __logger: Corporate_Database_Builder_Logger
    """
    The logger that will all the action of the application.
    """
    __data: List[Dict[str, Union[str, None]]]
    """
    The data that is fed from the Crawler.
    """
    ENV: Environment
    """
    The ENV file of the application which stores the important
    information which allows the application to operate
    smoothly.
    """
    __financial_calendar: Financial_Calendar
    """
    The model which will interact exclusively with the Financial
    Calendar.
    """

    def __init__(self) -> None:
        """
        Initializing the builder which will import and initialize
        the dependencies.
        """
        self.ENV = Environment()
        self.setLogger(Corporate_Database_Builder_Logger())
        self.setDatabaseHandler(Database_Handler())
        self.setFinancialCalendar(Financial_Calendar())
        self.getLogger().inform("The builder has been initialized and all of its dependencies are injected!")

    def getCrawler(self) -> Crawler:
        return self.__crawler
    
    def setCrawler(self, crawler: Crawler) -> None:
        self.__crawler = crawler

    def getDatabaseHandler(self) -> Database_Handler:
        return self.__Database_Handler
    
    def setDatabaseHandler(self, database_handler: Database_Handler) -> None:
        self.__Database_Handler = database_handler

    def getLogger(self) -> Corporate_Database_Builder_Logger:
        return self.__logger
    
    def setLogger(self, logger: Corporate_Database_Builder_Logger) -> None:
        self.__logger = logger

    def getData(self) -> List[Dict[str, Union[str, None]]]:
        return self.__data
    
    def setData(self, data: List[Dict[str, Union[str, None]]]) -> None:
        self.__data = data

    def getFinancialCalendar(self) -> Financial_Calendar:
        return self.__financial_calendar
    
    def setFinancialCalendar(self, financial_calendar: Financial_Calendar) -> None:
        self.__financial_calendar = financial_calendar
    
    def collectCorporateMetadata(self) -> None:
        """
        The first run consists of retrieving the metadata needed of
        any existing company in Mauritius.

        Return:
            (void)
        """
        quarter: Dict[str, Union[int, str]]
        request: dict[str, str] = {}
        FinancialCalendar: Union[RowType, Dict[str, Union[int, str]]] = self.getDatabaseHandler().getData(
            table_name="FinancialCalendar",
            filter_condition="CONCAT(YEAR(CURDATE()), '-', start_date) < CURDATE() AND CONCAT(YEAR(CURDATE()), '-', end_date) > CURDATE()",
            column_names="YEAR(CURDATE()) AS year, quarter, FROM_UNIXTIME(UNIX_TIMESTAMP(CONCAT(YEAR(CURDATE()), '-', start_date)), '%m/%d/%Y') AS start_date, FROM_UNIXTIME(UNIX_TIMESTAMP(CONCAT(YEAR(CURDATE()), '-', end_date)), '%m/%d/%Y') AS end_date"
        )[0]
        FinCorpLogs = self.getDatabaseHandler().getData(
            table_name="FinCorpLogs",
            parameters=None,
            filter_condition="status = 200",
            column_names="MIN(FROM_UNIXTIME(date_start, '%m/%d/%Y')) AS start_date, MAX(FROM_UNIXTIME(date_to, '%m/%d/%Y')) AS end_date"
        )[0]
        quarter = {
            "year": int(FinancialCalendar["year"]), # type: ignore
            "quarter": str(FinancialCalendar["quarter"]), # type: ignore
            "start_date": str(FinancialCalendar["start_date"]), # type: ignore
            "end_date": str(FinancialCalendar["end_date"]) # type: ignore
        }
        print(f"Logs: {FinCorpLogs}\nFinancial Calendar: {FinancialCalendar}\nQuarter: {quarter}")
        if len(logs) > 0:
            request = self.handleRequest(logs)
        else:
            date_to = datetime.strftime(
                datetime.strptime(
                    str(quarter["start_date"]),
                    "%m/%d/%Y"
                ) + timedelta(weeks=1),
                "%m/%d/%Y"
            )
            request = {
                "start_date": str(quarter["start_date"]),
                "end_date": date_to
            }
        self.setCrawler(Crawler())
        response = self.getCrawler().retrieveCorporateMetadata(
            str(request["start_date"]),
            str(request["end_date"]),
            0
        )
        self.validateCorporateMetadata(response, request, quarter) # type: ignore
        self.cleanCache()

    def cleanCache(self) -> None:
        """
        Cleaning the cache database after having retrieved the
        corporate metadata and storing them into the relational
        database server.

        Return:
            (void)
        """
        files = os.listdir(
            f"{self.ENV.getDirectory()}/Cache"
        )
        if len(files) > 0:
            self._cleanCache(files)

    def _cleanCache(self, files: list[str]) -> None:
        """
        Cleaning the Cache database based on the amount of files in
        it.

        Return:
            (void)
        """
        for index in range(0, len(files), 1):
            os.remove(
                f"{self.ENV.getDirectory()}/Cache/{files[index]}"
            )

    def handleRequest(self, logs: tuple[str, str]) -> dict:
        """
        Handling the request before that it is sent to the Crawler.

        Parameters:
            logs:   (array):    The data from FinCorpLogs

        Return:
            (object)
        """
        date_start = datetime.strftime(
            datetime.strptime(
                max(logs),
                "%m/%d/%Y"
            ) + timedelta(days=1),
            "%m/%d/%Y"
        )
        date_end = datetime.strftime(
            datetime.strptime(
                date_start,
                "%m/%d/%Y"
            ) + timedelta(weeks=1),
            "%m/%d/%Y"
        )
        date_end_unixtime = datetime.strptime(
            date_end,
            "%m/%d/%Y"
        ).timestamp()
        current_date = datetime.now() - timedelta(days=1)
        current_time = current_date.timestamp()
        if date_end_unixtime > current_time:
            date_end = datetime.strftime(
                datetime.strptime(
                    min(logs),
                    "%m/%d/%Y"
                ) - timedelta(days=1),
                "%m/%d/%Y"
            )
            date_start = datetime.strftime(
                datetime.strptime(
                    date_end,
                    "%m/%d/%Y"
                ) - timedelta(weeks=1),
                "%m/%d/%Y"
            )
        return {
            "start_date": date_start,
            "end_date": date_end
        }

    def validateCorporateMetadata(self, response: dict[str, int], request: dict[str, str], quarter: dict[str, int | str]) -> None:
        """
        Validating the response from the Crawler to save the data
        into the database server.

        Parameters:
            response:   (object):   The response after retrieving the data.
            request:    (object):   The request used to retrieve the data.
            quarter:    (object):   The data of the quarter.

        Return:
            (void)
        """
        method_name = "collectCorporateMetadata"
        date_start = int(datetime.strptime(
            str(request["start_date"]),
            "%m/%d/%Y"
        ).timestamp())
        date_end = int(datetime.strptime(
            str(request["end_date"]),
            "%m/%d/%Y"
        ).timestamp())
        if response["status"] == 200:
            parameters: tuple[str, str, int, int, int, int, int] = (
                method_name,
                str(quarter["quarter"]),
                date_start,
                date_end,
                int(response["status"]),
                int(response["amount"]),
                len(self.getCrawler().getCorporateMetadata())
            )
            self.setData(self.getCrawler().getCorporateMetadata())
            self.getCrawler().getDriver().quit()
            self.getLogger().inform("Storing the corporate metadata!")
            self.storeCorporateMetadata()
            self.getDatabaseHandler().postData(
                table="FinCorpLogs",
                columns="method_name, quarter, date_start, date_to, status, amount, amount_found",
                values="%s, %s, %s, %s, %s, %s, %s",
                parameters=parameters
            )
        else:
            parameters: tuple[str, str, int, int, int, int, int] = (
                method_name,
                str(quarter["quarter"]),
                date_start,
                date_end,
                int(response["status"]),
                0,
                0
            )
            self.getCrawler().getDriver().quit()
            self.getDatabaseHandler().postData(
                table="FinCorpLogs",
                columns="method_name, quarter, date_start, date_to, status, amount, amount_found",
                values="%s, %s, %s, %s, %s, %s, %s",
                parameters=parameters
            )
            self.getLogger().error(
                f"The application has failed to collect the data!  Please check the logs!\nStatus: {response['status']}"
            )
            raise Exception(
                f"The application has failed to collect the data!  Please check the logs!\nStatus: {response['status']}"
            )

    def storeCorporateMetadata(self) -> None:
        """
        Storing the metadata into the database server.

        Return:
            (void)
        """
        for index in range(0, len(self.getData()), 1):
            CompanyDetails = self.getData()[index]
            parameters: tuple[str, str, str, int, str, str] = (
                str(CompanyDetails["name"]),
                str(CompanyDetails["file_number"]),
                str(CompanyDetails["category"]),
                int(datetime.strptime(
                    str(CompanyDetails["date_incorporation"]),
                    "%d/%m/%Y"
                ).timestamp()),
                str(CompanyDetails["nature"]),
                str(CompanyDetails["status"])
            )
            self.getDatabaseHandler().postData(
                table="CompanyDetails",
                parameters=parameters,
                columns="name, file_number, category, date_incorporation, nature, status",
                values="%s, %s, %s, %s, %s, %s"
            )