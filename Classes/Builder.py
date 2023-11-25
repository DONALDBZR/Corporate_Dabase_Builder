from Classes.Crawler import Crawler


class Builder:
    """
    The builder which will build the database.
    """
    __crawler: Crawler
    """
    The main web-scrapper which will scraope the data from the
    database needed.
    """
    __date: str
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

    def getDate(self) -> str:
        return self.__date
    
    def setDate(self, date: str) -> None:
        self.__date = date