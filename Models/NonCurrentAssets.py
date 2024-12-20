"""
The model which will interact exclusively with the Non
Current Assets table.

Authors:
    Darkness4869
"""


from Models.DatabaseHandler import Database_Handler
from typing import Dict, Union, Tuple
from mysql.connector.errors import Error


class Non_Current_Assets(Database_Handler):
    """
    The model which will interact exclusively with the Non
    Current Assets table.
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
        self.setTableName("NonCurrentAssets")
        self.getLogger().inform("The model has been successfully been initiated with its dependencies.")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def addAsset(self, data: Dict[str, float], asset: int) -> int:
        """
        Adding the balance sheet of the company.

        Parameters:
            data: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}: The data of the assets.
            asset: int: The identifier of an asset.

        Returns:
            int
        """
        try:
            parameters: Tuple[int, float, float, float, float, float, float, float, float] = (asset, data["property_plant_equipment"], data["investment_properties"], data["intangible_assets"], data["other_investments"], data["subsidiaries_investments"], data["biological_assets"], data["others"], data["total"])
            self.postData(
                table=self.getTableName(),
                columns="Asset, property_plant_equipment, investment_properties, intangible_assets, other_investments, subsidiaries_investments, biological_assets, others, total",
                values="%s, %s, %s, %s, %s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            self.getLogger().inform(f"The data has been successfully stored.\nStatus: {self.created}")
            return self.created
        except Error as error:
            self.getLogger().error(f"An error occurred in {self.getTableName()}\nStatus: {self.service_unavailable}\nError: {error}")
            return self.service_unavailable