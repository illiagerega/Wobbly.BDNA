import psycopg2
from psycopg2 import Error
import sys
import os

sys.path.insert(0, os.path.abspath(''))

import config


def getTopLanguages():
    query = f'''SELECT language FROM links_language'''

    return selectAll(query)

def getTopKeywords():
    query = '''SELECT keyword FROM links_keywords'''

    return selectAll(query)

def getSemanticResults():
    query = '''SELECT character FROM links_semantic'''

    return selectAll(query)

def findNews(string):
    query = f'''SELECT * FROM links WHERE text ILIKE '%{string}%' LIMIT 50'''

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


def selectCount(query):
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

        return cursor.fetchone()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
