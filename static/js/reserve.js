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

function reserveCar() {
    
}