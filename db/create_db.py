import psycopg2
from psycopg2 import Error
import sys
import os

sys.path.insert(0, os.path.abspath(''))

import config


def createSiteTable():
    table = '''CREATE TABLE IF NOT EXISTS sites(
                id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
                link text NOT NULL,
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''

    createTable(table)


def createLinkTable():
    table = '''CREATE TABLE IF NOT EXISTS links (
                id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
                id_site text NOT NULL,
                link text NOT NULL,
                text text NOT NULL,
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''

    createTable(table)


def createLangTable():
    table = '''CREATE TABLE IF NOT EXISTS links_language (
                id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
                id_site text NOT NULL,
                id_link text NOT NULL,
                language text NOT NULL,
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''

    createTable(table)


def createKywordsTable():
    table = '''CREATE TABLE IF NOT EXISTS links_keywords (
                id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
                id_site text NOT NULL,
                id_link text NOT NULL,
                keyword text NOT NULL,
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''

    createTable(table)

def createSemanticTable():
    table = '''CREATE TABLE IF NOT EXISTS links_semantic (
                id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
                id_site text NOT NULL,
                id_link text NOT NULL,
                character text NOT NULL,
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''

    createTable(table)

def createTable(table):
    try:
        connection = psycopg2.connect(
            user=config.pg_user,
            password=config.pg_password,
            host=config.pg_host,
            port=config.pg_port,
            database=config.pg_db
        )

        cursor = connection.cursor()

        cursor.execute(table)
        connection.commit()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


createSiteTable()
createLinkTable()
createLangTable()
createKywordsTable()
createSemanticTable()