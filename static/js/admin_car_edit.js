
async function removeCar(carId) {
    console.log(carId);
    let response = await fetch("http://localhost/admin/remove_car", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "car_id": carId
        })
    });
    let data = await response.json();
    console.log(data);

    if (data.code == 200) {
        window.location.href = "/admin/cars";
    } else {
        alert(data.msg);
    }
}

async function editCar(carId) {
    if (carId == null) {
        return;
    }

    carName = document.getElementById("carName");
    carBrand = document.getElementById("carBrand");
    carMileage = document.getElementById("carMileage");
    carSeats = document.getElementById("carSeats");
    carModel = document.getElementById("carModel");
    carClass = document.getElementById("carClass");
    carPrice = document.getElementById("carPrice");
    carImage = document.getElementById("carImage");
    carRentPoint = document.getElementById("rentPoint");

    let response = await fetch("http://localhost/admin/edit_car", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "car_id": carId,
            "car_name": carName.value,
            "car_brand": carBrand.value,
            "car_mileage": parseInt(carMileage.value),
            "car_seats": parseInt(carSeats.value),
            "car_model": carModel.value,
            "car_class": carClass.value,
            "car_price": parseInt(carPrice.value),
            "car_image": carImage.value,
            "car_rent_point": carRentPoint.value
        })
    });
    let data = await response.json();
    console.log(data);

    if (data.code == 200) {
        window.location.href = "/admin/cars";
    } else {
        alert(data.msg);
    }
}

async function addCar() {
    carName = document.getElementById("carName");
    carBrand = document.getElementById("carBrand");
    carMileage = document.getElementById("carMileage");
    carSeats = document.getElementById("carSeats");
    carModel = document.getElementById("carModel");
    carClass = document.getElementById("carClass");
    carPrice = document.getElementById("carPrice");
    carImage = document.getElementById("carImage");
    carRentPoint = document.getElementById("rentPoint");

    let response = await fetch("http://localhost/admin/add_car", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "car_name": carName.value,
            "car_brand": carBrand.value,
            "car_mileage": parseInt(carMileage.value),
            "car_seats": parseInt(carSeats.value),
            "car_model": carModel.value,
            "car_class": carClass.value,
            "car_price": parseInt(carPrice.value),
            "car_image": carImage.value,
            "car_rent_point": carRentPoint.value
        })
    });
    let data = await response.json();
    console.log(data);

    if (data.code == 200) {
        window.location.href = "/admin/cars";
    } else {
        alert(data.msg);
    }
}