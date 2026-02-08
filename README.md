# Chemical Equipment Parameter Visualizer

**Hybrid Web + Desktop Application** | FOSSEE Intern Screening Task

A hybrid application that allows users to upload CSV files containing chemical equipment parameters (Equipment Name, Type, Flowrate, Pressure, Temperature), parse and analyze data via a Django REST backend, and visualize results through both a React Web frontend and a PyQt5 Desktop application.

Built for [FOSSEE](https://fossee.in/), IIT Bombay.

---

## Live Demo & Downloads

| Platform | Link |
|----------|------|
| **Web App** | [https://fossee-project-eta.vercel.app](https://fossee-project-eta.vercel.app) |
| **Backend API** | [https://dikshadamahe.pythonanywhere.com/api/](https://dikshadamahe.pythonanywhere.com/api/) |
| **Desktop App** | [Download Windows Installer](https://github.com/dikshadamahe/fossee-project/releases/latest) |

**Quick Start:**
1. Visit the [Web App](https://fossee-project-eta.vercel.app).
2. Register an account (optional, but required for history sync).
3. Upload the `sample_equipment_data.csv` file.
4. View charts, data tables, and download PDF reports.

---

## Tech Stack

*   **Frontend (Web):** React.js, Vite, Chart.js, TailwindCSS
*   **Frontend (Desktop):** PyQt5, Matplotlib
*   **Backend:** Django 5, Django REST Framework
*   **Data Processing:** Pandas, NumPy
*   **Database:** SQLite
*   **PDF Generation:** jsPDF (Web), ReportLab (Desktop)
*   **Authentication:** Token-based (DRF)

---

## Features

*   **CSV Upload:** Drag-and-drop or file selection.
*   **Data Analytics:** Automatic calculation of mean, min, max, and standard deviation for flowrate, pressure, and temperature.
*   **Visualizations:** Interactive bar charts, line trends, and doughnut charts for equipment distribution.
*   **History Sync:** Uploaded datasets are saved and synced between Web and Desktop apps (requires login).
*   **PDF Reports:** Generate professional A4 PDF reports with key insights and charts.
*   **Security:** Token-based authentication and secure data handling.

---

## Architecture

Both the React Web App and PyQt5 Desktop App communicate with the same Django backend via REST API.

*   **Web:** Hosted on Vercel.
*   **Backend:** Hosted on PythonAnywhere.
*   **Desktop:** Standalone executable.

---

## Setup Instructions

### Prerequisites
*   Python 3.12+
*   Node.js 18+
*   Git

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
Web App running at: `http://localhost:5173`

### 4. Desktop App Setup
```bash
cd desktop-app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## API Endpoints

Base URL: `https://dikshadamahe.pythonanywhere.com/api/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload/` | Upload CSV file |
| GET | `/datasets/` | List user's datasets |
| GET | `/datasets/{id}/` | Get dataset details |
| DELETE | `/datasets/{id}/` | Delete a dataset |
| GET | `/summary/{id}/` | Get statistical summary |
| GET | `/report/{id}/` | Download PDF report |
| POST | `/auth/login/` | User login |
| POST | `/auth/register/` | User registration |

---

## Sample Data

Use the provided `sample_equipment_data.csv` for testing:
*   **Equipment Name:** String (e.g., "Pump A")
*   **Type:** String (e.g., "Pump", "Valve")
*   **Flowrate:** numeric
*   **Pressure:** numeric
*   **Temperature:** numeric

---

## Credits

Developed by [Diksha Damahe](https://github.com/dikshadamahe) for FOSSEE, IIT Bombay.
