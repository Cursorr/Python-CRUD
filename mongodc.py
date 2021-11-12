import random
from pymongo import MongoClient

class Client:
    def __init__(self, db_name="Api", cluster="data"):
        self.major = MongoClient()[db_name]
        self.db = self.major[cluster]
    
    def create_user(self, data):
        user_id = random.randint(10**15, 9 * (10**15))
        data["_id"] = user_id
        self.db.insert_one(data)
        return data
    
    def read_user(self, data):
        user = self.db.find_one(data)
        if user is None:
            return {"Code": "404", "Error": "User not found"} 
        return user
    
    def read_all_users(self):
        return list(self.db.find({}))
    
    def update_user(self, data):
        if self.read_user({"_id": data[0]}) is None:
            return {"Code": "404", "Error": "User not found"}
        
        print(data[1])
        return self.db.update_one({"_id": data[0]}, {"$set": data[1]})
        
    def delete_user(self, data):
        if self.read_user(data) is None:
            return {"Code": "404", "Error": "User not found"}
        
        self.db.delete_one(data)
        return {"Code": "200", "Description": "User is deleted"}

    def delete_all(self):
        self.db.delete_many({})
        return {"Code": "200", "Description": "All users are deleted"}
    
mongo = Client()
