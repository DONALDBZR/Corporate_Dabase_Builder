"""
The model which will interact exclusively with the Balance
Sheets table.

Authors:
    Darkness4869
"""


from Data.BalanceSheets import BalanceSheets
from Models.DatabaseHandler import Database_Handler
from typing import Dict, Union, Tuple, List
from mysql.connector.errors import Error
from mysql.connector.types import RowType


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

    def getSpecific(self, company_detail:int, financial_year: int) -> BalanceSheets:
        """
        Retrieving the data of the balance sheet.

        Parameters:
            company_detail: int: The identifier of the company.
            financial_year: int: The financial year for which the data needs to be retrieved.

        Returns:
            {identifier: int, CompanyDetail: int, financial_year: int, currency: string, unit: int}
        """
        try:
            parameters: Tuple[int, int] = (company_detail, financial_year)
            data: Union[List[RowType], List[Dict[str, Union[int, str]]]] = self.getData(
                table_name=self.getTableName(),
                filter_condition="CompanyDetail = %s AND financial_year = %s",
                parameters=parameters # type: ignore
            )
            response: Dict[str, Union[int, BalanceSheets]] = self._getSpecific(data)
            self.getLogger().inform(f"The data from {self.getTableName()} has been retrieved!\nStatus: {response['status']}\nData: {data}")
            return response["data"] # type: ignore
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {self.service_unavailable}\nError: {error}")
            return BalanceSheets({})

    def _getSpecific(self, dataset: Union[List[RowType], List[Dict[str, Union[int, str]]]]) -> Dict[str, Union[int, BalanceSheets]]:
        """
        Retrieving the data into the correct data type for the
        application.

        Parameters:
            dataset: [{identfier: int, CompanyDetail: int, financial_year: int, currency: string, date_approved: int, unit: int|null}]: The data from the relational database server.

        Returns:
            {status: int, data: {identfier: int, CompanyDetail: int, financial_year: int, currency: string, date_approved: int, unit: int|null}}
        """
        status = self.ok if len(dataset) == 1 else self.service_unavailable
        status = self.no_content if len(dataset) == 0 else status
        data: List[BalanceSheets] = [BalanceSheets(balance_sheet) for balance_sheet in dataset] if len(dataset) > 0 else []
        return {
            "status": status,
            "data": data[0] if len(data) == 1 else BalanceSheets({})
        }