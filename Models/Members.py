"""
The Model which will interact exclusively with the Members
table.

Authors:
    Andy Ewen Gaspard
"""


from Models.DatabaseHandler import Database_Handler
from typing import Union, Dict, Tuple, List
from mysql.connector.errors import Error
from mysql.connector.types import RowType


class Member(Database_Handler):
    """
    The model which will interact exclusively with the Members.
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
        self.setTableName("Members")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addMember(self, data: Dict[str, Union[str, int]], company_detail: int) -> int:
        """
        Adding the shareholders data of the company into the
        relational database server.

        Parameters:
            data: {name: string, amount: int, date_start: int, currency: string}: The data that has been extracted for the members table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        response: int
        try:
            parameters: Tuple[str, int, int, str, int] = (
                str(data["name"]),
                int(data["amount"]),
                int(data["date_start"]),
                str(data["currency"]),
                company_detail
            )
            self.postData(
                table=self.getTableName(),
                columns="name, amount, date_start, currency, CompanyDetail",
                values="%s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            response = 201
        except Error as error:
            response = 503
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {response}\nError: {error}")
        return response