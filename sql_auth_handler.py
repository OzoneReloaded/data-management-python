import mysql.connector


def connect_to_database(username, password, host, database, use_winauth: bool):
    sql_connection = mysql.connector.connect(user=username,
                                             password=password,
                                             host=host,
                                             database=database)
    cursor = sql_connection.cursor()
    cursor.execute("SELECT database();")
    connected_database_name = cursor.fetchone()[0]
    return cursor, connected_database_name
