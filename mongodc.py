import random
from pymongo import MongoClient

class Client:
    def __init__(self, db_name="Api", cluster="data"):
        self.db = MongoClient()[db_name][cluster]
    
    def create_user(self, data):
        user_id = random.randint(10**15, 9 * (10**15))
        data["_id"] = user_id
        self.db.insert_one(data)
        return data
    
    def read_user(self, data):
        return self.db.find_one(data)
    
    def read_all_users(self):
        return list(self.db.find({}))
    
    def update_user(self, data):
        if self.read_user(data) is None:
            return {"Update": "Error", "Reason": "User Nout Found"}
        
        self.db.update_one({"_id": data[0]}, {"$set": data[1]})
        return self.read_user({"_id": data[0]})
        
    def delete_user(self, data):
        if self.read_user(data) is None:
            return {"Delete": "Error", "Reason": "User Not Found"}
        
        self.db.delete_one(data)
        return {"Delete": "Succes"}
    
mongo = Client()
