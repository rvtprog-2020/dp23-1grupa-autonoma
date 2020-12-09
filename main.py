from flask import Flask, render_template, redirect, request
import json
import math

from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

username = "boss"
password = "ZeP-iFc-jwZ-q46"
cluster_name = "test"
dbname = "test"

print("Connecting mongodb...")
client = MongoClient("mongodb+srv://" + username + ":" + password + "@" + cluster_name + ".839ly.mongodb.net/" + dbname + "?retryWrites=true&w=majority")

db = client[dbname]

cars_db = db["cars"]
reservations_db = db["reservations_db"]

print("Starting flask...")
app = Flask(__name__)

def find_car_by_id(id):
    return cars_db.find_one({"_id": ObjectId(id)})

def add_reservation(car_id, days, price):
    reservations_db.insert_one({
        "car_id": ObjectId(car_id),
        "days": days,
        "price": price
    })

def remove_reservation(car_id):
    reservations_db.remove({"car_id": ObjectId(car_id)})

# PAGES

def get_page_by_id(id):
    if (type(id) == str):
        try: id = int(id)
        except: return None
    return cars_db.find()

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/car/<id>")
def car_by_id(id):
    car = find_car_by_id(id)
    if not car: return "404"
    return render_template("car_info.html", car=car)

@app.route("/cars/<page_id>")
def cars_list(page_id):
    page = get_page_by_id(page_id)
    
    if not page: return redirect("/cars")

    return render_template("cars_list.html", cars=page, pages=[], page_id = int(page_id))

@app.route("/cars")
def cars_list_zero():
    return cars_list(0)

@app.route("/car/<id>/reserve")
def car_reserve(id):
    car = find_car_by_id(id)
    if not car: return "404"
    return render_template("car_reserve.html", car=car)

@app.route("/reserved")
def reserved_cars_list():
    reserved_cars = []

    for reservation in reservations_db.find():
        reservation_ent = [
            find_car_by_id(reservation["car_id"]), reservation["days"], reservation["price"]
        ]
        reserved_cars.append(reservation_ent)

    return render_template("reserved_cars_list.html", reserved_cars=reserved_cars)

@app.route("/admin/cars")
def admin_cars_list():
    cars_in_page = cars[:3] # TODO
    print(cars_in_page)
    return render_template("admin/cars_list.html", cars=cars_in_page)

@app.route("/admin/car/<id>")
def admin_car_info(id):
    car = find_car_by_id(id)
    if not car: return "404"
    return render_template("admin/car_info.html", car=car)

@app.route("/debug")
def debug():
    return render_template("debug.html")

@app.route("/get_cars_page", methods=["POST"])
def get_cars_page():
    if not request.content_type == "application/json": return { "code": 400, "msg": "Unknown request type" }

    try:
        jsonData = request.json
        page = get_page_by_id(jsonData["page_id"])
        
        if not page: return { "code": 404, "msg": "Page not found" }

        return {
            "code": 200,
            "page": page,
        }
    except Exception as e:
        print(e)
        return { "code": 500, "msg": "Error" }

@app.route("/reserve_car", methods=["POST"])
def reserve_car_post():
    if not request.content_type == "application/json": return { "code": 400, "msg": "Unknown request type" }

    try:
        jsonData = request.json
        car_id = jsonData["car_id"]
        days = jsonData["days"]

        print(car_id)
        print(days)
        
        if type(days) != int or days <= 0 or days > 30: return { "code": 400, "msg": "Uncorrect days count " + str(days) }

        finded_car = find_car_by_id(car_id)

        if not finded_car: return { "code": 400, "msg": "Uncorrect car id \"" + car_id + "\"" }

        if car_id in reserved_cars: return { "code": 400, "msg": "Car already in reserved cars list" }

        add_reservation(car_id, days, days * finded_car["price"])

        return { "code": 200, "msg": ":)" }
    except Exception as e:
        print(e)
        return { "code": 500, "msg": str(e) }

@app.route("/remove_car", methods=["POST"])
def remove_car_post():
    if not request.content_type == "application/json": return { "code": 400, "msg": "Unknown request type" }

    try:
        jsonData = request.json
        car_id = jsonData["car_id"]

        car = find_car_by_id(car_id)

        if not car: return { "code": 400, "msg": "Uncorrect car id \"" + car_id + "\"" }

        remove_reservation(car_id)

        return { "code": 200, "msg": ":)" }
    except Exception as e:
        print(e)
        return { "code": 500, "msg": str(e) }

if __name__ == '__main__':
    app.run(port=80, debug=True)