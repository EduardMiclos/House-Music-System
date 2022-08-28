import sqlite3 as sql
import os
from typing import List

class DatabaseManager:
    def __init__(self, db_name) -> None:
        self.db_name = db_name
        self.con = None
        self.cursor = None

        sql.enable_callback_tracebacks(True)

        if '.db' not in self.db_name:
            self.db_name += '.db'

    # Access modes:
        # ro -> read-only
        # rw -> read-write
    def __connect(self, open_mode: str = 'ro') -> bool:

        # Checking if the database exists.
        if os.path.exists(self.db_name):
            self.con = sql.connect(f'file:{self.db_name}?mode={open_mode}', uri = True)
            self.cursor = self.con.cursor()
            return True

        print('Failure: The specified path does not exist!')
        return False
    
    def __disconnect(self) -> bool:
        if self.con is None and self.cursor is None:
            return False

        self.con.close()
        self.cursor = None

        return True

    def __exec_query(self, query: str) -> sql.Cursor:
        self.cursor.execute(query)
        return self.cursor

    def read(self, query: str) -> List[str]:

        # Connecting to the database in read-only mode.
        is_connected = self.__connect(open_mode = 'ro')

        if is_connected is False:
            raise Exception('Failure: Coudld not connect to the database!')

        cursor = self.__exec_query(query)

        self.disconnect()
        return cursor

    def write(self, query: str) -> List[str]:

        # Connect to the database in write-only mode.
        is_connected = self.__connect(open_mode = 'rw')

        if is_connected is False:
            raise Exception('Failure: Could not connect to the database!')

        cursor = self.__exec_query(query)
        self.con.commit()

        self.__disconnect()
        return cursor

    def list_tables(self) -> List[str]:
        cursor = self.read("SELECT name FROM sqlite_master WHERE type = 'table';")

        tables = cursor.fetchall()

        if len(tables) == 0:
            raise Exception('Failure: No table was found!')

        return tables

         

