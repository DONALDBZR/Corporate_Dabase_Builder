"""
The Data Transfer Object for the Company Details.

Authors:
    Andy Ewen Gaspard
"""


from dataclasses import dataclass
from mysql.connector.types import RowType
from typing import Union, Dict


@dataclass
class CompanyDetails:
    """
    The Data Transfer Object for the Company Details.
    """
    identifier: int
    business_registration_number: str
    name: str
    file_number: str
    category: str
    date_incorporation: int
    nature: str
    status: str
    date_verified: Union[int, None]
    is_extracted: int
    company_identifier: int
    company_type: str

    def __init__(self, dataset: Union[RowType, Dict[str, Union[int, str, None]]]) -> None:
        """
        Initializing the data class object.

        Parameters:
            dataset: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int, is_extracted: int, company_identifier: int, company_type: string}: The result set from the relational database server.

        Returns:
            void
        """
        self.identifier = int(dataset["identifier"]) # type: ignore
        self.business_registration_number = str(dataset["business_registration_number"]) # type: ignore
        self.name = str(dataset["name"]) # type: ignore
        self.file_number = str(dataset["file_number"]) # type: ignore
        self.category = str(dataset["category"]) # type: ignore
        self.date_incorporation = int(dataset["date_incorporation"]) # type: ignore
        self.nature = str(dataset["nature"]) # type: ignore
        self.status = str(dataset["status"]) # type: ignore
        self.date_verified = dataset["date_verified"] # type: ignore
        self.is_extracted = dataset["is_extracted"] # type: ignore
        self.company_identifier = dataset["company_identifier"] # type: ignore
        self.company_type = dataset["company_type"] # type: ignore