from Classes.Crawler import Crawler
from Classes.DatabaseHandler import Database_Handler
from Classes.Logger import Corporate_Database_Builder_Logger
from datetime import datetime
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
    __date: datetime
    """
    The date to be used as a filter to retrieve the dataset to
    build the corporate database.
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

    def __init__(self, date: str) -> None:
        """
        Initializing the builder which will import and initialize
        the dependencies.

        Parameters:
            date:   (string):   The date to be used as a filter to retrieve the dataset to build the corporate database.
        """
        self.setDate(datetime.strptime(date, "%Y-%m-%d"))
        self.setLogger(Corporate_Database_Builder_Logger())
        self.setDatabaseHandler(Database_Handler())
        self.getLogger().setLogger(logging.getLogger(__name__))
        self.getLogger().inform("The builder has been initialized!")
        self.setCrawler(Crawler())
        self.firstRun()

    def getCrawler(self) -> Crawler:
        return self.__crawler
    
    def setCrawler(self, crawler: Crawler) -> None:
        self.__crawler = crawler

    def getDate(self) -> datetime:
        return self.__date
    
    def setDate(self, date: datetime) -> None:
        self.__date = date

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
        query = "SELECT YEAR(CURDATE()) AS year, quarter, FROM_UNIXTIME(UNIX_TIMESTAMP(CONCAT(YEAR(CURDATE()), '-', start_date)), '%m/%d/%Y') AS start_date, FROM_UNIXTIME(UNIX_TIMESTAMP(CONCAT(YEAR(CURDATE()), '-', end_date)), '%m/%d/%Y') AS end_date FROM FinancialCalendar WHERE CONCAT(YEAR(CURDATE()), '-', start_date) < CURDATE() AND CONCAT(YEAR(CURDATE()), '-', end_date) > CURDATE()"
        data: tuple[int, str, str, str] = self.getDatabaseHandler().get_data(
            table_name="FinancialCalendar",
            filter_condition=f"CONCAT(YEAR('{str(self.getDate().date())}'), '-', start_date) < '{str(self.getDate().date())}' AND CONCAT(YEAR('{str(self.getDate().date())}'), '-', end_date) > '{str(self.getDate().date())}'",
            column_names=f"YEAR('{str(self.getDate().date())}') AS year, quarter, FROM_UNIXTIME(UNIX_TIMESTAMP(CONCAT(YEAR('{str(self.getDate().date())}'), '-', start_date)), '%m/%d/%Y') AS start_date, FROM_UNIXTIME(UNIX_TIMESTAMP(CONCAT(YEAR('{str(self.getDate().date())}'), '-', end_date)), '%m/%d/%Y') AS end_date"
        )[0]
        quarter: dict[str, int | str] = {
            "year": int(data[0]),
            "quarter": str(data[1]),
            "start_date": str(data[2]),
            "end_date": str(data[3])
        }
        self.validateFinancialCalendarEndDate(quarter, self.getDate())
        response = self.getCrawler().retrieveCorporateMetadata(quarter["start_date"], quarter["end_date"])
        print(quarter)

    def validateFinancialCalendarEndDate(self, quarter: dict[str, int | str], date: datetime) -> dict:
        """
        Validating the quarter against to be able to date to know
        that the Crawler must take for a quarter that is before the
        current quarter.

        Parameters:
            quarter:    (object):   The quarter to be used as parameter for the search
            date:       (Datetime): The date entered by the user.

        Return:
            (object)
        """
        response: dict
        end_date = datetime.timestamp(datetime.strptime(str(quarter["end_date"]), "%m/%d/%Y"))
        date_entered = datetime.timestamp(date)
        if date_entered > end_date:
            response = {
                "status": 401,
                "message": "Data from the current quarter cannot be taken!"
            }
        else:
            response = {
                "status": 200,
                "message": f"Data from the quarter {quarter['year']} {quarter['quarter']} can be taken"
            }
        return response