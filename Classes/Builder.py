from Classes.Crawler import Crawler
from Classes.DatabaseHandler import Database_Handler
from Classes.Logger import Corporate_Database_Builder_Logger
from datetime import datetime
from datetime import timedelta
import logging


class Builder:
    """
    The builder which will build the database.
    """
    __crawler: Crawler
    """
    The main web-scrapper which will scraope the data from the
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

    def __init__(self) -> None:
        """
        Initializing the builder which will import and initialize
        the dependencies.
        """
        self.setLogger(Corporate_Database_Builder_Logger())
        self.setDatabaseHandler(Database_Handler())
        self.getLogger().setLogger(logging.getLogger(__name__))
        self.getLogger().inform("The builder has been initialized!")
        self.firstRun()

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
    
    def firstRun(self) -> None:
        """
        The first run consists of retrieving the metadata needed of
        any existing company in Mauritius.

        Return:
            (void)
        """
        quarter: dict[str, int | str]
        period: dict[str, str]
        FinancialCalendar: tuple[int, str, str, str] = self.getDatabaseHandler().get_data(
            table_name="FinancialCalendar",
            filter_condition="CONCAT(YEAR(CURDATE()), '-', start_date) < CURDATE() AND CONCAT(YEAR(CURDATE()), '-', end_date) > CURDATE()",
            column_names="YEAR(CURDATE()) AS year, quarter, FROM_UNIXTIME(UNIX_TIMESTAMP(CONCAT(YEAR(CURDATE()), '-', start_date)), '%m/%d/%Y') AS start_date, FROM_UNIXTIME(UNIX_TIMESTAMP(CONCAT(YEAR(CURDATE()), '-', end_date)), '%m/%d/%Y') AS end_date"
        )[0] # type: ignore
        logs: list[tuple[int, str, int, str, int, int , int, int]] = self.getDatabaseHandler().get_data(
            table_name="FinCorpLogs"
        ) # type: ignore
        if len(logs) > 0:
            pass
        else:
            quarter = {
                "year": int(FinancialCalendar[0]),
                "quarter": str(FinancialCalendar[1]),
                "start_date": str(FinancialCalendar[2]),
                "end_date": str(FinancialCalendar[3])
            }
            date_to = datetime.strftime(
                datetime.strptime(
                    str(quarter["start_date"]),
                    "%m/%d/%Y"
                ) + timedelta(weeks=1),
                "%m/%d/%Y"
            )
            period = {
                "start_date": str(quarter["start_date"]),
                "end_date": date_to
            }
            self.setCrawler(Crawler())
            response = self.getCrawler().retrieveCorporateMetadata(
                str(period["start_date"]),
                str(period["end_date"])
            )
            if response["status"] == 200:
                self.setData(self.getCrawler().getCorporateMetadata())
                self.storeCorporateMetadata()
                self.getCrawler().getDriver().quit()
                self.getLogger().inform("Storing the corporate metadata!")
            else:
                self.getCrawler().getDriver().quit()
                self.getLogger().error(
                    f"The application has failed to collect the data!  Please check the logs!\nStatus: {response['status']}"
                )
                raise Exception(
                    f"The application has failed to collect the data!  Please check the logs!\nStatus: {response['status']}"
                )