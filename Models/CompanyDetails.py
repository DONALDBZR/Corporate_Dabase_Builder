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
from Data.CompanyDetails import CompanyDetails
from symbol import parameters


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

    def getAmountDownloadedCorporateDocumentsStatus(self, dataset: Union[List[RowType], List[Dict[str, int]]]) -> int:
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

    def getAmount(self, date_incorporation: str) -> int:
        """
        Retrieving the amount of the downloaded of corporate
        documents for a specific date of incorporation.

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
                filter_condition="DATE(FROM_UNIXTIME(date_incorporation)) = %s",
                column_names=f"COUNT({self.getTableName()}.identifier) AS amount_found"
            )
            status: int = self.getAmountDownloadedCorporateDocumentsStatus(data)
            self.getLogger().inform(
                f"The data from {self.getTableName()} has been retrieved!\nStatus: {status}\nData: {data}"
            )
            return int(data[0]["amount_found"]) # type: ignore
        except Error as error:
            self.getLogger().error(
                f"An error occurred in {self.getTableName()}\nStatus: 503\nError: {error}"
            )
            return 0

    def getAmountDownloadedCorporateDocuments(self, date_incorporation: str) -> int:
        """
        Retrieving the amount of the downloaded of corporate
        documents for a specific date of incorporation.

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
                join_condition=f"DocumentFiles ON DocumentFiles.CompanyDetail = {self.getTableName()}.identifier",
                filter_condition="DATE(FROM_UNIXTIME(CompanyDetails.date_incorporation)) = %s AND DocumentFiles.identifier IS NOT NULL",
                column_names=f"COUNT({self.getTableName()}.identifier) AS amount_found"
            )
            status: int = self.getAmountDownloadedCorporateDocumentsStatus(data)
            self.getLogger().inform(
                f"The data from {self.getTableName()} has been retrieved!\nStatus: {status}\nData: {data}"
            )
            return int(data[0]["amount_found"]) # type: ignore
        except Error as error:
            self.getLogger().error(
                f"An error occurred in {self.getTableName()}\nStatus: 503\nError: {error}"
            )
            return 0

    def getCompanyDetailsForDownloadCorporateDocumentFile(self, date_incorporation: str) -> List[CompanyDetails]:
        """
        Retrieving the company details which will be used as
        parameters for the crawler to retrieve the corporate
        document file.

        Parameters:
            date_incorporation: string: The date at which the company was legally formed.

        Returns:
            [{identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int, is_extracted: int, company_identifier: int, company_type: string}]
        """
        try:
            parameters: Tuple[str] = (date_incorporation,)
            data: Union[List[RowType], List[Dict[str, Union[int, str]]]] = self.getData(
                table_name=self.getTableName(),
                parameters=parameters,
                filter_condition="DATE(FROM_UNIXTIME(date_incorporation)) = %s AND date_verified IS NULL"
            )
            response: Dict[str, Union[int, List[CompanyDetails]]] = self._getCompanyDetailsForDownloadCorporateDocumentFile(data)
            self.getLogger().inform(
                f"The data from {self.getTableName()} has been retrieved!\nStatus: {response['status']}\nData: {data}"
            )
            return response["data"]  # type: ignore
        except Error as error:
            self.getLogger().error(
                f"An error occurred in {self.getTableName()}\nStatus: 503\nError: {error}"
            )
            return []

    def _getCompanyDetailsForDownloadCorporateDocumentFile(self, dataset: Union[List[RowType], List[Dict[str, Union[int, str]]]]) -> Dict[str, Union[int, List[CompanyDetails]]]:
        """
        Retrieving the data into the correct data type for the
        application.

        Parameters:
            dataset: [{identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int, is_extracted: int, company_identifier: int, company_type: string}]: The data from the relational database server.

        Returns:
            {status: int, data: [{identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int, is_extracted: int, company_identifier: int, company_type: string}]}
        """
        company_details: Dict[str, Union[int, List[CompanyDetails]]]
        if len(dataset) > 0:
            company_details = self.__getCompanyDetailsForDownloadCorporateDocumentFile(dataset)
        else:
            company_details = {
                "status": 204,
                "data": []
            }
        return {
            "status": company_details["status"],
            "data": company_details["data"]
        }

    def __getCompanyDetailsForDownloadCorporateDocumentFile(self, dataset: Union[List[RowType], List[Dict[str, Union[int, str]]]]) -> Dict[str, Union[int, List[CompanyDetails]]]:
        """
        Formating the data into the correct datatype when the result
        set is not empty.

        Parameters:
            dataset: [{identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int, is_extracted: int, company_identifier: int, company_type: string}]: The data from the relational database server.

        Returns:
            {status: int, data: [{identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int, is_extracted: int, company_identifier: int, company_type: string}]}
        """
        status: int = 200
        data: List[CompanyDetails] = []
        for index in range(0, len(dataset), 1):
            data.append(CompanyDetails(dataset[index]))  # type: ignore
        return {
            "status": status,
            "data": data
        }

    def updateCompany(self, data: Dict[str, Union[int, str]]) -> None:
        """
        Updating the data inside of the company details table.

        Parameters:
            data: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int}: The data of the company to be updated.

        Returns:
            void
        """
        parameters: Tuple[str, str, str, int, str, str, int, int] = (
            str(data["name"]),
            str(data["file_number"]),
            str(data["category"]),
            int(data["date_incorporation"]),
            str(data["nature"]),
            str(data["status"]),
            int(data["date_verified"]),
            int(data["identifier"])
        )
        return self.updateData(
            table=self.getTableName(),
            values="name = %s, file_number = %s, category = %s, date_incorporation = %s, nature = %s, status = %s, date_verified = %s",
            parameters=parameters, # type: ignore
            condition="identifier = %s"
        )

    def updateCorporateMetadata(self, data: Dict[str, Union[str, int]], identifier: int) -> int:
        """
        Updating the Corporate Metadata.

        Parameters:
            data: {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int, is_extracted: int, company_identifier: int, company_type: string}: The data that has been extracted for the company details table.
            identifier: int: The identifier of the company.

        Returns:
            int
        """
        response: int
        try:
            parameters: Tuple[str, str, str, str, int, str, str, int, int, int, str, int] = (
                str(data["business_registration_number"]),
                str(data["name"]),
                str(data["file_number"]),
                str(data["category"]),
                int(data["date_incorporation"]),
                str(data["nature"]),
                str(data["status"]),
                int(data["is_extracted"]),
                int(data["date_verified"]),
                int(data["company_identifier"]),
                str(data["company_type"]),
                identifier
            )
            self.updateData(
                table=self.getTableName(),
                values="business_registration_number = %s, name = %s, file_number = %s, category = %s, date_incorporation = %s, nature = %s, status = %s, is_extracted = %s, date_verified = %s, company_identifier = %s, company_type = %s",
                parameters=parameters, # type: ignore
                condition="identifier = %s"
            )
            response = 202
        except Error as error:
            response = 503
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {response}\nError: {error}")
        return response

    def getSpecificCompanyDetails(self, identifier: int) -> CompanyDetails:
        """
        Retrieving a specific company detail.

        Parameters:
            identifier: int: The identifier of a company.

        Returns:
            {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int, is_extracted: int, company_identifier: int, company_type: string}
        """
        try:
            parameters: Tuple[int] = (identifier,)
            data: Union[RowType, Dict[str, Union[int, str]]] = self.getData(
                table_name=self.getTableName(),
                parameters=parameters,
                filter_condition="identifier = %s"
            )[0]
            response: Dict[str, Union[int, CompanyDetails]] = self._getSpecificCompanyDetails(data)
            self.getLogger().inform(
                f"The data from {self.getTableName()} has been retrieved!\nStatus: {response['status']}\nData: {data}"
            )
            return response["data"]  # type: ignore
        except Error as error:
            self.getLogger().error(
                f"An error occurred in {self.getTableName()}\nStatus: 503\nError: {error}"
            )
            return CompanyDetails({})

    def _getSpecificCompanyDetails(self, dataset: Union[RowType, Dict[str, Union[int, str]]]) -> Dict[str, Union[int, CompanyDetails]]:
        """
        Retrieving the data into the correct data type for the
        application.

        Parameters:
            dataset: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int, is_extracted: int, company_identifier: int, company_type: string}: The data from the relational database server.

        Returns:
            {status: int, data: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int, is_extracted: int, company_identifier: int, company_type: string}}
        """
        company_details: Dict[str, Union[int, CompanyDetails]]
        if len(dataset) > 0:
            company_details = self.__getSpecificCompanyDetails(dataset)
        else:
            company_details = {
                "status": 204,
                "data": CompanyDetails({})
            }
        return company_details