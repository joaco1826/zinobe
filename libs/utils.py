import hashlib
import logging
import os
import sqlite3
import requests
import pandas as pd
from http import HTTPStatus
from libs.exceptions import ExternalRequestFailed
from models.country import Country


class Utils:

    @staticmethod
    def encrypt(string):
        return hashlib.sha1(str(string + "_" + os.environ.get('PRIVATE_KEY')).encode('utf-8')).hexdigest()

    @staticmethod
    def external_request(url):
        headers = {
            'Content-Type': "Application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == HTTPStatus.OK:
            return response.json()
        else:
            raise ExternalRequestFailed

    @staticmethod
    def insert_document(data):
        Country.objects.insert([Country(**obj) for obj in data])

    @staticmethod
    def data_frame(data):
        df = pd.DataFrame(data)

        # Insert times in sqlite
        Utils.time_save(df['time'].sum(), df['time'].mean(), df['time'].min(), df['time'].max())

        # Insert data in sqlite
        Utils.country_save(df.to_dict('records'))

        # Generate data.json
        df.to_json(r'data.json', orient='records')

        # Insert data in mongo
        Utils.insert_document(df.to_dict('records'))
        return True

    @staticmethod
    def time_save(total, mean, min, max):
        connection = Utils.sql_connection()
        Utils.create_table_times(connection)
        cursor_obj = connection.cursor()
        cursor_obj.execute('''INSERT INTO times(total, mean, min, max) VALUES(?, ?, ?, ?)''', (total, mean, min, max))
        return connection.commit()

    @staticmethod
    def country_save(data):
        connection = Utils.sql_connection()
        Utils.create_table_countries(connection)
        for obj in data:
            cursor_obj = connection.cursor()
            cursor_obj.execute('''INSERT INTO countries(region, country, language, time) VALUES(?, ?, ?, ?)''', (obj['region'], obj['country'], obj['language'], obj['time']))
            connection.commit()
        return True

    @staticmethod
    def sql_connection():
        try:
            connection = sqlite3.connect(os.environ.get('DB_SQLITE'))
            logging.critical("Database connected!")
            return connection
        except:
            logging.fatal("Failed connect to Sqlite!")
            raise

    @staticmethod
    def create_table_times(connection):
        cursor_obj = connection.cursor()
        cursor_obj.execute("CREATE TABLE IF NOT EXISTS times ("
                           "id integer PRIMARY KEY, "
                           "total float, "
                           "mean float, "
                           "min float, "
                           "max float)")
        return connection.commit()

    @staticmethod
    def create_table_countries(connection):
        cursor_obj = connection.cursor()
        cursor_obj.execute("CREATE TABLE IF NOT EXISTS countries ("
                           "id integer PRIMARY KEY, "
                           "region varchar(30), "
                           "country varchar(50), "
                           "language varchar(100), "
                           "time float)")
        return connection.commit()
