"""
The Data Transfer Object for the Member.
"""


from dataclasses import dataclass
from mysql.connector.types import RowType
from typing import Union, Dict


@dataclass
class Member:
    """
    The Data Transfer Object for the Member.
    """
    identifier: int
    CompanyDetail: int
    name: str
    amount: int
    date_start: int
    currency: str

    def __init__(self, dataset: Union[RowType, Dict[str, Union[int, str]]]) -> None:
        """
        Initializing the data class object.

        Parameters:
            dataset: {identifier: int, CompanyDetail: int, name: string, amount: int, date_start: int, currency: string}: The result set from the relational database server.

        Returns:
            void
        """
        self.identifier = int(dataset["identifier"]) # type: ignore
        self.CompanyDetail = int(dataset["CompanyDetail"]) # type: ignore
        self.name = str(dataset["name"]) # type: ignore
        self.amount = int(dataset["amount"]) # type: ignore
        self.date_start = int(dataset["date_start"]) # type: ignore
        self.currency = str(dataset["currency"]) # type: ignore