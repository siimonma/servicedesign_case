import os.path
import sqlite3
from sqlite3 import Error
import os

PATH_DB_TABLES = os.path.abspath(os.path.dirname(__file__))


class SqliteDB:
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

    @staticmethod
    def execute_query(connection, query: str):
        """Use this function to insert data to database"""
        cursor = connection.cursor()
        try:
            cursor.execute(query)
        except Error as e:
            print(f"The error {e} occurred!")

    def open_connection(self, db: str):
        return self.create_connection(os.path.join(PATH_DB_TABLES, db + ".db"))

    @staticmethod
    def db_exists(self, db_name: str) -> bool:
        return os.path.isfile(os.path.join(PATH_DB_TABLES, db_name + ".db"))


class CoffeReviewDB(SqliteDB):
    def __init__(self):
        if not self.db_exists("coffee"):
            db_connect = self.open_connection("coffee")
            self.init_coffee_db(db_connect)
            db_connect.close()

    def init_coffee_db(self, connection):
        """
        Initiate coffee review database.
        """
        query = """
        CREATE TABLE IF NOT EXIST users(
        id INTEGER PRIMARY KEY AUTOINCREMENT
        );
        """

        self.execute_query(connection=connection, query=query)

        query = """
        CREATE TABLE IF NOT EXIST reviews(
        id INTEGER FOREIGN KEY REFERENCES users(id),
        coffee_name TEXT,
        review TEXT NOT NULL,
        review_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL 
        );
        """

        self.execute_query(connection=connection, query=query)
