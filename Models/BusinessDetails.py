"""
The Model which will interact exclusively with the Business
Details table.

Authors:
    Andy Ewen Gaspard
    Darkness4869
"""


from Models.DatabaseHandler import Database_Handler
from typing import Dict, Tuple, List, Union
from mysql.connector.errors import Error
from Data.BusinessDetails import BusinessDetails
from mysql.connector.types import RowType


class Business_Details(Database_Handler):
    """
    The model which will interact exclusively with the Business
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
        self.setTableName("BusinessDetails")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addBusinessDetailsDomestic(self, data: Dict[str, str], company_detail: int) -> int:
        """
        Adding the business details of a domestic company into the
        relational database server.

        Parameters:
            data: {registered_address: string, name: string, nature: string, operational_address: string}: The data that has been extracted for the business details table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        response: int
        try:
            parameters: Tuple[str, str, str, str, int] = (
                str(data["registered_address"]),
                str(data["name"]),
                str(data["nature"]),
                str(data["operational_address"]),
                company_detail
            )
            self.postData(
                table=self.getTableName(),
                columns="registered_address, name, nature, operational_address, CompanyDetail",
                values="%s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            response = 201
        except Error as error:
            response = 503
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {response}\nError: {error}")
        return response

    def addBusinessDetailsAuthorisedCompany(self, data: Dict[str, str], company_detail: int) -> int:
        """
        Adding the business details of an authorised company into
        the relational database server.

        Parameters:
            data: {registered_address: string}: The data that has been extracted for the business details table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        response: int
        try:
            parameters: Tuple[str, int] = (
                str(data["registered_address"]),
                company_detail
            )
            self.postData(
                table=self.getTableName(),
                columns="registered_address, CompanyDetail",
                values="%s, %s",
                parameters=parameters # type: ignore
            )
            response = 201
        except Error as error:
            response = 503
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {response}\nError: {error}")
        return response

    def addBusinessDetailsDomesticCivil(self, data: Dict[str, str], company_detail: int) -> int:
        """
        Adding the business details of a société civile or société
        commerciale into the relational database server.

        Parameters:
            data: {registered_address: string}: The data that has been extracted for the business details table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        response: int
        try:
            parameters: Tuple[str, int] = (
                str(data["registered_address"]),
                company_detail
            )
            self.postData(
                table=self.getTableName(),
                columns="registered_address, CompanyDetail",
                values="%s, %s",
                parameters=parameters # type: ignore
            )
            response = 201
        except Error as error:
            response = 503
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {response}\nError: {error}")
        return response

    def addBusinessDetailsForeignDomestic(self, data: Dict[str, str], company_detail: int) -> int:
        """
        Adding the business details of a domestic company into the
        relational database server.

        Parameters:
            data: {name: string, nature: string, operational_address: string}: The data that has been extracted for the business details table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        response: int
        try:
            parameters: Tuple[str, str, str, int] = (
                str(data["name"]),
                str(data["nature"]),
                str(data["operational_address"]),
                company_detail
            )
            self.postData(
                table=self.getTableName(),
                columns="name, nature, operational_address, CompanyDetail",
                values="%s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            response = 201
        except Error as error:
            response = 503
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {response}\nError: {error}")
        return response

    def getBusinessDetails(self) -> List[BusinessDetails]:
        """
        Retrieving the data from the Business Details for curation.

        Returns:
            [{identifier: int, CompanyDetail: int, registered_address: string|null, name: string|null, nature: string|null, operational_address: string|null}]
        """
        try:
            data: Union[List[RowType], List[Dict[str, Union[int, str, None]]]] = self.getData(
                table_name=self.getTableName()
            )
            response: Dict[str, Union[int, List[BusinessDetails]]] = self._getBusinessDetailsData(data)
            self.getLogger().inform(f"The data from {self.getTableName()} has been retrieved!\nStatus: {response['status']}\nData: {response['data']}")
            return response['data']  # type: ignore
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: 503\nError: {error}")
            return []

    def _getBusinessDetailsData(self, dataset: Union[List[RowType], List[Dict[str, Union[int, str, None]]]]) -> Dict[str, Union[int, List[BusinessDetails]]]:
        """
        Retrieving the data into the correct data type for the
        application.

        Parameters:
            dataset: [{identifier: int, CompanyDetail: int, registered_address: string|null, name: string|null, nature: string|null, operational_address: string|null}]: The data from the relational database server.

        Returns:
            {status: int, data: [{identifier: int, CompanyDetail: int, registered_address: string|null, name: string|null, nature: string|null, operational_address: string|null}]}
        """
        status: int = 200 if len(dataset) > 0 else 204
        data: List[BusinessDetails] = [BusinessDetails(business_detail) for business_detail in dataset] if len(dataset) > 0 else []
        return {
            "status": status,
            "data": data
        }

    def updateBusinessDetail(self, business_detail: BusinessDetails) -> int:
        """
        Updating the data that is stored in the relational database
        server.

        Parameters:
            business_detail: {identifier: int, CompanyDetail: int, registered_address: string|null, name: string|null, nature: string|null, operational_address: string|null}: The business detail data.

        Returns:
            int
        """
        parameters: Tuple[Union[str, None], Union[str, None], Union[str, None], Union[str, None], int, int] = (business_detail.registered_address, business_detail.name, business_detail.nature, business_detail.operational_address, business_detail.identifier, business_detail.CompanyDetail)
        try:
            self.updateData(
                table=self.getTableName(),
                values="registered_address = %s, name = %s, nature = %s, operational_address = %s",
                condition="identifier = %s AND CompanyDetail = %s",
                parameters=parameters # type: ignore
            )
            return 202
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: 503\nError: {error}")
            return 503