from flask import Flask, render_template, request
import json

app = Flask(__name__)

def load_cars():
    print("Loading cars...")
    try:
        return json.load(open("cars.json"))
    except:
        return []

cars = load_cars()

def find_car_by_id(id):
    if type(id) == str:
        try:
            id = int(id)
        except:
            return None
    return cars[id] if id >= 0 and id < len(cars) else None

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/car/<id>")
def car_by_id(id):
    car = find_car_by_id(id)
    if not car: return "404"
    return render_template("car_info.html", car=car)

@app.route("/cars")
def cars_list():
    cars_in_page = cars[:3]
    print(cars_in_page)
    return render_template("cars_list.html", cars=cars_in_page)

@app.route("/car/<id>/reserve")
def car_reserve(id):
    car = find_car_by_id(id)
    if not car: return "404"
    return render_template("car_reserve.html", car=car)

@app.route("/reserved")
def reserved_cars_list():
    return render_template("reserved_cars_list.html")

@app.route("/admin/cars")
def admin_cars_list():
    return render_template("admin/cars_list.html")

@app.route("/admin/car/<id>")
def admin_car_info(id):
    car = find_car_by_id(id)
    if not car: return "404"
    return render_template("admin/car_info.html", car=car)

@app.route("/debug")
def debug():
    return render_template("debug.html")

if __name__ == '__main__':
    app.run(port=80, debug=True)