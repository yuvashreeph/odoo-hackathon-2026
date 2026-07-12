window.onload = loadDrivers;

async function loadDrivers() {

    const token = localStorage.getItem("token");

    const response = await fetch("/drivers", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    const result = await response.json();

    let table = document.getElementById("driversTable");

    table.innerHTML = "";

    result.data.forEach(driver => {

        table.innerHTML += `
        <tr>
            <td>${driver.name}</td>
            <td>${driver.licenseNumber}</td>
            <td>${driver.licenseCategory}</td>
            <td>${driver.phone}</td>
            <td>${driver.safetyScore}</td>
            <td>${driver.status}</td>
        </tr>
        `;
    });

}