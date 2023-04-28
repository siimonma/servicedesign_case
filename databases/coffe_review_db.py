import os.path
import sqlite3
from sqlite3 import Error
import os
# from case_project.main import app

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
            connection.commit()
        except Error as e:
            print(f"The error {e} occurred!")

    def open_connection(self, db: str):
        return self.create_connection(os.path.join(PATH_DB_TABLES, db + ".db"))

    @staticmethod
    def db_exists(db_name: str) -> bool:
        return os.path.isfile(os.path.join(PATH_DB_TABLES, db_name + ".db"))

    @staticmethod
    def execute_read_query(connection, query: str, limit: int = None):
        """Use this function to read data from database"""
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            if limit is None:
                result = cursor.fetchall()
            else:
                result = cursor.fetchmany(limit)
            return result
        except Error as e:
            print(f"The error {e} occurred!")


class CoffeReviewDB(SqliteDB):
    def __init__(self):
        self.db_name = "coffee"
        if not self.db_exists(self.db_name):
            db_connect = self.open_connection(self.db_name)
            self.init_coffee_db(db_connect)
            db_connect.close()

    def init_coffee_db(self, connection):
        """
        Initiate coffee review database.
        """
        query = """
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
        );
        """

        self.execute_query(connection=connection, query=query)

        query = """
        CREATE TABLE IF NOT EXISTS Reviews(
        id INTEGER REFERENCES users(id),
        coffee_name TEXT UNIQUE,
        review TEXT NOT NULL,
        review_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL 
        );
        """

        self.execute_query(connection=connection, query=query)

    def get_user_review(self, user_id):
        """Returns all the reviews made by User:user_id"""
        connection = self.open_connection(self.db_name)
        connection.row_factory = sqlite3.Row
        query = f"""SELECT * FROM Reviews WHERE id={user_id}"""
        rows = self.execute_read_query(connection, query)
        connection.close()
        return rows

    def insert_test_users(self):
        connection = self.open_connection(self.db_name)
        query = """
        INSERT INTO Users (username, password) VALUES 
            ('Tom', 'tomisbest'),
            ('Jane', 'janeisbetter')
        ;
        """
        self.execute_query(connection, query)
        query = """
        INSERT INTO Reviews (id, coffee_name, review) VALUES
            (1, "Zoegas mörk rost", "Den va god"),
            (1, "Zoegas Mollbergs", "Sådär"),
            (2, "Gevalia - Mellanbrygg", "Pekant"),
            (2, "Arvid Nordqvist - Festival", "Hade jag köpt igen")
        ;
        """
        self.execute_query(connection, query)
        connection.close()


if __name__ == '__main__':
    review_db = CoffeReviewDB()
    review_db.insert_test_users()
