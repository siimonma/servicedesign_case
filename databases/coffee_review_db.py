import json
import os.path
import sqlite3
from sqlite3 import Error
import os
from case_project.api_return_code_classes import APIClientError

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
            # print("Connection to SQLite DB successful!")
        except Error as e:
            print(f"The error {e} occurred!")
        return connection

    @staticmethod
    def execute_write_query(connection, query: str):
        """Executes a query on a database connection. """
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
            if limit:
                result = cursor.fetchmany(limit)
            else:
                result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error {e} occurred!")

    def execute_query(self, query: str,
                      select: bool = False,
                      insert: bool = False,
                      update: bool = False,
                      delete: bool = False,
                      limit: int = None):
        """ Executes a database sqlite query."""

        results = None
        connection = self.open_connection(self.db_name)
        if insert or update or delete:
            self.execute_write_query(connection=connection, query=query)
        elif select:
            results = self.execute_read_query(connection=connection, query=query, limit=limit)
        connection.close()

        if select:
            return results


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

        self.execute_write_query(connection=connection, query=query)

        query = """
                CREATE TABLE IF NOT EXISTS Users_auth(
                id INTEGER REFERENCES Users(id),
                token TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL
                );
                """

        self.execute_write_query(connection=connection, query=query)

        query = """
        CREATE TABLE IF NOT EXISTS Reviews(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES Users(id),
        coffee_id TEXT NOT NULL,
        review TEXT NOT NULL,
        review_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL 
        );
        """

        self.execute_write_query(connection=connection, query=query)

    def get_rows(self, query: str):
        """Returns all rows from SELECT query"""
        connection = self.open_connection(self.db_name)
        rows = self.execute_read_query(connection, query)
        connection.close()
        return rows

    def user_exists(self, username: str = "", user_id: int = 0) -> bool:
        """Check if user already exists in db"""
        query = f"""SELECT * FROM Users WHERE username='{username}' or id='{user_id}';"""
        rows = self.execute_query(query=query, select=True)
        if len(rows) > 0:
            return True
        return False

    def is_authorized_user(self, token: str) -> bool:
        """ Checks if token is a valid user token."""
        # Add username check & match up id from table Users and Token table.
        query = f"""SELECT * FROM Users_auth WHERE token='{token}'"""
        rows = self.execute_query(query=query, select=True)
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
        return self.user_db_rows_to_dict(rows=self.execute_query(query=query, select=True))

    def get_all_users(self):
        """Returns all the users and their information in json-format"""
        query = f"""SELECT * FROM Users;"""
        return self.user_db_rows_to_dict(rows=self.execute_query(query=query, select=True))

    def insert_test_users(self):
        connection = self.open_connection(self.db_name)
        query = """
        INSERT INTO Users (username, password) VALUES 
            ('Tom', 'tomisbest'),
            ('Jane', 'janeisbetter')
        ;
        """
        self.execute_write_query(connection, query)
        query = """
        INSERT INTO Reviews (id, coffee_name, review) VALUES
            (1, "Zoegas mörk rost", "Den va god"),
            (1, "Zoegas Mollbergs", "Sådär"),
            (2, "Gevalia - Mellanbrygg", "Pekant"),
            (2, "Arvid Nordqvist - Festival", "Hade jag köpt igen")
        ;
        """
        self.execute_write_query(connection, query)
        connection.close()

    def add_new_user(self, username, email, token) -> dict:
        """ Add a user to database. """
        connection = self.open_connection(self.db_name)
        query = f"""INSERT INTO Users (username) VALUES ('{username}');"""
        self.execute_write_query(connection, query)

        query = f"""SELECT id FROM Users WHERE username='{username}';"""
        new_user_id = self.execute_read_query(connection, query)[0][0]

        query = f"""INSERT INTO Users_auth (id, token, email) VALUES ({new_user_id}, '{token}', '{email}');"""
        self.execute_write_query(connection, query)
        connection.close()

        new_user = {
            "id": new_user_id,
            "username": username,
            "email": email,
            "token": token
        }
        return new_user

    def add_review(self, coffee_id: int, token: str, review: dict):
        """ Adds a review to coffee review database"""
        query = f"""SELECT id FROM Users_auth WHERE token='{token}';"""
        user_id = self.get_rows(query=query)[0][0]

        query = f"""INSERT INTO Reviews (user_id, coffee_id, review) 
        VALUES ({user_id}, {coffee_id}, '{review['review']}')"""
        connection = self.open_connection(self.db_name)
        self.execute_write_query(connection=connection, query=query)
        review_id = self.execute_read_query(connection=connection,
                                            query="""SELECT last_insert_rowid();""")[0][0]
        review_entry = self.execute_read_query(connection=connection,
                                               query=f"""SELECT * FROM Reviews WHERE id={review_id}""")
        connection.close()
        return {'review': {
            'id': review_id,
            'user_id': review_entry[0][1],
            'coffee_id': review_entry[0][2],
            'review': review_entry[0][3],
            'timestamp': review_entry[0][4]
        }}

    def coffee_reviews_entry_to_dict(self, rows: list) -> dict:
        """Convert review entries from Reviews table, draw from database, to dictionary."""
        reviews = {'reviews': []}
        for row in rows:
            reviews['reviews'].append(
                {
                    'id': row[0],
                    'user_id': row[1],
                    'coffee_id': row[2],
                    'review': row[3],
                    'time_stamp': row[4]
                }
            )
        return reviews

    def review_exists(self, review_id: int) -> bool:
        query = f"""SELECT * FROM Reviews WHERE id='{review_id}'"""
        if len(self.coffee_reviews_entry_to_dict(self.execute_query(query=query, select=True))['reviews']) != 0:
            return True
        return False

    def get_reviews(self, coffee_id: str = None, user_id: int = None, review_id: int = None) -> dict:
        """Returns all coffee reviews connected to 'coffee_id' from database"""
        query = ""
        if review_id:
            query = f"""SELECT * FROM Reviews WHERE id='{review_id}';"""
        elif user_id and coffee_id:
            query = f"""SELECT * FROM Reviews WHERE user_id='{user_id}' AND coffee_id='{coffee_id}';"""
        elif user_id:
            query = f"""SELECT * FROM Reviews WHERE user_id='{user_id}';"""
        elif coffee_id:
            query = f"""SELECT * FROM Reviews WHERE coffee_id='{coffee_id}';"""
        else:
            query = f"""SELECT * FROM Reviews;"""
        return self.coffee_reviews_entry_to_dict(self.execute_query(query=query, select=True))

    def valid_authentication(self, token: str, user_id: int) -> bool:
        """ Checks if token and user is compatible. """
        query = f""" SELECT * FROM Users_auth WHERE id='{user_id}' AND token='{token}';"""
        if len(self.execute_query(query=query, select=True, limit=1)) > 0:
            return True
        return False

    def update_review(self, review_id: int, txt: str, token: str):
        """ Update review with new text. """
        review = self.get_reviews(review_id=review_id)['reviews'][0]
        if not self.valid_authentication(token, review['user_id']):
            raise APIClientError(f"Token and user missmatch. Can not modify other users reviews!", 403)
        query = f"""UPDATE Reviews 
                    SET review='{txt}', review_time=CURRENT_TIMESTAMP 
                    WHERE id={review_id}; """
        self.execute_query(query=query, update=True)

        return self.get_reviews(review_id=review_id)

    def delete_review(self, review_id: int, token: str):
        """ Removes review with id 'review_id' from database. """
        review = self.get_reviews(review_id=review_id)['reviews'][0]
        if not self.valid_authentication(token, review['user_id']):
            raise APIClientError(f"Token and user missmatch. Can not modify other users reviews!", 403)
        query = f"""DELETE FROM Reviews WHERE id={review_id}"""
        self.execute_query(query=query, delete=True)
        return review


if __name__ == '__main__':
    review_db = CoffeeReviewDB()
    print(review_db.add_review(123,
                               'Z1g5JlgmL3EsM3ksPVxKKF0wLytrfHU+KTthWC9BLDh8cUxecy5ZUWQwa1tiOidePVw=',
                               {'review': 'God och fräsch!'}))
    # print(review_db.add_new_user("simonma", "simonma@hej.com", "aosfnasnfae((9al=="))
    # review_db.insert_test_users()
