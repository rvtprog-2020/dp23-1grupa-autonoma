async function deleteReservation(reservation_id) {
    let response = await fetch("http://localhost/remove_car", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "reservation_id": reservation_id
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