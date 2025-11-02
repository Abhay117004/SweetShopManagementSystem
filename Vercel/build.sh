echo "🔧 Generating Firebase configuration..."

if [ -z "$FIREBASE_API_KEY" ]; then
  echo "⚠️  Warning: FIREBASE_API_KEY not set, using default config"
  echo "✅ Build complete (using existing firebase-config.js)"
  exit 0
fi

cat > frontend/firebase-config.js << EOF
// Firebase Configuration - Auto-generated from environment variables
// Generated at build time - DO NOT EDIT

const firebaseConfig = {
  apiKey: "${FIREBASE_API_KEY}",
  authDomain: "${FIREBASE_AUTH_DOMAIN}",
  projectId: "${FIREBASE_PROJECT_ID}",
  storageBucket: "${FIREBASE_STORAGE_BUCKET}",
  messagingSenderId: "${FIREBASE_MESSAGING_SENDER_ID}",
  appId: "${FIREBASE_APP_ID}",
  measurementId: "${FIREBASE_MEASUREMENT_ID}"
};

// Export for use in other files
window.FIREBASE_CONFIG = firebaseConfig;
EOF

echo "✅ Firebase config generated successfully with environment variables"
