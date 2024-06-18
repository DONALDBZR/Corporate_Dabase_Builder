"""
The Model which will interact exclusively with the Document
Files table.

Authors:
    Andy Ewen Gaspard
"""


from Models.DatabaseHandler import Database_Handler
from typing import Dict, Union, Tuple


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