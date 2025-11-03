Mithai Mandir: A Full-Stack Confectionery Management SystemThis document provides a comprehensive technical overview of the Mithai Mandir system, a full-stack web application architected for the meticulous management of a confectionery enterprise's inventory, clientele data, and order-processing workflows. The system is implemented utilizing a Flask-based server-side component and a React-based client-side interface (loaded via Content Delivery Network).Access the Live Deployment🌟 Core System FeaturesFirebase Authentication: Integration of a secure user authentication subsystem, facilitating login and registration via email/password credentials and Google OAuth.Product (Sweets) Management: Comprehensive support for all CRUD (Create, Read, Update, Delete) operations pertaining to product data, inclusive of image URL support.Clientele Management: Maintenance of a complete, persistent database repository for customer information.Order Management: A workflow for the creation, monitoring, and status updating of transactional orders.Inventory Control: An automated mechanism for the dynamic adjustment of stock levels, correlating directly with order creation and cancellation events.Analytical Dashboard: A high-level interface presenting key performance indicators and aggregate metrics, such as total sales, customer counts, and product quantities.Responsive Design: The user interface is implemented utilizing responsive design principles to ensure functional parity and visual integrity across desktop and mobile platforms.🛠️ Technological StackThe system's implementation is founded upon the following technological components:DomainConstituent TechnologiesBackendPython 3.12, Flask 3.0, SQLAlchemy 3.1, SQLite (local), PostgreSQL (prod)FrontendReact 18 (via CDN), JSX (transpiled by Babel), HTML5, CSS3, AxiosAuth & DeployFirebase Authentication, Vercel🚀 System Setup and Deployment ProceduresThe application supports two primary execution modes: local development and production deployment via Vercel.1. Firebase Prerequisite (Mandatory)Utilization of this application is contingent upon the pre-configuration of Firebase Authentication.Navigation to the Firebase Console is required, followed by the creation of a new project.A new Web App must be provisioned within the project.Within the Authentication > Sign-in method section, the following methodologies must be enabled:Email/PasswordGoogle (Optional)The firebaseConfig object must be extracted from the Web App's configuration settings.The file frontend/example_firebase-config.js is to be located and renamed to frontend/firebase-config.js.This configuration object must be inserted into both of the following file locations, superseding any placeholder data:frontend/firebase-config.js (designated for local development)Vercel/frontend/firebase-config.js (designated for production deployment)2. Local Development EnvironmentExecution within a local environment necessitates the concurrent operation of two distinct server processes.Process 1: Backend Server Initiation (API)# 1. The repository must be cloned
git clone [https://github.com/Abhay117004/SweetShopManagementSystem.git](https://github.com/Abhay117004/SweetShopManagementSystem.git)
cd SweetShopManagementSystem

# 2. A Python virtual environment is to be created and activated
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 3. All requisite Python dependencies must be installed from the root directory
pip install -r requirements.txt

# 4. The Flask server process is to be initiated from the 'backend' directory.
# This action will also provision the 'app.db' SQLite database file within said directory.
cd backend
python app.py

# ✅ The backend service will subsequently be available at http://localhost:5000



Process 2: Frontend Server Initiation# 1. From a new terminal instance, navigate to the project's root directory
cd SweetShopManagementSystem

# 2. Transition to the primary frontend directory
cd frontend

# 3. A static file server must be initiated
python -m http.server 8000

# ✅ The frontend application will subsequently be accessible at http://localhost:8000



Upon completion of these steps, the application can be accessed via a web browser at http://localhost:8000.3. Production Deployment (Vercel)The project is architected for production deployment from the Vercel directory.A fork of the repository must be created under the deploying entity's GitHub account.A PostgreSQL database instance is required. This may be provisioned from a cloud database provider (e.g., Neon, Supabase). The PostgreSQL Connection String must be obtained.The Vercel deployment procedure is as follows:Log in to the Vercel dashboard and select Add New... > Project.Import the previously forked GitHub repository.Crucial Step: Within the Vercel project settings, the Root Directory must be explicitly set to Vercel. The vercel.json file in the repository's root is also configured to facilitate this.Navigate to the Environment Variables section and define the following:DATABASE_URL_UNPOOLED: The acquired PostgreSQL connection string.All FIREBASE_... configuration keys (as found in firebase-config.js).FIREBASE_API_KEY=your_api_key
FIREBASE_AUTH_DOMAIN=your_auth_domain
FIREBASE_PROJECT_ID=your_project_id
# ...and so forth for all associated keys



Initiate the deployment by selecting Deploy.Final Configuration: Navigate to the Firebase Console > Authentication > Settings > Authorized domains and append the Vercel application's assigned URL (e.g., mithai-mandir.vercel.app) to the list.📁 Repository Directory StructureThe repository employs a structured layout, including a dedicated Vercel directory for deployment, which exists in parallel with the primary development directories. This monorepo-style structure separates local development concerns from production-specific configurations..
├── backend/            # <-- LOCAL: Flask backend logic
│   ├── app.py          # Main Flask application (development)
│   ├── database.py     # SQLAlchemy configuration (local SQLite)
│   ├── models.py       # ORM data models
│   ├── routes.py       # API route definitions
│   └── seed_data.py    # Initial data seeding script
├── frontend/           # <-- LOCAL: Frontend files
│   ├── app.jsx         # React component definitions
│   ├── auth.css        # Authentication page stylesheets
│   ├── example_firebase-config.js # Template
│   ├── firebase-config.js # Firebase setup (local)
│   ├── forgot-password.html
│   ├── index.html      # Main HTML (React root)
│   ├── login.html
│   ├── signup.html
│   └── style.css       # Main stylesheets
├── venv/               # (Virtual environment, ignored)
├── Vercel/             # <-- DEPLOYMENT ROOT (Designated in Vercel settings)
│   ├── api/
│   │   └── index.py    # Vercel Serverless Function entry point. This file 
│   │                   # imports the Flask app from the `backend/` directory
│   │                   # and exposes it as a serverless function.
│   ├── frontend/       # A production-ready copy of the frontend.
│   │                   # Vercel serves these static files directly.
│   │   ├── app.jsx
│   │   ├── auth.css
│   │   ├── firebase-config.js
│   │   ├── forgot-password.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   └── style.css
│   ├── .gitignore      # Ignores files specific to Vercel builds.
│   ├── requirements.txt # Production-specific Python dependencies 
│   │                    # (e.g., psycopg2-binary for PostgreSQL).
│   └── vercel.json      # Vercel-specific configuration, defining build
│                        # processes, rewrite rules (e.g., /api -> index.py),
│                        # and static output directories.
├── .gitattributes      # Defines file attributes for Git.
├── .gitignore          # Root-level ignore file (e.g., venv, app.db, .pyc)
├── README.md           # This document.
├── requirements.txt    # Local development Python dependencies.
└── vercel.json         # Root Vercel configuration file. Its primary
                        # function is to instruct the Vercel platform
                        # to utilize the `Vercel/` directory as the
                        # project's root for all build and deployment
                        # processes.


⚙️ Technical DetailsFurther technical specifications are encapsulated in the sections below.<details><summary><b>API Endpoint Specification</b></summary>SweetsGET /api/sweets - Retrieves all 'sweet' entities.GET /api/sweets/:id - Retrieves a singular 'sweet' entity by its unique identifier.POST /api/sweets - Creates a new 'sweet' entity.PUT /api/sweets/:id - Updates an existing 'sweet' entity.DELETE /api/sweets/:id - Deletes a 'sweet' entity.CustomersGET /api/customers - Retrieves all 'customer' entities.GET /api/customers/:id - Retrieves a singular 'customer' entity by its unique identifier.POST /api/customers - Creates a new 'customer' entity.PUT /api/customers/:id - Updates an existing 'customer' entity.DELETE /api/customers/:id - Deletes a 'customer' entity.OrdersGET /api/orders - Retrieves all 'order' entities.GET /api/orders/:id - Retrieves a singular 'order' entity by its unique identifier.POST /api/orders - Creates a new 'order' entity.PUT /api/orders/:id - Updates the status of an existing 'order'.DELETE /api/orders/:id - DeJletes an 'order' entity.DashboardGET /api/dashboard/stats - Retrieves aggregated statistical data.GET /api/categories - Retrieves all product categories.GET /api/health - Provides an API health check endpoint.</details><details><summary><b>View Database Schema</b></summary>Sweetid, name, description, price, stock, category, image_url, timestampsCustomerid, name, email (unique), phone, address, created_atOrderid, customer_id (FK), total_price, status, order_dateOrderItemid, order_S_id (FK), sweet_id (FK), quantity, price</details>
