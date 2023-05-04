# Imports MongoClient for base level access to the local MongoDB
from pymongo import MongoClient


class Database:
    # Class static variables used for database host ip and port information, database name
    # Static variables are referred to by using <class_name>.<variable_name>
    HOST = '127.0.0.1'
    PORT = '27017'
    DB_NAME = 'weather_db'

    def __init__(self):
        self._db_conn = MongoClient(f'mongodb://{Database.HOST}:{Database.PORT}')
        self._db = self._db_conn[Database.DB_NAME]
    
    # This method finds a single document using field information provided in the key parameter
    # It assumes that the key returns a unique document. It returns None if no document is found
    def get_single_data(self, collection, key):
        db_collection = self._db[collection]
        document = db_collection.find_one(key)
        return document
    
    # This method inserts the data in a new document. It assumes that any uniqueness check is done by the caller
    def insert_single_data(self, collection, data):
        db_collection = self._db[collection]
        document = db_collection.insert_one(data)
        return document.inserted_id

    # This method finds a single document based on username and device_id
    def get_by_username_and_device_id(self, collection, username, key):
        db_collection = self._db[collection]
        document = db_collection.find_one(key)
        return document

    # This method finds all document from the collection
    def find_all(self, collection):
        db_collection = self._db[collection]
        document = db_collection.find()
        return document
    
    # Update collection
    def update_query(self, collection, myquery, newvalues):
        db_collection = self._db[collection]
        document = db_collection.update_one(myquery, newvalues)
        return document
    
    # This method finds all document from the collection
    def get_all_data(self, collection, key, specific_row_return):
        db_collection = self._db[collection]
        document = db_collection.find(key, specific_row_return)
        return document
        
    # This method Drops Document from the collection
    def drop_doc(self, collection, username):
        db_collection = self._db[collection]
        db_collection.delete_one({'username': username})
    