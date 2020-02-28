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
        Utils.insert_sql(df['time'].sum(), df['time'].mean(), df['time'].min(), df['time'].max())

        # Generate data.json
        df.to_json(r'data.json', orient='records')

        # Insert data in mongo
        Utils.insert_document(df.to_dict('records'))
        return True

    @staticmethod
    def insert_sql(total, mean, min, max):
        connection = Utils.sql_connection()
        Utils.sql_table(connection)
        cursor_obj = connection.cursor()
        cursor_obj.execute('''INSERT INTO times(total, mean, min, max) VALUES(?, ?, ?, ?)''', (total, mean, min, max))
        return connection.commit()

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
    def sql_table(connection):
        cursor_obj = connection.cursor()
        cursor_obj.execute("CREATE TABLE IF NOT EXISTS times ("
                           "id integer PRIMARY KEY, "
                           "total float, "
                           "mean float, "
                           "min float, "
                           "max float)")
        return connection.commit()
