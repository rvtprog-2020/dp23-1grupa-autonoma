
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
    carName = document.getElementById("carName");
    carMileage = document.getElementById("carMileage");
    carSeats = document.getElementById("carSeats");
    carPrice = document.getElementById("carPrice");

    if (carId == null) {
        return;
    }

    let response = await fetch("http://localhost/admin/edit_car", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "car_id": carId,
            "car_name": carName.value,
            "car_mileage": parseInt(carMileage.value),
            "car_seats": parseInt(carSeats.value),
            "car_price": parseInt(carPrice.value)
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
    carMileage = document.getElementById("carMileage");
    carSeats = document.getElementById("carSeats");
    carPrice = document.getElementById("carPrice");
    carImage = document.getElementById("carImage");

    let response = await fetch("http://localhost/admin/add_car", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "car_name": carName.value,
            "car_mileage": parseInt(carMileage.value),
            "car_seats": parseInt(carSeats.value),
            "car_price": parseInt(carPrice.value),
            "car_image": carImage.value
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