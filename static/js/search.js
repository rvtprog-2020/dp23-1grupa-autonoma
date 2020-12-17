let filters = [];
let cars = [];

function addFilter(filterName, filterElement) {
    if (filters[filterName] == undefined) {
        filters[filterName] = []
    }
    filters[filterName][filterElement] = true;
}

function addCar(name, brand, carClass, mileage, url) {
    cars.push({name, brand, carClass, mileage, url});
}

window.addEventListener("load", function() {
    updateResults();
});

function updateResults() {
    let searchResults = document.getElementById("searchResults");

    searchResults.innerHTML = "<h2>Meklēšanas rezultāti:</h2>";

    for (let car of cars) {
        let add = true;

        for (let element of Object.keys(filters["brand"])) {
            if (car.brand == element && !filters["brand"][element]) {
                add = false;
                break;
            }
        }
        if (add) {
            for (let element of Object.keys(filters["mileage"])) {
                if (car.mileage == element && !filters["mileage"][element]) {
                    add = false;
                    break;
                }
            }
        }
        if (add) {
            for (let element of Object.keys(filters["class"])) {
                if (car.carClass == element && !filters["class"][element]) {
                    add = false;
                    break;
                }
            }
        }
        
        if (add) {
            searchResults.innerHTML += "<a class=\"car-link\" href=\"" + car.url + "\">" + car.name + "</a>"
            searchResults.innerHTML += "<p>Auto marka:" + car.brand + "</p>"
        }
    }
}

function updateFilter(filter, filterElement, checkbox) {
    if (filters[filter] == undefined) {
        filters[filter] = []
    }

    filters[filter][filterElement] = checkbox;

    updateResults();
}