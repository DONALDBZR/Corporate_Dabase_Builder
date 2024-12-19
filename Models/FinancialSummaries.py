"""
The model which will interact exclusively with the Financial
Summaries table.

Authors:
    Darkness4869
"""


from Models.DatabaseHandler import Database_Handler
from typing import Union, Tuple
from mysql.connector.errors import Error


class Financial_Summaries(Database_Handler):
    """
    The model which will interact exclusively with the Financial
    Summaries table.
    """
    __table_name: str
    """
    The table which the model is linked to.
    """
    __created: int = 201
    """
    The status code for a successful creation.
    """
    __service_unavailable: int = 503
    """
    The status code for an unavailable service.
    """