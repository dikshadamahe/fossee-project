# CHEM•VIZ — Chemical Equipment Parameter Visualizer

**Hybrid Web + Desktop Application** | FOSSEE Intern Screening Task

A hybrid application that allows users to upload a CSV file containing chemical equipment parameters (Equipment Name, Type, Flowrate, Pressure, Temperature), parses and analyzes the data via a Django REST backend, and displays data tables, charts, and summaries on both a **React Web frontend** and a **PyQt5 Desktop frontend**.

![FOSSEE](https://img.shields.io/badge/FOSSEE-IIT%20Bombay-blue)
![Django](https://img.shields.io/badge/Django-5.0+-092E20)
![React](https://img.shields.io/badge/React-18.x-61dafb)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-41cd52)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57)

---

## Live Demo & Downloads

| Platform | Link |
|----------|------|
| **Web App** | [https://fossee-project-eta.vercel.app](https://fossee-project-eta.vercel.app) |
| **Backend API** | [https://dikshadamahe.pythonanywhere.com/api/](https://dikshadamahe.pythonanywhere.com/api/) |
| **Desktop App** | [Download ChemViz.exe (Windows)](https://github.com/dikshadamahe/fossee-project/releases/latest) |

> **Quick Start:** Visit the web app, register an account, upload `sample_equipment_data.csv`, and explore the charts, summaries, and PDF export.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend (Web) | React.js + Chart.js | Data table + chart visualization |
| Frontend (Desktop) | PyQt5 + Matplotlib | Same visualization in desktop |
| Backend | Python Django + Django REST Framework | Common backend API |
| Data Handling | Pandas | Reading CSV & analytics |
| Database | SQLite | Store last 5 uploaded datasets |
| PDF Generation | jsPDF (Web) + ReportLab (Desktop) | Export analysis reports |
| Authentication | Token-based (DRF Tokens) | Login, Register, Logout |
| Version Control | Git & GitHub | Collaboration & submission |
| Sample Data | `sample_equipment_data.csv` | Provided for testing & demo |

---

## Features Implemented

| # | Feature | Web | Desktop | Details |
|---|---------|-----|---------|---------|
| 1 | **CSV Upload** | Yes | Yes | Drag-and-drop + file dialog upload to Django backend |
| 2 | **Data Summary API** | Yes | Yes | Total count, averages (flowrate, temperature, pressure), equipment type distribution |
| 3 | **Visualization** | Yes (Chart.js) | Yes (Matplotlib) | Equipment Distribution (Bar), Temperature Profile (Line), Pressure Analysis (Bar) |
| 4 | **History Management** | Yes | Yes | Stores last 5 uploaded datasets with summary; sidebar + full history screen |
| 5 | **PDF Report** | Yes (jsPDF) | Yes (ReportLab) | A4 formatted report with KPIs, charts, data table, FOSSEE branding |
| 6 | **Authentication** | Yes | Yes | Token-based login/register/logout with dataset ownership |
| 7 | **Data Tables** | Yes | Yes | Sortable equipment table with status badges, zebra striping |
| 8 | **Sample CSV** | Yes | Yes | `sample_equipment_data.csv` included in repo root (25 records, 7 equipment types) |

---

## Architecture

```
┌──────────────────┐     HTTP/REST     ┌──────────────────┐
│   React Web App  │ ◄───────────────► │  Django Backend   │
│   (Vercel)       │                   │  (PythonAnywhere)  │
└──────────────────┘                   │  SQLite + Pandas  │
                                       └──────────────────┘
┌──────────────────┐     HTTP/REST            ▲
│  PyQt5 Desktop   │ ◄───────────────────────►│
│   (.exe release) │
└──────────────────┘
```

Both frontends connect to the **same Django backend API**.

---

## Setup Instructions

### Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.12+ |
| Node.js | 18+ |
| npm | 9+ |
| Git | 2.x |

### 1. Clone the Repository

```bash
git clone https://github.com/dikshadamahe/fossee-project.git
cd fossee-project
```

### 2. Start the Backend (required first)

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

API is now live at **http://localhost:8000/api/**

> **Optional:** Create a superuser for the Django admin panel:
> ```bash
> python manage.py createsuperuser
> ```
> Then visit http://localhost:8000/admin/

### 3a. Start the Web Frontend (React)

```bash
# From the project root (not backend/)
cd web-frontend
npm install
npm run dev
```

Open **http://localhost:5173**

### 3b. Run the Desktop Application (PyQt5)

```bash
cd desktop-app
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt
python main.py
```

### 4. Test with Sample Data

Upload the included `sample_equipment_data.csv` from the repo root through either the Web or Desktop interface to see charts, KPIs, and data tables.

---

## Project Structure

```
fossee-web/
├── README.md                        # This file
├── sample_equipment_data.csv        # Sample CSV for testing & demo
├── package.json                     # Root project config
│
├── backend/                         # Django REST API Backend
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3                   # SQLite database
│   ├── config/                      # Django project config
│   │   ├── settings.py              # DB, CORS, REST, auth settings
│   │   ├── urls.py                  # Root URL routing
│   │   └── wsgi.py                  # WSGI entry point
│   ├── api/                         # Main API application
│   │   ├── models.py                # Dataset model (CSV metadata + storage)
│   │   ├── serializers.py           # DRF serializers
│   │   ├── views.py                 # Upload, list, summary, analysis endpoints
│   │   ├── auth_views.py            # Login, register, logout endpoints
│   │   ├── authentication.py        # Lenient token auth (anonymous fallback)
│   │   ├── services.py              # Pandas analytics engine
│   │   └── urls.py
│   └── media/                       # Uploaded files storage
│
├── web-frontend/                    # React Web Frontend
│   ├── index.html                   # Web entry point
│   ├── vite.config.js               # Vite configuration
│   ├── package.json                 # React dependencies
│   └── src/
│       ├── App.jsx                  # Main app with routing
│       ├── main.jsx                 # Entry point
│       ├── styles/
│       │   └── index.css            # Global base styles & tokens
│       ├── api/
│       │   └── client.js            # API client (Axios wrapper)
│       ├── context/
│       │   └── AuthContext.jsx      # Auth state management
│       ├── components/
│       │   ├── Layout.jsx           # Header, Sidebar, MainContent
│       │   ├── AuthModal.jsx        # Login/Register modal
│       │   ├── ChartCard.jsx        # Chart.js visualization wrapper
│       │   └── DataTable.jsx        # Equipment data table
│       └── pages/
│           ├── UploadPage.jsx       # File upload with drag-and-drop
│           ├── DashboardPage.jsx    # Analytics dashboard
│           └── HistoryPage.jsx      # Dataset history list
│
└── desktop-app/                     # PyQt5 Desktop Frontend
    ├── main.py                      # Application entry point
    ├── requirements.txt
    ├── api_client.py                # HTTP client for Django API
    ├── assets/                      # Icons and images
    ├── pages/
    │   ├── auth_page.py             # Login/Register screens
    │   ├── upload_page.py           # CSV upload screen
    │   ├── dashboard_page.py        # Analytics dashboard
    │   └── history_page.py          # History list screen
    ├── widgets/
    │   ├── sidebar.py               # Navigation sidebar
    │   └── pdf_report_dialog.py     # PDF generation dialog
    └── styles/
        └── fossee_style.py          # QSS stylesheet & theme
```

---

## API Endpoints

Base URL: **https://dikshadamahe.pythonanywhere.com/api/** (hosted) or **http://localhost:8000/api/** (local)

### Datasets

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/datasets/upload/` | Upload a CSV file |
| GET | `/api/datasets/` | List datasets (last 5) |
| GET | `/api/datasets/{id}/` | Get dataset details |
| DELETE | `/api/datasets/{id}/` | Delete a dataset |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/summary/{id}/` | Summary stats (total count, averages, type distribution) |
| GET | `/api/analysis/{id}/` | Chart data (equipment distribution, temperature, pressure) |
| GET | `/api/history/` | Dataset upload history (last 5) |

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Create new account |
| POST | `/api/auth/login/` | Login → returns auth token |
| POST | `/api/auth/logout/` | Logout → invalidates token |
| GET | `/api/auth/user/` | Get current user info |

Full API documentation: [backend/README.md](backend/README.md)

---

## Sample Data

The repository includes `sample_equipment_data.csv` with 25 records across 7 equipment types:

| Column | Description | Example Values |
|--------|-------------|----------------|
| Equipment Name | Unique equipment identifier | Heat Exchanger A1, Reactor C2 |
| Type | Equipment category | Heat Exchanger, Reactor, Pump, Compressor, Distillation Column, Boiler, Condenser, Storage Tank |
| Flowrate | Flow rate value | 0.0 – 420.0 |
| Pressure | Operating pressure | 1.0 – 10.5 |
| Temperature | Operating temperature | 25.0 – 260.0 |

---

## Licenses & Credits

**FOSSEE Project, IIT Bombay**

Built as part of the [FOSSEE](https://fossee.in/) initiative at the Indian Institute of Technology Bombay.

---

## Deployment Status

### Web Frontend — Vercel
- Auto-deploys from `main` branch.
- Live at [https://fossee-web.vercel.app](https://fossee-web.vercel.app).

### Backend — PythonAnywhere
- Django app hosted at [https://dikshadamahe.pythonanywhere.com](https://dikshadamahe.pythonanywhere.com).
- CORS configured to accept requests from Vercel and Desktop.

### Desktop — GitHub Releases
- Built with **PyInstaller**.
- Download latest `.exe` from [Releases](https://github.com/dikshadamahe/fossee-project/releases/latest).
