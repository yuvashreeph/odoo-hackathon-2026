document.getElementById("loginForm").addEventListener("submit", async function (e) {

    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {

        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const result = await response.json();

        if (response.ok) {

            // Save JWT Token
            localStorage.setItem("token", result.data.token);

            // Save User (Optional)
            localStorage.setItem("user", JSON.stringify(result.data.user));

            // Redirect to dashboard page
            window.location.href = "/dashboard-page";

        } else {

            alert(result.message);

        }

    } catch (err) {

        alert("Unable to connect to server.");

        console.log(err);

    }

});