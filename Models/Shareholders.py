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
            status = self.service_unavailable
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
            status = self.ok
            data = [value["type_shares"] for value in result_set]  # type: ignore
        else:
            status = self.no_content
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
            status = self.service_unavailable
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
            status = self.ok
            data = [value["currencies"] for value in result_set]  # type: ignore
        else:
            status = self.no_content
            data = []
        response = {
            "status": status,
            "response": data
        }
        return response

    def get(self) -> List[Shareholder]:
        """
        Retrieving all of the data from the Shareholders table.

        Returns:
            [{identifier: int, CompanyDetail: int, name: string, amount_shares: int, type_shares: string, currency: string}]
        """
        try:
            data: Union[List[RowType], List[Dict[str, Union[int, str]]]] = self.getData(
                table_name=self.getTableName()
            )
            response: Dict[str, Union[int, List[Shareholder]]] = self._get(data)
            self.getLogger().inform(f"The data from {self.getTableName()} has been retrieved!\nStatus: {response['status']}\nData: {response['data']}")
            return response["data"]  # type: ignore
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {self.service_unavailable}\nError: {error}")
            return []

    def _get(self, dataset: Union[List[RowType], List[Dict[str, Union[int, str]]]]) -> Dict[str, Union[int, List[Shareholder]]]:
        """
        Formatting the result set data in the correct format for the
        Shareholder model.

        Parameters:
            dataset: [{identifier: int, CompanyDetail: int, name: string, amount_shares: int, type_shares: string, currency: string}]: The result set data that needs to be formatted.

        Returns:
            {status: int, data: [{identifier: int, CompanyDetail: int, name: string, amount_shares: int, type_shares: string, currency: string}]}
        """
        status: int = self.ok if len(dataset) > 0 else self.no_content
        data: List[Shareholder] = [Shareholder(shareholder) for shareholder in dataset] if len(dataset) > 0 else []
        return {
            "status": status,
            "data": data
        }

    def delete(self) -> int:
        """
        Deleting the data that is in the relational database server.

        Returns:
            int
        """
        try:
            self.deleteData(
                table=self.getTableName(),
                parameters=None
            )
            response = self.no_content
            self.getLogger().inform(f"The data from {self.getTableName()} has been deleted!\nStatus: {response}")
            return response
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {self.service_unavailable}\nError: {error}")
            return self.service_unavailable

    def addCuratedShareholder(self, data: Shareholder) -> int:
        """
        Adding the shareholder data of the company into the
        relational database server.

        Parameters:
            data: {identifier: int, CompanyDetail: int, name: string, amount_shares: int, type_shares: string, currency: string}: The data that has been extracted for the office bearers table.

        Returns:
            int
        """
        response: int
        try:
            parameters: Tuple[int, int, str, int, str, str] = (
                data.identifier,
                data.CompanyDetail,
                data.name,
                data.amount_shares,
                data.type_shares,
                data.currency
            )
            self.postData(
                table=self.getTableName(),
                columns="identifier, CompanyDetail, name, amount_shares, type_shares, currency",
                values="%s, %s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            response = self.created
        except Error as error:
            response = self.service_unavailable
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {response}\nError: {error}")
        return response
