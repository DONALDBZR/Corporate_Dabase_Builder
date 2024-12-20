"""
The Data Transfer Object for the Balance Sheets.

Authors:
    Darkness4869
"""


from dataclasses import dataclass
from mysql.connector.types import RowType
from typing import Union, Dict

@dataclass
class FinancialSummaries:
    """
    The Data Transfer Object for the Balance Sheets.
    """
    identifier: int
    CompanyDetail: int
    financial_year: int
    currency: str
    unit: int

    def __init__(self, dataset: Union[RowType, Dict[str, Union[int, str]]]):
        """
        Initializing the data class object.

        Parameters:
            dataset: {identifier: int, CompanyDetail: int, financial_year: int, currency: string, unit: int}: The result set from the relational database server.
        """
        self.identifier = int(dataset["identifier"]) # type: ignore
        self.CompanyDetail = int(dataset["CompanyDetail"]) # type: ignore
        self.financial_year = int(dataset["financial_year"]) # type: ignore
        self.currency = str(dataset["currency"]) # type: ignore
        self.unit = int(dataset["unit"]) # type: ignore