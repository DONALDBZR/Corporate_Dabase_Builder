"""
The Model which will interact exclusively with the
Shareholders table.
"""
from Models.DatabaseHandler import Database_Handler
from typing import Union, Dict, Tuple, List
from mysql.connector.errors import Error
from mysql.connector.types import RowType
from Data.Shareholders import Shareholder


class Shareholders(Database_Handler):
    """
    The model which will interact exclusively with the
    Shareholders.
    """
    __table_name: str
    """
    The table which the model is linked to.
    """
    service_unavailable: int = 503
    """
    The status code for service unavailable
    """
    created: int = 201
    """
    The status code for a success creation
    """
    ok: int = 200
    """
    The status code for a success read
    """
    no_content: int = 204
    """
    The status code for no content.
    """

    def __init__(self) -> None:
        """
        Initializing all of the dependencies which will be used to
        operate the application.
        """
        super().__init__()
        self.setTableName("Shareholders")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addShareholders(self, data: Dict[str, Union[str, int]], company_detail: int) -> int:
        """
        Adding the shareholders data of the company into the
        relational database server.

        Parameters:
            data: {name: string, amount_shares: int, type_shares: string, currency: string}: The data that has been extracted for the office bearers table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        response: int
        try:
            parameters: Tuple[str, int, str, str, int] = (
                str(data["name"]),
                int(data["amount_shares"]),
                str(data["type_shares"]),
                str(data["currency"]),
                company_detail
            )
            self.postData(
                table=self.getTableName(),
                columns="name, amount_shares, type_shares, currency, CompanyDetail",
                values="%s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            response = self.created
        except Error as error:
            response = self.service_unavailable
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {response}\nError: {error}")
        return response

    def getPossibleShareTypes(self) -> List[str]:
        """
        Retrieving all of the possible share types that are stored
        in the relational database server.
        
        Returns:
            [string]
        """
        response: List[str] = []
        try:
            result_set: Union[List[RowType], List[Dict[str, str]]] = self.getData(
                table_name=self.getTableName(),
                parameters=None,
                column_names="DISTINCT UPPER(type_shares) AS type_shares"
            )
            dataset: Dict[str, Union[int, List[str]]] = self._getPossibleShareTypes(result_set)
            response = dataset["response"] # type: ignore
            self.getLogger().inform(f"The data from the {self.getTableName()} table has been successfully retrieved.\nStatus: {dataset['status']}\nData: {dataset['response']}")
        except Error as error:
            status = 503
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {status}\nError: {error}")
        return response

    def _getPossibleShareTypes(self, result_set: Union[List[RowType], List[Dict[str, str]]]) -> Dict[str, Union[int, List[str]]]:
        """
        Formatting the result set data in the correct format for the
        application.

        Parameters:
            result_set: [{position: string}]: The list of types of shares for the shareholders.

        Returns:
            {status: int, response: [string]}
        """
        response: Dict[str, Union[int, List[str]]]
        status: int
        data: List[str]
        if len(result_set) > 0:
            status = 200
            data = [value["type_shares"] for value in result_set]  # type: ignore
        else:
            status = 204
            data = []
        response = {
            "status": status,
            "response": data
        }
        return response

    def getPossibleCurrencies(self) -> List[str]:
        """
        Retrieving all of the possible currencies that are stored in
        the relational database server.
        
        Returns:
            [string]
        """
        response: List[str] = []
        try:
            result_set: Union[List[RowType], List[Dict[str, str]]] = self.getData(
                table_name=self.getTableName(),
                parameters=None,
                column_names="DISTINCT currency AS currencies"
            )
            dataset: Dict[str, Union[int, List[str]]] = self._getPossibleCurrencies(result_set)
            response = dataset["response"] # type: ignore
            self.getLogger().inform(f"The data from the {self.getTableName()} table has been successfully retrieved.\nStatus: {dataset['status']}\nData: {dataset['response']}")
        except Error as error:
            status = 503
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {status}\nError: {error}")
        return response

    def _getPossibleCurrencies(self, result_set: Union[List[RowType], List[Dict[str, str]]]) -> Dict[str, Union[int, List[str]]]:
        """
        Formatting the result set data in the correct format for the
        application.

        Parameters:
            result_set: [{currencies: string}]: The list of types of shares for the shareholders.

        Returns:
            {status: int, response: [string]}
        """
        response: Dict[str, Union[int, List[str]]]
        status: int
        data: List[str]
        if len(result_set) > 0:
            status = 200
            data = [value["currencies"] for value in result_set]  # type: ignore
        else:
            status = 204
            data = []
        response = {
            "status": status,
            "response": data
        }
        return response