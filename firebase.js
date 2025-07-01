// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyApakPCq5s-qySSOroY9a4X85fFC1iTfvA",
  authDomain: "escslas.firebaseapp.com",
  projectId: "escslas",
  storageBucket: "escslas.firebasestorage.app",
  messagingSenderId: "804887685890",
  appId: "1:804887685890:web:af0df71f8dd97ca35df01b",
  measurementId: "G-SBKXC7MTJX"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

