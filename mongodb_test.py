from pymongo import MongoClient
from bson.json_util import dumps

# TO INSTALL (WINDOWS):
# USE: pip install pymongo[srv]
# IF ALREADY EXISTS BEFORE INSTALLING: pip uninstall pymongo AND pip install dnspython

def run():
    username = "boss"
    password = "ZeP-iFc-jwZ-q46"
    cluster_name = "test"
    dbname = "test"

    print("Connecting mongodb...")
    client = MongoClient("mongodb+srv://" + username + ":" + password + "@" + cluster_name + ".839ly.mongodb.net/" + dbname + "?retryWrites=true&w=majority")

    db = client[dbname]

    cars_db = db["cars"]

    cars_db.insert_one({"name": "Nissan X-Trail", "image": "nissan", "milleage": 100000, "seats": 4, "price": 4})

if __name__ == "__main__":
    run()