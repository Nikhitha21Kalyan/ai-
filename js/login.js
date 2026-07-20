const firebaseConfig = {
    apiKey: "AIzaSyBOQjqA6jSEhgEh0gxBhO1QD3oQVx5y1zs",
    authDomain: "ai-helath.firebaseapp.com",
    projectId: "ai-helath",
    storageBucket: "ai-helath.firebasestorage.app",
    messagingSenderId: "522555254932",
    appId: "1:522555254932:web:9185b3c2e34a0d23feec81",
    measurementId: "G-HE9WH0YMZM"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.firestore();

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

loginForm.classList.add("active");

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

loginForm.onsubmit = function(e){
    e.preventDefault();

    const emailValue = loginUsername.value.trim();
    const passwordValue = loginPassword.value.trim();

    if (!emailValue || !passwordValue) {
        alert("Please enter your email and password.");
        return;
    }

    auth.signInWithEmailAndPassword(emailValue, passwordValue)
        .then((userCredential) => {
            const user = userCredential.user;
            localStorage.setItem("userProfile", JSON.stringify({
                uid: user.uid,
                email: user.email
            }));
            alert("Login Successful");
            window.location.href = "dashboard.html";
        })
        .catch((error) => {
            alert(error.message || "Login failed");
        });
};

signupForm.onsubmit = function(e){
    e.preventDefault();

    const fullNameValue = fullName.value.trim();
    const emailValue = email.value.trim();
    const usernameValue = signupUsername.value.trim();
    const passwordValue = signupPassword.value.trim();

    if (!fullNameValue || !emailValue || !usernameValue || !passwordValue) {
        alert("Please fill in all fields.");
        return;
    }

    auth.createUserWithEmailAndPassword(emailValue, passwordValue)
        .then((userCredential) => {
            const user = userCredential.user;
            return db.collection("users").doc(user.uid).set({
                fullName: fullNameValue,
                email: emailValue,
                username: usernameValue
            });
        })
        .then(() => {
            localStorage.setItem("userProfile", JSON.stringify({
                fullName: fullNameValue,
                email: emailValue,
                username: usernameValue
            }));

            alert("Account Created Successfully");
            signupBtn.classList.remove("active");
            loginBtn.classList.add("active");
            signupForm.classList.remove("active");
            loginForm.classList.add("active");
            window.location.href = "profile.html";
        })
        .catch((error) => {
            if (error.code === "auth/email-already-in-use") {
                alert("This email is already registered. Please log in instead.");
                signupBtn.classList.remove("active");
                loginBtn.classList.add("active");
                signupForm.classList.remove("active");
                loginForm.classList.add("active");
                loginUsername.value = emailValue;
                loginPassword.focus();
            } else {
                alert(error.message || "Account creation failed");
            }
        });
};