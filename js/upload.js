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

    }else{

        fileName.innerHTML = "No file selected";

    }

});

detectBtn.addEventListener("click", function(){

    if(fileInput.files.length == 0){

        alert("Please upload a CSV file first.");

    }else{

        alert("Dataset uploaded successfully!\nAI Fraud Detection Started...");

        window.location.href = "results.html";

    }

});