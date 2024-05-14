"""
The module which will have the main corporate database
builder.

Authors:
    Andy Ewen Gaspard
"""


from Data.FinancialCalendar import FinancialCalendar
from Data.FinCorpLogs import FinCorpLogs
from Models.Crawler import Crawler
from Models.DatabaseHandler import Database_Handler
from Models.Logger import Corporate_Database_Builder_Logger
from Models.FinancialCalendar import Financial_Calendar
from Models.FinCorpLogs import FinCorp_Logs
from datetime import datetime
from datetime import timedelta
from Environment import Environment
from typing import List, Tuple, Union, Dict
from mysql.connector.types import RowType
from time import time
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
    __fincorp_logs: FinCorp_Logs
    """
    The model which will interact exclusively with the FinCorp
    Logs.
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
        self.setFinCorpLogs(FinCorp_Logs())
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

    def getFinCorpLogs(self) -> FinCorp_Logs:
        return self.__fincorp_logs
    
    def setFinCorpLogs(self, fincorp_logs: FinCorp_Logs) -> None:
        self.__fincorp_logs = fincorp_logs
    
    def collectCorporateMetadata(self) -> None:
        """
        The first run consists of retrieving the metadata needed of
        any existing company in Mauritius.

        Returns:
            void
        """
        request: dict[str, str] = {}
        quarter: FinancialCalendar = self.getFinancialCalendar().getCurrentQuarter() # type: ignore
        successful_logs: List[FinCorpLogs] = self.getFinCorpLogs().getSuccessfulRunsLogs()
        if len(successful_logs) == 1 and successful_logs[0].status == 204:
            date_to = datetime.strftime(
                datetime.strptime(
                    quarter.start_date,
                    "%m/%d/%Y"
                ) + timedelta(weeks=1),
                "%m/%d/%Y"
            )
            request = {
                "start_date": quarter.start_date,
                "end_date": date_to
            }
        else:
            request = self.handleRequest(successful_logs)
        self.setCrawler(Crawler())
        response = self.getCrawler().retrieveCorporateMetadata(
            str(request["start_date"]),
            str(request["end_date"]),
            0
        )
        self.validateCorporateMetadata(response, request, quarter) # type: ignore
        # self.cleanCache()

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

    def getDateStart(self, logs: List[FinCorpLogs]) -> str:
        """
        Retrieving the next start date for the data collection which
        will be based on the latest end date that is in the logs.

        Parameters:
            logs: array

        Returns:
            string
        """
        date_end: int = 0
        for index in range(0, len(logs), 1):
            if logs[index].date_to > date_end:
                date_end = logs[index].date_to
            else:
                date_end = date_end
        return datetime.strftime(
            datetime.strptime(
                datetime.fromtimestamp(date_end).strftime("%m/%d/%Y"),
                "%m/%d/%Y"
            ) + timedelta(
                days=1
            ),
            "%m/%d/%Y"
        )

    def getDateEnd(self, logs: List[FinCorpLogs]) -> str:
        """
        Retrieving the next end date for the data collection which
        will be based on the earliest start date that is in the
        logs.

        Parameters:
            logs: array

        Returns:
            string
        """
        date_start: int = int(time())
        for index in range(0, len(logs), 1):
            if logs[index].date_start < date_start:
                date_start = logs[index].date_start
            else:
                date_start = date_start
        return datetime.strftime(
            datetime.strptime(
                datetime.fromtimestamp(date_start).strftime("%m/%d/%Y"),
                "%m/%d/%Y"
            ) - timedelta(
                days=1
            ),
            "%m/%d/%Y"
        )

    def handleRequest(self, logs: List[FinCorpLogs]) -> Dict[str, str]:
        """
        Handling the request before that it is sent to the Crawler.

        Parameters:
            logs: array: The data from FinCorpLogs

        Returns:
            {start_date: string, end_date: string}
        """
        date_start: str
        date_end: str
        date_start = self.getDateStart(logs)
        date_end = datetime.strftime(
            datetime.strptime(
                date_start,
                "%m/%d/%Y"
            ) + timedelta(
                weeks=1
            ),
            "%m/%d/%Y"
        )
        date_end_unixtime: float = datetime.strptime(
            date_end,
            "%m/%d/%Y"
        ).timestamp()
        current_date: datetime = datetime.now() - timedelta(
            days=1
        )
        current_time: float = current_date.timestamp()
        if date_end_unixtime > current_time:
            date_end = self.getDateEnd(logs)
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
            parameters: Tuple[str, str, int, int, int, int, int] = (
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
                parameters=parameters # type: ignore
            )
        else:
            parameters: Tuple[str, str, int, int, int, int, int] = (
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
                parameters=parameters # type: ignore
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
            parameters: Tuple[str, str, str, int, str, str] = (
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
                parameters=parameters, # type: ignore
                columns="name, file_number, category, date_incorporation, nature, status",
                values="%s, %s, %s, %s, %s, %s"
            )