"""
The model which will interact exclusively with the Equity
And Liabilities table.

Authors:
    Darkness4869
"""


from Models.DatabaseHandler import Database_Handler
from typing import Dict, Tuple
from mysql.connector.errors import Error
from Data.Liabilities import Liabilities as data_object


class Equity_And_Liabilities(Database_Handler):
    """
    The model which will interact exclusively with the Equity
    And Liabilities table.
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
        self.setTableName("EquityAndLiabilities")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addLiability(self, data: Dict[str, float], liability: int) -> int:
        """
        Adding the equity and liability of the company.

        Parameters:
            data: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}: The data of the equity and liability.
            liability: int: The identifier of a liability.

        Returns:
            int
        """
        try:
            parameters: Tuple[int, float, float, float, float, float] = (liability, float(data["share_capital"]), float(data["other_reserves"]), float(data["retained_earnings"]), float(data["others"]), float(data["total"]))
            self.postData(
                table=self.getTableName(),
                columns="Liability, share_capital, other_reserves, retained_earnings, others, total",
                values="%s, %s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            self.getLogger().inform(f"The data has been successfully stored.\nStatus: {self.created}")
            return self.created
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {self.service_unavailable}\nError: {error}")
            return self.service_unavailable