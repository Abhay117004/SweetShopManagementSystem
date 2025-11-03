# Mithai Mandir: A Full-Stack Confectionery Management System

This document provides a comprehensive technical overview of the Mithai Mandir system — a full-stack web application designed for efficient management of a confectionery enterprise's inventory, clientele data, and order workflows.

The system is implemented using a Flask-based backend and a React-based frontend (loaded via CDN).

---

## Access the Live Deployment

**Live Demo:** <https://sweet-shop-management-system-five-umber.vercel.app/>

---

## Core System Features

### Firebase Authentication

Secure user authentication supporting:

- Email/password login & registration
- Google OAuth integration

### Product (Sweets) Management

Full CRUD (Create, Read, Update, Delete) functionality for sweet/product data, including image URL support.

### Clientele Management

Persistent database for customer information with create, edit, and delete capabilities.

### Order Management

Workflow for creating, tracking, and updating orders with real-time status control.

### Inventory Control

Automatic stock level adjustments when orders are created or cancelled.

### Analytical Dashboard

Dashboard displaying KPIs and summary metrics:

- Total sales
- Customer count
- Product quantities

### Responsive Design

Responsive UI ensuring functional parity and visual consistency across devices.

---

## Technological Stack

| Domain | Technologies Used |
|---------|-------------------|
| Backend | Python 3.12, Flask 3.0, SQLAlchemy 3.1, SQLite (local), PostgreSQL (prod) |
| Frontend | React 18 (via CDN), JSX (Babel), HTML5, CSS3, Axios |
| Auth & Deploy | Firebase Authentication, Vercel |

---

## System Setup and Deployment

The application supports two execution modes:

- Local development
- Production deployment via Vercel

---

### 1. Firebase Prerequisite (Mandatory)

1. Navigate to the Firebase Console and create a new project.
2. Add a Web App under that project.
3. Enable the following sign-in methods under **Authentication → Sign-in method**:
   - Email/Password
   - Google (Optional)
4. Retrieve the `firebaseConfig` object from the Web App settings.
5. Locate and rename `frontend/example_firebase-config.js` to `frontend/firebase-config.js`.
6. Insert the configuration object into:
   - `frontend/firebase-config.js` (local)
   - `Vercel/frontend/firebase-config.js` (production)

---

### 2. Local Development Environment

Run two servers concurrently: one for backend and one for frontend.

#### Process 1: Backend Server (API)

```bash
# 1. Clone the repository
git clone https://github.com/Abhay117004/SweetShopManagementSystem.git
cd SweetShopManagementSystem

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start Flask backend
cd backend
python app.py
```

Backend will be available at: `http://localhost:5000`

#### Process 2: Frontend Server

```bash
# 1. Open a new terminal
cd SweetShopManagementSystem

# 2. Navigate to frontend
cd frontend

# 3. Start a static file server
python -m http.server 8000
```

Frontend will be available at: `http://localhost:8000`

Once both are running, visit: `http://localhost:8000` in your browser.

---

### 3. Production Deployment (Vercel)

1. Fork the repository into your GitHub account.
2. Provision a PostgreSQL database (via Neon, Supabase, or other provider).
3. Obtain the PostgreSQL connection string.
4. In Vercel:
   - Click Add New → Project
   - Import the forked repository
   - Set Root Directory to `Vercel`
   - Add environment variables:
     - `DATABASE_URL_UNPOOLED` (PostgreSQL connection string)
     - All `FIREBASE_...` configuration keys (same as firebase-config.js)

   ```bash
   FIREBASE_API_KEY=your_api_key
   FIREBASE_AUTH_DOMAIN=your_auth_domain
   FIREBASE_PROJECT_ID=your_project_id
   # ...and so forth for all keys
   ```

5. Deploy the project.
6. Add your deployed domain (e.g. `mithai-mandir.vercel.app`) under **Firebase Console → Authentication → Settings → Authorized domains**.

---

## Repository Directory Structure

```text
├── backend/
│   ├── app.py              # Main Flask application
│   ├── database.py         # SQLAlchemy config (SQLite local)
│   ├── models.py           # ORM models
│   ├── routes.py           # API routes
│   └── seed_data.py        # Initial data seeding
│
├── frontend/
│   ├── app.jsx             # React components
│   ├── auth.css            # Auth page styles
│   ├── example_firebase-config.js
│   ├── firebase-config.js  # Firebase setup (local)
│   ├── forgot-password.html
│   ├── index.html          # React root
│   ├── login.html
│   ├── signup.html
│   └── style.css
│
├── venv/                   # Virtual environment (ignored)
│
├── Vercel/
│   ├── api/
│   │   └── index.py        # Vercel Serverless entry (imports Flask app)
│   ├── frontend/           # Production-ready frontend copy
│   │   ├── app.jsx
│   │   ├── auth.css
│   │   ├── firebase-config.js
│   │   ├── forgot-password.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   └── style.css
│   ├── .gitignore
│   ├── requirements.txt    # Production deps (e.g., psycopg2-binary)
│   └── vercel.json         # Vercel config (builds, rewrites, static dirs)
│
├── .gitattributes
├── .gitignore
├── README.md
├── requirements.txt        # Local development dependencies
└── vercel.json             # Root Vercel config (points to /Vercel directory)
```

---

## Technical Details

### API Endpoint Specification

#### Sweets

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sweets` | Retrieve all sweets |
| GET | `/api/sweets/:id` | Retrieve a sweet by ID |
| POST | `/api/sweets` | Create a new sweet |
| PUT | `/api/sweets/:id` | Update a sweet |
| DELETE | `/api/sweets/:id` | Delete a sweet |

#### Customers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/customers` | Retrieve all customers |
| GET | `/api/customers/:id` | Retrieve a customer by ID |
| POST | `/api/customers` | Create a customer |
| PUT | `/api/customers/:id` | Update a customer |
| DELETE | `/api/customers/:id` | Delete a customer |

#### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders` | Retrieve all orders |
| GET | `/api/orders/:id` | Retrieve an order by ID |
| POST | `/api/orders` | Create a new order |
| PUT | `/api/orders/:id` | Update order status |
| DELETE | `/api/orders/:id` | Delete an order |

#### Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/stats` | Retrieve aggregated statistics |
| GET | `/api/categories` | Retrieve all product categories |
| GET | `/api/health` | API health check |

---

## Database Schema

### Sweet

- id
- name
- description
- price
- stock
- category
- image_url
- timestamps

### Customer

- id
- name
- email (unique)
- phone
- address
- created_at

### Order

- id
- customer_id (FK)
- total_price
- status
- order_date

### OrderItem

- id
- order_id (FK)
- sweet_id (FK)
- quantity
- price
