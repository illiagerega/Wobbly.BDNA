import psycopg2
from psycopg2 import Error
import sys
import os

sys.path.insert(0, os.path.abspath(''))

import config


def getAllSites():
    query = '''SELECT * FROM sites'''

    return selectAll(query)


def selectAll(query):
    try:
        connection = psycopg2.connect(
            user=config.pg_user,
            password=config.pg_password,
            host=config.pg_host,
            port=config.pg_port,
            database=config.pg_db
        )

        cursor = connection.cursor()

        cursor.execute(query)

        return cursor.fetchall()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
