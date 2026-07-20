// Load user profile on page load
document.addEventListener('DOMContentLoaded', async () => {
    // Check if user is authenticated
    if (!isAuthenticated()) {
        window.location.href = "login.html";
        return;
    }

    try {
        const profile = await APIClient.getUserProfile();
        document.getElementById("fullName").textContent = `${profile.first_name} ${profile.last_name}` || "Not available";
        document.getElementById("email").textContent = profile.email || "Not available";
        document.getElementById("username").textContent = profile.email || "Not available"; // Using email as username
    } catch (error) {
        console.error("Failed to load profile:", error);
        document.getElementById("fullName").textContent = "Not available";
        document.getElementById("email").textContent = "Not available";
        document.getElementById("username").textContent = "Not available";
    }
});

// Logout handler
function logout() {
    APIClient.logout();
    window.location.href = "login.html";
}
