async function removeCar(car_id) {
    let response = await fetch("http://localhost/remove_car", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "car_id": car_id
        })
    });
    let data = await response.json();
    consolle.log(data);

    if (data.code == 200) {
        window.location.reload();
    } else {
        alert(data.msg);
    }
}