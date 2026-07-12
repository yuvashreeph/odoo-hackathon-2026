window.onload = loadTrips;

async function loadTrips() {

    const token = localStorage.getItem("token");

    const response = await fetch("/trips", {

        headers: {
            "Authorization": "Bearer " + token
        }

    });

    const result = await response.json();

    let table = document.getElementById("tripsTable");

    table.innerHTML = "";

    result.data.forEach(trip => {

        table.innerHTML += `

        <tr>

            <td>${trip.source}</td>

            <td>${trip.destination}</td>

            <td>${trip.driverId}</td>

            <td>${trip.vehicleId}</td>

            <td>${trip.cargoWeight}</td>

            <td>${trip.plannedDistance}</td>

            <td>${trip.revenue}</td>

            <td>${trip.status}</td>

        </tr>

        `;

    });

}