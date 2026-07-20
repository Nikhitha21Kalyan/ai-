// Check authentication on page load
document.addEventListener('DOMContentLoaded', () => {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return;
    }
    loadResults();
});

async function loadResults() {
    try {
        const records = await APIClient.getHealthRecords('upload');
        
        if (records.records && records.records.length > 0) {
            const totalEl = document.getElementById('total');
            const fraudEl = document.getElementById('fraud');
            const safeEl = document.getElementById('safe');
            
            const total = records.records.length;
            const fraudCount = records.records.filter(r => r.data && r.data.is_fraud).length;
            const safeCount = total - fraudCount;
            
            totalEl.textContent = total;
            fraudEl.textContent = fraudCount;
            safeEl.textContent = safeCount;
            
            // Populate table
            const tableBody = document.querySelector('table tbody');
            tableBody.innerHTML = '';
            
            records.records.forEach(record => {
                const row = document.createElement('tr');
                const claimData = record.data.claim_data || {};
                const isFraud = record.data.is_fraud ? 'Fraud' : 'Safe';
                const riskScore = record.data.risk_score || '0.0';
                
                row.innerHTML = `
                    <td>${record._id}</td>
                    <td>${claimData.patient || 'N/A'}</td>
                    <td class="${record.data.is_fraud ? 'fraud' : 'safe'}">${isFraud}</td>
                    <td>${riskScore}</td>
                `;
                tableBody.appendChild(row);
            });
        }
    } catch (error) {
        console.error("Error loading results:", error);
    }
}

document.getElementById("downloadBtn").addEventListener("click", function(){
    const element = document.documentElement;
    const opt = {
        margin: 10,
        filename: 'fraud-detection-results.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { orientation: 'portrait', unit: 'mm', format: 'a4' }
    };
    // html2pdf() is a popular library but not loaded by default
    // For now, use a simple alert
    alert("Download functionality requires additional library. Please use print to PDF instead.");
});

document.getElementById("dashboardBtn").addEventListener("click", function(){
    window.location.href="dashboard.html";
});