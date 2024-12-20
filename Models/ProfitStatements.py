"""
The model which will interact exclusively with the Profit
Statements table.

Authors:
    Darkness4869
"""


from Models.DatabaseHandler import Database_Handler
from typing import Dict, Union, Tuple
from mysql.connector.errors import Error


class Profit_Statements(Database_Handler):
    """
    The model which will interact exclusively with the Profit
    Statements table.
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

    def __init__(self):
        """
        Initializing all of the dependencies which will be used to
        operate the application.
        """
        super().__init__()
        self.setTableName("ProfitStatements")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addProfitStatement(self, data: Dict[str, Union[Dict[str, Union[int, str]], float]], financial_summary: int) -> int:
        """
        Adding the profit statement of the company.

        Parameters:
            data: {financial_summary: {financial_year: int, currency: string, date_approved: int, unit: int}, turnover: float, cost_of_sales: float, gross_profit: float, other_income: float, distribution_cost: float, administration_cost: float, expenses: float, finance_cost: float, net_profit_before_taxation: float, taxation: float, net_profit: float}: The data of the profit statement.
            financial_summary: int: The identifier of the financial summary.

        Returns:
            int
        """
        try:
            parameters: Tuple[int, float, float, float, float, float, float, float, float, float, float, float] = (financial_summary, float(data["turnover"]), float(data["cost_of_sales"]), float(data["gross_profit"]), float(data["other_income"]), float(data["distribution_cost"]), float(data["administration_cost"]), float(data["expenses"]), float(data["finance_cost"]), float(data["net_profit_before_taxation"]), float(data["taxation"]), float(data["net_profit"])) # type: ignore
            self.postData(
                table=self.getTableName(),
                columns="FinancialSummary, turnover, cost_of_sales, gross_profit, other_income, distribution_cost, administration_cost, expenses, finance_cost, net_profit_before_taxation, taxation, net_profit",
                values="%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            self.getLogger().inform(f"The data has been successfully stored.\nStatus: {self.created}")
            return self.created
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {self.service_unavailable}\nError: {error}")
            return self.service_unavailable