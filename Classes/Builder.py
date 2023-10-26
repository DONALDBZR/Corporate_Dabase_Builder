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

    def __init__(self) -> None:
        """
        Initializing the builder which will import and initialize
        the dependencies.
        """
        self.setCrawler(Crawler())

    def getCrawler(self) -> Crawler:
        return self.__crawler
    
    def setCrawler(self, crawler: Crawler) -> None:
        self.__crawler = crawler