import psycopg2
import sys


class DatabaseHandler:
    def __init__(self, host: str, user: str, database: str, password: str):
        self.host = host
        self.database = database
        self.user = user
        self.password = password  # for real???????
        self.connection = self.connect_to_database()
        self.cursor = self.connection.cursor()

    def connect_to_database(self):
        """ Connect to the PostgreSQL database server """
        return psycopg2.connect(
            database=self.database,
            user=self.user,
            host=self.host,
            password=self.password)