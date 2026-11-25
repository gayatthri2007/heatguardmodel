# 🚀 HeatGuard - RUN YOUR COMPLETE SYSTEM

**This file shows you EXACTLY how to get everything running in 3 simple steps!**

---

## ⚡ 3-Minute Quickstart

### Step 1️⃣: Check You Have Required Software

**Windows - Open PowerShell and run:**
```powershell
python --version
node --version
npm --version
```

If any command fails:
- **Python:** Download from https://www.python.org/
- **Node.js:** Download from https://nodejs.org/ (this includes npm)

---

### Step 2️⃣: Install Dependencies (First Time Only)

**Windows PowerShell - Run from project folder:**
```powershell
cd frontend
npm install
cd..
```

This downloads all required libraries (~2-3 minutes).

---

### Step 3️⃣: Start Everything!

**Choose ONE method:**

#### ✅ BEST - Automated Script (Recommended!)
```powershell
# PowerShell - Easiest!
.\start-heatguard.ps1

# OR Command Prompt
start-heatguard.bat
```
This automatically:
- ✅ Checks everything is installed
- ✅ Starts backend on http://localhost:5000
- ✅ Starts frontend on http://localhost:5173
- ✅ Opens browser automatically

#### OR Manual - Two Terminal Windows
```powershell
# TERMINAL 1 - Backend
cd backend
python app.py

# TERMINAL 2 - Frontend
cd frontend
npm run dev
```

---

## 🌐 Access Your Application

**After startup (should happen automatically):**

| Access Point | URL | Purpose |
|---|---|---|
| **Frontend** | http://localhost:5173 | The web app (what users see) |
| **Backend API** | http://localhost:5000/api | The server backend |
| **Model Test** | http://localhost:5000/model-test | Test the AI prediction |
| **Health Check** | http://localhost:5000/api/health | Check backend status |

---

## 👤 Login & Test

### Pre-Made Test Accounts (Already Created)
- **Worker:** `worker1` / `password123`
- **Supervisor:** `supervisor1` / `admin123`
- **Admin:** `admin` / `admin123`

### Or Create Your Own
1. Go to http://localhost:5173
2. Click "Register"
3. Fill in details
4. Choose role (Worker or Supervisor)
5. Complete registration
6. Login with your credentials

---

## 🎮 What Can You Do?

### As a Worker 👷
- ✅ View your real-time heat risk level
- ✅ Run Digital Twin simulation (predict outcomes)
- ✅ Track your vital signs (temperature, heart rate)
- ✅ Receive and manage alerts
- ✅ See heat stress history

### As a Supervisor 👨‍💼
- ✅ Monitor all workers in real-time
- ✅ See risk distribution across your team
- ✅ Manage alerts and escalations
- ✅ View worker history and trends
- ✅ Get dashboard analytics

---

## 🧪 Test the System

### Test the ML Model
Visit: http://localhost:5000/model-test
- Shows AI prediction sample
- Displays risk level and DTHS score
- Confirms model is working

### Test the API with Browser
Visit: http://localhost:5000/api/health
- Should show: `{"status": "ok"}`
- Confirms backend is running

### Create Test Data
1. Login as a worker
2. Go to digital twin simulator
3. Enter some vital signs data
4. Click "Predict" to test ML model
5. View results (risk level, recommendations)

---

## 🆘 Troubleshooting (Quick Fixes)

### ❌ "Port 5000 is already in use"
```powershell
# Find what's using port 5000
netstat -ano | findstr :5000

# Kill it (replace 12345 with actual PID number)
taskkill /PID 12345 /F
```

### ❌ "Python not found"
- Reinstall Python from https://www.python.org/
- **Important:** Check "Add Python to PATH"
- Restart PowerShell after installation

### ❌ "npm not found"
- Reinstall Node.js from https://nodejs.org/
- Restart PowerShell after installation

### ❌ "Module not found errors"
```powershell
cd backend
pip install -r requirements.txt
```

### ❌ "Frontend won't load"
```powershell
cd frontend
rm -r node_modules package-lock.json
npm install
npm run dev
```

### ❌ "Can't login"
- Check backend is running (should show in Terminal 1)
- Clear browser cache (Ctrl+Shift+Delete)
- Try in an incognito window

### ❌ Need to reset everything
```powershell
# Delete database (will be recreated)
rm backend/instance/heatguard.db

# Restart backend
cd backend
python app.py
```

