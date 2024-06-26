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

    def addBusinessDetails(self, data: Dict[str, str], company_detail: int) -> int:
        """
        Adding the business details into the relational database
        server.

        Parameters:
            data: {registered_address: string, name: string, nature: string, operational_address: string}: The data that has been extracted for the business details table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        response: int
        try:
            parameters: Tuple[str, str, str, str, int] = (
                str(data["registered_address"]),
                str(data["name"]),
                str(data["nature"]),
                str(data["operational_address"]),
                company_detail
            )
            self.postData(
                table=self.getTableName(),
                columns="registered_address, name, nature, operational_address, CompanyAddress",
                values="%s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            response = 201
        except Error as error:
            response = 503
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {response}\nError: {error}")
        return response