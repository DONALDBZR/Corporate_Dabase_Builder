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