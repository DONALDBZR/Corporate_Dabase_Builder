"""
The model which will interact exclusively with the Financial
Summaries table.

Authors:
    Darkness4869
"""


from Models.DatabaseHandler import Database_Handler
from typing import Union, Tuple, Dict
from mysql.connector.errors import Error


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