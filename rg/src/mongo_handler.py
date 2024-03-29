from pymongo import MongoClient
import pprint
import os
import json


class MongodbHandler:
    def __init__(self):
        # Get environment variables
        self.user = os.getenv('MONGO_INITDB_ROOT_USERNAME')
        self.password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
        self.db_name = os.getenv('DB_NAME')
        self.port = '27017'
        # self.connection = MongoClient('mongodb://root:example@mongodb:27017/')
        self.connection = MongoClient(
            'mongodb://%s:%s@%s:%s/' % (self.user, self.password, 'mongodb', self.port))
        self.db = self.connection[self.db_name]
        # creating db
        self.connection[self.db_name]

    def is_collection_exist(self, collection_name):
        if collection_name in self.db.list_collection_names():
            return True, self.db[collection_name]
        return False, None

    def get_database(self, db_name):
        # getting a database
        return self.connection[db_name]

    def get_collection(self, collection_name):
        is_exist, collection = self.is_collection_exist(collection_name)
        if is_exist:
            return collection
        return None

    # returns a cursor with the specific field and values without the id field
    # for more examples of querying in pymongo see https://www.analyticsvidhya.com/blog/2020/08/query-a-mongodb-database-using-pymongo/
    def get_documents(self, collection_name, field, value):
        return self.get_collection(collection_name).find({field: value}, {"_id": 0})
    # returns a Cursor without the id field

    def get_all_documents(self, collection_name):
        return self.get_collection(collection_name).find({}, {"_id": 0})

    def get_documents_by_location(self, collection_name):
        # Get the collection and sort the documents by location
        collection = self.get_collection(collection_name)
        documents = collection.find().sort("location")

        # Create an empty dictionary to store the documents by location
        documents_by_location = {}

        # Iterate over the documents and group them by location
        for document in documents:
            location = document.get("location")

            # Check if the location key exists in the dictionary
            if location not in documents_by_location:
                documents_by_location[location] = []

            # Remove the _id field from the document
            if "_id" in document:
                del document["_id"]

            # Add the document to the corresponding location array
            documents_by_location[location].append(document)

        # Convert the dictionary to a list of arrays and return it
        return list(documents_by_location.values())

    # returns list of dic, each dic holds a json object
    def get_all_documents_in_list(self, collection_name):
        return list(self.get_collection(collection_name).find({}, {"_id": 0}))
        # returns a dic with the specific field and values without the id field

    def get_find_one(self, collection_name, field, value):
        return self.get_collection(collection_name).find_one({field: value}, {"_id": 0})

    def get_collection_sorted(self, collection_name):
        documents = list(self.get_collection(
            collection_name).find({}, {"_id": 0}).sort("location"))
    # convert the cursor to a list of dictionaries and then to JSON
        documents_json = json.dumps(documents)
        return documents_json

    # function gets documents from get_documents or get_all_documents
    def print_documents(self, documents):
        for document in documents:
            MyPrettyPrinter().pprint(document)

    def insert_document(self, collection_name, document):
        collection = self.db[collection_name]
        collection.insert_one(document)

    def insert_documents(self, collection_name, documents):
        collection = self.db[collection_name]
        collection.insert_many(documents)


class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)
