# HeatGuard - Complete Deployment Manual

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Running the Application](#running-the-application)
4. [Production Deployment](#production-deployment)
5. [Troubleshooting](#troubleshooting)
6. [API Documentation](#api-documentation)

---

## System Requirements

### Minimum Requirements
- **OS:** Windows 10/11, macOS, or Linux
- **RAM:** 4 GB
- **Storage:** 500 MB free space
- **Internet:** For npm package downloads

### Required Software

#### Windows:
1. **Python 3.8+**
   - Download: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Node.js LTS (includes npm)**
   - Download: https://nodejs.org/
   - Verify: `node --version` and `npm --version`

3. **Git (optional for version control)**
   - Download: https://git-scm.com/download/win

#### macOS:
```bash
# Using Homebrew
brew install python nodejs
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip nodejs npm
```

---

## Installation Steps

### Step 1: Clone/Extract Project
```bash
# If using git
git clone <repository-url> heatguardmodel
cd heatguardmodel

# Or extract the provided ZIP file
```

### Step 2: Install Python Dependencies (Backend)
```bash
cd backend
pip install -r requirements.txt
cd ..
```

### Step 3: Install Node Modules (Frontend)
```bash
cd frontend
npm install
cd ..
```

### Step 4: Initialize Database (Optional - Auto-initializes)
```bash
cd backend
python -c "from app import create_app; app = create_app(); app.app_context().push()"
cd ..
```

---

## Running the Application

### Method 1: Automated Scripts (Recommended)

#### Windows PowerShell:
```bash
.\start-heatguard.ps1
```

#### Windows Command Prompt:
```bash
start-heatguard.bat
```

This will automatically:
- ✅ Check all requirements
- ✅ Install frontend dependencies if needed
- ✅ Start backend on port 5000
- ✅ Start frontend on port 5173
- ✅ Open the application in your browser

---

### Method 2: Manual Start (Two Terminals)

#### Terminal 1 - Start Backend:
```bash
cd backend
python app.py
```
✅ Backend runs on: `http://localhost:5000`

#### Terminal 2 - Start Frontend:
```bash
cd frontend
npm run dev
```
✅ Frontend runs on: `http://localhost:5173`

---

### Method 3: Production Build & Run

#### Build Frontend:
```bash
cd frontend
npm run build
cd ..
```

#### Run Backend (serves built frontend):
```bash
cd backend
python app.py
```

Access at: `http://localhost:5000`

---

## Production Deployment

### Docker Deployment (Recommended)

#### Prerequisites:
- Docker Desktop installed: https://www.docker.com/products/docker-desktop

#### Build and Run:
```bash
# Build images
docker-compose build

# Start services
docker-compose up

# Run in background
docker-compose up -d
```

**Access:** http://localhost

#### Stop Services:
```bash
docker-compose down
```

---

### Cloud Deployment Options

#### Option 1: Heroku
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-heatguard-app

# Deploy
git push heroku main

# See logs
heroku logs --tail
```

#### Option 2: AWS EC2
1. Launch EC2 instance (Ubuntu 20.04+)
2. Install Docker and Docker Compose
3. Clone repository
4. Update environment variables
5. Run `docker-compose up -d`

#### Option 3: DigitalOcean App Platform
1. Connect GitHub repository
2. Configure environment
3. Deploy via DigitalOcean dashboard

---

## Environment Variables

### Development (.env file)
```
FLASK_ENV=development
JWT_SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///instance/heatguard.db
FRONTEND_URL=http://localhost:5173
```

### Production (.env file)
```
FLASK_ENV=production
JWT_SECRET_KEY=<generate-strong-random-key>
DATABASE_URL=postgresql://user:pass@db-host:5432/heatguard
FRONTEND_URL=https://your-domain.com
CORS_ORIGINS=https://your-domain.com
```

---

## Test Accounts

### Worker Account
- **Username:** worker1
- **Password:** password123
- **Role:** Worker
- **Features:** Personal dashboard, vital tracking, risk assessment

### Supervisor Account
- **Username:** supervisor1
- **Password:** admin123
- **Role:** Supervisor
- **Features:** Multi-worker monitoring, analytics, alert management

### Create New Accounts
- Visit the registration page
- Fill in username, email, password
- Select role (Worker or Supervisor)
- Accounts are immediately active

---

## Key Endpoints

### Health & Status
```
GET  /api/health                    - System health check
GET  /model-test                    - ML model test page
```

### Authentication
```
POST /api/auth/register             - Create new account
POST /api/auth/login                - Login (returns JWT)
GET  /api/auth/me                   - Get current user (requires JWT)
POST /api/auth/logout               - Logout
```

### Predictions
```
POST /api/predictions/predict       - Get risk prediction (requires JWT)
POST /predict                       - Quick predict (no auth)
```

### Worker API
```
GET  /api/worker/profile            - Get worker profile
GET  /api/worker/metrics            - Get vital metrics
GET  /api/worker/alerts             - Get alerts
PUT  /api/worker/alerts/{id}/read   - Mark alert as read
```

### Supervisor API
```
GET  /api/supervisor/workers        - List all workers
GET  /api/supervisor/dashboard/stats - Dashboard statistics
GET  /api/supervisor/worker/{id}/history - Worker history
```

---

## Database

### Development (SQLite)
- **Location:** `backend/instance/heatguard.db`
- **Auto-initialized:** Yes
- **Reset:** Delete the database file

### Production (PostgreSQL)
```bash
# Create database
createdb heatguard

# Set environment variable
export DATABASE_URL=postgresql://user:password@localhost:5432/heatguard

# Database migrations (if applicable)
python -m alembic upgrade head
```

---

## Monitoring & Debugging

### Backend Logs
```bash
cd backend
python app.py       # See logs in console
```

### Frontend Development Issues
```bash
cd frontend
npm run dev         # See detailed output
```

### Model Performance Testing
```
Visit: http://localhost:5000/model-test
```

### API Testing
```bash
# Health check
curl http://localhost:5000/api/health

# Test prediction
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

## Troubleshooting

### Issue: Port Already in Use

**Port 5000 (Backend):**
```bash
# Windows - Find process
netstat -ano | findstr :5000

# Kill process (replace PID)
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

**Port 5173 (Frontend):**
```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5173
kill -9 <PID>
```

### Issue: Python Not Found
```bash
# Verify Python is installed
python --version

# If not in PATH, reinstall Python and check "Add Python to PATH"

# Use full path if needed
C:\Users\<username>\AppData\Local\Programs\Python\Python311\python.exe --version
```

### Issue: npm Packages Won't Install
```bash
# Clear cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -r frontend/node_modules frontend/package-lock.json

# Reinstall
cd frontend
npm install
```

### Issue: Backend Module Import Errors
```bash
# Reinstall dependencies
cd backend
pip install --upgrade -r requirements.txt

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
```

### Issue: Frontend Won't Load
```bash
# Clear browser cache (Ctrl+Shift+Delete)
# Hard refresh (Ctrl+Shift+R)

# Check if backend is running
curl http://localhost:5000/api/health

# Rebuild frontend
cd frontend
npm run build
```

### Issue: Database Errors
```bash
# Reset database (deletes all data!)
rm backend/instance/heatguard.db

# Restart backend to reinitialize
python app.py
```

---

## Performance Optimization

### Frontend
```bash
# Build production bundle
cd frontend
npm run build

# Analyze bundle
npm install -g webpack-bundle-analyzer
```

### Backend
```bash
# Use Gunicorn for production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Use PostgreSQL instead of SQLite
DATABASE_URL=postgresql://... python app.py
```

---

## Security Checklist

Before production deployment:

- [ ] Change `JWT_SECRET_KEY` to strong random value
- [ ] Set `FLASK_ENV=production`
- [ ] Enable HTTPS/SSL certificate
- [ ] Configure firewall rules
- [ ] Set strong database password
- [ ] Update CORS origins to your domain
- [ ] Remove debug endpoints in production
- [ ] Use environment variables for all secrets
- [ ] Set up database backups
- [ ] Configure monitoring and logging

---

## Support

### Additional Resources
- [README.md](README.md) - Project overview
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide

### Common Issues Resolution
1. Check error messages in terminal
2. Review logs in `backend/logs/` (if configured)
3. Test model at `/model-test` endpoint
4. Verify all ports are available
5. Ensure all dependencies are installed

---

**Ready to deploy?** Start with [QUICKSTART.md](QUICKSTART.md) or run `.\start-heatguard.ps1`
