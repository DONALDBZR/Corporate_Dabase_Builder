"""
The Data Transfer Object for the Office Bearer.
"""


from dataclasses import dataclass
from mysql.connector.types import RowType
from typing import Union, Dict


@dataclass
class OfficeBearer:
    """
    The Data Transfer Object for the Office Bearer.
    """
    identifier: int
    CompanyDetail: int
    position: str
    name: str
    address: Union[str, None]
    date_appointment: int
    def __init__(self, dataset: Union[RowType, Dict[str, Union[int, str, None]]]) -> None:
        """
        Initializing the data class object.

        Parameters:
            dataset: {identifier: int, CompanyDetail: int, position: string, name: string, address: string | null, date_appointment: int}: The result set from the relational database server.

        Returns:
            void
        """
        self.identifier = int(dataset["identifier"]) # type: ignore
        self.CompanyDetail = int(dataset["CompanyDetail"]) # type: ignore
        self.position = str(dataset["position"]) # type: ignore
        self.name = str(dataset["name"]) # type: ignore
        self.address = dataset["address"] # type: ignore
        self.date_appointment = int(dataset["date_appointment"]) # type: ignore