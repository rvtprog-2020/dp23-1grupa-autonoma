var days = 0;

window.addEventListener("load", function() {
    let daysSlider = document.getElementById("slider-days");
    changeSlider(daysSlider.value);
});

function changeSlider(carPrice, value) {
    let reserveDays = document.getElementById("reserve-days");
    let reservePrice = document.getElementById("reserve-price");
    
    if (value === undefined) {
        reserveDays.innerText = "";
        reservePrice.innerText = "";
    } else {
        days = value;

        reserveDays.innerText = days;
        reservePrice.innerText = days + " * " + carPrice + "€ = " + days * carPrice + "€";
    }
}

async function deleteReservation(reservationId) {
    let response = await fetch("http://localhost/delete_reservation", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "reservation_id": reservationId
        })
    });
    let data = await response.json();
    console.log(data);

    if (data.code == 200) {
        window.location.reload();
    } else {
        alert(data.msg);
    }
}

async function reserveCar(car_id) {
    let rentDate = document.getElementById("rentDate");

    let response = await fetch("http://localhost/reserve_car", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "car_id": car_id,
            "days": parseInt(days),
            "rent_date": rentDate.value
        })
    });
    let data = await response.json();
    console.log(data);

    if (data.code == 200) {
        window.location.href = "/reserved";
    } else {
        alert(data.msg);
    }
}

async function editReservation(reservationId) {
    let response = await fetch("http://localhost/edit_reservation", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "reservation_id": reservationId,
            "days": parseInt(days)
        })
    });
    let data = await response.json();
    console.log(data);

    if (data.code == 200) {
        window.location.href = "/reserved";
    } else {
        alert(data.msg);
    }
}