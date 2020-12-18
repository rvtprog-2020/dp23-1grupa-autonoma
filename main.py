from flask import Flask, render_template, redirect, request
import json
import math

from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://boss:ZeP-iFc-jwZ-q46@test.839ly.mongodb.net/test?retryWrites=true&w=majority")

db = client["test"]
cars_db = db["cars"]
reservations_db = db["reservations"]
rent_points_db = db["rent_points"]

app = Flask(__name__)

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
            page = pages[page_id]
            for car in page:
                car["reservation"] = reservations_db.find_one({"car_id": ObjectId(car["_id"])})
                car["rent_point"] = rent_points_db.find_one({"_id": car["rent_point_id"]})
            return page
        else:
            return None

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search")
def search():
    brands_list = set()
    mileage_list = set()
    class_list = set()
    
    for car in cars_db.find():
        brands_list.add(car["brand"])
        mileage_list.add(car["mileage"])
        class_list.add(car["class"])
        
    filters = [
        {
            "id": "brand",
            "name": "Auto marka",
            "elements": brands_list
        },
        {
            "id": "mileage",
            "name": "Auto nobraukums",
            "elements": mileage_list
        },
        {
            "id": "class",
            "name": "Auto klase",
            "elements": class_list
        }
    ]

    return render_template("search.html", filters=filters, cars=list(cars_db.find()))

@app.route("/car/<id>")
def car_by_id(id):
    car = cars_db.find_one({"_id": ObjectId(id)})
    if not car: return "404 - car not found"
    reservation = reservations_db.find_one({"car_id": ObjectId(id)})
    if reservation:
        return redirect("/reserved/" + str(reservation["_id"]))
    rent_point = rent_points_db.find_one({"_id": car["rent_point_id"]})
    if not rent_point: return "404 - rent point not found"
    car["rent_point"] = rent_point
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
    car = cars_db.find_one({"_id": ObjectId(id)})
    if not car: return "404 - car not found"
    reservation = reservations_db.find_one({"car_id": ObjectId(id)})
    if reservation:
        return "already is reserved"
    rent_point = rent_points_db.find_one({"_id": car["rent_point_id"]})
    if not rent_point: return "404 - rent point not found"
    car["rent_point"] = rent_point
    return render_template("car_reserve.html", car=car)

@app.route("/reserved/<reservation_id>")
def view_reserved_car(reservation_id):
    reservation = reservations_db.find_one({"_id": ObjectId(reservation_id)})
    if not reservation: return "404 - reservation not found"
    car = cars_db.find_one({"_id": ObjectId(reservation["car_id"])})
    if not car: return "404 - car not found"

    rent_point = rent_points_db.find_one({"_id": car["rent_point_id"]})
    if not rent_point: return "404 - rent point not found"
    car["rent_point"] = rent_point

    return render_template("reserved_car.html", car=car, reservation=reservation)

@app.route("/reserved/<reservation_id>/edit")
def reserved_car_edit(reservation_id):
    reservation = reservations_db.find_one({"_id": ObjectId(reservation_id)})
    if not reservation: return "404 - reservation not found"
    car = cars_db.find_one({"_id": ObjectId(reservation["car_id"])})
    if not car: return "404 - car not found"
    rent_point = rent_points_db.find_one({"_id": car["rent_point_id"]})
    if not rent_point: return "404 - rent point not found"
    car["rent_point"] = rent_point
    return render_template("reserved_car_edit.html", car=car, reservation = reservation)

@app.route("/reserved")
def reserved_cars_list():
    cars = []

    for reservation in reservations_db.find():
        car = cars_db.find_one({"_id": ObjectId(reservation["car_id"])})
        if car:
            car["reservation"] = reservation
            cars.append(car)
            rent_point = rent_points_db.find_one({"_id": car["rent_point_id"]})
            if not rent_point: return "404 - rent point not found"
            car["rent_point"] = rent_point

    return render_template("reserved_cars_list.html", cars=cars)

@app.route("/rent_points")
def rent_points_list():
    return render_template("rent_points_list.html", rent_points=list(rent_points_db.find()))

@app.route("/rent_points/<rent_point_id>")
def rent_point_view(rent_point_id):
    rent_point_id = ObjectId(rent_point_id)
    rent_point = rent_points_db.find_one({"_id": rent_point_id})
    if not rent_point: return "404 - rent point not found"
    return render_template("rent_point_view.html", rent_point=rent_point, cars=list(cars_db.find({"rent_point_id": rent_point_id})))

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
    car = cars_db.find_one({"_id": ObjectId(car_id)})
    if not car: return "404 - car not found"
    rent_point = rent_points_db.find_one({"_id": car["rent_point_id"]})
    if not rent_point: return "404 - rent point not found"
    car["rent_point"] = rent_point
    return render_template("admin/car_info.html", car=car)

