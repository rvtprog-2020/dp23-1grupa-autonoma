window.addEventListener("load", async function() {
    let data = await loadCars();
    
    let carsListElement = document.getElementById("auto-list");

    let listContent;

    if (data.code == 200) {
        console.log(data);
        listContent = "";

        pageData = data.page;

        for (car_n in pageData) {
            car = pageData[car_n];
            console.log(car);

            listContent += `
            <li>
                <div class="left">
                    <img src="/static/images/${car.image}" alt="" class="auto-image">
                </div>
                <div class="center">
                    <a class="car-link" href="/car/${car.id}">${car.name}</a>
                    <p>Nobraukums: ${car.mileage} km</p>
                    <p>Sēdvietas: ${car.seats}</p>
                    <p>Cena: ${car.price}€ / diena</p>
                </div>
                <div class="right">
                    <a href="/car/${car.id}/reserve" class="btn btn-blue">Rezervēt</a>
                </div>
            </li>
            `
        }
    } else {
        listContent = "Failed to load!";
    }

    carsListElement.innerHTML = listContent;
});

async function loadCars() {
    let response = await fetch("http://localhost/get_cars_page", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "page_id": 0
        })
    });
    let data = await response.json();
    return data;
}