import os.path
import sqlite3
from sqlite3 import Error
import os

PATH_DB_TABLES = os.path.abspath(os.path.dirname(__file__)) + "/databases"


class coffeReviewDB:
    def __init__(self):
        db_connect = self.open_connection("coffe")

        db_connect.close()

    @staticmethod
    def create_connection(path: str):
        """Open path as a database"""
        connection = None
        try:
            # Försöker du koppla till en fil som inte finns,
            # skapar sqlite3.connect en ny fil enligt "path"
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful!")
        except Error as e:
            print(f"The error {e} occurred!")
        return connection

    def open_connection(self, db: str):
        return self.create_connection(os.path.join(PATH_DB_TABLES, db + ".db"))
