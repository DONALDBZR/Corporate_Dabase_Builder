"""
The Model which will interact exclusively with the Document
Files table.

Authors:
    Andy Ewen Gaspard
"""


from Models.DatabaseHandler import Database_Handler
from Data.DocumentFiles import DocumentFiles
from typing import Dict, Union, Tuple, List, Any
from mysql.connector.types import RowType
from mysql.connector.errors import Error


class Document_Files(Database_Handler):
    """
    The model which will interact exclusively with the Document
    Files table.
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
        self.setTableName("DocumentFiles")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addDocumentFile(self, data: Dict[str, Union[int, Dict[str, Union[str, None, int]], bytes, None]], amount_found: int) -> int:
        """
        Storing the corporate document file into the relational
        database server.

        Parameters:
            data: {status: int, CompanyDetails: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}, DocumentFiles: bytes|null}: The dataset to be used for the data manipulation.
            amount_found: int: The amount of corporate documents that are downloaded.

        Returns:
            int
        """
        amount_downloaded: int
        if data["DocumentFiles"] != None:
            parameters: Tuple[int, bytes] = (
                int(data["CompanyDetails"]["identifier"]), # type: ignore
                bytes(data["DocumentFiles"]) # type: ignore
            )
            self.postData(
                table=self.getTableName(),
                columns="CompanyDetail, file_data",
                values="%s, %s",
                parameters=parameters # type: ignore
            )
            amount_downloaded = amount_found + 1
        else:
            amount_downloaded = amount_found
        return amount_downloaded

    def getCorporateRegistries(self, date_incorporation: str) -> List[DocumentFiles]:
        """
        Retrieving the corporate registries based on the date of
        incorporation of the company.

        Parameters:
            date_incorporation: string: The date of incorporation of the company.

        Returns:
            [{identifier: int, file_data: bytes, company_detail: int}]
        """
        try:
            parameters: Tuple[str] = (date_incorporation,)
            data: Union[List[RowType], List[Dict[str, Union[int, bytes]]]] = self.getData(
                table_name=self.getTableName(),
                parameters=parameters,
                join_condition=f"CompanyDetails ON {self.getTableName()}.CompanyDetail = CompanyDetails.identifier",
                filter_condition="CompanyDetails.is_extracted = 0 AND DATE(FROM_UNIXTIME(CompanyDetails.date_incorporation)) = %s",
                column_names=f"{self.getTableName()}.identifier, {self.getTableName()}.file_data, {self.getTableName()}.CompanyDetail",
                sort_condition=f"{self.getTableName()}.identifier ASC"
            )
            response: Dict[str, Union[int, List[DocumentFiles]]] = self._getCorporateRegistries(data)
            self.getLogger().inform(
                f"The data from {self.getTableName()} has been retrieved!\nStatus: {response['status']}\nData: {data}"
            )
            return response["data"] # type: ignore
        except Error as error:
            self.getLogger().error(
                f"An error occurred in {self.getTableName()}\nStatus: 503\nError: {error}"
            )
            return []

    def _getCorporateRegistries(self, dataset: Union[List[RowType], List[Dict[str, Union[int, bytes]]]]) -> Dict[str, Union[int, List[DocumentFiles]]]:
        """
        Retrieving the correct data type for the application.

        Parameters:
            dataset: [{identifier: int, file_data: bytes, CompanyDetail: int}]: The data from the relational database server.

        Returns:
            {status: int, data: [{identifier: int, file_data: bytes, company_detail: int}]}
        """
        document_files: Dict[str, Union[int, List[DocumentFiles]]]
        if len(dataset) > 0:
            document_files = self.__getCorporateRegistries(dataset)
        else:
            document_files = {
                "status": 204,
                "data": []
            }
        return {
            "status": document_files["status"],
            "data": document_files["data"]
        }

    def __getCorporateRegistries(self, dataset: Union[List[RowType], List[Dict[str, Union[int, bytes]]]]) -> Dict[str, Union[int, List[DocumentFiles]]]:
        """
        Formating the data into the correct datatype when the result
        set is not empty.

        Parameters:
            dataset: [{identifier: int, file_data: bytes, CompanyDetail: int}]: The data from the relational database server.

        Returns:
            {status: int, data: [{identifier: int, file_data: bytes, company_detail: int}]}
        """
        status: int = 200
        data: List[DocumentFiles] = []
        for index in range(0, len(dataset), 1):
            data.append(DocumentFiles(dataset[index]))
        return {
            "status": status,
            "data": data
        }

    def getAmount(self, date_incorporation: str) -> int:
        """
        Retrieving the amount of corporate registries for a specific
        date of incorporation.

        Parameters:
            date_incorporation: string: The date at which the company was legally formed.

        Returns:
            int
        """
        try:
            parameters: Tuple[str] = (date_incorporation,)
            data: Union[List[RowType], List[Dict[str, int]]] = self.getData(
                table_name=self.getTableName(),
                parameters=parameters,
                join_condition=f"CompanyDetails ON {self.getTableName()}.CompanyDetail = CompanyDetails.identifier",
                filter_condition="DATE(FROM_UNIXTIME(CompanyDetails.date_incorporation)) = %s",
                column_names=f"COUNT({self.getTableName()}.identifier) AS amount_found"
            )
            status: int = self.getAmountStatus(data)
            self.getLogger().inform(
                f"The data from {self.getTableName()} has been retrieved!\nStatus: {status}\nData: {data}"
            )
            return int(data[0]["amount_found"]) # type: ignore
        except Error as error:
            self.getLogger().error(
                f"An error occurred in {self.getTableName()}\nStatus: 503\nError: {error}"
            )
            return 0

    def getAmountFound(self, date_incorporation: str) -> int:
        """
        Retrieving the amount of corporate registries for a specific
        date of incorporation.

        Parameters:
            date_incorporation: string: The date at which the company was legally formed.

        Returns:
            int
        """
        try:
            parameters: Tuple[str] = (date_incorporation,)
            data: Union[List[RowType], List[Dict[str, int]]] = self.getData(
                table_name=self.getTableName(),
                parameters=parameters,
                join_condition=f"CompanyDetails ON {self.getTableName()}.CompanyDetail = CompanyDetails.identifier",
                filter_condition="DATE(FROM_UNIXTIME(CompanyDetails.date_incorporation)) = %s AND CompanyDetails.is_extracted = 1",
                column_names=f"COUNT({self.getTableName()}.identifier) AS amount_found"
            )
            status: int = self.getAmountStatus(data)
            self.getLogger().inform(
                f"The data from {self.getTableName()} has been retrieved!\nStatus: {status}\nData: {data}"
            )
            return int(data[0]["amount_found"]) # type: ignore
        except Error as error:
            self.getLogger().error(
                f"An error occurred in {self.getTableName()}\nStatus: 503\nError: {error}"
            )
            return 0

    def getAmountStatus(self, dataset: Union[List[RowType], List[Dict[str, int]]]) -> int:
        """
        Retrieving the status code based on the dataset given.

        Parameters:
            dataset: [{amount_found: int}]: The result set from the relational database server.

        Returns:
            int
        """
        if int(dataset[0]["amount_found"]) == 0: # type: ignore
            return 204
        else:
            return 200