from http import HTTPStatus
from models.country import Country
import json


class Controller:
    KEY_VALUES = 'ms.statics.values'

    @staticmethod
    def list_countries():
        countries = Country.objects.all()
        response = {
            'list': list(map(lambda c: c.to_json(), countries))
        }
        return response, HTTPStatus.OK
