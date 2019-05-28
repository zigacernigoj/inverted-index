import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    # finally:
    #    conn.close()


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_sql(conn, sql, values):
    cur = conn.cursor()
    try:
        cur.execute(sql, values)
        conn.commit()
        return cur.lastrowid
    except Error as e:
        # print("Napaka: ", e)
        return -1


def select_sql(conn, sql, values):
    cur = conn.cursor()
    cur.execute(sql, values)

    return cur.fetchall()


def close_connection(conn):
    conn.close()
