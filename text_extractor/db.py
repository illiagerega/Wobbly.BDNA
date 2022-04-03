import psycopg2
from psycopg2 import Error
import sys
import os

sys.path.insert(0, os.path.abspath(''))

import config


def checkLink(link):
    query = f'''SELECT COUNT(*) FROM links WHERE link = {"'" + link + "'"}'''

    return selectCount(query)


def insertLink(link, site_id, text):
    query = f'''INSERT INTO links (id_site, link, text) VALUES ({"'" + str(site_id) + "'"}, {"'" + link + "'"}, {"'" + text + "'"})'''

    insert(query)


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


def insert(query):
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

        connection.commit()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
