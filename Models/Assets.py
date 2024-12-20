"""
The model which will interact exclusively with the Assets
table.

Authors:
    Darkness4869
"""


from Data.Assets import Assets as data_object
from Models.DatabaseHandler import Database_Handler
from typing import Dict, Union, Tuple, List
from mysql.connector.errors import Error
from mysql.connector.types import RowType


class Assets(Database_Handler):
    """
    The model which will interact exclusively with the Assets
    table.
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
    ok: int = 200
    """
    The status code for a successful response
    """
    no_content: int = 204
    """
    The status code when there is no content.
    """

    def __init__(self):
        """
        Initializing all of the dependencies which will be used to
        operate the application.
        """
        super().__init__()
        self.setTableName("Assets")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addAssets(self, data: Dict[str, Union[Dict[str, float], float]], balance_sheet: int) -> int:
        """
        Adding the balance sheet of the company.

        Parameters:
            data: {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}: The data of the assets.
            balance_sheet: int: The identifier of a balance sheet.

        Returns:
            int
        """
        try:
            parameters: Tuple[int, float] = (balance_sheet, float(data["total"])) # type: ignore
            self.postData(
                table=self.getTableName(),
                columns="BalanceSheet, total",
                values="%s, %s",
                parameters=parameters # type: ignore
            )
            self.getLogger().inform(f"The data has been successfully stored.\nStatus: {self.created}")
            return self.created
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {self.service_unavailable}\nError: {error}")
            return self.service_unavailable

    def getSpecific(self, balance_sheet: int) -> data_object:
        """
        Retrieving the data of the assets.

        Parameters:
            balance_sheet: int: The identifier of the balance sheet.

        Returns:
            {identifier: int, BalanceSheet: int, date_updated: int, total: float}
        """
        try:
            parameters: Tuple[int] = (balance_sheet,)
            data: Union[List[RowType], List[Dict[str, Union[int, float]]]] = self.getData(
                table_name=self.getTableName(),
                filter_condition="BalanceSheet = %s",
                parameters=parameters # type: ignore
            )
            response: Dict[str, Union[int, data_object]] = self._getSpecific(data)
            self.getLogger().inform(f"The data from {self.getTableName()} has been retrieved!\nStatus: {response['status']}\nData: {data}")
            return response["data"] # type: ignore
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {self.service_unavailable}\nError: {error}")
            return data_object({})