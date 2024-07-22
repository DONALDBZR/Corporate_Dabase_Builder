"""
The module which will have the object-relational mapper of
the application.

Authors:
    Andy Ewen Gaspard
    Solofonavalona Randriantsilavo
"""


from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from Environment import Environment
from Models.Logger import Corporate_Database_Builder_Logger
from typing import List, Tuple, Union, Any
from mysql.connector.types import RowType
from mysql.connector import Error
import mysql.connector
import logging


class Database_Handler:
    """
    The database handler that will communicate with the database
    server.
    """
    __host: str
    """
    The host of the application
    """
    __database: str
    """
    The database of the application
    """
    __username: str
    """
    The user that have access to the database
    """
    __password: str
    """
    The password that allows the required user to connect to the
    database.
    """
    __database_handler: Union[PooledMySQLConnection, MySQLConnection]
    """
    The database handler needed to execute the queries needed
    """
    __statement: "MySQLCursor"
    """
    The statement to be used to execute all of the requests to
    the database server
    """
    __query: str
    """
    The query to be used to be sent to the database server to
    either get, post, update or delete data.
    """
    __parameters: Union[Tuple[Any], None]
    """
    Parameters that the will be used to sanitize the query which
    is either get, post, update or delete.
    """
    __Logger: Corporate_Database_Builder_Logger
    """
    The logger that will all the action of the application.
    """

    def __init__(self):
        """
        Instantiating the class which will try to connect to the
        database.
        """
        ENV = Environment()
        self.setLogger(Corporate_Database_Builder_Logger())
        self.getLogger().setLogger(logging.getLogger(__name__))
        self.__setHost(ENV.getHost())
        self.__setDatabase(ENV.getDatabase())
        self.__setUsername(ENV.getUsername())
        self.__setPassword(ENV.getPassword())
        try:
            self.__setDatabaseHandler(
                mysql.connector.connect(
                    host=self.__getHost(),
                    database=self.__getDatabase(),
                    username=self.__getUsername(),
                    password=self.__getPassword()
                )
            )
            self.getLogger().inform(
                "The application has been successfully connected to the database server!"
            )
        except Error as error:
            self.getLogger().error(
                f"Connection Failed!\nError: {error}"
            )

    def __getHost(self) -> str:
        return self.__host

    def __setHost(self, host: str) -> None:
        self.__host = host

    def __getDatabase(self) -> str:
        return self.__database

    def __setDatabase(self, database: str) -> None:
        self.__database = database

    def __getUsername(self) -> str:
        return self.__username

    def __setUsername(self, username: str) -> None:
        self.__username = username

    def __getPassword(self) -> str:
        return self.__password

    def __setPassword(self, password: str) -> None:
        self.__password = password

    def __getDatabaseHandler(self) -> Union[PooledMySQLConnection, MySQLConnection]:
        return self.__database_handler

    def __setDatabaseHandler(self, database_handler: Union[PooledMySQLConnection, MySQLConnection]) -> None:
        self.__database_handler = database_handler

    def __getStatement(self) -> "MySQLCursor":
        return self.__statement

    def __setStatement(self, statement: "MySQLCursor") -> None:
        self.__statement = statement

    def getQuery(self) -> str:
        return self.__query

    def setQuery(self, query: str) -> None:
        self.__query = query

    def getParameters(self) -> Union[Tuple[Any], None]:
        return self.__parameters

    def setParameters(self, parameters: Union[Tuple[Any], None]) -> None:
        self.__parameters = parameters

    def getLogger(self) -> Corporate_Database_Builder_Logger:
        return self.__Logger

    def setLogger(self, logger: Corporate_Database_Builder_Logger) -> None:
        self.__Logger = logger

    def _query(self, query: str, parameters: Union[Tuple[Any], None]):
        """
        Preparing the SQL query that is going to be handled by the
        database handler.

        Parameters:
            query: string
            parameters: array | null

        Returns:
            Generator[MySQLCursor, None, None] | None
        """
        self.__setStatement(
            self.__getDatabaseHandler().cursor(
                prepared=True,
                dictionary=True
            )
        )
        self.getLogger().debug(
            f"Query to be used as a request to the database server!\nQuery: {query}\nParameters: {parameters}"
        )
        self.__getStatement().execute(query, parameters)

    def _execute(self) -> None:
        """
        Executing the SQL query which will send a command to the
        database server

        Returns:
            void
        """
        self.__getDatabaseHandler().commit()

    def _resultSet(self) -> List[RowType]:
        """
        Fetching all the data that is requested from the command that
        was sent to the database server.

        Returns:
            arrays
        """
        result_set = self.__getStatement().fetchall()
        self.__getStatement().close()
        return result_set

    def getData(self, table_name: str, parameters: Union[Tuple[Any], None] = None, join_condition: str = "", filter_condition: str = "", column_names: str = "*", sort_condition: str = "", limit_condition: int = 0) -> List[RowType]:
        """
        Retrieving data from the database.

        Parameters:
            parameters:         (array|null):   The parameters to be passed into the query.
            table_name:         (string):       The name of the table.
            column_names:       (string):       The name of the columns.
            join_condition      (string):       Joining table condition.
            filter_condition    (string):       Items to be filtered with.
            sort_condition      (string):       The items to be sorted.
            limit_condition     (int):          The amount of items to be returned

        Return:
            (array)
        """
        query = f"SELECT {column_names} FROM {table_name}"
        self.setQuery(query)
        self.setParameters(parameters)
        self._getJoin(join_condition)
        self._getFilter(filter_condition)
        self._getSort(sort_condition)
        self._getLimit(limit_condition)
        self.getLogger().inform(
            f"Query built for retrieving data!\nQuery: {self.getQuery()}\nParameters: {self.getParameters()}"
        )
        self._query(self.getQuery(), self.getParameters())
        return self._resultSet()

    def _getJoin(self, condition: str) -> None:
        """
        Building the query needed for retrieving data that is in at
        least two tables.

        Parameters:
            condition:  (string): The JOIN statement that is used.

        Return:
            (void)
        """
        if condition == "":
            query = self.getQuery()
        else:
            query = f"{self.getQuery()} LEFT JOIN {condition}"
        self.setQuery(query)

    def _getFilter(self, condition: str) -> None:
        """
        Building the query needed for retrieving specific data.

        Parameters:
            condition:  (string): The WHERE statement that will be used.

        Return:
            (void)
        """
        if condition == "":
            query = self.getQuery()
        else:
            query = f"{self.getQuery()} WHERE {condition}"
        self.setQuery(query)

    def _getSort(self, condition: str) -> None:
        """
        Building the query needed to be used to sort the result set.

        Parameters:
            condition:  (string): The ORDER BY statement that will be used.

        Return:
            (void)
        """
        if condition == "":
            query = self.getQuery()
        else:
            query = f"{self.getQuery()} ORDER BY {condition}"
        self.setQuery(query)

    def _getLimit(self, limit: int) -> None:
        """
        Building the query needed to be used to limit the amount of
        data from the result set.

        Parameters:
            limit:  (int): The ORDER BY statement that will be used.

        Return:
            (void)
        """
        if limit > 0:
            query = f"{self.getQuery()} LIMIT {limit}"
        else:
            query = self.getQuery()
        self.setQuery(query)

    def postData(self, table: str, columns: str, values: str, parameters: Tuple[Any]) -> None:
        """
        Creating records to store data into the database server.

        Parameters:
            table:      (string):   Table Name
            columns:    (string):   Column names
            values:     (string):   Data to be inserted

        Return:
            (void)
        """
        query = f"INSERT INTO {table}({columns}) VALUES ({values})"
        self.setQuery(query)
        self.setParameters(parameters)
        self.getLogger().inform(
            f"Query built for adding data!\nQuery: {self.getQuery()}\nParameters: {self.getParameters()}"
        )
        try:
            self._query(self.getQuery(), self.getParameters())
            self._execute()
        except Error as error:
            self.__handlePostDataError(error)

    def __handlePostDataError(self, error: Error) -> None:
        """
        Handling any error that is generated on the relational
        database server's level.

        Parameters:
            error: mysql.connector.Error: The error object of MySQL

        Returns:
            void
        """
        print(f"An error occured while posting the data into the relational database server.\nError: {error}\nMySQL Error Number: {error.errno}\nSQL State: {error.sqlstate}\n{error=}")
        exit()

    def updateData(self, table: str, values: str, parameters: Union[Tuple[Any], None], condition: str = "") -> None:
        """
        Updating a specific table in the database.

        Parameters:
            table:      (string):   Table
            values:     (string):   Columns to be modified and data to be put within
            condition:  (string):   Condition for the data to be modified
            parameters: (array):    Data to be used for data manipulation.

        Return:
            (void)
        """
        query = f"UPDATE {table} SET {values}"
        self.setQuery(query)
        self.setParameters(parameters)
        self._getFilter(condition)
        self.getLogger().inform(
            f"Query built for updating data!\nQuery: {self.getQuery()}\nParameters: {self.getParameters()}"
        )
        self._query(self.getQuery(), self.getParameters())
        self._execute()

    def deleteData(self, table: str, parameters: Union[Tuple[Any], None], condition: str = "") -> None:
        """
        Deleting data from the database.

        Parameters:
            table:      (string):   Table
            parameters: (array):    Data to be used for data manipulation.
            condition:  (string):   Specification

        Return:
            (void)
        """
        query = f"DELETE FROM {table}"
        self.setQuery(query)
        self.setParameters(parameters)
        self._getFilter(condition)
        self.getLogger().inform(
            f"Query built for removing data!\nQuery: {self.getQuery()}\nParameters: {self.getParameters()}"
        )
        self._query(self.getQuery(), self.getParameters())
        self._execute()
