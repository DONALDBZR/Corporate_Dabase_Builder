"""
The Data Transfer Object for the Financial Summaries.

Authors:
    Darkness4869
"""


from dataclasses import dataclass
from mysql.connector.types import RowType
from typing import Union, Dict

@dataclass
class FinancialSummaries:
    """
    The Data Transfer Object for the Financial Summaries.
    """
    identifier: int
    CompanyDetail: int
    financial_year: int
    currency: str
    date_approved: int
    unit: Union[int, None]

    def __init__(self, dataset: Union[RowType, Dict[str, Union[int, str, None]]]):
        """
        Initializing the data class object.

        Parameters:
            dataset: {identifier: int, CompanyDetail: int, financial_year: int, currency: string, date_approved: string, unit: int|null}: The result set from the relational database server.
        """
        self.identifier = int(dataset["identifier"]) # type: ignore
        self.CompanyDetail = int(dataset["CompanyDetail"]) # type: ignore
        self.financial_year = int(dataset["financial_year"]) # type: ignore
        self.currency = str(dataset["currency"]) # type: ignore
        self.date_approved = int(dataset["date_approved"]) # type: ignore
        self.unit = dataset["unit"] # type: ignore