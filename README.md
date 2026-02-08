# Chemical Equipment Parameter Visualizer

<p align="center">
  <img src="screenshots/logo.png" alt="FOSSEE Scientific Analytics" width="200"/>
</p>

> **FOSSEE Scientific Analytics Platform** — A full-stack application for analyzing and visualizing chemical equipment parameters from CSV data.

[![Python](https://img.shields.io/badge/Python-3.12.0-3776AB?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.1.4-092E20?logo=django)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-18.3.1-61DAFB?logo=react)](https://react.dev)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15-41CD52?logo=qt)](https://riverbankcomputing.com/software/pyqt/)

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
  - [Backend Setup (Django)](#1-backend-setup-django)
  - [Web Frontend Setup (React)](#2-web-frontend-setup-react)
  - [Desktop App Setup (PyQt5)](#3-desktop-app-setup-pyqt5)
- [Quick Start](#-quick-start)
- [Demo CSV Format](#-demo-csv-format)
- [API Endpoints](#-api-endpoints)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [Design System](#-design-system)
- [License](#-license)

---

## ✨ Features

| Feature | Web | Desktop |
|---------|:---:|:-------:|
| CSV Upload (drag & drop) | ✅ | ✅ |
| Column Auto-Detection | ✅ | ✅ |
| Statistical Summary | ✅ | ✅ |
| Type Distribution Chart | ✅ | ✅ |
| Parameter Line Charts | ✅ | ✅ |
| Dataset History | ✅ | ✅ |
| PDF Report Download | ✅ | ✅ |
| Plain English Insights | ✅ | ✅ |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FOSSEE Platform                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    HTTP/REST    ┌──────────────────────────┐ │
│  │ React 18     │◄───────────────►│  Django 5 + DRF          │ │
│  │ + Chart.js   │    :5173→:8000  │  SQLite / PostgreSQL     │ │
│  │ + Tailwind   │                 │                          │ │
│  └──────────────┘                 └──────────────────────────┘ │
│                                              ▲                  │
│  ┌──────────────┐    HTTP/REST               │                  │
│  │ PyQt5        │◄───────────────────────────┘                  │
│  │ + Matplotlib │    :8000                                      │
│  └──────────────┘                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Prerequisites

### Required Software

| Software | Version | Download |
|----------|---------|----------|
| **Python** | 3.12.0 | [python.org/downloads](https://www.python.org/downloads/release/python-3120/) |
| **Node.js** | 18+ | [nodejs.org](https://nodejs.org/) |
| **npm** | 9+ | Included with Node.js |
| **Git** | Latest | [git-scm.com](https://git-scm.com/) |

### Verify Installation

```bash
# Check Python version (must be 3.12.x)
python3.12 --version
# Output: Python 3.12.0

# Check Node.js version
node --version
# Output: v18.x.x or higher

# Check npm version
npm --version
# Output: 9.x.x or higher
```

### macOS (Homebrew)

```bash
# Install Python 3.12
brew install python@3.12

# Install Node.js
brew install node
```

### Ubuntu/Debian

```bash
# Install Python 3.12
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev

# Install Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### Windows

1. Download Python 3.12.0 from [python.org](https://www.python.org/downloads/release/python-3120/)
2. Check "Add Python to PATH" during installation
3. Download Node.js LTS from [nodejs.org](https://nodejs.org/)

---

## 🚀 Installation

### 1. Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment with Python 3.12
python3.12 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start Django server
python manage.py runserver 0.0.0.0:8000
```

**Backend will be available at:** `http://localhost:8000`

### 2. Web Frontend Setup (React)

```bash
# Open a new terminal
cd web-frontend

# Install npm dependencies
npm install

# Start Vite development server
npm run dev
```

**Web app will be available at:** `http://localhost:5173`

### 3. Desktop App Setup (PyQt5)

```bash
# Open a new terminal
cd desktop-app

# Create virtual environment with Python 3.12
python3.12 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Launch desktop application
python main.py
```

---

## ⚡ Quick Start

Use the provided shell scripts for one-command startup:

```bash
# Terminal 1 - Start Backend (required first)
./run_backend.sh

# Terminal 2 - Start Web Frontend
./run_web.sh

# Terminal 3 - Start Desktop App
./run_desktop.sh
```

---

## 📊 Demo CSV Format

A demo file `sample_data.csv` is included. Format:

```csv
timestamp,equipment_type,flow_rate,pressure,temperature
2026-01-01 08:00:00,Pump,45.2,120.5,65.3
2026-01-01 08:15:00,Pump,46.8,121.2,66.1
2026-01-01 08:30:00,Valve,12.3,85.4,72.8
2026-01-01 08:45:00,Reactor,78.9,200.1,180.5
```

### Column Specifications

| Column | Type | Description | Unit |
|--------|------|-------------|------|
| `timestamp` | datetime | ISO 8601 format | - |
| `equipment_type` | string | Equipment category | - |
| `flow_rate` | float | Flow measurement | L/min |
| `pressure` | float | Pressure reading | kPa |
| `temperature` | float | Temperature reading | °C |

### Supported Equipment Types

- Pump
- Valve
- Reactor
- Heat Exchanger
- Compressor
- Tank
- Filter
- Separator

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload/` | Upload CSV file |
| `GET` | `/api/datasets/` | List all datasets |
| `GET` | `/api/datasets/{id}/` | Get dataset details |
| `DELETE` | `/api/datasets/{id}/` | Delete dataset |
| `GET` | `/api/summary/{id}/` | Get statistical summary |
| `GET` | `/api/report/{id}/` | Download PDF report |

See [API_SPEC.yaml](API_SPEC.yaml) for full API documentation.

---

## 📸 Screenshots

### Web Application

#### Upload Page
![Upload Page](screenshots/web-upload.png)
*Drag & drop CSV upload with column auto-detection*

#### Dashboard
![Dashboard](screenshots/web-dashboard.png)
*Statistical summary with interactive Chart.js visualizations*

#### History Page
![History](screenshots/web-history.png)
*Browse and manage uploaded datasets*

---

### Desktop Application

#### Upload View
![Desktop Upload](screenshots/desktop-upload.png)
*PyQt5 upload interface with progress indicator*

#### Dashboard View
![Desktop Dashboard](screenshots/desktop-dashboard.png)
*Matplotlib charts with FOSSEE color palette*

#### History Panel
![Desktop History](screenshots/desktop-history.png)
*Dataset management with view/delete actions*

---

## 📁 Project Structure

```
fossee-project/
├── backend/                    # Django REST API
│   ├── api/
│   │   ├── models.py          # Dataset model
│   │   ├── views.py           # API views
│   │   ├── services/
│   │   │   ├── csv_parser.py  # CSV parsing logic
│   │   │   ├── analytics.py   # Statistical analysis
│   │   │   └── pdf_generator.py
│   │   └── urls.py
│   ├── config/                # Django settings
│   ├── manage.py
│   └── requirements.txt
│
├── web-frontend/              # React + Vite
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js      # Axios API client
│   │   ├── components/
│   │   │   ├── Layout.jsx
│   │   │   ├── CSVUploadZone.jsx
│   │   │   └── Charts/
│   │   ├── pages/
│   │   │   ├── Upload.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── History.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── tailwind.config.js
│
├── desktop-app/               # PyQt5 Application
│   ├── widgets/
│   │   ├── upload_widget.py
│   │   ├── table_widget.py
│   │   ├── chart_widget.py
│   │   └── history_panel.py
│   ├── pages/
│   │   ├── upload_page.py
│   │   ├── dashboard_page.py
│   │   └── history_page.py
│   ├── api_client.py          # Requests API client
│   ├── fossee_style.py        # FOSSEE colors
│   ├── main.py
│   └── requirements.txt
│
├── screenshots/               # Screenshot placeholders
├── sample_data.csv            # Demo CSV file
├── API_SPEC.yaml              # API specification
├── design.md                  # FOSSEE design system
├── run_backend.sh             # Backend startup script
├── run_web.sh                 # Web frontend script
├── run_desktop.sh             # Desktop app script
└── README.md                  # This file
│   │   └── styles/
│   └── package.json
├── desktop/                # PyQt5 application
│   ├── main.py
│   ├── styles/
│   └── components/
├── sample_data/            # Sample CSV files
├── requirements.txt        # Python dependencies
└── README.md
```

## Quick Start

---

## 🎨 Design System

Following the **FOSSEE Scientific Analytics UI** design system:

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Primary 900 | `#0F2A44` | Headers, text |
| Primary 700 | `#1B7F79` | Flow rate, accents |
| Primary 600 | `#3A4E9F` | Pressure, buttons |
| Temperature | `#C53030` | Temperature data |
| Success | `#38A169` | Success states |
| Warning | `#D69E2E` | Warnings |
| Surface | `#F7FAFC` | Backgrounds |

### Typography

- **Headings:** Inter, 600-700 weight
- **Body:** Inter, 400-500 weight
- **Monospace:** JetBrains Mono (data tables)

---

## 🧪 Testing

```bash
# Backend tests
cd backend
source venv/bin/activate
python manage.py test

# Frontend tests
cd web-frontend
npm test
```

---

## 📝 License

This project is developed for **FOSSEE (Free/Libre and Open Source Software for Education)** at IIT Bombay.

---

## 👤 Author

**Diksha Damahe**

---

<p align="center">
  <strong>FOSSEE Scientific Analytics Platform</strong><br>
  Built with ❤️ for scientific research
</p>
