# HeatGuard Complete Setup Checklist

## ✅ Pre-Deployment Checklist

### System Requirements
- [ ] Python 3.8+ installed: `python --version`
- [ ] Node.js 14+ installed: `node --version`
- [ ] npm installed: `npm --version`
- [ ] At least 4 GB RAM available
- [ ] At least 500 MB free disk space

### Backend Setup
- [ ] `backend/requirements.txt` exists
- [ ] All backend dependencies installed: `pip install -r backend/requirements.txt`
- [ ] `backend/app.py` exists and is runnable
- [ ] `backend/config.py` properly configured
- [ ] `backend/database/db.py` exists
- [ ] `backend/models/` contains User, Worker, Alert models
- [ ] `backend/routes/` contains auth, predictions, worker, supervisor
- [ ] `backend/ml_engine/` contains twin_engine.py
- [ ] `models/random_forest.pkl` exists (ML model)

### Frontend Setup
- [ ] `frontend/package.json` exists
- [ ] Node modules installed: `npm install` in frontend/
- [ ] `frontend/vite.config.js` exists
- [ ] `frontend/src/App.jsx` exists
- [ ] All components in `frontend/src/components/` properly set up
- [ ] API client configured at `frontend/src/api/client.js`

### Configuration Files
- [ ] `.env` file created and configured
- [ ] `.env.example` file exists as template
- [ ] `.gitignore` file exists and complete
- [ ] `docker-compose.yml` configured correctly

### Documentation
- [ ] `QUICKSTART.md` created ✓
- [ ] `DEPLOYMENT.md` created ✓
- [ ] `API_DOCUMENTATION.md` created ✓
- [ ] `PROJECT_OVERVIEW.md` created ✓
- [ ] `README.md` exists ✓

### Scripts
- [ ] `start-heatguard.ps1` created (Windows PowerShell)
- [ ] `start-heatguard.bat` created (Windows Command Prompt)
- [ ] `init_db.py` created for database initialization

---

## 🚀 Installation Steps

### Step 1: Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
# Should complete without errors
```

### Step 2: Install Frontend Dependencies
```bash
cd frontend
npm install
# Should complete without errors
```

### Step 3: Create Environment Configuration
```bash
# .env file should already exist
# Verify it contains necessary variables
cat .env
```

### Step 4: Initialize Database (Optional)
```bash
# Automatic on first backend startup, or run manually:
python init_db.py
```

---

## ✨ Running the System

### Method 1: Automated (Windows)
```bash
# PowerShell
.\start-heatguard.ps1

# Or Command Prompt
start-heatguard.bat
```
Both methods will:
- Verify requirements
- Install frontend dependencies if needed
- Start backend on http://localhost:5000
- Start frontend on http://localhost:5173
- Open browser automatically

### Method 2: Manual (Any OS)
```bash
# Terminal 1
cd backend
python app.py
# Backend running on http://localhost:5000

# Terminal 2
cd frontend
npm run dev
# Frontend running on http://localhost:5173
```

### Method 3: Docker
```bash
docker-compose build
docker-compose up
# Application on http://localhost
```

---

## 📝 Verification Checklist

After starting the system:

### Backend Verification
- [ ] Backend runs without errors
- [ ] Health check works: `curl http://localhost:5000/api/health`
- [ ] Model test accessible: `http://localhost:5000/model-test`
- [ ] Database initialized: `backend/instance/heatguard.db` exists

### Frontend Verification
- [ ] Frontend starts without errors
- [ ] Browser opens to http://localhost:5173
- [ ] Login page loads correctly
- [ ] Can navigate to registration page

### Integration Verification
- [ ] Can register new account
- [ ] Can login with credentials
- [ ] Backend receives frontend requests (check terminal logs)
- [ ] Frontend receives API responses (check browser console)
- [ ] Digital twin prediction works
- [ ] Dashboards load correctly

### Database Verification
- [ ] Sample accounts created: worker1, supervisor1
- [ ] Users can login
- [ ] User data persists across sessions
- [ ] Metrics can be viewed

---

## 🔧 Common Setup Issues

### Issue: Python Not Found
```bash
# Windows: Verify Python in PATH
path

# If not found, reinstall Python and check:
# ☑ "Add Python to PATH" during installation

# Use full path as fallback:
C:\Users\<username>\AppData\Local\Programs\Python\Python311\python.exe app.py
```

