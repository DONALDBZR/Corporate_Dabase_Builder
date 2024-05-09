"""
The Data Transfer Object for the FinCorp Logs.

Authors:
    Andy Ewen Gaspard
"""


from dataclasses import dataclass
from mysql.connector.types import RowType
from typing import Union, Dict
from time import time
from datetime import datetime
from datetime import timedelta


@dataclass
class FinCorpLogs:
    """
    The Data Transfer Object for the Financial Calendar.
    """
    identifier: int
    method_name: str
    year: int
    quarter: str
    date_start: int
    date_to: int
    status: int
    amount: int

    def __init__(self, dataset: Union[RowType, Dict[str, Union[int, str, None]]]) -> None:
        """
        Initializing the data class object.

        Parameters:
            dataset: {year: int, quarter: string, start_date: string, end_date: string}

        Returns:
            void
        """
        self.identifier = self.handleIdentifier(dataset["identifier"]) # type: ignore
        self.method_name = self.handleMethodName(dataset["method_name"]) # type: ignore
        self.year = self.handleYear(dataset["year"]) # type: ignore
        self.quarter = self.handleQuarter(dataset["quarter"]) # type: ignore
        self.date_start = self.handleDateStart(dataset["date_start"]) # type: ignore
        self.date_to = self.handleDateTo(dataset["date_to"]) # type: ignore
        self.status = self.handleStatus(dataset["status"]) # type: ignore
        self.amount = self.handleAmount(dataset["amount"]) # type: ignore

    def handleIdentifier(self, identifier: Union[int, None]) -> int:
        """
        Ensuring that the identifier is in the correct format for
        the application.

        Parameters:
            identifier: int | null

        Returns:
            int
        """
        if type(identifier) is int:
            return identifier
        else:
            return int(time())

    def handleMethodName(self, method_name: Union[str, None]) -> str:
        """
        Ensuring that the method name is in the correct format for
        the application.

        Parameters:
            method_name: string | null

        Returns:
            string
        """
        if type(method_name) is str:
            return method_name
        else:
            return ""

    def handleYear(self, year: Union[int, None]) -> int:
        """
        Ensuring that the year is in the correct format for the
        application.

        Parameters:
            year: int | null

        Returns:
            int
        """
        if type(year) is int:
            return year
        else:
            return int(
                datetime.fromtimestamp(
                    self.identifier
                ).strftime(
                    "%Y"
                )
            )

    def handleQuarter(self, quarter: Union[str, None]) -> str:
        """
        Ensuring that the quarter is in the correct format for the
        application.

        Parameters:
            quarter: string | null

        Returns:
            string
        """
        if type(quarter) is str:
            return quarter
        else:
            return ""

    def handleDateStart(self, date_start: Union[int, None]) -> int:
        """
        Ensuring that the date start is in the correct format for
        the application.

        Parameters:
            date_start: int | null

        Returns:
            int
        """
        if type(date_start) is int:
            return date_start
        else:
            return int(time())

    def handleDateTo(self, date_to: Union[int, None]) -> int:
        """
        Ensuring that the date to is in the correct format for the
        application.

        Parameters:
            date_to: int | null

        Returns:
            int
        """
        if type(date_to) is int:
            return date_to
        else:
            return int(
                datetime.strptime(
                    datetime.strftime(
                        datetime.strptime(
                            datetime.fromtimestamp(
                                self.date_start
                            ).strftime(
                                "%H:%M:%S %m/%d/%Y"
                            ),
                            "%H:%M:%S %m/%d/%Y"
                        ) + timedelta(
                            weeks=1
                        ),
                        "%H:%M:%S %m/%d/%Y"
                    ),
                    "%H:%M:%S %m/%d/%Y"
                ).timestamp()
            )

    def handleStatus(self, status: Union[int, None]) -> int:
        """
        Ensuring that the status is in the correct format for the
        application.

        Parameters:
            status: int | null

        Returns:
            int
        """
        if type(status) is int:
            return status
        else:
            return 204

    def handleAmount(self, amount: Union[int, None]) -> int:
        """
        Ensuring that the amount is in the correct format for the
        application.

        Parameters:
            amount: int | null

        Returns:
            int
        """
        if type(amount) is int:
            return amount
        else:
            return 0