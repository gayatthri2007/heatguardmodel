# 📖 HeatGuard - Documentation Index & Getting Started

## 🚀 IMMEDIATE ACTION: Run the System

```powershell
# Windows PowerShell
.\start-heatguard.ps1

# Windows Command Prompt
start-heatguard.bat
```

**Done!** Browser opens automatically to http://localhost:5173

---

## 📚 Documentation Map

### 🎯 For Running the System

| File | Purpose | Read Time |
|------|---------|-----------|
| **[RUN.md](RUN.md)** | ⭐ **START HERE** - Complete running instructions | 5 min |
| **[QUICKSTART.md](QUICKSTART.md)** | Fast setup (3 steps) + test accounts | 3 min |
| **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** | What's been set up for you | 5 min |

### 🏗️ For Understanding the System

| File | Purpose | Read Time |
|------|---------|-----------|
| **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** | Project architecture & features | 10 min |
| **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** | Complete API reference | 15 min |
| **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** | Verification checklist | 10 min |

### 🚀 For Deploying the System

| File | Purpose | Read Time |
|------|---------|-----------|
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Production deployment guide | 20 min |
| **[SETUP_GUIDE.md](SETUP_GUIDE.md)** | Detailed setup information | 15 min |

### 📋 This Document
| File | Purpose |
|------|---------|
| **[README.md](README.md)** | Project overview |
| **[docker-compose.yml](docker-compose.yml)** | Docker configuration |
| **[.env](.env)** | Development configuration |

---

## 🎯 Choose Your Path

### ⚡ Path 1: "Just Let Me Run It!" (5 minutes)
1. Open PowerShell in project folder
2. Run: `.\start-heatguard.ps1`
3. Browser opens automatically
4. Login with: `worker1` / `password123`
5. Done! 🎉

### 📖 Path 2: "I Want to Understand First" (20 minutes)
1. Read: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) (5 min)
2. Read: [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) (10 min)
3. Skim: [API_DOCUMENTATION.md](API_DOCUMENTATION.md) (5 min)
4. Run: `.\start-heatguard.ps1`
5. Explore the system

### 🏭 Path 3: "I'm Deploying to Production" (45 minutes)
1. Read: [DEPLOYMENT.md](DEPLOYMENT.md) (20 min)
2. Read: [SETUP_GUIDE.md](SETUP_GUIDE.md) (15 min)
3. Review: [API_DOCUMENTATION.md](API_DOCUMENTATION.md) (10 min)
4. Follow deployment steps

---

## 🔍 Quick Reference

### Access Points
```
Frontend:        http://localhost:5173
Backend API:     http://localhost:5000/api
Health Check:    http://localhost:5000/api/health
Model Test:      http://localhost:5000/model-test
```

### Test Accounts
```
Worker:      worker1 / password123
Supervisor:  supervisor1 / admin123
Admin:       admin / admin123
```

### Key Files
```
Backend:     backend/app.py
Frontend:    frontend/src/App.jsx
ML Model:    models/random_forest.pkl
Database:    backend/instance/heatguard.db
Config:      .env
```

### Critical Commands
```bash
# Start system
.\start-heatguard.ps1

# Start backend only
cd backend && python app.py

# Start frontend only
cd frontend && npm run dev

# Reset database
rm backend/instance/heatguard.db

# Install dependencies
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

---

## 🔄 User Journey

```
┌─────────────────┐
│   Open Browser  │
│   localhost:    │
│   5173          │
└────────┬────────┘
         │
    ┌────▼─────────────┐
    │ Login Page       │
    │ (or Register)    │
    └────┬─────────────┘
         │
    ┌────▼──────────────────┐
    │ Role Selection        │
    │ Choose: Worker or     │
    │ Supervisor            │
    └────┬──────────────────┘
         │
    ┌────▼──────────────────┐
    │ Worker Path           │
    │ - Dashboard           │
    │ - Vital Metrics       │
    │ - Digital Twin        │
    │ - Alerts              │
    └───────────────────────┘
         OR
    ┌────────────────────────┐
    │ Supervisor Path        │
    │ - Multi-worker View    │
    │ - Analytics            │
    │ - Alert Management     │
    │ - Zone Overview        │
    └────────────────────────┘
```

---

## ⚡ Quick Start Flowchart

```
START
  │
  ├─→ Check prerequisites
  │   ├─→ Python 3.8+? ✓
  │   ├─→ Node.js 14+? ✓
  │   └─→ npm installed? ✓
  │
  ├─→ Run startup script
  │   └─→ .\start-heatguard.ps1
  │
  ├─→ Browser opens
  │   └─→ http://localhost:5173
  │
  ├─→ Login
  │   ├─→ Test account or
  │   └─→ Register new
  │
  ├─→ Explore features
  │   ├─→ Dashboard
  │   ├─→ Predictions
  │   ├─→ Alerts
  │   └─→ Metrics
  │
  └─→ SUCCESS! 🎉
```

---

## 📊 System Components Overview

```
┌─────────────────────────────────────────────┐
│         🌐 Web Browser                      │
│  ├─ React Components                        │
│  ├─ Real-time Charts                        │
│  ├─ User Interface                          │
│  └─ Data Visualization                      │
└────────────┬────────────────────────────────┘
             │
      REST JSON API
      JWT Authentication
             │
