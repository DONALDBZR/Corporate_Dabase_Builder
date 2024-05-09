"""
The Data Transfer Object for the Financial Calendar.

Authors:
    Andy Ewen Gaspard
"""


from dataclasses import dataclass
from mysql.connector.types import RowType
from typing import Union, Dict


@dataclass
class FinancialCalendar:
    """
    The Data Transfer Object for the Financial Calendar.
    """
    year: int
    quarter: str
    start_date: str
    end_date: str

    def __init__(self, dataset: Union[RowType, Dict[str, Union[int, str]]]) -> None:
        """
        Initializing the data class object.

        Parameters:
            dataset: {year: int, quarter: string, start_date: string, end_date: string}

        Returns:
            void
        """
        self.year = dataset["year"] # type: ignore
        self.quarter = dataset["quarter"] # type: ignore
        self.start_date = dataset["start_date"] # type: ignore
        self.end_date = dataset["end_date"] # type: ignore