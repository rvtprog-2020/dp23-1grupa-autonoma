var carPrice = 0;
var days = 0;

function setPrice(price) {
    carPrice = price;
}

window.addEventListener("load", function() {
    let daysSlider = document.getElementById("slider-days");

    changeSlider(daysSlider.value);
});

function changeSlider(value) {
    let reserveInfo = document.getElementById("reserve-info");
    let reserveDays = document.getElementById("reserve-days");
    let reservePrice = document.getElementById("reserve-price");
    
    reserveInfo.classList.remove("hidden");

    days = value;

    reserveDays.innerText = value;
    reservePrice.innerText = value + " * " + carPrice + "€ = " + value * carPrice + "€";
}

async function reserveCar(car_id) {
    let response = await fetch("http://localhost/reserve_car", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "car_id": car_id,
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