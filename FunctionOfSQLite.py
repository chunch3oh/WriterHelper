import sqlite3
from sqlite3 import Error
import os


def drop():
    db_file = "book.db"

    try:
        os.remove(db_file)
        print(f"Database {db_file} dropped successfully.")
    except OSError as e:
        print(f"Error occurred while dropping the database: {e}")


def create_connection():
    conn = None
    db_file = "book.db"
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def Building(table_name, columns, values):
    print("=====Building=====")
    conn = create_connection()
    if conn is not None:
        try:
            query = f'CREATE TABLE {table_name} ({", ".join([f"{col} text NOT NULL" for col in columns])});'
            conn.execute(query)

            print(f"Table {table_name} created successfully.")
            placeholders = ', '.join('?' for _ in values)
            query = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({placeholders})'
            conn.execute(query, values)
            conn.commit()
            print("Values inserted successfully.")
        except Error as e:
            print("In Building ->", e)
        finally:
            if conn:
                conn.close()
    else:
        print("Error! cannot create the database connection.")


def AddColumn(table_name, column_name, default_value):
    print("=====AddColumn=====")
    print("new column", column_name, "is adding")
    conn = create_connection()

    if conn is not None:
        conn.execute(
            f'ALTER TABLE {table_name} ADD COLUMN {column_name} text DEFAULT {default_value};')
        conn.commit()
        conn.close()
    else:
        print("Error! cannot create the database connection.")


def TakeContent(table_name, column_name):
    print("=====TakeContent=====")
    conn = create_connection()
    content = ""

    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute(f'SELECT "{column_name}" FROM "{table_name}"')

            rows = cur.fetchall()
            for row in rows:
                content += str(row[0]) + "\n"
                print(row[0])

        except Error as e:
            print("In Take", e)

        finally:
            if conn:
                conn.close()
    else:
        print("Error! cannot create the database connection.")

    return content


def Update(table_name, column_name, new_value):
    print("=====Update=====")
    print(f"Updating {column_name} in {table_name}")
    conn = create_connection()

    if conn is not None:
        conn.execute(
            f'UPDATE {table_name} SET {column_name} = ?;', (new_value,))
        conn.commit()
        conn.close()
    else:
        print("Error! cannot create the database connection.")