@app.route("/admin/car/<car_id>/edit")
def admin_car_edit(car_id):
    car = cars_db.find_one({"_id": ObjectId(car_id)})
    if not car: return "404 - car not found"
    rent_point = rent_points_db.find_one({"_id": car["rent_point_id"]})
    if not rent_point: return "404 - rent point not found"
    car["rent_point"] = rent_point
    return render_template("admin/car_edit.html", car=car, rent_points=rent_points_db.find())

@app.route("/admin/add_car")
def admin_add_car():
    return render_template("admin/car_add.html", rent_points=rent_points_db.find())

@app.route("/admin/car/<car_id>/reservations")
def admin_reservations_view(car_id):
    car = cars_db.find_one({"_id": ObjectId(car_id)})
    if not car: return "404 - car not found"
    data = list(reservations_db.find({"car_id": ObjectId(car_id)}))
    rent_point = rent_points_db.find_one({"_id": car["rent_point_id"]})
    if not rent_point: return "404 - rent point not found"
    car["rent_point"] = rent_point
    return render_template("admin/car_reservations.html", car=car, data=data)

@app.route("/admin/rent_points")
def admin_rent_points_list():
    return render_template("admin/rent_points_list.html", rent_points=list(rent_points_db.find()))

@app.route("/admin/rent_points/<rent_point_id>")
def admin_rent_point_view(rent_point_id):
    rent_point_id = ObjectId(rent_point_id)
    rent_point = rent_points_db.find_one({"_id": rent_point_id})
    if not rent_point: return "404 - rent point not found"
    return render_template("admin/rent_point_view.html", rent_point=rent_point, cars=list(cars_db.find({"rent_point_id": rent_point_id})))

@app.route("/admin/create_rent_point")
def admin_rent_point_create():
    return render_template("admin/rent_point_create.html")

@app.route("/admin/rent_points/<rent_point_id>/edit")
def admin_rent_point_edit(rent_point_id):
    rent_point_id = ObjectId(rent_point_id)
    rent_point = rent_points_db.find_one({"_id": rent_point_id})
    if not rent_point: return "404 - rent point not found"
    return render_template("admin/rent_point_edit.html", rent_point=rent_point)

# REDIRECTS

@app.route("/admin")
def redirect1():
    return redirect("/")

@app.route("/car")
def redirect2():
    return redirect("/")

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
        print("Exception error:")
        print(e)
        return { "code": 500, "msg": "Error" }

@app.route("/reserve_car", methods=["POST"])
def reserve_car_post():
    if not request.content_type == "application/json": return { "code": 400, "msg": "Unknown request type" }

    try:
        jsonData = request.json
        days = jsonData["days"]
        
        if type(days) != int or days <= 0 or days > 30: return { "code": 400, "msg": "Uncorrect days count " + str(days) }

        car_id = jsonData["car_id"]
        car = cars_db.find_one({"_id": ObjectId(car_id)})

        if not car: return { "code": 400, "msg": "Uncorrect car id \"" + car_id + "\"" }

        reservation = reservations_db.find_one({"car_id": ObjectId(car_id)})

        if reservation: return { "code": 400, "msg": "Reservation at this car already exists" }

        reservations_db.insert_one({
            "car_id": ObjectId(car_id),
            "days": days,
            "price": days * car["price"],
            "date": jsonData["rent_date"]
        })

        return { "code": 200, "msg": "Successfully reserved!" }
    except Exception as e:
        print("Exception error:")
        print(e)
        return { "code": 500, "msg": str(e) }

@app.route("/delete_reservation", methods=["POST"])
def delete_reservation_post():
    if not request.content_type == "application/json": return { "code": 400, "msg": "Unknown request type" }

    try:
        jsonData = request.json

        reservations_db.remove({"_id": ObjectId(jsonData["reservation_id"])})

        return { "code": 200, "msg": "Successfully deleted!" }
    except Exception as e:
        print("Exception error:")
        print(e)
        return { "code": 500, "msg": str(e) }

