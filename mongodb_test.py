from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

# TO INSTALL (WINDOWS):
# USE: pip install pymongo[srv]
# IF ALREADY EXISTS BEFORE INSTALLING: pip uninstall pymongo AND pip uninstall dnspython

def connect_db(dbname):
    username = "boss"
    password = "ZeP-iFc-jwZ-q46"
    cluster_name = "test"
    
    return MongoClient("mongodb+srv://" + username + ":" + password + "@" + cluster_name + ".839ly.mongodb.net/" + dbname + "?retryWrites=true&w=majority")

def run():
    client = connect_db("test")

    db = client["test"]

    cars_db = db["rent_points"]

    cars_db.insert_one({"name": "1. Nomas Punkts", "location": "Aisteres iela 3"})
    cars_db.insert_one({"name": "2. Nomas Punkts", "location": "Kristapa iela 10"})
    cars_db.insert_one({"name": "3. Nomas Punkts", "location": "Hermaņa iela 5"})
    cars_db.insert_one({"name": "4. Nomas Punkts", "location": "Artilērijas iela 14"})

if __name__ == "__main__":
    run()