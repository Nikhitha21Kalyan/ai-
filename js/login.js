// Login and Signup Handler
const loginBtn = document.getElementById("loginBtn");
const signupBtn = document.getElementById("signupBtn");

const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");

const loginUsername = document.getElementById("loginUsername");
const loginPassword = document.getElementById("loginPassword");
const fullName = document.getElementById("fullName");
const email = document.getElementById("email");
const signupUsername = document.getElementById("signupUsername");
const signupPassword = document.getElementById("signupPassword");

// Set active form on page load
loginForm.classList.add("active");

// Tab switching
loginBtn.onclick = () => {
    loginForm.classList.add("active");
    signupForm.classList.remove("active");
    loginBtn.classList.add("active");
    signupBtn.classList.remove("active");
};

signupBtn.onclick = () => {
    signupForm.classList.add("active");
    loginForm.classList.remove("active");
    signupBtn.classList.add("active");
    loginBtn.classList.remove("active");
};

// Login Form Handler
loginForm.onsubmit = async function(e) {
    e.preventDefault();

    const emailValue = loginUsername.value.trim();
    const passwordValue = loginPassword.value.trim();

    if (!emailValue || !passwordValue) {
        alert("Please enter your email and password.");
        return;
    }

    try {
        const response = await APIClient.login(emailValue, passwordValue);
        alert("Login Successful");
        window.location.href = "dashboard.html";
    } catch (error) {
        console.error("Login error:", error);
        alert(error.message || "Login failed. Please try again.");
    }
};

// Signup Form Handler
signupForm.onsubmit = async function(e) {
    e.preventDefault();

    const fullNameValue = fullName.value.trim();
    const emailValue = email.value.trim();
    const usernameValue = signupUsername.value.trim();
    const passwordValue = signupPassword.value.trim();

    if (!fullNameValue || !emailValue || !usernameValue || !passwordValue) {
        alert("Please fill in all fields.");
        return;
    }

    if (passwordValue.length < 6) {
        alert("Password must be at least 6 characters long.");
        return;
    }

    try {
        // Extract first and last name from fullName
        const nameParts = fullNameValue.split(' ');
        const firstName = nameParts[0];
        const lastName = nameParts.slice(1).join(' ') || nameParts[0];

        const response = await APIClient.register(
            emailValue,
            passwordValue,
            firstName,
            lastName
        );

        alert("Account created successfully! Please login.");
        
        // Switch to login form
        loginForm.classList.add("active");
        signupForm.classList.remove("active");
        loginBtn.classList.add("active");
        signupBtn.classList.remove("active");

        // Clear form
        signupForm.reset();
    } catch (error) {
        console.error("Signup error:", error);
        alert(error.message || "Signup failed. Please try again.");
    }
};