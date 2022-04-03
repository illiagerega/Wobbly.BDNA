import psycopg2
from psycopg2 import Error
import sys
import os

sys.path.insert(0, os.path.abspath(''))

import config


def selectAllTexts():
    query = f'''SELECT * FROM links'''

    return selectAll(query)


def findLangLink(id_link):
    query = f'''SELECT COUNT(*) FROM links_language WHERE id_link = {"'" + str(id_link) + "'"}'''

    return selectCount(query)


def insertLangLink(id_site, id_link, language):
    query = f'''INSERT INTO links_language (id_site, id_link, language) VALUES ({"'" + str(id_site) + "'"}, {"'" + str(id_link) + "'"}, {"'" + language + "'"})'''

    insert(query)


def insertKeywords(id_site, id_link, keyword):
    query = f'''INSERT INTO links_keywords (id_site, id_link, keyword) VALUES ({"'" + str(id_site) + "'"}, {"'" + str(id_link) + "'"}, {"'" + keyword + "'"})'''

    insert(query)


def checkKeywords(id_site, id_link):
    query = f'''SELECT COUNT(*) FROM links_keywords WHERE id_site = {"'" + str(id_site) + "'"} AND id_link = {"'" + str(id_link) + "'"}'''

    return selectCount(query)


def insertSemantic(id_site, id_link, character):
    query = f'''INSERT INTO links_semantic (id_site, id_link, character) VALUES ({"'" + str(id_site) + "'"}, {"'" + str(id_link) + "'"}, {"'" + character + "'"})'''

    insert(query)


def checkSemantic(id_site, id_link):
    query = f'''SELECT COUNT(*) FROM links_semantic WHERE id_site = {"'" + str(id_site) + "'"} AND id_link = {"'" + str(id_link) + "'"}'''

    return selectCount(query)


def selectOne(query):
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
