import os
import sqlite3

APP_PATH = os.path.abspath(os.path.join(__file__, os.pardir))
DB_NAME = os.path.join(APP_PATH, 'URLData.db')


def connect_to_db(db_name: str = DB_NAME) -> sqlite3.Connection:
    conn = sqlite3.connect(db_name)
    return conn


def execute_query(query: str, conn: sqlite3.Connection, params: tuple = ()) -> None:
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    cursor.close()


def create_db_table(db_name: str = DB_NAME) -> None:
    with connect_to_db(db_name) as conn:
        query = (
            "CREATE TABLE IF NOT EXISTS tbl_url_data ("
            "id INTEGER PRIMARY KEY, "
            "domainName TEXT, "
            "title TEXT, "
            "statusCode INTEGER, "
            "finalStatusCode INTEGER, "
            "finalUrl TEXT"
            ");"
        )
        execute_query(query, conn)


def clear_db(db_name: str = DB_NAME) -> None:
    with connect_to_db(db_name) as conn:
        query = "DROP TABLE IF EXISTS tbl_url_data;"
        execute_query(query, conn)


def insert_data(collected_data: dict, db_name: str = DB_NAME) -> None:
    with connect_to_db(db_name) as conn:
        query = (
            'INSERT INTO tbl_url_data (domainName, title, statusCode, finalStatusCode, finalUrl) '
            'VALUES (?, ?, ?, ?, ?);'
        )
        params = (collected_data['domain_name'],
                  collected_data['title'],
                  collected_data['status_code'],
                  collected_data['final_status_code'],
                  collected_data['final_url'])
        execute_query(query, conn, params)


def get_all_db_data(db_name: str = DB_NAME) -> list[tuple]:
    with connect_to_db(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tbl_url_data;')
        rows = cursor.fetchall()
        cursor.close()

    return rows
