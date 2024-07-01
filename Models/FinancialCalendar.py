"""
The Model which will interact exclusively with the Financial
Calendar table.

Authors:
    Solofonavalona Randirantsilavo
    Andy Ewen Gaspard
"""


from Models.DatabaseHandler import Database_Handler
from Data.FinancialCalendar import FinancialCalendar
from typing import Union, Dict
from mysql.connector.types import RowType
from mysql.connector.errors import Error


class Financial_Calendar(Database_Handler):
    """
    The model which will interact exclusively with the Financial
    Calendar.
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
        self.setTableName("FinancialCalendar")
        self.getLogger().inform(
            "The model has been successfully been initiated with its dependencies."
        )

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def getCurrentQuarter(self) -> Union[FinancialCalendar, None]:
        """
        Retrieving the current financial quarter.

        Returns:
            {year: int, quarter: string, start_date: string, end_date: string} | null
        """
        try:
            data: Union[RowType, Dict[str, Union[int, str]]] = self.getData(
                table_name=self.getTableName(),
                filter_condition="CONCAT(YEAR(CURDATE()), '-', start_date) <= CURDATE() AND CONCAT(YEAR(CURDATE()), '-', end_date) >= CURDATE()",
                column_names="YEAR(CURDATE()) AS year, quarter, FROM_UNIXTIME(UNIX_TIMESTAMP(CONCAT(YEAR(CURDATE()), '-', start_date)), '%m/%d/%Y') AS start_date, FROM_UNIXTIME(UNIX_TIMESTAMP(CONCAT(YEAR(CURDATE()), '-', end_date)), '%m/%d/%Y') AS end_date"
            )[0]
            self.getLogger().inform(
                f"The data from {self.getTableName()} has been retrieved!\nStatus: 200\nData: {data}"
            )
            return FinancialCalendar(data)
        except Error as error:
            self.getLogger().error(
                f"An error occurred in {self.getTableName()}\nStatus: 503\nError: {error}"
            )
            return None