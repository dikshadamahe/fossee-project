# Chemical Equipment Parameter Visualizer

**Hybrid Web + Desktop Application**

A hybrid application that allows users to upload CSV files containing chemical equipment parameters (Equipment Name, Type, Flowrate, Pressure, Temperature), parse and analyze data via a Django REST backend, and visualize results through both a React Web frontend and a PyQt5 Desktop application.

![FOSSEE](https://img.shields.io/badge/FOSSEE-IIT%20Bombay-blue)
![Django](https://img.shields.io/badge/Django-5.0+-092E20)
![React](https://img.shields.io/badge/React-18.x-61dafb)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-41cd52)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB)
![Vercel](https://img.shields.io/badge/Deployed-Vercel-black)

---

## Live Demo & Downloads

| Platform | Link |
|----------|------|
| **Web App** | [https://fossee-project-eta.vercel.app](https://fossee-project-eta.vercel.app) |
| **Backend API** | [https://fossee-project-api.vercel.app/api/](https://fossee-project-api.vercel.app/api/) |
| **Desktop App** | [Download Windows EXE](https://github.com/dikshadamahe/fossee-project/releases/latest) |

**Quick Start:**
1. Visit the [Web App](https://fossee-project-eta.vercel.app).
2. Register an account (optional, but required for history sync).
3. Upload `sample_data.csv` from the repo root.
4. View charts, data tables, and download PDF reports.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend (Web) | React.js + Vite + Chart.js | Data table and chart visualization |
| Frontend (Desktop) | PyQt5 + Matplotlib | Same visualization in desktop |
| Backend | Django 5 + Django REST Framework | Common REST API (Vercel serverless) |
| Data Handling | Pandas | CSV parsing and analytics |
| Database | SQLite (`/tmp` on Vercel) | Store uploaded datasets |
| PDF Generation | jsPDF (Web) / ReportLab (Desktop) | Export analysis reports |
| Authentication | Token-based (DRF Tokens) | Login, Register, Logout |

---

## Features

| Feature | Web | Desktop | Details |
|---------|-----|---------|---------|
| CSV Upload | Yes | Yes | Drag-and-drop and file dialog upload |
| Data Summary | Yes | Yes | Total count, averages, type distribution |
| Visualization | Yes | Yes | Bar charts, line charts, doughnut charts |
| History | Yes | Yes | Saved datasets synced across platforms (requires login) |
| PDF Report | Yes | Yes | A4 formatted report with KPIs and charts |
| Authentication | Yes | Yes | Token-based login with data ownership |
| Data Tables | Yes | Yes | Sortable equipment table with status badges |

---

## Architecture

```
+------------------+                +----------------------+
|  React Web App   |<-- REST API -->|   Django Backend     |
|  (Vercel)        |                |   (Vercel)           |
+------------------+                |                      |
                                    |  - SQLite (/tmp)     |
+------------------+                |  - Pandas Analytics  |
|  PyQt5 Desktop   |<-- REST API -->|  - Token Auth        |
|  (.exe)          |                +----------------------+
+------------------+
```

Both frontends connect to the same Django backend API.

---

## Setup Instructions

### Prerequisites

- Python 3.12+
- Node.js 18+
- Git

### 1. Clone Repository

```bash
git clone https://github.com/dikshadamahe/fossee-project.git
cd fossee-project
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

API running at: `http://localhost:8000/api/`

### 3. Web Frontend Setup

```bash
cd web-frontend
npm install
npm run dev
```

Web App running at: `http://localhost:3000`

### 4. Desktop App Setup

```bash
cd desktop-app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

The desktop app connects to the hosted backend at `https://fossee-project-api.vercel.app/api/` by default. No local backend setup is required.

### 5. Build Desktop EXE

```bash
cd desktop-app
pip install pyinstaller
pyinstaller --clean FOSSEE_Visualizer.spec
```

The standalone `.exe` will be generated in `desktop-app/dist/FOSSEE_Visualizer.exe`.

### 6. Test with Sample Data

Upload `sample_data.csv` from the repo root (or `sample_data/equipment_sample.csv`).

---

## Project Structure

```
fossee-project/
├── README.md
├── sample_data.csv
│
├── backend/                    # Django REST API
│   ├── config/                 # Django settings, WSGI
│   ├── api/                    # API views, serializers
│   ├── equipment/              # Data models
│   ├── vercel.json             # Vercel serverless config
│   └── requirements.txt
│
├── web-frontend/               # React + Vite
│   ├── src/
│   │   ├── pages/              # Upload, Dashboard, History
│   │   ├── components/         # Charts, Tables, Layout
│   │   └── api/                # API client
│   └── package.json
│
└── desktop-app/                # PyQt5 Application
    ├── main.py                 # Application entry point
    ├── api_client.py           # REST API client
    ├── FOSSEE_Visualizer.spec  # PyInstaller build config
    ├── assets/                 # Icons and images
    ├── pages/                  # UI screens
    ├── widgets/                # Reusable components
    ├── styles/                 # FOSSEE design system
    └── requirements.txt
```

---

## API Endpoints

Base URL: `https://fossee-project-api.vercel.app/api/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/upload/` | Upload CSV file |
| GET | `/datasets/` | List user's datasets |
| GET | `/datasets/{id}/` | Get dataset details |
| DELETE | `/datasets/{id}/` | Delete a dataset |
| GET | `/summary/{id}/` | Get statistical summary |
| GET | `/report/{id}/` | Download PDF report |
| POST | `/auth/login/` | User login |
| POST | `/auth/register/` | User registration |
| POST | `/auth/logout/` | User logout |
| GET | `/auth/user/` | Current user profile |

---

## Sample Data Format

`sample_data.csv` contains equipment records with these columns:

| Column | Type | Example |
|--------|------|---------|
| Equipment Name | String | Heat Exchanger A1 |
| Type | String | Pump, Reactor, Compressor |
| Flowrate | Float | 0.0 - 420.0 |
| Pressure | Float | 1.0 - 10.5 |
| Temperature | Float | 25.0 - 260.0 |

---

## Deployment

| Component | Platform | URL |
|-----------|----------|-----|
| Web Frontend | Vercel | [https://fossee-project-eta.vercel.app](https://fossee-project-eta.vercel.app) |
| Backend API | Vercel (serverless Django) | [https://fossee-project-api.vercel.app/api/](https://fossee-project-api.vercel.app/api/) |
| Desktop App | GitHub Releases | [Download Windows EXE](https://github.com/dikshadamahe/fossee-project/releases/latest) |

### Web Frontend (Vercel)

- Auto-deploys from `main` on push to `dikshadamahe/fossee-project`.
- Root directory: `web-frontend`.
- Production builds use `https://fossee-project-api.vercel.app` as the API base URL.

### Backend (Vercel)

- Django API deployed as a serverless Python function via `backend/vercel.json`.
- SQLite database stored in `/tmp` (ephemeral per cold start — suitable for demos; data may reset after idle).
- CORS allows the Vercel web frontend and desktop app.

### Desktop (GitHub Releases)

```bash
cd desktop-app
pip install pyinstaller
pyinstaller --clean FOSSEE_Visualizer.spec
```

Output: `desktop-app/dist/FOSSEE_Visualizer.exe`

---

## License

Built for FOSSEE, IIT Bombay.

Free and Open Source Software for Education.

---

**Developed by Diksha Damahe** — [dikshadamahe](https://github.com/dikshadamahe) · dikshadamahe1@gmail.com
