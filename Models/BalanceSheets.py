"""
The model which will interact exclusively with the Balance
Sheets table.

Authors:
    Darkness4869
"""


from Models.DatabaseHandler import Database_Handler
from typing import Dict, Union, Tuple
from mysql.connector.errors import Error


class Balance_Sheets(Database_Handler):
    """
    The model which will interact exclusively with the Balance
    Sheets table.
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

    def __init__(self):
        """
        Initializing all of the dependencies which will be used to
        operate the application.
        """
        super().__init__()
        self.setTableName("BalanceSheets")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addBalanceSheet(self, data: Dict[str, Union[int, str]], company_detail: int) -> int:
        """
        Adding the balance sheet of the company.

        Parameters:
            data: {financial_year: int, currency: string, unit: int}: The data of the profit statement.
            company_detail: int: The identifier of a company.

        Returns:
            int
        """
        try:
            parameters: Tuple[int, int, str, int] = (company_detail, int(data["financial_year"]), str(data["currency"]), int(data["unit"])) # type: ignore
            self.postData(
                table=self.getTableName(),
                columns="CompanyDetail, financial_year, currency, unit",
                values="%s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            self.getLogger().inform(f"The data has been successfully stored.\nStatus: {self.created}")
            return self.created
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {self.service_unavailable}\nError: {error}")
            return self.service_unavailable