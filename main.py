from flask import Flask, render_template
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
    cars_in_page = page
    print(cars_in_page)
    return render_template("cars_list.html", cars=cars_in_page, pages=pages)

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
    cars_in_page = [ car for car in cars if 'reserved' in car ]
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

if __name__ == '__main__':
    app.run(port=80, debug=True)