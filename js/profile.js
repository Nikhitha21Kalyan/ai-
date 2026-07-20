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

firebase.auth().onAuthStateChanged((user) => {
    if (!user) {
        window.location.href = "login.html";
        return;
    }

    db.collection("users").doc(user.uid).get().then((doc) => {
        if (doc.exists) {
            const profile = doc.data();
            document.getElementById("fullName").textContent = profile.fullName || "Not available";
            document.getElementById("email").textContent = profile.email || "Not available";
            document.getElementById("username").textContent = profile.username || "Not available";
        }
    }).catch(() => {
        document.getElementById("fullName").textContent = "Not available";
        document.getElementById("email").textContent = "Not available";
        document.getElementById("username").textContent = "Not available";
    });
});
