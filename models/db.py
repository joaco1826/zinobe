import logging
import os
from mongoengine import connect

try:
    connect(os.environ.get('MONGODB_DB'), host="mongodb://" + os.environ.get('MONGODB_USERNAME') + ":" +
                                               os.environ.get('MONGODB_PASSWORD') +
                                               "@" + os.environ.get('MONGODB_HOST') +
                                               ":" + str(os.environ.get('MONGODB_PORT')) + '/?authSource=admin')
    logging.critical("Database connected!")
except:
    logging.fatal("Failed connect to MongoDB!")
    raise
