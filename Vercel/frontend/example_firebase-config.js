// EXAMPLE Firebase Configuration
// Copy this file to firebase-config.js and replace with your actual values
// OR set these as environment variables in your deployment platform

const firebaseConfig = {
  apiKey: "YOUR_FIREBASE_API_KEY",
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT.firebasestorage.app",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID",
  measurementId: "YOUR_MEASUREMENT_ID"
};

// Export for use in other files
window.FIREBASE_CONFIG = firebaseConfig;
