"""
The Data Transfer Object for the State Capital.

Authors:
    Darkness4869
"""


from dataclasses import dataclass
from mysql.connector.types import RowType
from typing import Union, Dict


@dataclass
class StateCapital:
    """
    The Data Transfer Object for the State Capital.
    """
    identifier: int
    CompanyDetail: int
    type: Union[str, None]
    amount: Union[int, None]
    stated_capital: Union[float, None]
    amount_unpaid: Union[float, None]
    currency: Union[str, None]
    def __init__(self, dataset: Union[RowType, Dict[str, Union[int, str, float, None]]]) -> None:
        """
        Initializing the data class object.

        Parameters:
            dataset: {identifier: int, CompanyDetail: int, type: string|null, amount: int|null, stated_capital: float|null, amount_unpaid: float|null, currency: string|null}: The result set from the relational database server.

        Returns:
            void
        """
        print(f"{dataset=}")
        self.identifier = int(dataset["identifier"]) # type: ignore
        self.CompanyDetail = int(dataset["CompanyDetail"]) # type: ignore
        self.type = dataset["type"] # type: ignore
        self.amount = dataset["amount"] # type: ignore
        self.stated_capital = dataset["stated_capital"] # type: ignore
        self.amount_unpaid = dataset["amount_unpaid"] # type: ignore
        self.currency = dataset["currency"] # type: ignore