#!/bin/bash

echo "🔧 Generating Firebase configuration..."

# Check if required environment variables are set
if [ -z "$FIREBASE_API_KEY" ]; then
  echo "❌ ERROR: FIREBASE_API_KEY environment variable is not set!"
  echo "Please set all required Firebase environment variables in Vercel dashboard."
  exit 1
fi

# Use environment variables
API_KEY="${FIREBASE_API_KEY}"
AUTH_DOMAIN="${FIREBASE_AUTH_DOMAIN}"
PROJECT_ID="${FIREBASE_PROJECT_ID}"
STORAGE_BUCKET="${FIREBASE_STORAGE_BUCKET}"
SENDER_ID="${FIREBASE_MESSAGING_SENDER_ID}"
APP_ID="${FIREBASE_APP_ID}"
MEASUREMENT_ID="${FIREBASE_MEASUREMENT_ID}"

cat > frontend/firebase-config.js << EOF
// Firebase Configuration - Auto-generated from environment variables
// Generated at build time - DO NOT EDIT

const firebaseConfig = {
  apiKey: "${API_KEY}",
  authDomain: "${AUTH_DOMAIN}",
  projectId: "${PROJECT_ID}",
  storageBucket: "${STORAGE_BUCKET}",
  messagingSenderId: "${SENDER_ID}",
  appId: "${APP_ID}",
  measurementId: "${MEASUREMENT_ID}"
};

// Export for use in other files
window.FIREBASE_CONFIG = firebaseConfig;
EOF

echo "✅ Firebase config generated successfully!"
echo "   Using API Key: ${API_KEY:0:20}..."
