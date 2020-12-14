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

def find_reservation(reservation_id):
    return reservations_db.find_one({"_id": ObjectId(reservation_id)})

def get_pages():
    cars_list = list(cars_db.find())
    pages_count = math.ceil(len(cars_list) / 4)
    
    pages_list = []

    for i in range(pages_count):
        pages_list.append([cars_list[j + i * 4] for j in range(4) if j + i * 4 < len(cars_list)])

    return pages_list

def get_page_by_id(page_id):
    if type(page_id) == str:
        try:
            page_id = int(page_id)
        except:
            return None
    if page_id >= 0:
        pages = get_pages()
        if page_id < len(pages):
            return pages[page_id]
        else:
            return None

def remove_reservation(car_id):
    reservations_db.remove({"car_id": ObjectId(car_id)})

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
    
    if not page:
        if page_id == 0:
            page = []
        else:
            return redirect("/cars")

    return render_template("cars_list.html", cars=page, pages=get_pages(), page_id = int(page_id))

@app.route("/cars")
def cars_list_zero():
    return cars_list(0)

@app.route("/car/<id>/reserve")
def car_reserve(id):
    car = find_car_by_id(id)
    if not car: return "404"
    return render_template("car_reserve.html", car=car)

@app.route("/reserved/<reservation_id>")
def view_reserved_car(reservation_id):
    reservation = find_reservation(reservation_id)
    
    if not reservation: return redirect("/reserved")

    return render_template("reserved_car.html", car = find_car_by_id(reservation["car_id"]), reservation = reservation)

@app.route("/reserved/<reservation_id>/edit")
def reserved_car_edit(reservation_id):
    reservation = find_reservation(reservation_id)
    
    if not reservation: return redirect("/reserved")

    return render_template("reserved_car_edit.html", car = find_car_by_id(reservation["car_id"]), reservation = reservation)

@app.route("/reserved")
def reserved_cars_list():
    reserved_cars = []

    for reservation in reservations_db.find():
        reservation_ent = [
            find_car_by_id(reservation["car_id"]), reservation["days"], reservation["price"], reservation["_id"]
        ]
        reserved_cars.append(reservation_ent)

    return render_template("reserved_cars_list.html", reserved_cars=reserved_cars)

@app.route("/admin/cars/<page_id>")
def admin_cars_list(page_id):
    page = get_page_by_id(page_id)
    
    if not page:
        if page_id == 0:
            page = []
        else:
            return redirect("/cars")

    return render_template("admin/cars_list.html", cars=page, pages=get_pages(), page_id = int(page_id))

@app.route("/admin/cars")
def admin_cars_list_zero():
    return admin_cars_list(0)

@app.route("/admin/car/<car_id>")
def admin_car_info(car_id):
    car = find_car_by_id(car_id)
    if not car: return "404"
    return render_template("admin/car_info.html", car=car)

@app.route("/admin/car/<car_id>/edit")
def admin_car_edit(car_id):
    car = find_car_by_id(car_id)
    if not car: return "404"
    return render_template("admin/car_edit.html", car=car)

@app.route("/admin/add_car")
def admin_add_car():
    return render_template("admin/car_add.html")

@app.route("/admin/car/<car_id>/reservations")
def admin_reservation_view(car_id):
    car = find_car_by_id(car_id)
    if not car: return "404"

    data = list(reservations_db.find({"car_id": ObjectId(car_id)}))

    return render_template("admin/car_reservations.html", car=car, data=data)

@app.route("/debug")
def debug():
    return render_template("debug.html")

# POSTS

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

        reservation = reservations_db.find_one({"car_id": ObjectId(car_id)})

        if reservation: return { "code": 400, "msg": "Reservation at this car already exists" }

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

@app.route("/edit_reservation", methods=["POST"])
def edit_reservation_post():
    if not request.content_type == "application/json": return { "code": 400, "msg": "Unknown request type" }

    try:
        jsonData = request.json
        reservation_id = jsonData["reservation_id"]

        reservation = find_reservation(reservation_id)

        if not reservation: return { "code": 400, "msg": "Kek 1" }

        car = find_car_by_id(reservation["car_id"])

        if not car: return { "code": 400, "msg": "Kek 2" }

        reservations_db.update_one({"_id": ObjectId(reservation_id)}, {
            "$set": {
                "days": jsonData["days"],
                "price": jsonData["days"] * car["price"]
            }
        })

        return { "code": 200, "msg": ":)" }
    except Exception as e:
        print("Exception error:")
        print(e)
        return { "code": 500, "msg": str(e) }

@app.route("/admin/edit_car", methods=["POST"])
def admin_edit_car_post():
    if not request.content_type == "application/json": return { "code": 400, "msg": "Unknown request type" }

    try:
        jsonData = request.json
        car_id = jsonData["car_id"]

        car = find_car_by_id(car_id)

        if not car: return { "code": 400, "msg": "Kek 1" }

        cars_db.update_one({"_id": ObjectId(car_id)}, {
            "$set": {
                "name": jsonData["car_name"],
                "mileage": jsonData["car_mileage"],
                "seats": jsonData["car_seats"],
                "price": jsonData["car_price"],
            }
        })

        return { "code": 200, "msg": ":)" }
    except Exception as e:
        print("Exception error:")
        print(e)
        return { "code": 500, "msg": str(e) }

@app.route("/admin/remove_car", methods=["POST"])
def admin_remove_car_post():
    if not request.content_type == "application/json": return { "code": 400, "msg": "Unknown request type" }

    try:
        jsonData = request.json
        car_id = jsonData["car_id"]

        car = find_car_by_id(car_id)

        if not car: return { "code": 400, "msg": "Kek 1" }

        cars_db.remove({"_id": ObjectId(car_id)})

        return { "code": 200, "msg": ":)" }
    except Exception as e:
        print("Exception error:")
        print(e)
        return { "code": 500, "msg": str(e) }

@app.route("/admin/add_car", methods=["POST"])
def add_car_post():
    if not request.content_type == "application/json": return { "code": 400, "msg": "Unknown request type" }

    try:
        jsonData = request.json

        cars_db.insert_one({
            "name": jsonData["car_name"],
            "mileage": jsonData["car_mileage"],
            "seats": jsonData["car_seats"],
            "price": jsonData["car_price"],
            "image": jsonData["car_image"]
        })

        return { "code": 200, "msg": ":)" }
    except Exception as e:
        print(e)
        return { "code": 500, "msg": str(e) }

if __name__ == '__main__':
    app.run(port=80, debug=True)