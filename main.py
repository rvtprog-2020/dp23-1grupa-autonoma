from flask import Flask, render_template, redirect, request
import json
import math

app = Flask(__name__)

# CARS LIST

def load_cars():
    print("Loading cars...")
    try:
        data = json.load(open("cars.json"))

        for car in data:
            car["id"] = data.index(car)

        print(data)

        return data
    except Exception as e:
        print(e)
        return []

cars = load_cars()

def find_car_by_id(id):
    if type(id) == str:
        try:
            id = int(id)
        except:
            return None
    return cars[id] if id >= 0 and id < len(cars) else None

reserved_cars = []

# PAGES

def generate_pages():
    pages = []
    pages_count = math.ceil(len(cars) / 3)

    for i in range(pages_count):
        page = [ cars[i * 3] ]

        if (i * 3 + 1 < len(cars)):
            page.append(cars[i * 3 + 1])
        if (i * 3 + 2 < len(cars)):
            page.append(cars[i * 3 + 2])
        
        pages.append(page)

    return pages

pages = generate_pages()

def get_page_by_id(id):
    if type(id) == str:
        try:
            id = int(id)
        except:
            return None
    return pages[id] if id >= 0 and id < len(pages) else None

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

    cars_in_page = page

    return render_template("cars_list.html", cars=cars_in_page, pages=pages, page_id = int(page_id))
    #return render_template("cars_list.html")

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
    cars_in_page = [ cars[car_id] for car_id in reserved_cars ]
    return render_template("reserved_cars_list.html", cars=cars_in_page)

@app.route("/admin/cars")
def admin_cars_list():
    cars_in_page = cars[:3]
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

        if type(car_id) != int or find_car_by_id(car_id) == None: return { "code": 400, "msg": "Uncorrect car id" }

        if car_id in reserved_cars: return { "code": 400, "msg": "Car already in reserved cars list" } 

        reserved_cars.append(car_id)

        return { "code": 200, "msg": ":)" }
    except Exception as e:
        print(e)
        return { "code": 500, "msg": str(e) }

if __name__ == '__main__':
    app.run(port=80, debug=True)