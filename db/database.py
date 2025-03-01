import json
from pymongo import MongoClient
from . import DbInterface, DbType


class DbFile(DbInterface):
    def __init__(self, connection_string: str):
        super().__init__(connection_string)
        self.storage = self.read()

    def read(self) -> dict:
        try:
            with open(self.connection_string, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def write(self, data: dict):
        self.storage.update({data["word"]: data})
        with open(self.connection_string, "w", encoding="utf-8") as f:
            json.dump(self.storage, f, indent=4)

    def exists(self, key: str) -> bool:
        return key in self.storage

    def get_or_none(self, key: str) -> dict:
        return self.storage.get(key)

    def update(self, key: str, data: dict):
        if key in self.storage:
            self.storage[key].update(data)
        else:
            self.storage[key] = data
        with open(self.connection_string, "w", encoding="utf-8") as f:
            json.dump(self.storage, f, indent=4)

    def get_whole_data(self) -> dict:
        return self.storage


class DbMongo(DbInterface):
    def __init__(self, connection_string: str, db_name: str, collection_name: str):
        super().__init__(connection_string)
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def read(self):
        return list(self.collection.find({}, {"_id": 0}))

    def write(self, data: dict):
        self.collection.update_one({"word": data["word"]}, {"$set": data}, upsert=True)

    def exists(self, key: str) -> bool:
        return self.collection.count_documents({"word": key}, limit=1) > 0

    def get_or_none(self, key: str) -> dict:
        return self.collection.find_one({"word": key}, {"_id": 0})

    def update(self, key: str, data: dict):
        self.collection.update_one({"word": key}, {"$set": data}, upsert=True)

    def get_whole_data(self):
        return list(self.collection.find({}, {"_id": 0}))


class DbFactory:
    @staticmethod
    def create_db(
        db_type: DbType,
        connection_string: str,
        db_name: str = None,
        collection_name: str = None,
    ):
        if db_type == DbType.FILE:
            return DbFile(connection_string)
        elif db_type == DbType.MONGO:
            if not db_name or not collection_name:
                raise ValueError(
                    "MongoDB requires both a database name and collection name."
                )
            return DbMongo(connection_string, db_name, collection_name)
        else:
            raise ValueError("Unsupported database type")
