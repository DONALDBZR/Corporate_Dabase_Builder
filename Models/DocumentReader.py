"""
The module which will have the model needed to generate the
portable document file version of the corporate registry, as
well as extracting the data from it before deleting it from
the cache of the server of the application.

Authors:
    Andy Ewen Gaspard
"""


from Models.Logger import Corporate_Database_Builder_Logger
from Environment import Environment


class Document_Reader:
    """
    The model needed to generate the portable document file
    version of the corporate registry, as well as extracting the
    data from it before deleting it from the cache of the server
    of the application.
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

    def __init__(self) -> None:
        """
        Initializing the document reader which will import and
        initialize the dependencies.
        """
        self.ENV = Environment()
        self.setLogger(Corporate_Database_Builder_Logger())
        self.getLogger().inform("The builder has been initialized and all of its dependencies are injected!")

    def getLogger(self) -> Corporate_Database_Builder_Logger:
        return self.__logger

    def setLogger(self, logger: Corporate_Database_Builder_Logger) -> None:
        self.__logger = logger