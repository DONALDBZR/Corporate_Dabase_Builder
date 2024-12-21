"""
The model which will interact exclusively with the Current
Liabilities table.

Authors:
    Darkness4869
"""


from Models.DatabaseHandler import Database_Handler
from typing import Dict, Union, Tuple
from mysql.connector.errors import Error


class Current_Liabilities(Database_Handler):
    """
    The model which will interact exclusively with the Current
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
        self.setTableName("CurrentLiabilities")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addLiability(self, data: Dict[str, float], liability: int) -> int:
        """
        Adding the current liability of the company.

        Parameters:
            data: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}: The data of the equity and liability.
            liability: int: The identifier of a liability.

        Returns:
            int
        """
        try:
            parameters: Tuple[int, float, float, float, float, float, float] = (liability, float(data["trade"]), float(data["short_term_borrowings"]), float(data["current_tax_payable"]), float(data["short_term_provisions"]), float(data["others"]), float(data["total"]))
            self.postData(
                table=self.getTableName(),
                columns="Liability, trade, short_term_borrowings, current_tax_payable, short_term_provisions, others, total",
                values="%s, %s, %s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            self.getLogger().inform(f"The data has been successfully stored.\nStatus: {self.created}")
            return self.created
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {self.service_unavailable}\nError: {error}")
            return self.service_unavailable