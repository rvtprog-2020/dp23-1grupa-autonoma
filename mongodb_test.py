from pymongo import MongoClient
#from bson.json_util import dumps
#from bson.objectid import ObjectId

def run():
    print("Running...")
    password = "ZeP-iFc-jwZ-q46"
    dbname = "cluster0"

    client = MongoClient("mongodb+srv://boss:" + password + "@cluster0.839ly.mongodb.net/" + dbname + "?retryWrites=true&w=majority")

    print(client)

if __name__ == "__main__":
    run()

# db = client["cluster0"]

# print(db)

# users_db = db.users

# users_db.insert_one({"name": "Kek", "surname": "Petrovich", "password": "qwerty12345"})

#client = MongoClient("mongodb+srv://maris:famN3CBh7Wvtc6Pj@flaskproject.3itkl.mongodb.net/myproject?retryWrites=true&w=majority")