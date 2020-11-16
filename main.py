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

print(cars)

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

        return render_template("car.html", car=cars[id])
    except:
        return "404 car not found"

if __name__ == '__main__':
    app.run(port=80, debug=True)