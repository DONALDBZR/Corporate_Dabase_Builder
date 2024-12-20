"""
The Data Transfer Object for the Liabilities.

Authors:
    Darkness4869
"""


from dataclasses import dataclass
from mysql.connector.types import RowType
from typing import Union, Dict

@dataclass
class Liabilities:
    """
    The Data Transfer Object for the Liabilities.
    """
    identifier: int
    BalanceSheet: int
    date_updated: int
    total_liabilities: float
    total_equity_and_liabilities: float

    def __init__(self, dataset: Union[RowType, Dict[str, Union[int, float]]]):
        """
        Initializing the data class object.

        Parameters:
            dataset: {identifier: int, BalanceSheet: int, date_updated: int, total_liabilities: float, total_equity_and_liabilities: float} The result set from the relational database server.
        """
        self.identifier = int(dataset["identifier"]) # type: ignore
        self.BalanceSheet = int(dataset["BalanceSheet"]) # type: ignore
        self.date_updated = int(dataset["date_updated"]) # type: ignore
        self.total_liabilities = float(dataset["total_liabilities"]) # type: ignore
        self.total_equity_and_liabilities = float(dataset["total_equity_and_liabilities"]) # type: ignore