┌────────────▼────────────────────────────────┐
│      🖥️ Flask Web Server                    │
│  ├─ Authentication                          │
│  ├─ Data Management                         │
│  ├─ API Endpoints                           │
│  └─ Business Logic                          │
└────────────┬────────────────────────────────┘
             │
      ┌──────┴──────┐
      │             │
  ┌───▼────┐  ┌────▼────────┐
  │ SQLite │  │   ML Engine  │
  │ Database   ├─ Twin Logic │
  │        │  ├─ Prediction │
  │        │  ├─ Risk Score │
  │        │  └─ DTHS Calc  │
  └────────┘  └──────────────┘
```

---

## 🎓 Learning Path

### Beginner (New to the system)
1. Run the system: `.\start-heatguard.ps1`
2. Explore: Test accounts (worker1 / supervisor1)
3. Learn: Check dashboards and features
4. Read: [QUICKSTART.md](QUICKSTART.md)

### Intermediate (Want to understand better)
1. Read: [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
2. Explore: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
3. Test: API calls using cURL
4. Customize: Configuration in `.env`

### Advanced (Building/deploying)
1. Study: [DEPLOYMENT.md](DEPLOYMENT.md)
2. Review: Backend code in `backend/`
3. Review: Frontend code in `frontend/src/`
4. Deploy: Using Docker or cloud platform
5. Monitor: Set up logging and alerts

---

## 🆘 Problem Solving

### Problem: "Port already in use"
→ See [DEPLOYMENT.md#troubleshooting](DEPLOYMENT.md#troubleshooting)

### Problem: "Python/Node not found"
→ See [DEPLOYMENT.md#troubleshooting](DEPLOYMENT.md#troubleshooting)

### Problem: "Module import errors"
→ See [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)

### Problem: "Database issues"
→ See [DEPLOYMENT.md#troubleshooting](DEPLOYMENT.md#troubleshooting)

### Problem: "Frontend won't load"
→ See [DEPLOYMENT.md#troubleshooting](DEPLOYMENT.md#troubleshooting)

---

## ✨ Key Features at a Glance

### 🔥 4-Pillar Digital Twin
- Baseline adjustment (BMI, fitness)
- Environmental analysis (WBGT, temp, humidity)
- Cooling intervention modeling
- DTHS computation + ML prediction

### 👷 Worker Features
- Real-time risk dashboard
- Digital Twin simulator
- Vital metrics tracking
- Alert management
- Heat strain history

### 👨‍💼 Supervisor Features
- Multi-worker monitoring
- Zone-based overview
- Risk analytics
- Alert escalation
- Worker history

### 🤖 AI/ML Capabilities
- Random Forest prediction
- Real-time risk scoring
- Pattern recognition
- Personalized recommendations

---

## 🎯 What You Get

✅ **Complete Working System**
- Backend API fully functional
- Frontend web app ready
- ML model integrated
- Database configured
- Authentication system
- All features implemented

✅ **Ready to Use**
- No additional setup needed
- Test accounts pre-created
- Sample data included
- Configuration complete
- Startup scripts ready

✅ **Documentation**
- Quick start guide
- Full API reference
- Deployment guide
- Troubleshooting help
- Architecture overview

✅ **Production Ready**
- Docker support
- Configuration management
- Database options (SQLite/PostgreSQL)
- Error handling
- Security features

---

## 🚀 3 Step Quick Reference

```
1. RUN IT
   .\start-heatguard.ps1

2. LOGIN
   worker1 / password123

3. EXPLORE!
   Dashboards, Predictions, Alerts
```

---

## 📞 Need Help?

### Quick Answers
- See: [QUICKSTART.md](QUICKSTART.md) - Common questions answered
- See: [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - Verification steps
- See: [DEPLOYMENT.md](DEPLOYMENT.md) - Troubleshooting section

### In-depth Understanding
- See: [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - System architecture
- See: [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API details
- See: [DEPLOYMENT.md](DEPLOYMENT.md) - Full guide

### Code/Implementation
- Backend: `backend/app.py`
- Frontend: `frontend/src/App.jsx`
- ML Engine: `backend/ml_engine/twin_engine.py`
- Database: `backend/models/`

---

## 🎉 Ready?

Everything is configured and tested. Just run:

```powershell
.\start-heatguard.ps1
```

**Get started:** → Open [RUN.md](RUN.md)

**Questions?** → Check documentation above

**Let's protect workers with heat stress monitoring! 🔥**

---

## 📋 Complete File List

```
Documentation:
✓ README.md - Project overview
✓ RUN.md - How to run everything
✓ QUICKSTART.md - Fast setup  
✓ DEPLOYMENT.md - Production guide
✓ API_DOCUMENTATION.md - API reference
✓ PROJECT_OVERVIEW.md - Architecture
✓ SETUP_CHECKLIST.md - Verification
✓ SETUP_GUIDE.md - Detailed setup
✓ IMPLEMENTATION_SUMMARY.md - What's built
✓ This file - Documentation index

Configuration:
✓ .env - Development config
✓ .env.example - Config template
✓ .gitignore - Git settings
✓ docker-compose.yml - Docker config

Scripts:
✓ start-heatguard.ps1 - Windows PowerShell
✓ start-heatguard.bat - Windows batch
✓ init_db.py - DB initialization

Application:
✓ backend/ - Flask API
✓ frontend/ - React app
✓ models/ - ML models
✓ data/ - Sample data
```

---

**👉 START HERE:** [RUN.md](RUN.md) or run `.\start-heatguard.ps1`
