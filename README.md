# HeatGuard - Worker Heat Safety Monitoring System

A comprehensive digital twin-based heat stress monitoring system for occupational safety.

## Features

🔥 **4-Pillar Digital Twin Logic**
- Baseline adjustment (BMI, fitness levels)
- Environmental exposure analysis
- Cooling intervention modelling
- Digital Heat Strain Score (DTHS) computation
- Machine Learning predictions with rule-based overrides

👷 **Worker Dashboard**
- Real-time risk assessment
- Digital Twin simulation
- Alert notifications
- Vital metrics tracking
- Heat strain history

👨‍💼 **Supervisor Dashboard**
- Multi-worker monitoring
- Zone-based oversight
- Risk distribution analytics
- Alert management
- Real-time vital signs monitoring

## Tech Stack

**Backend:**
- Flask 2.3.3
- Flask-SQLAlchemy (ORM)
- Flask-JWT-Extended (Authentication)
- scikit-learn (ML models)
- pandas (Data processing)

**Frontend:**
- React 18.2.0
- Vite (Build tool)
- Recharts (Data visualization)
- Lucide React (Icons)
- Axios (HTTP client)

**Database:**
- SQLite (Development)
- PostgreSQL (Production)

## 🚀 Quick Start (RECOMMENDED)

### ⚡ Fastest Way to Get Running

**Windows PowerShell:**
```powershell
.\start-heatguard.ps1
```

**Windows Command Prompt:**
```bash
start-heatguard.bat
```

**Manual Setup (Any OS):**
```bash
# Terminal 1 - Backend
cd backend
pip install -r requirements.txt
python app.py

# Terminal 2 - Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Then visit: **http://localhost:5173**

### ✅ See [RUN.md](RUN.md) for complete running instructions

---

## 📖 Full Documentation

| Document | Purpose |
|----------|---------|
| **[RUN.md](RUN.md)** | ⚡ **START HERE** - How to run everything |
| **[QUICKSTART.md](QUICKSTART.md)** | Fast setup guide & test accounts |
| **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** | Complete verification checklist |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Production deployment guide |
| **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** | Full API reference |
| **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** | Architecture & features |

---

## Installation Details

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Server runs on `http://localhost:5000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

## Project Structure

```
heatguardmodel/
├── backend/
│   ├── ml_engine/          # ML models and DTHS calculation
│   ├── models/             # Database models
│   ├── routes/             # API endpoints
│   ├── database/           # DB configuration
│   ├── app.py              # Flask application
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── api/            # API client
│   │   └── styles/         # Global styles
│   ├── package.json
│   └── vite.config.js
│
└── data/                   # CSV datasets for training
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Create new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Predictions
- `POST /api/predictions/predict` - Get heat stress prediction

### Worker Routes
- `GET /api/worker/profile` - Get worker profile
- `GET /api/worker/metrics` - Get metrics history
- `GET /api/worker/alerts` - Get worker alerts

### Supervisor Routes
- `GET /api/supervisor/workers` - Get all workers
- `GET /api/supervisor/dashboard/stats` - Dashboard statistics
- `GET /api/supervisor/zones` - Zone overview

## Usage

### Test Credentials

**Worker:**
- Username: `worker1`
- Password: `password123`

**Supervisor:**
- Username: `supervisor1`
- Password: `admin123`  <!-- seeded in app startup, not the same as worker -->

> 💡 *The supervisor account is created with `admin123` by default.  If you
> register a new supervisor via the UI you can choose any password you like.*

## OSHA Compliance

This system adheres to OSHA guidelines for heat stress management:
- Monitors WBGT (Wet Bulb Globe Temperature)
- Tracks physiological indicators
- Recommends rest periods
- Critical alerts for dangerous conditions

## License

MIT License - 2026
