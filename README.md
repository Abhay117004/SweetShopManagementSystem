# Mithai Mandir - Sweet Shop Management System

A complete web-based management system for sweet shops, built with Flask and React. This application helps shop owners manage their inventory, customers, and orders efficiently.

**NOTE** - This website is deployed and can be accessed via the followng link https://sweet-shop-management-system-five-umber.vercel.app/
## Features

- **Firebase Authentication** with email/password and Google OAuth
- Secure user login and registration system
- Product catalog with image support
- Customer database management
- Order processing with real-time inventory updates
- Dashboard with business analytics
- Search and filter capabilities
- Responsive design for mobile and desktop

## Technology Stack

**Backend:**
- Python 3.12
- Flask 3.0.0
- SQLAlchemy 3.1.1
- SQLite database
- Flask-CORS 4.0.0

**Frontend:**
- React 18
- JavaScript ES6+
- CSS3
- Axios for API calls

## Project Structure

```
├── backend/
│   ├── app.py              # Flask application
│   ├── database.py         # Database configuration
│   ├── models.py           # Data models
│   ├── routes.py           # API routes
│   └── seed_data.py        # Sample data
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── style.css           # Styles
│   └── app.jsx             # React components
├── api/
│   └── index.py            # Serverless entry point
├── requirements.txt        # Python dependencies
├── vercel.json             # Deployment config
└── README.md
```

## Installation and Setup

### Prerequisites
- Python 3.12+
- Git
- Firebase account (for authentication)

### Quick Start

**Option 1: Use the startup scripts (Recommended)**
```bash
# Windows
start.bat

# Mac/Linux
./start.sh
```

**Option 2: Manual setup**

1. Clone the repository:
```bash
git clone <your-repository-url>
cd mithai-mandir
```

2. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. **Configure Firebase Authentication:**
   - Follow the guide in `FIREBASE_SETUP.md`
   - Update Firebase config in `frontend/login.html`, `frontend/signup.html`, and `frontend/index.html`

5. Run the backend server:
```bash
cd backend
python app.py
```
The API will be available at `http://localhost:5000`

6. Serve the frontend (in a new terminal):
```bash
cd frontend
python -m http.server 8000
```

7. Open your browser and navigate to:
   - Login page: `http://localhost:8000/login.html`
   - Or directly: `http://localhost:8000` (will redirect to login if not authenticated)

The application will automatically create a SQLite database with sample data on first run.

## Usage

The application has four main sections:

**Dashboard**
- View statistics including total products, customers, orders, and revenue
- Quick overview of business metrics

**Sweets Management**
- Add, edit, and delete products
- Upload product images or use image URLs
- Search products by name or category
- Track inventory levels

**Customer Management**
- Maintain customer database
- Store contact information and addresses
- Edit or remove customer records

**Order Management**
- Create new orders by selecting customer and products
- Update order status (pending, completed, cancelled)
- Automatic inventory adjustment on order creation/deletion
- View order history with details

## API Endpoints

### Sweets
- `GET /api/sweets` - Get all sweets
- `GET /api/sweets/:id` - Get sweet by ID
- `POST /api/sweets` - Create new sweet
- `PUT /api/sweets/:id` - Update sweet
- `DELETE /api/sweets/:id` - Delete sweet

### Customers
- `GET /api/customers` - Get all customers
- `GET /api/customers/:id` - Get customer by ID
- `POST /api/customers` - Create new customer
- `PUT /api/customers/:id` - Update customer
- `DELETE /api/customers/:id` - Delete customer

### Orders
- `GET /api/orders` - Get all orders
- `GET /api/orders/:id` - Get order by ID
- `POST /api/orders` - Create new order
- `PUT /api/orders/:id` - Update order status
- `DELETE /api/orders/:id` - Delete order

### Dashboard
- `GET /api/dashboard/stats` - Get statistics
- `GET /api/categories` - Get all categories
- `GET /api/health` - Health check

## Database Schema

**Sweet**
- id, name, description, price, stock, category, image_url, timestamps

**Customer**
- id, name, email (unique), phone, address, created_at

**Order**
- id, customer_id (FK), total_price, status, order_date

