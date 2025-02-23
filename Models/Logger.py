"""
The module of the Corporate Database Builder Logger which
will help the application to log all of the actions done by
the application.

Authors:
    Andy Ewen Gaspard
"""


from logging.__init__ import Logger
from Environment import Environment
import logging


class Corporate_Database_Builder_Logger:
    """
    The logger that will all the action of the application.
    """
    __logger: Logger
    """
    It is responsible for logging all of the actions done by the
    application.
    """

    def __init__(self) -> None:
        """
        Instantiating the Logger which will keep track of everything
        that the application does.
        """
        ENV = Environment()
        logging.basicConfig(
            filename=f"{ENV.getDirectory()}/Logs/CDB.log",
            encoding="utf-8",
            filemode="a",
            format="----------\nCurrent Time: %(asctime)s\nModule: %(name)s\nLog Level: %(levelname)s\nMessage: %(message)s"
        )
        self.setLogger(logging.getLogger(__name__))

    def getLogger(self) -> Logger:
        return self.__logger

    def setLogger(self, logger: Logger) -> None:
        self.__logger = logger

    def debug(self, message: str) -> None:
        """
        Logging the data for debugging

        Parameters:
            message: string: The action done.

        Returns:
            void
        """
        self.getLogger().setLevel(logging.DEBUG)
        self.getLogger().debug(message)
        print(message)

    def inform(self, message: str) -> None:
        """
        Logging informational data.

        Parameters:
            message: string: The action done.

        Returns:
            void
        """
        self.getLogger().setLevel(logging.INFO)
        self.getLogger().info(message)
        print(message)

    def warn(self, message: str) -> None:
        """
        Logging the data for a warning.

        Parameters:
            message: string: The action done.

        Returns:
            void
        """
        self.getLogger().setLevel(logging.WARNING)
        self.getLogger().warning(message)
        print(message)

    def error(self, message: str) -> None:
        """
        Logging the data for an error.

        Parameters:
            message: string: The action done.

        Returns:
            void
        """
        self.getLogger().setLevel(logging.ERROR)
        self.getLogger().error(message)
        print(message)
