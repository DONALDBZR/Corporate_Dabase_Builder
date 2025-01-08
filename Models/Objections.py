"""
The Model which will interact exclusively with the
Objections table.

Authors:
    Andy Ewen Gaspard
    Darkness4869
"""


from Models.DatabaseHandler import Database_Handler
from typing import Union, Dict, Tuple, List
from mysql.connector.errors import Error
from mysql.connector.types import RowType


class Objections(Database_Handler):
    """
    The Model which will interact exclusively with the
    Objections table.
    """
    __table_name: str
    """
    The table which the model is linked to.
    """
    created: int = 201
    """
    The status code for a success write.
    """
    service_unavailable: int = 503
    """
    The status code for unavailability of service.
    """

    def __init__(self) -> None:
        """
        Initializing all of the dependencies which will be used to
        operate the application.
        """
        super().__init__()
        self.setTableName("Objections")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addObjection(self, data: Dict[str, Union[int, str]], company_detail: int) -> int:
        """
        Adding the objection of the company.

        Parameters:
            data: [{date_objection: int, objector: string}]: The data of the objection.
            company_detail: int: The identifier of a company.

        Returns:
            int
        """
        try:
            parameters: Tuple[int, int, str] = (company_detail, int(str(data["date_objection"])), str(data["objector"]))
            self.postData(
                table=self.getTableName(),
                columns="CompanyDetail, date_objection, objector",
                values="%s, %s, %s",
                parameters=parameters # type: ignore
            )
            self.getLogger().inform(f"The data has been successfully stored.\nStatus: {self.created}")
            return self.created
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {self.service_unavailable}\nError: {error}")
            return self.service_unavailable