---

## 📂 Project Structure

```
heatguardmodel/
├── backend/                          # The server (Python/Flask)
│   ├── app.py                       # Main application file
│   ├── requirements.txt              # Python packages to install
│   └── ... (other backend files)
│
├── frontend/                         # The website (React)
│   ├── package.json                 # Node packages to install
│   ├── src/
│   │   ├── App.jsx                  # Main app file
│   │   └── ... (other components)
│   └── ... (other frontend files)
│
├── models/                           # AI/ML models
│   └── random_forest.pkl            # The prediction model
│
├── docker-compose.yml                # Docker configuration (if using Docker)
├── start-heatguard.ps1               # Windows startup script ✨
├── start-heatguard.bat              # Windows startup script (alt) ✨
├── .env                              # Configuration file
│
├── QUICKSTART.md                     # Quick setup guide
├── DEPLOYMENT.md                     # Full deployment guide
├── API_DOCUMENTATION.md              # API reference
├── PROJECT_OVERVIEW.md               # Project details
└── SETUP_CHECKLIST.md               # Complete checklist
```

---

## 🔄 Typical Workflow

```
1. Start System
   ↓
   ├─ Run: .\start-heatguard.ps1
   └─ OR manually: backend in Terminal 1, frontend in Terminal 2
   
2. Open Browser
   ↓
   └─ Go to: http://localhost:5173
   
3. Login
   ↓
   └─ Use: worker1 / password123
   
4. Test Features
   ↓
   ├─ View Dashboard
   ├─ Run Prediction
   ├─ Check Alerts
   └─ View Metrics
   
5. Stop When Done
   ↓
   └─ Close terminal windows OR Ctrl+C
```

---

## 📊 System Components

### Frontend (What You See)
- Web interface at http://localhost:5173
- Login page, dashboards, charts
- Built with React + Vite
- Communicates with backend via API

### Backend (The Server)
- API server at http://localhost:5000
- Handles authentication, data, predictions
- Built with Flask (Python)
- Stores data in SQLite database

### ML Model
- AI system for heat stress prediction
- Uses worker metrics + environment data
- Returns risk level + recommendations
- Accessible at /model-test or via API

---

## 🔐 Security Notes

- **Passwords:** Encrypted and stored securely
- **API:** Protected with JWT tokens
- **Database:** Local SQLite (secure for development)
- **HTTPS:** Not enabled (development only)

For **production**, see [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📚 More Information

Need more details? Check these files:

| Document | Contains |
|----------|----------|
| **QUICKSTART.md** | Fast setup + test accounts |
| **SETUP_CHECKLIST.md** | Complete verification checklist |
| **DEPLOYMENT.md** | Full deployment + troubleshooting |
| **API_DOCUMENTATION.md** | All API endpoints + examples |
| **PROJECT_OVERVIEW.md** | Project details + architecture |

---

## ✅ Common Successful Setup Sequence

1. ✅ Open PowerShell in project folder
2. ✅ Check: `python --version` and `node --version`
3. ✅ Install: `cd frontend && npm install && cd..`
4. ✅ Start: `.\start-heatguard.ps1`
5. ✅ Wait for browser to open automatically
6. ✅ Login with: `worker1` / `password123`
7. ✅ Test Digital Twin prediction
8. ✅ Explore dashboards
9. ✅ Done! 🎉

---

## 🎯 Next Steps

**Right Now:**
```powershell
.\start-heatguard.ps1
```

**First Time Setup Issues?**
- Check [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
- Review [QUICKSTART.md](QUICKSTART.md)

**Want to Deploy?**
- Read [DEPLOYMENT.md](DEPLOYMENT.md)

**Need API Details?**
- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## 🚀 You're Ready!

**The system is fully configured and ready to run!**

Just run:
```powershell
.\start-heatguard.ps1
```

Everything will start automatically, and the system will open in your browser. 

**Good luck! 🔥**

---

**Questions?** See [DEPLOYMENT.md#troubleshooting](DEPLOYMENT.md) or check the other documentation files.

**All documentation created:**
- ✅ QUICKSTART.md - Fast setup
- ✅ DEPLOYMENT.md - Complete guide
- ✅ API_DOCUMENTATION.md - API reference
- ✅ PROJECT_OVERVIEW.md - Project details
- ✅ SETUP_CHECKLIST.md - Verification checklist
- ✅ This file - RUN instructions
