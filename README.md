# CHEM•VIZ — Chemical Equipment Parameter Visualizer

<div align="center">

**Hybrid Web + Desktop Application** | FOSSEE Intern Screening Task

[![FOSSEE](https://img.shields.io/badge/FOSSEE-IIT%20Bombay-blue?style=for-the-badge)](https://fossee.in/)
[![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18.x-61dafb?style=for-the-badge&logo=react)](https://react.dev/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-41cd52?style=for-the-badge)](https://www.riverbankcomputing.com/software/pyqt/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

A hybrid application that allows users to upload CSV files containing chemical equipment parameters, parse and analyze data via a Django REST backend, and visualize results through both a **React Web frontend** and a **PyQt5 Desktop application**.

[🌐 Live Demo](https://fossee-project-eta.vercel.app) · [📥 Download Desktop App](https://github.com/dikshadamahe/fossee-project/releases/latest) · [📡 API Docs](#api-endpoints)

</div>

---

## 🚀 Live Demo & Downloads

| Platform | Link | Status |
|----------|------|--------|
| **🌐 Web App** | [fossee-project-eta.vercel.app](https://fossee-project-eta.vercel.app) | ![Vercel](https://img.shields.io/badge/Vercel-Live-success) |
| **📡 Backend API** | [dikshadamahe.pythonanywhere.com/api/](https://dikshadamahe.pythonanywhere.com/api/) | ![PythonAnywhere](https://img.shields.io/badge/PythonAnywhere-Live-success) |
| **💻 Desktop App** | [Download ChemViz.exe](https://github.com/dikshadamahe/fossee-project/releases/latest) | ![Windows](https://img.shields.io/badge/Windows-x64-blue) |

> **Quick Start:** Visit the web app → Register an account → Upload `sample_equipment_data.csv` → Explore charts, summaries, and PDF export!

---

## ✨ Features

| Feature | Web | Desktop | Description |
|---------|:---:|:-------:|-------------|
| **CSV Upload** | ✅ | ✅ | Drag-and-drop + file dialog upload |
| **Data Analytics** | ✅ | ✅ | Total count, averages, equipment type distribution |
| **Visualizations** | ✅ | ✅ | Bar charts, line charts, doughnut charts |
| **History Management** | ✅ | ✅ | Last 5 uploads synced across platforms (requires login) |
| **PDF Export** | ✅ | ✅ | A4 formatted report with KPIs, charts, FOSSEE branding |
| **Authentication** | ✅ | ✅ | Token-based login with data synced across web & desktop |
| **Data Tables** | ✅ | ✅ | Sortable, filterable equipment table |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend (Web)** | React 18 + Vite + Chart.js + TailwindCSS | Modern SPA with data visualization |
| **Frontend (Desktop)** | PyQt5 + Matplotlib | Native Windows application |
| **Backend** | Django 5 + Django REST Framework | RESTful API server |
| **Data Processing** | Pandas + NumPy | CSV parsing & statistical analysis |
| **Database** | SQLite | Lightweight data storage |
| **PDF Generation** | jsPDF (Web) / ReportLab (Desktop) | Export analysis reports |
| **Authentication** | DRF Token Auth | Secure user sessions |
| **Deployment** | Vercel (Web) + PythonAnywhere (API) | Cloud hosting |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CHEM•VIZ                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐         ┌──────────────────────────┐     │
│  │   React Web App  │ ◄─────► │                          │     │
│  │   (Vercel)       │  REST   │   Django REST Backend    │     │
│  └──────────────────┘         │   (PythonAnywhere)       │     │
│                               │                          │     │
│  ┌──────────────────┐         │  • SQLite Database       │     │
│  │  PyQt5 Desktop   │ ◄─────► │  • Pandas Analytics      │     │
│  │   (.exe)         │  REST   │  • Token Authentication  │     │
│  └──────────────────┘         └──────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

Both frontends connect to the **same Django backend API** — your data syncs between web and desktop!

---

## 📦 Quick Start

### Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.12+ | [python.org](https://www.python.org/downloads/) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org/) |
| Git | 2.x | [git-scm.com](https://git-scm.com/) |

### 1️⃣ Clone Repository

```bash
git clone https://github.com/dikshadamahe/fossee-project.git
cd fossee-project
```

### 2️⃣ Start Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

🟢 API running at **http://localhost:8000/api/**

### 3️⃣ Start Web Frontend

```bash
cd web-frontend
npm install
npm run dev
```

🟢 Web app at **http://localhost:5173**

### 4️⃣ Run Desktop App (Optional)

```bash
cd desktop-app
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python main.py
```

### 5️⃣ Test with Sample Data

Upload the included `sample_equipment_data.csv` from the repo root!

---

## 📁 Project Structure

```
fossee-project/
├── 📄 README.md
├── 📊 sample_equipment_data.csv     # Test data (25 records)
│
├── 🐍 backend/                       # Django REST API
│   ├── config/                       # Django settings
│   ├── api/                          # API views, serializers
│   ├── equipment/                    # Data models
│   └── requirements.txt
│
├── ⚛️ web-frontend/                  # React + Vite
│   ├── src/
│   │   ├── pages/                    # Upload, Dashboard, History
│   │   ├── components/               # Charts, Tables, Layout
│   │   └── api/                      # API client
│   └── package.json
│
└── 🖥️ desktop-app/                   # PyQt5 Application
    ├── pages/                        # UI screens
    ├── widgets/                      # Reusable components
    └── requirements.txt
```

---

## 📡 API Endpoints

**Base URL:** `https://dikshadamahe.pythonanywhere.com/api/`

### Datasets

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/upload/` | Optional | Upload CSV file |
| `GET` | `/datasets/` | Required | List user's datasets |
| `GET` | `/datasets/{id}/` | Optional | Get dataset details |
| `DELETE` | `/datasets/{id}/` | Optional | Delete a dataset |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/summary/{id}/` | Get statistics (totals, averages, distribution) |
| `GET` | `/report/{id}/` | Download PDF report |

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register/` | Create new account |
| `POST` | `/auth/login/` | Login → returns token |
| `POST` | `/auth/logout/` | Invalidate token |
| `GET` | `/auth/user/` | Get current user |

---

## 📊 Sample Data Format

The `sample_equipment_data.csv` contains 25 records:

| Column | Type | Example |
|--------|------|---------|
| Equipment Name | String | `Heat Exchanger A1` |
| Type | String | `Pump`, `Reactor`, `Compressor` |
| Flowrate | Float | `0.0 – 420.0` |
| Pressure | Float | `1.0 – 10.5` |
| Temperature | Float | `25.0 – 260.0` |

---

## 🚢 Deployment

| Component | Platform | URL |
|-----------|----------|-----|
| Web Frontend | Vercel | [fossee-project-eta.vercel.app](https://fossee-project-eta.vercel.app) |
| Backend API | PythonAnywhere | [dikshadamahe.pythonanywhere.com](https://dikshadamahe.pythonanywhere.com) |
| Desktop App | GitHub Releases | [Latest Release](https://github.com/dikshadamahe/fossee-project/releases/latest) |

---

## 📜 License & Credits

<div align="center">

**Built for [FOSSEE](https://fossee.in/), IIT Bombay**

Free and Open Source Software for Education

---

Made with ❤️ by [Diksha Damahe](https://github.com/dikshadamahe)

</div>
