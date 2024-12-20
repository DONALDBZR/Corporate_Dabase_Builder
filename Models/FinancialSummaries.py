"""
The model which will interact exclusively with the Financial
Summaries table.

Authors:
    Darkness4869
"""


from Data.FinancialSummaries import FinancialSummaries
from Models.DatabaseHandler import Database_Handler
from typing import Union, Tuple, Dict, List
from mysql.connector.errors import Error
from mysql.connector.types import RowType


class Financial_Summaries(Database_Handler):
    """
    The model which will interact exclusively with the Financial
    Summaries table.
    """
    __table_name: str
    """
    The table which the model is linked to.
    """
    created: int = 201
    """
    The status code for a successful creation.
    """
    service_unavailable: int = 503
    """
    The status code for an unavailable service.
    """

    def __init__(self) -> None:
        """
        Initializing all of the dependencies which will be used to
        operate the application.
        """
        super().__init__()
        self.setTableName("FinancialSummaries")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addFinancialSummary(self, financial_summary: Dict[str, Union[int, str]], company_detail: int) -> int:
        """
        Adding the financial summary data of the company into the
        relational database server.

        Parameters:
            financial_summary: {financial_year: int, currency: string, date_approved: int}: The data that has been extracted for the table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        try:
            parameters: Tuple[int, int, str, int] = (company_detail, int(financial_summary["financial_year"]), str(financial_summary["currency"]), int(financial_summary["date_approved"]))
            self.postData(
                table=self.getTableName(),
                columns="CompanyDetail, financial_year, currency, date_approved",
                values="%s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            self.getLogger().inform(f"The data has been successfully stored.\nStatus: {self.created}")
            return self.created
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {self.service_unavailable}\nError: {error}")
            return self.service_unavailable

    def getSpecific(self, company_detail: int, financial_year: int) -> FinancialSummaries:
        """
        Retrieving the data of the financial summary.

        Parameters:
            company_detail: int: The identifier of the company.
            financial_year: int: The financial year for which the data needs to be retrieved.

        Returns:
            int
        """
        try:
            parameters: Tuple[int] = (company_detail,)
            data: Union[List[RowType], List[Dict[str, Union[int, str]]]] = self.getData(
                table_name=self.getTableName(),
                filter_condition="CompanyDetail = %s",
                parameters=parameters # type: ignore
            )
            response: Dict[str, Union[int, FinancialSummaries]] = self._getSpecific(data)
            self.getLogger().inform(f"The data from {self.getTableName()} has been retrieved!\nStatus: {response['status']}\nData: {data}")
            return response["data"] # type: ignore
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {self.service_unavailable}\nError: {error}")
            return FinancialSummaries({})

    def _getSpecific(self, dataset: Union[List[RowType], List[Dict[str, Union[int, str, None]]]]) -> Dict[str, Union[int, FinancialSummaries]]:
        """
        Retrieving the data into the correct data type for the
        application.

        Parameters:
            dataset: [{identfier: int, CompanyDetail: int, financial_year: int, currency: string, date_approved: int, unit: int|null}]: The data from the relational database server.

        Returns:
            {status: int, data: {identfier: int, CompanyDetail: int, financial_year: int, currency: string, date_approved: int, unit: int|null}}
        """
        no_content: int = 204
        ok: int = 200
        service_unavailable: int = 503
        status: int = 0
        status = ok if len(dataset) == 1 else service_unavailable
        status = no_content if len(dataset) == 0 else status
        data: List[FinancialSummaries] = [FinancialSummaries(financial_summary) for financial_summary in dataset] if len(dataset) > 0 else []
        return {
            "status": status,
            "data": data[0] if len(data) == 1 else FinancialSummaries({})
        }