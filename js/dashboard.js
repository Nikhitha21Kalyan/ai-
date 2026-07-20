const refreshBtn = document.getElementById("refreshBtn");
const claimsEl = document.getElementById("claims");
const fraudEl = document.getElementById("fraud");
const safeEl = document.getElementById("safe");
const accuracyEl = document.getElementById("accuracy");
const dashboardMessage = document.getElementById("dashboardMessage");

refreshBtn.addEventListener("click", function () {
    claimsEl.textContent = "0";
    fraudEl.textContent = "0";
    safeEl.textContent = "0";
    accuracyEl.textContent = "Pending";

    if (dashboardMessage) {
        dashboardMessage.textContent = "No fresh data available yet. Upload a claims file to begin analysis.";
    }
});