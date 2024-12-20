"""
The model which will interact exclusively with the Non
Current Liabilities table.

Authors:
    Darkness4869
"""


from Models.DatabaseHandler import Database_Handler
from typing import Dict, Union, Tuple
from mysql.connector.errors import Error


class Non_Current_Liabilities(Database_Handler):
    """
    The model which will interact exclusively with the Non
    Current Liabilities table.
    """
    __table_name: str
    """
    The table which the model is linked to.
    """
    created: int = 201
    """
    The status code for a successful creation.
    """
    service_unavailable: int = 503
    """
    The status code for an unavailable service.
    """
    ok: int = 200
    """
    The status code for a successful response
    """
    no_content: int = 204
    """
    The status code when there is no content.
    """

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name