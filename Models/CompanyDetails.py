"""
The Model which will interact exclusively with the Company
Details table.

Authors:
    Solofonavalona Randirantsilavo
    Andy Ewen Gaspard
"""


from Models.DatabaseHandler import Database_Handler
from typing import Union, Dict, List, Tuple, Any
from mysql.connector.types import RowType
from mysql.connector.errors import Error


class Company_Details(Database_Handler):
    """
    The model which will interact exclusively with the Company
    Details.
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
        self.setTableName("CompanyDetails")
        self.getLogger().inform(
            "The model has been successfully been initiated with its dependencies."
        )

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addCompany(self, data: Tuple[Any]) -> None:
        """
        Adding the compony metadata into the relational database
        server.

        Parameters:
            data: array

        Returns:
            void
        """
        return self.postData(
            table=self.getTableName(),
            parameters=data,
            columns="name, file_number, category, date_incorporation, nature, status",
            values="%s, %s, %s, %s, %s, %s"
        )
