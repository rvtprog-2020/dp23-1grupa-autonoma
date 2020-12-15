async function createRentPoint() {
    rentPointName = document.getElementById("rentPointName");
    rentPointLocation = document.getElementById("rentPointLocation");
    rentPointImage = document.getElementById("rentPointImage");

    let response = await fetch("http://localhost/admin/create_rent_point", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "rent_point_name": rentPointName.value,
            "rent_point_location": rentPointLocation.value,
            "rent_point_image": rentPointImage.value
        })
    });
    let data = await response.json();
    console.log(data);

    if (data.code == 200) {
        window.location.href = "/admin/rent_points";
    } else {
        alert(data.msg);
    }
}

async function deleteRentPoint(rentPointId) {
    let response = await fetch("http://localhost/admin/rent_point_delete", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "rent_point_id": rentPointId
        })
    });
    let data = await response.json();
    console.log(data);

    if (data.code == 200) {
        window.location.href = "/admin/rent_points";
    } else {
        alert(data.msg);
    }
}

async function editRentPoint(rentPointId) {
    rentPointName = document.getElementById("rentPointName");
    rentPointLocation = document.getElementById("rentPointLocation");
    rentPointImage = document.getElementById("rentPointImage");

    let response = await fetch("http://localhost/admin/edit_rent_point", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "rent_point_id": rentPointId,
            "rent_point_name": rentPointName.value,
            "rent_point_location": rentPointLocation.value,
            "rent_point_image": rentPointImage.value
        })
    });
    let data = await response.json();
    console.log(data);

    if (data.code == 200) {
        window.location.href = "/admin/rent_points";
    } else {
        alert(data.msg);
    }
}