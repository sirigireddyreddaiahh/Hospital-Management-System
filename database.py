import sqlite3

def connect_db(db_name='hospital.db'):
    connection = sqlite3.connect(db_name)
    return connection

def execute_query(connection, query, parameters=()):
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    connection.commit()
    return cursor.fetchall()