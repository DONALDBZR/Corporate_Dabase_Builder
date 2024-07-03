"""
The Model which will interact exclusively with the
Shareholders table.

Authors:
    Andy Ewen Gaspard
"""


from Models.DatabaseHandler import Database_Handler
from typing import Union, Dict, Tuple
from mysql.connector.errors import Error


class Shareholders(Database_Handler):
    """
    The model which will interact exclusively with the
    Shareholders.
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
        self.setTableName("Shareholders")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addShareholders(self, data: Dict[str, Union[str, int]], company_detail: int) -> int:
        """
        Adding the shareholders data of the company into the
        relational database server.

        Parameters:
            data: {name: string, amount: int, type: string, currency: string}: The data that has been extracted for the office bearers table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        response: int
        try:
            parameters: Tuple[str, int, str, str, int] = (
                str(data["name"]),
                int(data["amount_shares"]),
                str(data["type"]),
                str(data["currency"]),
                company_detail
            )
            self.postData(
                table=self.getTableName(),
                columns="name, amount_shares, type_shares, currency, CompanyDetail",
                values="%s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            response = 201
        except Error as error:
            response = 503
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {response}\nError: {error}")
        return response