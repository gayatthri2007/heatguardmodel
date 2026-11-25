// src/firebase.js

import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";

const firebaseConfig = {
  apiKey: "AIzaSyAILmpqTCBExE9Fbquxb9fDhPXlK7WZwBs",
  authDomain: "heatguard-cda13.firebaseapp.com",
  databaseURL: "https://heatguard-cda13-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "heatguard-cda13",
  storageBucket: "heatguard-cda13.firebasestorage.app",
  messagingSenderId: "386071303457",
  appId: "1:386071303457:web:4cecb28c3b42014aa39a60",
  measurementId: "G-W71KLT7FXG"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Get Realtime Database
export const database = getDatabase(app);