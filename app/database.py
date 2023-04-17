from os import getenv
from typing import Iterable

from dotenv import load_dotenv
from pymongo import MongoClient


class Database:
    load_dotenv()
    database = MongoClient(getenv("MONGO_URL"))["Database"]
    default_projection = {"_id": False}

    def __init__(self, collection: str):
        self.collection = self.database[collection]

    def count(self, query: dict = None) -> int:
        return self.collection.count_documents(query or {})

    def search(self, search: str, projection: dict = None) -> list[dict]:
        if projection is None:
            projection = self.default_projection
        return list(self.find({"$text": {"$search": search}}, projection=projection))

    def find(self, query: dict = None, projection: dict = None) -> list[dict]:
        if projection is None:
            projection = self.default_projection
        return list(self.collection.find(query or {}, projection=projection))

    def find_one(self, query: dict = None, projection: dict = None) -> dict:
        if projection is None:
            projection = self.default_projection
        return self.collection.find_one(query or {}, projection=projection)

    def write_one(self, record: dict):
        self.collection.insert_one(record)

    def write_many(self, records: Iterable[dict]):
        self.collection.insert_many(records)

    def update_one(self, query, update):
        self.collection.update_one(query, {"$set": update})

    def delete_one(self, query):
        self.collection.delete_one(query)

    def delete_many(self, query):
        self.collection.delete_many(query)

    def reset_collection(self):
        self.database.drop_collection(self.collection.name)
        self.make_index()

    def make_index(self):
        self.collection.create_index([("$**", "text")])

    def drop_index(self):
        self.collection.drop_indexes()
