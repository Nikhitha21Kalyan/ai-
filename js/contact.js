document.getElementById("contactForm").addEventListener("submit", function(e){

    e.preventDefault();

    alert("Your message has been submitted successfully.");

    document.getElementById("contactForm").reset();

});