"""
The Model which will interact exclusively with the Office
Bearers table.

Authors:
    Andy Ewen Gaspard
"""


from Models.DatabaseHandler import Database_Handler
from typing import Union, Dict, Tuple, List
from mysql.connector.errors import Error
from mysql.connector.types import RowType


class Office_Bearers(Database_Handler):
    """
    The model which will interact exclusively with the Office
    Bearers.
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
        self.setTableName("OfficeBearers")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addDirectors(self, data: Dict[str, Union[str, int]], company_detail: int) -> int:
        """
        Adding the directors data of the company into the relational
        database server.

        Parameters:
            data: {position: string, name: string, address: string, date_appointment: int}: The data that has been extracted for the office bearers table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        response: int
        try:
            parameters: Tuple[str, str, str, int, int] = (
                str(data["position"]),
                str(data["name"]),
                str(data["address"]),
                int(data["date_appointment"]),
                company_detail
            )
            self.postData(
                table=self.getTableName(),
                columns="position, name, address, date_appointment, CompanyDetail",
                values="%s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            response = 201
        except Error as error:
            response = 503
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {response}\nError: {error}")
        return response

    def getPossiblePositions(self) -> List[str]:
        """
        Retrieving all of the possible positions that are stored in
        the relational database server.
        
        Returns:
            [string]
        """
        response: List[str] = []
        try:
            result_set: Union[List[RowType], List[Dict[str, str]]] = self.getData(
                table_name=self.getTableName(),
                parameters=None,
                column_names="DISTINCT UPPER(position) AS position"
            )
            dataset: Dict[str, Union[int, List[str]]] = self._getPossiblePositions(result_set)
            response = dataset["response"] # type: ignore
            self.getLogger().inform(f"The data from the {self.getTableName()} table has been successfully retrieved.\nStatus: {dataset['status']}\nData: {dataset['response']}")
        except Error as error:
            status = 503
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {status}\nError: {error}")
        return response

    def _getPossiblePositions(self, result_set: Union[List[RowType], List[Dict[str, str]]]) -> Dict[str, Union[int, List[str]]]:
        """
        Formatting the result set data in the correct format for the
        application.

        Parameters:
            result_set: [{position: string}]: The list of positions for the office bearers.

        Returns:
            {status: int, response: [string]}
        """
        response: Dict[str, Union[int, List[str]]]
        status: int
        data: List[str]
        if len(result_set) > 0:
            status = 200
            data = [value["position"] for value in result_set]  # type: ignore
        else:
            status = 204
            data = []
        response = {
            "status": status,
            "response": data
        }
        return response

    def addDirectorsForeignDomestic(self, data: Dict[str, Union[str, int]], company_detail: int) -> int:
        """
        Adding the directors data of a foreign domestic company into
        the relational database server.

        Parameters:
            data: {position: string, name: string, date_appointment: int}: The data that has been extracted for the office bearers table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        response: int
        try:
            parameters: Tuple[str, str, int, int] = (
                str(data["position"]),
                str(data["name"]),
                int(data["date_appointment"]),
                company_detail
            )
            self.postData(
                table=self.getTableName(),
                columns="position, name, date_appointment, CompanyDetail",
                values="%s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            response = 201
        except Error as error:
            response = 503
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {response}\nError: {error}")
        return response