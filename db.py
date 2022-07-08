import json
from datetime import datetime

import bson
from os import environ
from pymongo import MongoClient

mongo_client = MongoClient(environ["MONGO_URL"])
db = mongo_client.stocks_db


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bson.decimal128.Decimal128):
            return float(obj.to_decimal())

        if isinstance(obj, datetime):
            return obj.strftime("%m/%d/%Y")

