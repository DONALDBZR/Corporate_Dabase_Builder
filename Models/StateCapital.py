"""
The Model which will interact exclusively with the State
Capital table.

Authors:
    Andy Ewen Gaspard
"""


from Models.DatabaseHandler import Database_Handler
from typing import Union, Dict, Tuple
from mysql.connector.errors import Error


class State_Capital(Database_Handler):
    """
    The model which will interact exclusively with the State
    Capital.
    """
    __table_name: str
    """
    The table which the model is linked to.
    """

    def __init__(self) -> None:
        """
        Initializing all of the dependencies which will be used to
        operate the application.
        """
        super().__init__()
        self.setTableName("StateCapital")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name