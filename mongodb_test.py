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

    cars_db = db["cars"]

    for car in cars_db.find():
        print(car["name"])
        brand_name = input()
        print(brand_name)

        cars_db.update({"_id": car["_id"]}, {
            "$set": {
                "brand": brand_name
            }

        })

if __name__ == "__main__":
    run()