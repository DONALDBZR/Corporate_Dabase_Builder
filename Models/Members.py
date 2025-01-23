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
from Data.Members import Member as Member_Data


class Member(Database_Handler):
    """
    The model which will interact exclusively with the Members.
    """
    __table_name: str
    """
    The table which the model is linked to.
    """
    service_unavailable: int = 503
    """
    The status code for service unavailable
    """
    created: int = 201
    """
    The status code for a success creation
    """
    ok: int = 200
    """
    The status code for a success read
    """
    no_content: int = 204
    """
    The status code for no content.
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
            response = self.created
        except Error as error:
            response = self.service_unavailable
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {response}\nError: {error}")
        return response

    def get(self) -> List[Member_Data]:
        """
        Retrieving all of the data from the Members table.

        Returns:
            [{identifier: int, CompanyDetail: int, name: string, amount: int, date_start: int, currency: string}]
        """
        try:
            data: Union[List[RowType], List[Dict[str, Union[int, str]]]] = self.getData(
                table_name=self.getTableName()
            )
            response: Dict[str, Union[int, List[Member_Data]]] = self._get(data)
            self.getLogger().inform(f"The data from {self.getTableName()} has been retrieved!\nStatus: {response['status']}\nData: {response['data']}")
            return response["data"]  # type: ignore
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {self.service_unavailable}\nError: {error}")
            return []
