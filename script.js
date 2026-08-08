// -----------------------------
// Greenhorn-to-Nexaris Mock Interviewer
// script.js
// -----------------------------

// Welcome message
window.onload = function () {
    console.log("Greenhorn-to-Nexaris Mock Interviewer Loaded Successfully");
};

// Registration Form Validation
function validateRegister() {

    let name = document.getElementById("name").value.trim();
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();

    if (name === "" || email === "" || password === "") {
        alert("Please fill all fields.");
        return false;
    }

    if (password.length < 6) {
        alert("Password must contain at least 6 characters.");
        return false;
    }

    return true;
}

// Login Form Validation
function validateLogin() {

    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();

    if (email === "" || password === "") {
        alert("Please enter your email and password.");
        return false;
    }

    return true;
}

// Confirm Logout
function confirmLogout() {

    return confirm("Are you sure you want to logout?");
}

// Quiz Timer (10 Minutes)
let time = 600;

function startTimer() {

    const timer = document.getElementById("timer");

    if (!timer) return;

    let countdown = setInterval(function () {

        let minutes = Math.floor(time / 60);
        let seconds = time % 60;

        timer.innerHTML =
            "Time Left: " +
            minutes +
            ":" +
            (seconds < 10 ? "0" + seconds : seconds);

        time--;

        if (time < 0) {
            clearInterval(countdown);
            alert("Time is over! Your answers will be submitted.");
            document.getElementById("quizForm").submit();
        }

    }, 1000);
}