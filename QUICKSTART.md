# HeatGuard - Quick Start Guide

## 🚀 Start the Complete System in 3 Steps

### **Step 1: Install Node.js (Frontend Requirement)**
If you don't have Node.js installed:
1. Download from https://nodejs.org/ (LTS version recommended)
2. Run the installer and follow prompts
3. Verify installation:
   ```bash
   node --version
   npm --version
   ```

### **Step 2: Install Frontend Dependencies**
Open PowerShell in the project folder and run:
```bash
cd frontend
npm install
cd..
```

### **Step 3: Start the System**

#### Option A: Quick Start Script (Recommended)
```bash
.\start-heatguard.ps1
```
This will:
- ✅ Start backend on http://localhost:5000
- ✅ Build and start frontend on http://localhost:5173
- ✅ Enable full development environment

#### Option B: Manual Start
**Terminal 1 - Start Backend:**
```bash
cd backend
python app.py
```
Backend runs on: http://localhost:5000

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm run dev
```
Frontend runs on: http://localhost:5173

---

## 🌐 Access the Application

**Development:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000/api
- Model Test: http://localhost:5000/model-test

---

## 👤 Test Accounts

### Worker Account
- **Username:** worker1
- **Password:** password123
- **Role:** Worker
- **Zone:** Zone A - Construction

### Supervisor Account
- **Username:** supervisor1
- **Password:** admin123
- **Role:** Supervisor

### Admin Account
- **Username:** admin
- **Password:** admin123
- **Role:** Supervisor

*New accounts can be created via the registration page*

---

## 🔧 System Components

### Backend (Flask)
- API Server: `http://localhost:5000`
- Health Check: `http://localhost:5000/api/health`
- Prediction Engine: `http://localhost:5000/api/predictions/predict`
- Database: SQLite (auto-initialized)
- Authentication: JWT

### Frontend (React + Vite)
- Development Server: `http://localhost:5173`
- Components:
  - 👤 Login page
  - 👷 Worker dashboard with real-time monitoring
  - 👨‍💼 Supervisor dashboard with multi-worker oversight
  - 🔥 Digital twin simulation
  - 📊 Alert management

---

## ✅ Features Implemented

### 🔥 4-Pillar Digital Twin Logic
- ✅ Baseline adjustment (BMI, fitness levels)
- ✅ Environmental exposure analysis
- ✅ Cooling intervention modeling
- ✅ Digital Heat Strain Score (DTHS) computation
- ✅ Machine Learning predictions with rule-based overrides

### 👷 Worker Features
- ✅ Real-time risk assessment
- ✅ Digital Twin simulation
- ✅ Alert notifications
- ✅ Vital metrics tracking
- ✅ Heat strain history

### 👨‍💼 Supervisor Features
- ✅ Multi-worker monitoring
- ✅ Zone-based oversight
- ✅ Risk distribution analytics
- ✅ Alert management
- ✅ Real-time vital signs monitoring

---

## 🔌 Production Deployment (Docker)

### Build Docker Images
```bash
docker-compose build
```

### Run with Docker
```bash
docker-compose up
```

Application will run on:
- Frontend: http://localhost
- Backend: http://localhost:5000

---

## 📚 Additional Commands

### Backend Only
```bash
cd backend
python app.py
```

### Frontend Development with Hot Reload
```bash
cd frontend
npm run dev
```

### Build Frontend for Production
```bash
cd frontend
npm run build
```
Built files will be in `frontend/dist`

### Test Model Predictions
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "body_temp_post": 37.2,
    "body_temp_pre": 36.8,
    "heart_rate_post": 85,
    "heart_rate_pre": 72,
    "wbgt": 29,
    "ambient_temp": 32,
    "humidity": 60,
    "radiant_heat": 500,
    "break_duration": 10,
    "bmi_bucket": "medium",
    "fitness_level": "medium"
  }'
```

---

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 or 5173 is in use:

**For Backend (Port 5000):**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**For Frontend (Port 5173):**
```bash
# Find process using port 5173
netstat -ano | findstr :5173

# Kill the process
taskkill /PID <PID> /F
```

### Python Not Found
- Ensure Python 3.8+ is installed
- Add Python to PATH
- Use full path: `C:\Users\<username>\AppData\Local\Programs\Python\Python311\python.exe`

### npm Not Found
- Ensure Node.js is installed correctly
- Restart terminal after Node.js installation
- Run `npm install -g npm` to update npm

### Backend Errors
- Delete `heatguard.db` to reset database
- Run `pip install -r requirements.txt` to ensure all packages are installed

### Frontend Build Errors
- Delete `node_modules` folder
- Delete `package-lock.json`
- Run `npm install` again

---

## 📊 Database

The system uses SQLite for development. Database file is automatically created:
- Location: `backend/instance/heatguard.db`
- To reset: Delete the database file and restart backend

For production, configure PostgreSQL via DATABASE_URL environment variable.

---

## 🆘 Support

1. Check the [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup instructions
2. Check the [README.md](README.md) for project overview
3. Review error messages in terminal output
4. Check backend logs at `http://localhost:5000/model-test` for model diagnostics

---

**Ready to start?** Run: `.\start-heatguard.ps1`
