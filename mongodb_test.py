from pymongo import MongoClient
from bson.json_util import dumps

# TO INSTALL (WINDOWS):
# USE: pip install pymongo[srv]
# IF ALREADY EXISTS AT BEFORE INSTALLING: pip uninstall pymongo AND pip install dnspython

def run():
    print("Running...")
    password = "ZeP-iFc-jwZ-q46"
    dbname = "test"

    
    client = MongoClient("mongodb+srv://boss:" + password + "@test.839ly.mongodb.net/" + dbname + "?retryWrites=true&w=majority")

    print("\nClient:")
    print(client)

    db = client.test

    print("\nDB:")
    print(db)

    users_db = db["users"]

    print("\nUsers DB:")
    print(users_db)

    print("Users:", dumps(users_db.find()))

    users_db.insert_one({"name": "Kek", "surname": "Petrovich", "password": "qwerty12345"})

if __name__ == "__main__":
    run()