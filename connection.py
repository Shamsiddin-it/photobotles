import psycopg2
from secret import * 

def connection_database():
    connection = psycopg2.connect(
        database="bott",
        user="postgres",
        host="localhost",
        password=password1,
        port=5432
    )
    return connection

def close_connection(conn, cur):
    cur.close()
    conn.close()