**OrderItem**
- id, order_id (FK), sweet_id (FK), quantity, price

## Key Features

**Inventory Management**
- Real-time stock tracking
- Automatic updates on order placement
- Stock restoration on order cancellation
- Visual low-stock indicators

**Order Processing**
- Multi-item order support
- Automatic total calculation
- Stock validation before order confirmation
- Status tracking (pending/completed/cancelled)

**API Design**
- RESTful endpoints
- Blueprint-based route organization
- CORS enabled for cross-origin requests
- JSON response format

## Firebase Setup (Required)

This application uses **Firebase Authentication**. Follow these steps:

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project (or use existing)
3. Add a Web App to your project
4. Go to **Authentication** > **Sign-in method** and enable:
   - Email/Password
   - Google (optional)
5. Copy your Firebase SDK configuration
6. Paste it in `frontend/firebase-config.js` (replace the existing `firebaseConfig` object)

That's it! The same config file is used by all pages.

## Deployment

### GitHub
The application is ready for GitHub deployment:
1. Create a new repository on GitHub
2. Push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-repository-url>
git push -u origin main
```

### Vercel Deployment (Recommended)

This application is optimized for **Vercel** deployment with serverless functions:

**Prerequisites:**

- Vercel account (free tier works)
- PostgreSQL database (Neon, Supabase, or any PostgreSQL provider)
- Firebase project configured

**Deployment Steps:**

1. **Prepare Environment Variables**

   In Vercel Dashboard → Settings → Environment Variables, add:

   ```env
   DATABASE_URL_UNPOOLED=postgresql://username:password@host:port/database
   FIREBASE_API_KEY=your_firebase_api_key
   FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
   FIREBASE_PROJECT_ID=your_project_id
   FIREBASE_STORAGE_BUCKET=your_project_id.appspot.com
   FIREBASE_MESSAGING_SENDER_ID=your_sender_id
   FIREBASE_APP_ID=your_app_id
   FIREBASE_MEASUREMENT_ID=your_measurement_id
   ```

2. **Deploy to Vercel**

   ```bash
   # Install Vercel CLI
   npm i -g vercel

   # Deploy from the Vercel folder
   cd Vercel
   vercel
   ```

   Or connect your GitHub repository in Vercel Dashboard for automatic deployments.

3. **Configure Root Directory**

   - In Vercel Dashboard → Settings → General
   - Set Root Directory to `Vercel`
   - Or use the root `vercel.json` file which handles this automatically

4. **Update Firebase Console**

   - Go to Firebase Console → Authentication → Settings
   - Add your Vercel domain to Authorized domains (e.g., `your-app.vercel.app`)

**Project Structure for Vercel:**

```text
Vercel/
├── api/
│   └── index.py         # Serverless Flask API (@vercel/python)
├── frontend/
│   ├── index.html       # Main app
│   ├── login.html       # Login page
│   ├── signup.html      # Signup page
│   ├── forgot-password.html
│   ├── app.jsx          # React components
│   ├── style.css
│   ├── auth.css
│   └── firebase-config.js
├── vercel.json          # Deployment configuration
└── requirements.txt     # Python dependencies
```

**Key Features of Vercel Deployment:**

- ✅ Serverless Flask backend with PostgreSQL
- ✅ Static frontend hosting with CDN
- ✅ Automatic HTTPS
- ✅ Environment variable management
- ✅ Automatic deployments on Git push
- ✅ Zero-downtime deployments
- ✅ Global edge network

**Database Setup:**

- Use Neon, Supabase, or any PostgreSQL provider
- Tables are created automatically on first deployment
- Copy the connection string and add it to Vercel environment variables as `DATABASE_URL_UNPOOLED`

**Live Demo:**

<https://sweet-shop-management-system-five-umber.vercel.app/>

### Other Platforms

The backend can also be deployed as a standard Flask application:

1. Deploy the backend to Heroku, Railway, Render, etc.
2. Update the API_URL in `frontend/app.jsx`
3. Deploy frontend to Netlify or Firebase Hosting
4. Update CORS settings in backend if needed

**Important:** Remember to update Firebase configuration with your production domain in the Firebase Console under Authentication → Settings → Authorized domains.

