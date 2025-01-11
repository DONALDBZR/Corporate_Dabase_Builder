"""
The model which will interact exclusively with the Details
table.

Authors:
    Darkness4869
"""


from Models.DatabaseHandler import Database_Handler
from typing import Dict, Union, Tuple
from mysql.connector.errors import Error


class Details(Database_Handler):
    """
    The model which will interact exclusively with the Details
    table.
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

    def __init__(self):
        """
        Initializing all of the dependencies which will be used to
        operate the application.
        """
        super().__init__()
        self.setTableName("Details")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addDetail(self, data: Dict[str, Union[str, int, None]], company_detail: int) -> int:
        """
        Adding the detail of the company.

        Parameters:
            data: {type: string, date_start: int, date_end: int|null, status: string}: The data of the detail
            company_detail: int: The identifier of a company

        Returns:
            int
        """
        try:
            parameters: Tuple[int, str, int, Union[int, None], str] = (company_detail, str(data["type"]), int(str(data["date_start"])), data["date_end"], str(data["status"])) # type: ignore
            self.postData(
                table=self.getTableName(),
                columns="CompanyDetail, type, date_start, date_end, status",
                values="%s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            self.getLogger().inform(f"The data has been successfully stored.\nStatus: {self.created}")
            return self.created
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {self.service_unavailable}\nError: {error}")
            return self.service_unavailable