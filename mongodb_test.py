from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

# TO INSTALL (WINDOWS):
# USE: pip install pymongo[srv]
# IF ALREADY EXISTS BEFORE INSTALLING: pip uninstall pymongo AND pip uninstall dnspython

def run():
    username = "boss"
    password = "ZeP-iFc-jwZ-q46"
    cluster_name = "test"
    dbname = "test"

    print("Connecting mongodb...")
    client = MongoClient("mongodb+srv://" + username + ":" + password + "@" + cluster_name + ".839ly.mongodb.net/" + dbname + "?retryWrites=true&w=majority")

    db = client[dbname]

    cars_db = db["cars"]

    filter = {"_id": ObjectId("5fd3375fbded2ade3b7feb68")}

    print(cars_db.find_one(filter))

    cars_db.update_one(filter, {"$set": {"image": "nissan.jpg"}})

if __name__ == "__main__":
    run()