"""
The Data Transfer Object for the Corporate Registries.

Authors:
    Andy Ewen Gaspard
"""


from dataclasses import dataclass
from mysql.connector.types import RowType
from typing import Union, Dict


@dataclass
class DocumentFiles:
    """
    The Data Transfer Object for the corporate registries.
    """
    identifier: int
    file_data: bytes
    company_detail: int

    def __init__(self, dataset: Union[RowType, Dict[str, Union[int, bytes]]]) -> None:
        """
        Initializing the data class object.

        Parameters:
            dataset: {identifier: int, file_data: bytes, CompanyDetail: int}

        Returns:
            void
        """
        self.identifier = int(dataset["identifier"]) # type: ignore
        self.file_data = bytes(dataset["file_data"]) # type: ignore
        self.company_detail = int(dataset["CompanyDetail"]) # type: ignore