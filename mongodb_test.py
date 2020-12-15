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

    rent_points_db = db["rent_points"]

    rent_points_db.update_many({}, {
            "$set": {
                "image": "https://i.redd.it/w5eatab9oop01.jpg"
            }
        })

if __name__ == "__main__":
    run()