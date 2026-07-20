// Check authentication on page load
document.addEventListener('DOMContentLoaded', () => {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return;
    }
    loadDashboardData();
});

const refreshBtn = document.getElementById("refreshBtn");
const claimsEl = document.getElementById("claims");
const fraudEl = document.getElementById("fraud");
const safeEl = document.getElementById("safe");
const accuracyEl = document.getElementById("accuracy");
const dashboardMessage = document.getElementById("dashboardMessage");

async function loadDashboardData() {
    try {
        const records = await APIClient.getHealthRecords();
        const fraudRecords = records.records.filter(r => r.data && r.data.is_fraud);
        const safeRecords = records.records.filter(r => r.data && !r.data.is_fraud);
        
        const total = records.records.length;
        const fraud = fraudRecords.length;
        const safe = safeRecords.length;
        const accuracy = total > 0 ? ((safe / total) * 100).toFixed(1) : "0.0";

        claimsEl.textContent = total;
        fraudEl.textContent = fraud;
        safeEl.textContent = safe;
        accuracyEl.textContent = accuracy + "%";

        if (total === 0 && dashboardMessage) {
            dashboardMessage.textContent = "Upload claims to begin generating real fraud analysis results.";
        } else if (dashboardMessage) {
            dashboardMessage.style.display = "none";
        }
    } catch (error) {
        console.error("Error loading dashboard data:", error);
        claimsEl.textContent = "0";
        fraudEl.textContent = "0";
        safeEl.textContent = "0";
        accuracyEl.textContent = "Pending";
    }
}

refreshBtn.addEventListener("click", function () {
    loadDashboardData();
});