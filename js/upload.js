// Check authentication on page load
document.addEventListener('DOMContentLoaded', () => {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return;
    }
});

const chooseBtn = document.getElementById("chooseBtn");
const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const detectBtn = document.getElementById("detectBtn");

chooseBtn.addEventListener("click", function () {
    fileInput.click();
});

fileInput.addEventListener("change", function () {
    if(fileInput.files.length > 0){
        fileName.innerHTML = fileInput.files[0].name;
    } else {
        fileName.innerHTML = "No file selected";
    }
});

detectBtn.addEventListener("click", async function(){
    if(fileInput.files.length == 0){
        alert("Please upload a CSV file first.");
        return;
    }

    try {
        const file = fileInput.files[0];
        
        // Read and parse CSV file
        const text = await file.text();
        const lines = text.split('\n');
        const headers = lines[0].split(',');
        
        // Parse CSV data
        const records = [];
        for (let i = 1; i < lines.length; i++) {
            if (lines[i].trim()) {
                const values = lines[i].split(',');
                const record = {};
                headers.forEach((header, index) => {
                    record[header.trim()] = values[index].trim();
                });
                records.push(record);
            }
        }

        // Store records in backend
        for (const record of records) {
            await APIClient.createHealthRecord('upload', {
                claim_data: record,
                file_name: file.name
            }, file.name);
        }

        alert("Dataset uploaded successfully!\nAI Fraud Detection Started...");
        window.location.href = "results.html";
    } catch (error) {
        console.error("Upload error:", error);
        alert("Error uploading file: " + (error.message || "Unknown error"));
    }
});