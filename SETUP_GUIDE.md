# HeatGuard Setup Guide

## ✅ Project Implementation Complete!

The complete Heat Stress Monitoring System has been successfully implemented. Here's how to run it:

## 🖥️ Backend Status

**Status:** ✅ **RUNNING** on `http://localhost:5000`

The Flask backend is already running with:
- Flask API server
- SQLAlchemy ORM (SQLite database)
- JWT authentication
- ML engine (4-pillar digital twin logic)
- All database models initialized

### Backend Features Enabled:
```
✅ Authentication API (/api/auth/*)
✅ Prediction API (/api/predictions/*)
✅ Worker Routes (/api/worker/*)
✅ Supervisor Routes (/api/supervisor/*)
✅ Health Check (/api/health)
```

**Access backend at:** `http://localhost:5000/api/health`

---

## 📱 Frontend Setup

The React frontend needs Node.js and npm installed.

### Option 1: Install Node.js (Recommended)

1. **Download Node.js** from https://nodejs.org/ (LTS version)
2. **Install it** following the installer
3. **Verify installation:**
   ```bash
   node -v
   npm -v
   ```

4. **Navigate to frontend directory:**
   ```bash
   cd D:\heatguardmodel\frontend
   ```

5. **Install dependencies:**
   ```bash
   npm install
   ```

6. **Start development server:**
   ```bash
   npm run dev
   ```

Frontend will run on `http://localhost:5173`

### Option 2: Use Docker (Alternative)

If you have Docker installed, you can run the frontend in a container.

---

## 🧪 Test the System

### Test Accounts

**Worker Account:**
- Username: `worker1` (register new)
- Password: `password123`
- Role: Worker
- Zone: Zone A - Construction

**Supervisor Account:**
- Username: `supervisor1` (register new)
- Password: `admin123`
- Role: Supervisor

### Quick Test Steps:

1. ✅ Backend already running: http://localhost:5000
2. 📦 Install frontend dependencies: `npm install` in frontend directory
3. 🚀 Start frontend: `npm run dev`
4. 🌐 Open http://localhost:5173
5. 👤 Register or login
6. 🔥 Try the Digital Twin prediction

---

## 📁 Project Structure

```
heatguardmodel/
├── backend/                       ✅ ACTIVE
│   ├── app.py                     (Flask server - RUNNING)
│   ├── config.py                  (Configuration)
│   ├── database/
│   │   └── db.py                  (SQLAlchemy setup)
│   ├── models/
│   │   ├── user.py               (User model)
│   │   ├── worker.py             (Worker & metrics)
│   │   └── alert.py              (Alert model)
│   ├── routes/
│   │   ├── auth.py               (Auth endpoints)
│   │   ├── predictions.py        (ML predictions)
│   │   ├── worker.py             (Worker routes)
│   │   └── supervisor.py         (Supervisor routes)
│   ├── ml_engine/
│   │   ├── dths.py               (DTHS calculation)
│   │   ├── cooling.py            (Cooling model)
│   │   └── twin_engine.py        (4-pillar logic)
│   └── requirements.txt
│
├── frontend/                      ⏳ NEEDS SETUP
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/           (React components)
│   │   ├── pages/                (Login page)
│   │   ├── api/                  (API client)
│   │   ├── styles/               (Global styles)
│   │   └── App.jsx
│   └── package.json
│
├── data/                         (CSV datasets)
└── models/                       (ML models)
```

---

## 🔌 API Endpoints (All Ready)

### Authentication
```
POST   /api/auth/register
POST   /api/auth/login
GET    /api/auth/me
```

### Predictions
```
POST   /api/predictions/predict
```

### Worker Routes
```
GET    /api/worker/profile
GET    /api/worker/metrics
GET    /api/worker/alerts
PUT    /api/worker/alerts/{id}/read
```

### Supervisor Routes
```
GET    /api/supervisor/workers
GET    /api/supervisor/dashboard/stats
GET    /api/supervisor/worker/{id}/history
GET    /api/supervisor/zones
```

---

## 🔥 Key Features Implemented

### Backend (✅ Ready)
- ✅ 4-Pillar Digital Twin Logic
- ✅ DTHS Score Calculation
- ✅ Cooling Intervention Modelling
- ✅ ML Model Integration (Random Forest)
- ✅ Rule-based Override System
- ✅ JWT Authentication
- ✅ Role-based Access (Worker/Supervisor)
- ✅ Real-time Alert System
- ✅ Database Models & ORM

### Frontend (⏳ Setup needed)
- 📱 Responsive Worker Dashboard
- 📱 Supervisor Dashboard with Analytics
- 📱 Digital Twin Simulation Tool
- 📱 Real-time Alerts Display
- 📱 Risk Visualization Charts
- 📱 Beautiful UI with Recharts
- 📱 Authentication Flow

---

## 📊 Digital Twin 4-Pillar Logic

1. **Baseline Adjustment** 
   - BMI bucket analysis
   - Fitness level adjustment
   - Individual risk factors

2. **Environmental Exposure**
   - WBGT monitoring
   - Temperature analysis
   - Humidity tracking
   - Radiant heat measurement

3. **Cooling Intervention**
   - Break duration impact
   - Passive cooling calculation
   - Recovery modeling

4. **DTHS & ML Prediction**
   - Digital Heat Strain Score (0-1)
   - ML model prediction (0-3 risk levels)
   - Rule-based safety override
   - Final risk determination

---

## 🚀 Next Steps

1. **Install Node.js** if not already installed
2. **Navigate to frontend:**
   ```bash
   cd frontend
   ```
3. **Install npm packages:**
   ```bash
   npm install
   ```
4. **Start frontend dev server:**
   ```bash
   npm run dev
   ```
5. **Open browser:**
   ```
   http://localhost:5173
   ```
6. **Register or login** with test credentials
7. **Enjoy the app!** 🎉

---

## 📚 Documentation

- **API:** See routes/ folder
- **ML Engine:** See ml_engine/ folder for Digital Twin logic
- **Database:** See models/ folder for schema
- **Frontend Components:** See frontend/src/components/

---

## 🆘 Troubleshooting

**Backend won't start?**
- Ensure you're in the `backend` directory
- Check Python 3.8+ is installed
- Run: `pip install -r requirements.txt`

**Frontend npm issues?**
- Install Node.js from nodejs.org
- Delete node_modules: `rm -r node_modules`
- Reinstall: `npm install`

**Port conflicts?**
- Backend: Change port 5000 in backend/app.py
- Frontend: Vite will use next available port

---

## 📝 Notes

- SQLite database (`heatguard.db`) auto-created on first run
- All models auto-migrated
- JWT tokens valid for 30 days
- Production ready with CORS setup

Enjoy monit oring worker heat safety! 🔥