### Issue: npm Not Found
```bash
# Verify Node.js installation
node --version
npm --version

# If not found, reinstall Node.js from https://nodejs.org/
# Restart terminal after installation

# Use full path as fallback:
# C:\Program Files\nodejs\npm install
```

### Issue: Port 5000 Already In Use
```bash
# Windows - Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Issue: Port 5173 Already In Use
```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5173
kill -9 <PID>
```

### Issue: Module Import Errors
```bash
# Reinstall dependencies
cd backend
pip install --upgrade -r requirements.txt

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
```

### Issue: npm Modules Won't Install
```bash
# Clear npm cache
npm cache clean --force

# Delete and reinstall
rm -r frontend/node_modules frontend/package-lock.json
cd frontend
npm install
```

---

## 📊 System Architecture

```
┌─────────────────────────────────────┐
│   Frontend (React + Vite)           │
│   http://localhost:5173             │
│  - Login Page                       │
│  - Worker Dashboard                 │
│  - Supervisor Dashboard             │
│  - Digital Twin Simulator           │
└────────────┬────────────────────────┘
             │ REST API
             │ JWT Authentication
             │
┌────────────▼────────────────────────┐
│   Backend (Flask)                   │
│   http://localhost:5000             │
│  - Auth Routes                      │
│  - Prediction Engine                │
│  - Worker Routes                    │
│  - Supervisor Routes                │
└────────────┬────────────────────────┘
             │
      ┌──────┴──────┐
      │             │
  ┌───▼────┐   ┌────▼──────────┐
  │ SQLite │   │ ML Engineered │
  │ (Dev)  │   │ - Twin Logic  │
  │        │   │ - Prediction  │
  │ or     │   │ - Risk Score  │
  │ PostgreSQL  └───────────────┘
  │ (Prod)│
  └────────┘
```

---

## 🔐 Security Setup (Production)

Before deploying to production:

1. **Change JWT Secret**
   ```bash
   # In .env file
   JWT_SECRET_KEY=<generate-strong-random-string>
   ```

2. **Update Database**
   ```bash
   # Use PostgreSQL with strong password
   DATABASE_URL=postgresql://user:strong_password@db_host:5432/heatguard
   ```

3. **Enable HTTPS**
   - Get SSL certificate (Let's Encrypt recommended)
   - Configure reverse proxy (nginx, Apache)

4. **Set Environment**
   ```bash
   FLASK_ENV=production
   DEBUG=False
   ```

5. **Configure CORS**
   ```bash
   CORS_ORIGINS=https://your-domain.com
   ```

---

## 📈 Performance Optimization

### Frontend Optimization
```bash
# Build production bundle (optimized)
cd frontend
npm run build
# Output: frontend/dist/
```

### Backend Optimization
```bash
# Use Gunicorn for production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 'backend.app:create_app()'

# Use PostgreSQL instead of SQLite
# Set DATABASE_URL to PostgreSQL connection
```

---

## 🆘 Support & Troubleshooting

### Quick Links
- **Fast Setup:** [QUICKSTART.md](QUICKSTART.md)
- **Deployment Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **API Reference:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Project Overview:** [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)

### Debug Mode
```bash
# Enable Flask debug mode in .env
FLASK_ENV=development
DEBUG=True

# Check logs in terminal for detailed information
```

### Testing
```bash
# Test model
curl http://localhost:5000/model-test

# Test API
curl http://localhost:5000/api/health
```

---

## ✅ Final Verification

Run this checklist to ensure complete setup:

```bash
# 1. Check Python
python --version

# 2. Check Node.js
node --version
npm --version

# 3. Check backend installation
pip list | grep Flask

# 4. Check frontend installation
cd frontend && npm list react

# 5. Start and test (use automated script)
# Windows:
.\start-heatguard.ps1

# macOS/Linux:
# Terminal 1: cd backend && python app.py
# Terminal 2: cd frontend && npm run dev
```

---

## 🎯 Next Steps

1. ✅ Complete the checklist above
2. ✅ Run startup script or manual startup
3. ✅ Access http://localhost:5173 in browser
4. ✅ Register and login
5. ✅ Test Digital Twin prediction
6. ✅ Explore worker and supervisor dashboards
7. ✅ Review API documentation
8. ✅ Deploy to production when ready

---

**All setup complete? Start here:** [QUICKSTART.md](QUICKSTART.md) or run `.\start-heatguard.ps1`
