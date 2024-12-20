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