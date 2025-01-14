"""
The model which will interact exclusively with the Charges
table.

Authors:
    Darkness4869
"""


from Models.DatabaseHandler import Database_Handler
from typing import Dict, Union, Tuple
from mysql.connector.errors import Error


class Charges(Database_Handler):
    """
    The model which will interact exclusively with the Charges
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
        self.setTableName("Charges")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addCharge(self, data: Dict[str, Union[str, int]], company_detail: int) -> int:
        """
        Adding the detail of the company.

        Parameters:
            data: {volume: string, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}: The data of the charge
            company_detail: int: The identifier of a company

        Returns:
            int
        """
        try:
            parameters: Tuple[int, str, str, str, int, int, int, str] = (company_detail, str(data["volume"]), str(data["property"]), str(data["nature"]), int(data["amount"]), int(data["date_charged"]), int(data["date_filled"]), str(data["currency"]))
            self.postData(
                table=self.getTableName(),
                columns="CompanyDetail, volume, property, nature, amount, date_charged, date_filled, currency",
                values="%s, %s, %s, %s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            self.getLogger().inform(f"The data has been successfully stored.\nStatus: {self.created}")
            return self.created
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {self.service_unavailable}\nError: {error}")
            return self.service_unavailable