"""
The model which will interact exclusively with the
Liabilities table.

Authors:
    Darkness4869
"""


from Models.DatabaseHandler import Database_Handler
from typing import Dict, Union, Tuple
from mysql.connector.errors import Error


class Liabilities(Database_Handler):
    """
    The model which will interact exclusively with the
    Liabilities table.
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
        self.setTableName("Liabilities")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addLiabilities(self, data: Dict[str, Union[Dict[str, float], float]], balance_sheet: int) -> int:
        """
        Adding the balance sheet of the company.

        Parameters:
            data: {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}: The data of the assets.
            balance_sheet: int: The identifier of a balance sheet.

        Returns:
            int
        """
        try:
            parameters: Tuple[int, float, float] = (balance_sheet, float(data["total_liabilities"]), float(data["total_equity_and_liabilities"])) # type: ignore
            self.postData(
                table=self.getTableName(),
                columns="BalanceSheet, total_liabilities, total_equity_and_liabilities",
                values="%s, %s, %s",
                parameters=parameters # type: ignore
            )
            self.getLogger().inform(f"The data has been successfully stored.\nStatus: {self.created}")
            return self.created
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {self.service_unavailable}\nError: {error}")
            return self.service_unavailable