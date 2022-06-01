from pymongo import MongoClient


class DataBaseHelper:

    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client['baza']
        self.groups = self.db['groups']
        self.anime = self.db['anime']