@app.route("/edit_reservation", methods=["POST"])
def edit_reservation_post():
    if not request.content_type == "application/json": return { "code": 400, "msg": "Unknown request type" }

    try:
        jsonData = request.json
        reservation_id = jsonData["reservation_id"]

        reservation = reservations_db.find_one({"_id": ObjectId(reservation_id)})

        if not reservation: return { "code": 400, "msg": "Reservation not found" }

        car = cars_db.find_one({"_id": ObjectId(reservation["car_id"])})

        if not car: return { "code": 400, "msg": "Car not found" }

        reservations_db.update_one({"_id": ObjectId(reservation_id)}, {
            "$set": {
                "days": jsonData["days"],
                "price": jsonData["days"] * car["price"]
            }
        })

        return { "code": 200, "msg": "Successfully edited!" }
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

        car = cars_db.find_one({"_id": ObjectId(car_id)})

        if not car: return { "code": 400, "msg": "Kek 1" }

        cars_db.update_one({"_id": ObjectId(car_id)}, {
            "$set": {
                "name": jsonData["car_name"],
                "mileage": jsonData["car_mileage"],
                "seats": jsonData["car_seats"],
                "model": jsonData["car_model"],
                "class": jsonData["car_class"],
                "price": jsonData["car_price"],
                "image": jsonData["car_image"],
                "rent_point": jsonData["car_rent_point"]
            }
        })

        return { "code": 200, "msg": "Successfully edited!" }
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

        car = cars_db.find_one({"_id": ObjectId(car_id)})

        if not car: return { "code": 400, "msg": "Car not found" }

        cars_db.remove({"_id": ObjectId(car_id)})

        return { "code": 200, "msg": "Successfully removed!" }
    except Exception as e:
        print("Exception error:")
        print(e)
        return { "code": 500, "msg": str(e) }

@app.route("/admin/add_car", methods=["POST"])
def add_car_post():
    if not request.content_type == "application/json": return { "code": 400, "msg": "Unknown request type" }

    try:
        jsonData = request.json
        rent_point_id = ObjectId(jsonData["car_rent_point"])
        rent_point = rent_points_db.find_one({"_id": rent_point_id})
        
        if not rent_point: return { "code": 400, "msg": "Rent Point not found" }

        cars_db.insert_one({
            "name": jsonData["car_name"],
            "brand": jsonData["car_brand"],
            "mileage": jsonData["car_mileage"],
            "seats": jsonData["car_seats"],
            "model": jsonData["car_model"],
            "class": jsonData["car_class"],
            "price": jsonData["car_price"],
            "image": jsonData["car_image"],
            "rent_point_id": rent_point_id
        })

        return { "code": 200, "msg": "Successfully added!" }
    except Exception as e:
        print("Exception error:")
        print(e)
        return { "code": 500, "msg": str(e) }

@app.route("/admin/create_rent_point", methods=["POST"])
def create_rent_point_post():
    if not request.content_type == "application/json": return { "code": 400, "msg": "Unknown request type" }

    try:
        jsonData = request.json

        rent_points_db.insert_one({
            "name": jsonData["rent_point_name"],
            "location": jsonData["rent_point_location"],
            "image": jsonData["rent_point_image"]
        })

        return { "code": 200, "msg": "Successfully added!" }
    except Exception as e:
        print("Exception error:")
        print(e)
        return { "code": 500, "msg": str(e) }

@app.route("/admin/edit_rent_point", methods=["POST"])
def edit_rent_point_post():
    if not request.content_type == "application/json": return { "code": 400, "msg": "Unknown request type" }

    try:
        jsonData = request.json

        rent_point_id = ObjectId(jsonData["rent_point_id"])
        rent_point = rent_points_db.find({"_id": rent_point_id})
        if not rent_point: return { "code": 400, "msg": "rent point not found" }

        rent_points_db.update_one({"_id": rent_point_id}, {
            "$set": {
                "name": jsonData["rent_point_name"],
                "location": jsonData["rent_point_location"],
                "image": jsonData["rent_point_image"]
            }
        })

        return { "code": 200, "msg": "Successfully edited!" }
    except Exception as e:
        print("Exception error:")
        print(e)
        return { "code": 500, "msg": str(e) }

@app.route("/admin/rent_point_delete", methods=["POST"])
def rent_point_delete_post():
    if not request.content_type == "application/json": return { "code": 400, "msg": "Unknown request type" }

    try:
        jsonData = request.json

        rent_point_id = ObjectId(jsonData["rent_point_id"])
        rent_point = rent_points_db.find({"_id": rent_point_id})
        if not rent_point: return { "code": 400, "msg": "rent point not found" }

        rent_points_db.remove({"_id": rent_point_id})

        return { "code": 200, "msg": "Successfully deleted!" }
    except Exception as e:
        print("Exception error:")
        print(e)
        return { "code": 500, "msg": str(e) }

if __name__ == '__main__':
    app.run(port=80, debug=True)