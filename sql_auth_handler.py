import psycopg2
import sys


class DatabaseHandler():
    def __init__(self, host: str, user: str, database: str, password: str):
        self.host = host
        self.database = database
        self.user = user
        self.password = password  # for real???????

    def connect_to_database(self):
        """ Connect to the PostgreSQL database server """
        return psycopg2.connect(
            database=self.database,
            user=self.user,
            host=self.host,
            password=self.password)

    def get_connection_info(self):
        """ этот геттер я посвящаю тем кто мне близок по духу и по другим причинам """
        return vars(self)