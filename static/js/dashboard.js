window.onload = loadDashboard;

async function loadDashboard() {

    const token = localStorage.getItem("token");

    if (!token) {

        window.location.href = "/";

        return;

    }

    try {

        const response = await fetch("/dashboard", {

            method: "GET",

            headers: {
                "Authorization": "Bearer " + token
            }

        });

        const result = await response.json();

        if (!response.ok) {

            alert(result.msg || result.message);

            localStorage.clear();

            window.location.href = "/";

            return;

        }

        const data = result.data;

        document.getElementById("totalVehicles").innerHTML =
            data.totalVehicles;

        document.getElementById("availableVehicles").innerHTML =
            data.availableVehicles;

        document.getElementById("onTrip").innerHTML =
            data.vehiclesOnTrip;

        document.getElementById("maintenance").innerHTML =
            data.vehiclesInShop;

        console.log(data);

    }

    catch (err) {

        console.log(err);

        alert("Dashboard loading failed.");

    }

}

function logout() {

    localStorage.clear();

    window.location.href = "/";

}