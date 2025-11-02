// Firebase Configuration
// INSTRUCTIONS: 
// 1. Rename this file to firebase-config.js
// 2. Go to https://console.firebase.google.com/
// 3. Create a new project or select an existing one
// 4. Go to Project Settings > Your apps > Add app > Web
// 5. Copy the firebaseConfig object and paste it below
// 6. Enable Authentication > Sign-in method > Email/Password

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID",
  measurementId: "YOUR_MEASUREMENT_ID"
};

// Export for use in other files
window.FIREBASE_CONFIG = firebaseConfig;
