"""
The Data Transfer Object for the Assets.

Authors:
    Darkness4869
"""


from dataclasses import dataclass
from mysql.connector.types import RowType
from typing import Union, Dict

@dataclass
class Assets:
    """
    The Data Transfer Object for the Assets.
    """
    identifier: int
    BalanceSheet: int
    date_updated: int
    total: float

    def __init__(self, dataset: Union[RowType, Dict[str, Union[int, float]]]):
        """
        Initializing the data class object.

        Parameters:
            dataset: {identifier: int, BalanceSheet: int, date_updated: int, total: float: The result set from the relational database server.
        """
        self.identifier = int(dataset["identifier"]) # type: ignore
        self.BalanceSheet = int(dataset["BalanceSheet"]) # type: ignore
        self.date_updated = int(dataset["date_updated"]) # type: ignore
        self.total = float(dataset["total"]) # type: ignore