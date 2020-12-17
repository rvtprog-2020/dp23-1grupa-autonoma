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

def run_fixer():
    client = connect_db("test")

    db = client["test"]

    cars_db = db["cars"]

    for car in cars_db.find():
        print(car["name"])

        if "model" not in car:
            name = input()
            print(name)

            cars_db.update_one({"_id": car["_id"]}, {
                "$set": {
                    "model": name
                }
            })

def check_car(car):
    return "name" in car and "image" in car and "mileage" in car and "seats" in car and "price" in car and "rent_point_id" in car and "brand" in car

def check_reservation(reservation):
    return "car_id" in reservation and "days" in reservation and "price" in reservation and "date" in reservation

def check_rent_point(rent_point):
    return "name" in rent_point and "location" in rent_point and "image" in rent_point

def run_db_check():
    client = connect_db("test")
    db = client["test"]
    cars_db = db["cars"]
    reservations_db = db["reservations"]
    rent_points_db = db["rent_points"]

    for car in cars_db.find():
        if not check_car(car):
            print("Check failed car", car)
            exit()
    
    for reservation in reservations_db.find():
        if not check_reservation(reservation):
            print("Check failed reservation", reservation)
            exit()
    
    for rent_point in rent_points_db.find():
        if not check_rent_point(rent_point):
            print("Check failed rent point", rent_point)
            exit()
    
    print("Successfully checked!")

if __name__ == "__main__":
    run_fixer()