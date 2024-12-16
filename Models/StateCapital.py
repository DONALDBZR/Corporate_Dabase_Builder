"""
The Model which will interact exclusively with the State
Capital table.

Authors:
    Andy Ewen Gaspard
"""


from Data.StateCapital import StateCapital
from Models.DatabaseHandler import Database_Handler
from typing import Union, Dict, Tuple, List
from mysql.connector.errors import Error
from mysql.connector.types import RowType


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
            parameters: Tuple[str, int, int, float, str, int] = (
                str(data["type"]),
                int(data["amount"]),
                int(data["stated_capital"]),
                float(data["amount_unpaid"]),
                str(data["currency"]),
                company_detail
            )
            self.postData(
                table=self.getTableName(),
                columns="type, amount, stated_capital, amount_unpaid, currency, CompanyDetail",
                values="%s, %s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            response = 201
        except Error as error:
            response = 503
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {response}\nError: {error}")
        return response

    def get(self) -> List[StateCapital]:
        """
        Retrieving all of the data from the State Capital tables.

        Returns:
            [{identifier: int, CompanyDetail: int, type: string|null, amount: int|null, state_capital: float|null, amount_unpaid: float|null, currency: string|null}]
        """
        try:
            data: Union[List[RowType], List[Dict[str, Union[int, str, None, float]]]] = self.getData(
                table_name=self.getTableName()
            )
            response: Dict[str, Union[int, List[StateCapital]]] = self._get(data)
            self.getLogger().inform(f"The data from {self.getTableName()} has been retrieved!\nStatus: {response['status']}\nData: {response['data']}")
            return response["data"]  # type: ignore
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: 503\nError: {error}")
            return []

    # def _get(self, dataset: Union[List[RowType], List[Dict[str, Union[int, str, None, float]]]]) -> Dict[str, Union[int, List[StateCapital]]]:
    #     """
    #     Formatting the result set data in the correct format for the
    #     State Capital model.

    #     Parameters:
    #         dataset: The result set data that needs to be formatted.

    #     Returns:
    #         {status: int, data: [{identifier: int, CompanyDetail: int, type: string|null, amount: int|null, state_capital: float|null, amount_unpaid: float|null, currency: string|null}]}
    #     """
    #     status: int = 200 if len(dataset) > 0 else 204
    #     data: List[StateCapital] = [StateCapital(state_capital) for state_capital in dataset] if len(dataset) > 0 else []
    #     return {
    #         "status": status,
    #         "data": data
    #     }