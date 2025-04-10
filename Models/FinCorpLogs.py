"""
The Model which will interact exclusively with the
FinCorpLogs table.

Authors:
    Solofonavalona Randirantsilavo
    Andy Ewen Gaspard
"""


from time import sleep
from Models.DatabaseHandler import Database_Handler
from Data.FinCorpLogs import FinCorpLogs
from typing import Union, Dict, List, Tuple, Any
from mysql.connector.types import RowType
from mysql.connector.errors import Error


class FinCorp_Logs(Database_Handler):
    """
    The model which will interact exclusively with the
    FinCorpLogs.
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
        self.setTableName("FinCorpLogs")
        self.getLogger().inform(
            "The model has been successfully been initiated with its dependencies."
        )

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def getSuccessfulRunsLogs(self, method_name: str) -> List[FinCorpLogs]:
        """
        Retrieving the list of all successful runs.

        Parameters:
            method_name: string: The name of the method.

        Returns:
            [{identifier: int, method_name: string, year: int, quarter: string, date_start: int, date_to: int, status: int, amount: int}]
        """
        try:
            parameters: Tuple[str] = (method_name,)
            data: Union[List[RowType], List[Dict[str, Union[int, str]]]] = self.getData(
                table_name=self.getTableName(),
                parameters=parameters,
                filter_condition="status <= 499 AND method_name = %s"
            )
            response: Dict[str, Union[int, List[FinCorpLogs]]] = self._getSuccessfulLogs(data)
            self.getLogger().inform(f"The data from {self.getTableName()} has been retrieved!\nStatus: {response['status']}\nData: {data}")
            return response["data"]  # type: ignore
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: 503\nError: {error}")
            return []

    def _getSuccessfulLogs(self, dataset: Union[List[RowType], List[Dict[str, Union[int, str]]]]) -> Dict[str, Union[int, List[FinCorpLogs]]]:
        """
        Retrieving the data into the correct data type for the
        application.

        Parameters:
            data: [{identifier: int, method_name: string, year: int, quarter: string, date_start: int, date_to: int, status: int, amount: int}]: The data from the relational database server.

        Returns:
            {status: int, data: [{identifier: int, method_name: string, year: int, quarter: string, date_start: int, date_to: int, status: int, amount: int}]}
        """
        succesful_logs: Dict[str, Union[int, List[FinCorpLogs]]]
        if len(dataset) > 0:
            succesful_logs = self.__getSuccessfulLogs(dataset)
        else:
            succesful_logs = {
                "status": 204,
                "data": [
                    FinCorpLogs({
                        "identifier": None,
                        "method_name": None,
                        "year": None,
                        "quarter": None,
                        "date_start": None,
                        "date_to": None,
                        "status": None,
                        "amount": None,
                    })
                ]
            }
        return {
            "status": succesful_logs["status"],
            "data": succesful_logs["data"]
        }

    def __getSuccessfulLogs(self, dataset: Union[List[RowType], List[Dict[str, Union[int, str]]]]) -> Dict[str, Union[int, List[FinCorpLogs]]]:
        """
        Formating the data into the correct datatype when the result
        set is not empty.

        Parameters:
            dataset: [{identifier: int, method_name: string, year: int, quarter: string, date_start: int, date_to: int, status: int, amount: int}]: The data from the relational database server.

        Returns:
            {status: int, data: [{identifier: int, method_name: string, year: int, quarter: string, date_start: int, date_to: int, status: int, amount: int}]}
        """
        status: int = 200
        data: List[FinCorpLogs] = []
        for index in range(0, len(dataset), 1):
            data.append(FinCorpLogs(dataset[index]))  # type: ignore
        return {
            "status": status,
            "data": data
        }

    def postSuccessfulCorporateDataCollectionRun(self, data: Tuple[Any]) -> None:
        """
        Inserting the successful run for the corporate data collection.

        Parameters:
            data (Tuple[Any]): The data to be inserted.

        Returns:
            None
        """
        sleep(1)
        return self.postData(
            table=self.getTableName(),
            columns="method_name, quarter, date_start, date_to, status, amount, amount_found",
            values="%s, %s, %s, %s, %s, %s, %s",
            parameters=data
        )

    def postFailedCorporateDataCollectionRun(self, data: Tuple[Any]) -> None:
        """
        Inserting the failure run for the corporate data collection.

        Parameters:
            data: array

        Returns:
            void
        """
        return self.postData(
            table=self.getTableName(),
            columns="method_name, quarter, date_start, date_to, status, amount, amount_found",
            values="%s, %s, %s, %s, %s, %s, %s",
            parameters=data
        )
