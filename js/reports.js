// Check authentication on page load
document.addEventListener('DOMContentLoaded', () => {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return;
    }
    loadReports();
});

async function loadReports() {
    try {
        const response = await APIClient.getReports();
        
        if (response.reports && response.reports.length > 0) {
            // Update summary cards
            document.getElementById('totalClaims').textContent = response.reports.length;
            
            // Calculate fraud vs safe
            let fraudCount = 0, safeCount = 0;
            response.reports.forEach(report => {
                if (report.data && report.data.diagnosis && report.data.diagnosis.includes('fraud')) {
                    fraudCount++;
                } else {
                    safeCount++;
                }
            });
            
            document.getElementById('fraudClaims').textContent = fraudCount;
            document.getElementById('safeClaims').textContent = safeCount;
            
            const accuracy = response.reports.length > 0 
                ? ((safeCount / response.reports.length) * 100).toFixed(1) 
                : '0.0';
            document.getElementById('accuracy').textContent = accuracy + '%';
            
            // Combine all reports into one
            const reportTextarea = document.getElementById('report');
            let reportText = `Medical Reports Summary\n`;
            reportText += `Generated: ${new Date().toLocaleString()}\n`;
            reportText += `Total Reports: ${response.reports.length}\n\n`;
            reportText += `---\n\n`;
            
            response.reports.forEach((report, index) => {
                reportText += `Report ${index + 1}\n`;
                reportText += `Title: ${report.data.title}\n`;
                reportText += `Doctor: ${report.data.doctor || 'N/A'}\n`;
                reportText += `Diagnosis: ${report.data.diagnosis || 'N/A'}\n`;
                reportText += `Content: ${report.data.content}\n`;
                reportText += `---\n\n`;
            });
            
            reportTextarea.value = reportText;
        } else {
            document.getElementById('report').value = 'No reports available yet. Create reports to view them here.';
        }
    } catch (error) {
        console.error("Error loading reports:", error);
        document.getElementById('report').value = 'Error loading reports. Please try again.';
    }
}

document.getElementById("downloadBtn").addEventListener("click", function(){
    const reportText = document.getElementById('report').value;
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(reportText));
    element.setAttribute('download', 'fraud-detection-report.txt');
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
});

document.getElementById("dashboardBtn").addEventListener("click", function(){
    window.location.href="dashboard.html";
});