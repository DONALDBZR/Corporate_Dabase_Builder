"""
The Model which will interact exclusively with the Office
Bearers table.

Authors:
    Andy Ewen Gaspard
"""


from Models.DatabaseHandler import Database_Handler
from typing import Union, Dict, Tuple
from mysql.connector.errors import Error


class Office_Bearers(Database_Handler):
    """
    The model which will interact exclusively with the Office
    Bearers.
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
        self.setTableName("OfficeBearers")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addDirectors(self, data: Dict[str, Union[str, int]], company_detail: int) -> int:
        """
        Adding the directors data of the company into the relational
        database server.

        Parameters:
            data: {position: string, name: string, address: string, date_appointment: int}: The data that has been extracted for the office bearers table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        response: int
        try:
            parameters: Tuple[str, str, str, int, int] = (
                str(data["position"]),
                str(data["name"]),
                str(data["address"]),
                int(data["date_appointment"]),
                company_detail
            )
            self.postData(
                table=self.getTableName(),
                columns="position, name, address, date_appointment, CompanyDetail",
                values="%s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            response = 201
        except Error as error:
            response = 503
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {response}\nError: {error}")
        return response