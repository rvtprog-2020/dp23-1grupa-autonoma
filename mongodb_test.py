from pymongo import MongoClient
#from bson.json_util import dumps
#from bson.objectid import ObjectId

def run():
    print("Running...")
    password = "ZeP-iFc-jwZ-q46"
    dbname = "cluster0"

    client = MongoClient("mongodb://boss:" + password + "@cluster0.839ly.mongodb.net/" + dbname + "?retryWrites=true&w=majority")

    print("\nClient:")
    print(client)

    db = client['cluster0']

    print("\nDB:")
    print(db)

    users_db = db["users"]

    print("\nUsers DB:")
    print(users_db)

    # SOS
    users_db.insert_one({"name": "Kek", "surname": "Petrovich", "password": "qwerty12345"})

if __name__ == "__main__":
    run()