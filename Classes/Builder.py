from Classes.Crawler import Crawler
from datetime import datetime


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

    def __init__(self, date: str) -> None:
        """
        Initializing the builder which will import and initialize
        the dependencies.

        Parameters:
            date:   (string):   The date to be used as a filter to retrieve the dataset to build the corporate database.
        """
        self.setDate(date)
        self.setCrawler(Crawler())

    def getCrawler(self) -> Crawler:
        return self.__crawler
    
    def setCrawler(self, crawler: Crawler) -> None:
        self.__crawler = crawler

    def getDate(self) -> datetime:
        return self.__date
    
    def setDate(self, date: datetime) -> None:
        self.__date = date
    
    def firstRun(self) -> None:
        """
        The first run consists of retrieving the metadata needed of
        any existing company in Mauritius.

        Return:
            (void)
        """
        