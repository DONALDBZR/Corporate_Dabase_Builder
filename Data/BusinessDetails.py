"""
The Data Transfer Object for the Business Details.

Authors:
    Darkness4869
"""


from dataclasses import dataclass
from mysql.connector.types import RowType
from typing import Union, Dict


@dataclass
class BusinessDetails:
    """
    The Data Transfer Object for the Business Details.
    """
    identifier: int
    CompanyDetail: int
    registered_address: Union[str, None]
    name: Union[str, None]
    nature: Union[str, None]
    operational_address: Union[str, None]
    def __init__(self, dataset: Union[RowType, Dict[str, Union[int, str, None]]]) -> None:
        """
        Initializing the data class object.

        Parameters:
            dataset: {identifier: int, CompanyDetail: int, registered_address: string|null, name: string|null, nature: string|null, operational_address: string|null}: The result set from the relational database server.

        Returns:
            void
        """
        self.identifier = int(dataset["identifier"]) # type: ignore
        self.CompanyDetail = int(dataset["CompanyDetail"]) # type: ignore
        self.registered_address = dataset["registered_address"] # type: ignore
        self.name = dataset["name"] # type: ignore
        self.nature = dataset["nature"] # type: ignore
        self.operational_address = dataset["operational_address"] # type: ignore