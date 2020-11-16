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

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/car/<id>")
def car_by_id(id):
    try:
        id = int(id)

        print(id)
        
        if id < 0 or id >= len(cars):
            raise Exception("Out of index")

        return render_template("car_info.html", car=cars[id])
    except:
        return "404 car not found"

@app.route("/cars")
def cars_list():
    cars_in_page = cars[:3]
    print(cars_in_page)
    return render_template("cars_list.html", cars=cars_in_page)

@app.route("/car/0/reserve")
def car_reserve():
    return render_template("car_reserve.html")

@app.route("/reserved")
def reserved_cars_list():
    return render_template("reserved_cars_list.html")

@app.route("/admin/cars")
def admin_cars_list():
    return render_template("admin/cars_list.html")

@app.route("/admin/car/0/edit")
def admin_car_edit():
    return render_template("admin/car_edit.html")

@app.route("/debug")
def debug():
    return render_template("debug.html")

if __name__ == '__main__':
    app.run(port=80, debug=True)