import json
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
    def execute_insert_query(connection, query: str):
        """Executes a INSERT query on a database connection. """
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


class CoffeeReviewDB(SqliteDB):
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
        regtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
        """

        self.execute_insert_query(connection=connection, query=query)

        query = """
                CREATE TABLE IF NOT EXISTS Users_auth(
                id INTEGER REFERENCES Users(id),
                token TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL
                );
                """

        self.execute_insert_query(connection=connection, query=query)

        query = """
        CREATE TABLE IF NOT EXISTS Reviews(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES Users(id),
        coffee_id INTEGER,
        review TEXT NOT NULL,
        review_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL 
        );
        """

        self.execute_insert_query(connection=connection, query=query)

    def get_rows(self, query: str):
        """Returns all rows from SELECT query"""
        connection = self.open_connection(self.db_name)
        rows = self.execute_read_query(connection, query)
        connection.close()
        return rows

    def user_exists(self, username: str = "", user_id: int = 0) -> bool:
        """Check if user already exists in db"""
        query = f"""SELECT * FROM Users WHERE username='{username}' or id='{user_id}';"""
        rows = self.get_rows(query=query)
        if len(rows) > 0:
            return True
        return False

    def is_authorized_user(self, token: str) -> bool:
        """ Checks if token is a valid user token."""
        # Add username check & match up id from table Users and Token table.
        query = f"""SELECT * FROM Users_auth WHERE token='{token}'"""
        rows = self.get_rows(query=query)
        if len(rows) > 0:
            return True
        return False

    def user_db_rows_to_dict(self, rows) -> dict:
        """Convert user information read from DB to dictionary-format"""
        users_dict = {
            'users': []
        }
        for row in rows:
            users_dict['users'].append({
                "id": row[0],
                "username": row[1],
                "regtime": row[2]
            })
        return users_dict

    def get_user(self, user_id: int):
        """ Returns information stored in database about user with id: 'user_id'"""
        query = f"""SELECT * FROM Users WHERE id={user_id}"""
        return self.user_db_rows_to_dict(rows=self.get_rows(query=query))

    def get_all_users(self):
        """Returns all the users and their information in json-format"""
        query = f"""SELECT * FROM Users;"""
        return self.user_db_rows_to_dict(rows=self.get_rows(query=query))

    def get_user_reviews(self, user_id):
        """Returns all the reviews made by User:user_id"""

        connection = self.open_connection(self.db_name)
        query = f"""SELECT * FROM Reviews WHERE id={user_id};"""
        rows = self.execute_read_query(connection, query)
        connection.close()

        reviews_dict = {}
        review_count = 1
        for row in rows:
            reviews_dict["r" + str(review_count)] = {
                "user_id": row[0],
                "coffe_name": row[1],
                "review": row[2],
                "timestamp": row[3]
            }
            review_count += 1
        reviews_json = json.dumps(reviews_dict)
        return reviews_json

    def insert_test_users(self):
        connection = self.open_connection(self.db_name)
        query = """
        INSERT INTO Users (username, password) VALUES 
            ('Tom', 'tomisbest'),
            ('Jane', 'janeisbetter')
        ;
        """
        self.execute_insert_query(connection, query)
        query = """
        INSERT INTO Reviews (id, coffee_name, review) VALUES
            (1, "Zoegas mörk rost", "Den va god"),
            (1, "Zoegas Mollbergs", "Sådär"),
            (2, "Gevalia - Mellanbrygg", "Pekant"),
            (2, "Arvid Nordqvist - Festival", "Hade jag köpt igen")
        ;
        """
        self.execute_insert_query(connection, query)
        connection.close()

    def add_new_user(self, username, email, token) -> dict:
        """ Add a user to database. """
        connection = self.open_connection(self.db_name)
        query = f"""INSERT INTO Users (username) VALUES ('{username}');"""
        self.execute_insert_query(connection, query)
        query = f"""SELECT id FROM Users WHERE username='{username}';"""
        new_user_id = self.execute_read_query(connection, query)[0][0]
        print(type(new_user_id))
        query = f"""INSERT INTO Users_auth (id, token, email) VALUES ({new_user_id}, '{token}', '{email}');"""
        self.execute_insert_query(connection, query)
        connection.close()

        new_user = {
            "id": new_user_id,
            "username": username,
            "email": email,
            "token": token
        }
        return new_user

    def add_review(self, coffee_id: int, token: str, review: dict):
        pass


if __name__ == '__main__':
    review_db = CoffeeReviewDB()
    print(review_db.add_new_user("simonma", "simonma@hej.com", "aosfnasnfae((9al=="))
    # review_db.insert_test_users()
