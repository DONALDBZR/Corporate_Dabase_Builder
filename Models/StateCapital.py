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

    def addStateCapital(self, data: Dict[str, Union[str, int]], company_detail: int) -> int:
        """
        Adding the state capital data of the company into the
        relational database server.

        Parameters:
            data: {type: string, amount: int, currency: string, stated_capital: int, amount_unpaid: int, par_value: int}: The data that has been extracted for the shareholder table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        response: int
        try:
            parameters: Tuple[str, int, int, int, int, str, int] = (
                str(data["type"]),
                int(data["amount"]),
                int(data["stated_capital"]),
                int(data["amount_unpaid"]),
                int(data["par_value"]),
                str(data["currency"]),
                company_detail
            )
            self.postData(
                table=self.getTableName(),
                columns="type, amount, stated_capital, amount_unpaid, par_value, currency, CompanyDetail",
                values="%s, %s, %s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            response = 201
        except Error as error:
            response = 503
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {response}\nError: {error}")
        return response