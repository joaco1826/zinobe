import os

from mongoengine import connect, StringField, FloatField
from mongoengine_goodjson import Document

connect(os.environ.get('MONGODB_DB'), host="mongodb://" + os.environ.get('MONGODB_USERNAME') + ":" +
                                           os.environ.get('MONGODB_PASSWORD')  + "@" + os.environ.get('MONGODB_HOST') +
                                           ":" + str(os.environ.get('MONGODB_PORT')) + '/?authSource=admin')


class Country(Document):
    region = StringField(required=True)
    country = StringField(required=True)
    language = StringField(required=True)
    time = FloatField(required=True)

    meta = {
        'collection': "countries",
        'strict': False
    }

    def to_json(self):
        return {
            'region': self.region,
            'country': self.country,
            'language': self.language,
            'time': self.time
        }
