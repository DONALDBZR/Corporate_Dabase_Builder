"""
The Model which will interact exclusively with the Company
Details table.

Authors:
    Solofonavalona Randirantsilavo
    Andy Ewen Gaspard
"""


from Models.DatabaseHandler import Database_Handler
from typing import Union, Dict, List, Tuple, Any
from mysql.connector.types import RowType
from mysql.connector.errors import Error


class Company_Details(Database_Handler):
    """
    The model which will interact exclusively with the Company
    Details.
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
        self.setTableName("CompanyDetails")
        self.getLogger().inform(
            "The model has been successfully been initiated with its dependencies."
        )

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addCompany(self, data: Tuple[Any]) -> None:
        """
        Adding the compony metadata into the relational database
        server.

        Parameters:
            data: array

        Returns:
            void
        """
        return self.postData(
            table=self.getTableName(),
            parameters=data,
            columns="name, file_number, category, date_incorporation, nature, status",
            values="%s, %s, %s, %s, %s, %s"
        )

    def getCompanyDetailsForDownloadCorporateDocumentFile(self, date_incorporation: str) -> List[CompanyDetails]:
        """
        Retrieving the company details which will be used as
        parameters for the crawler to retrieve the corporate
        document file.

        Parameters:
            date_incorporation: string: The date at which the company was legally formed.

        Returns:
            [{identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}]
        """
        try:
            parameters: Tuple[str] = (date_incorporation,)
            data: Union[List[RowType], List[Dict[str, Union[int, str]]]] = self.getData(
                table_name=self.getTableName(),
                parameters=parameters,
                filter_condition="DATE(FROM_UNIXTIME(date_incorporation)) = %s"
            )
            response: Dict[str, Union[int, List[CompanyDetails]]] = self._getSuccessfulLogs(data)
            self.getLogger().inform(
                f"The data from {self.getTableName()} has been retrieved!\nStatus: {response['status']}\nData: {data}"
            )
            return response["data"]  # type: ignore
        except Error as error:
            self.getLogger().error(
                f"An error occurred in {self.getTableName()}\nStatus: 503\nError: {error}"
            )
            return []
