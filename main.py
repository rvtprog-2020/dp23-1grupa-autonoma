from flask import Flask, render_template, request

app = Flask(__name__)

cars = [
    {
        "name": "Audi 80",
        "mileage": 455000,
        "seats": 4,
        "price": 6,
    },
    {
        "name": "CitroenXsara",
        "mileage": 290000,
        "seats": 4,
        "price": 7,
    },
    {
        "name": "VolksWagen Golf 3",
        "mileage": 300000,
        "seats": 4,
        "price": 4,
    },
]

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