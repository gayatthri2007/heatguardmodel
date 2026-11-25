# 🔥 HeatGuard - Worker Heat Safety Monitoring System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Node.js 14+](https://img.shields.io/badge/node-14+-green.svg)](https://nodejs.org/)
[![Flask 2.3+](https://img.shields.io/badge/flask-2.3+-red.svg)](https://flask.palletsprojects.com/)
[![React 18+](https://img.shields.io/badge/react-18+-blue.svg)](https://react.dev/)

A comprehensive **digital twin-based heat stress monitoring system** for occupational worker safety in high-temperature environments.

---

## 🎯 Overview

HeatGuard is an intelligent monitoring system designed to protect workers in hot environments by:
- **Real-time monitoring** of vital signs and environmental conditions
- **AI-powered risk assessment** using ML models and digital twin logic
- **Multi-level dashboards** for workers and supervisors
- **Proactive alerts** for heat stress prevention

---

## ✨ Key Features

### 🔥 4-Pillar Digital Twin Logic
- **Baseline Adjustment:** Account for individual differences (BMI, fitness)
- **Environmental Analysis:** WBGT, temperature, humidity, radiant heat
- **Cooling Intervention:** Model effect of cooling breaks
- **DTHS Calculation:** Digital Heat Strain Score + ML prediction

### 👷 Worker Features
- ✅ Real-time risk assessment dashboard
- ✅ Digital Twin simulation with interactive scenarios
- ✅ Alert notifications and history
- ✅ Personal vital metrics tracking
- ✅ Heat strain history and trends

### 👨‍💼 Supervisor Features
- ✅ Multi-worker monitoring dashboard
- ✅ Zone-based worker management
- ✅ Risk distribution analytics
- ✅ Alert management and escalation
- ✅ Workforce health insights and reports

### 🤖 AI/ML Capabilities
- ✅ Random Forest heat stress prediction
- ✅ Real-time risk scoring
- ✅ Pattern recognition and trend analysis
- ✅ Personalized recommendations

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         Frontend (React + Vite)             │
│  http://localhost:5173                      │
└────────────┬────────────────────────────────┘
             │
             ├─ /api/auth (authentication)
             ├─ /api/predictions (ML predictions)
             ├─ /api/worker (worker endpoints)
             └─ /api/supervisor (supervisor endpoints)
             │
┌────────────▼────────────────────────────────┐
│     Backend (Flask + SQLAlchemy)            │
│  http://localhost:5000                      │
└────────────┬────────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼────────┐  ┌────▼──────────────┐
│  SQLite    │  │  ML Engine        │
│  Database  │  │  (Models & Logic) │
└────────────┘  └───────────────────┘
```

---

## 🚀 Quick Start

### Option 1: Windows Automated Script (Recommended)
```bash
# PowerShell
.\start-heatguard.ps1

# Or Command Prompt
start-heatguard.bat
```

### Option 2: Manual Setup
```bash
# Terminal 1 - Backend
cd backend
pip install -r requirements.txt
python app.py

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

### Access Points
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5000
- **Model Test:** http://localhost:5000/model-test

---

## 👤 Test Accounts

| Role | Username | Password | Features |
|------|----------|----------|----------|
| **Worker** | worker1 | password123 | Dashboard, Vital tracking |
| **Supervisor** | supervisor1 | admin123 | Multi-worker monitoring |
| **Admin** | admin | admin123 | Full access |

---

## 📋 Prerequisites

### System Requirements
- **OS:** Windows, macOS, or Linux
- **RAM:** 4 GB minimum
- **Storage:** 500 MB free space

### Required Software
- **Python 3.8+** → https://www.python.org/downloads/
- **Node.js 14+ (LTS)** → https://nodejs.org/
- **Docker (Optional)** → https://www.docker.com/

---

## 📦 Tech Stack

### Backend
| Component | Technology |
|-----------|-----------|
| Framework | Flask 2.3.3 |
| Database | SQLAlchemy ORM (SQLite/PostgreSQL) |
| Auth | JWT (Flask-JWT-Extended) |
| ML Models | scikit-learn, pandas |
| CORS | Flask-CORS |

### Frontend
| Component | Technology |
|-----------|-----------|
| Framework | React 18.2.0 |
| Build Tool | Vite 4.4.5 |
| Routing | React Router v6 |
| HTTP | Axios |
| Charts | Recharts |
| Icons | Lucide React |

### Database
- **Development:** SQLite (auto-initialized)
- **Production:** PostgreSQL

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[QUICKSTART.md](QUICKSTART.md)** | Fast setup guide (recommended) |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Comprehensive deployment guide |
| **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** | Full API reference |
| **[SETUP_GUIDE.md](SETUP_GUIDE.md)** | Detailed configuration guide |

---

## 🔌 API Endpoints

### Public (No Auth)
```
GET  /api/health              # System health check
POST /predict                 # Quick ML prediction
GET  /model-test              # Model diagnostics page
```

### Authentication
```
POST /api/auth/register        # Register new user
POST /api/auth/login           # Login (returns JWT)
GET  /api/auth/me              # Get current user
POST /api/auth/logout          # Logout
```

### Worker APIs
```
GET  /api/worker/profile       # Worker information
GET  /api/worker/metrics       # Vital metrics history
GET  /api/worker/alerts        # Alert history
PUT  /api/worker/alerts/{id}   # Mark alert as read
```

### Supervisor APIs
```
GET  /api/supervisor/workers   # List all workers
GET  /api/supervisor/dashboard/stats   # Dashboard stats
GET  /api/supervisor/worker/{id}/history  # Worker history
```

### Predictions
```
POST /api/predictions/predict  # Get risk prediction
```

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for full details.

---

## 🐳 Docker Deployment

### Build and Run
```bash
# Build images
docker-compose build

# Start services
docker-compose up

# Run in background
docker-compose up -d

# Stop services
docker-compose down
```

**Access:** http://localhost (frontend on port 80)

---

## 🔍 Key Files

```
heatguardmodel/
├── backend/                           # Flask backend
│   ├── app.py                        # Main application
│   ├── config.py                     # Configuration
│   ├── requirements.txt               # Python dependencies
│   ├── database/                     # Database setup
│   ├── models/                       # Data models (User, Worker, etc.)
│   ├── routes/                       # API endpoints
│   ├── ml_engine/                    # ML logic & digital twin
│   └── utils/                        # Utilities
│
├── frontend/                          # React application
│   ├── package.json                  # Node dependencies
│   ├── vite.config.js                # Vite configuration
│   ├── src/
│   │   ├── App.jsx                   # Main app component
│   │   ├── pages/                    # Page components
│   │   ├── components/               # React components
│   │   ├── api/                      # API client
│   │   └── styles/                   # Global styles
│   └── public/                       # Static assets
│
├── data/                              # Sample datasets
├── models/                            # ML models (pickle files)
│
├── QUICKSTART.md                      # Fast start (recommended!)
├── DEPLOYMENT.md                      # Deployment guide
├── API_DOCUMENTATION.md               # API reference
├── docker-compose.yml                 # Docker configuration
├── .env                               # Environment variables
└── start-heatguard.ps1/bat           # Startup scripts
```

---

## 🧪 Testing

### Test Model Predictions
Visit: `http://localhost:5000/model-test`

### Test with cURL
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

### Test the System
1. Register a new account at http://localhost:5173
2. Login with credentials
3. Try the Digital Twin simulation
4. Check alerts and metrics
5. (As Supervisor) Monitor multiple workers

---

## 🐛 Troubleshooting

### Quick Fixes
```bash
# Port already in use?
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Reset database
rm backend/instance/heatguard.db

# Reinstall frontend
rm -r frontend/node_modules frontend/package-lock.json
cd frontend
npm install
```

See [DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting) for detailed troubleshooting.

---

## 🚀 Production Deployment

### Cloud Options
- **Heroku** - Easy deployment via git push
- **AWS EC2** - Full control with Docker
- **DigitalOcean** - Simple and affordable
- **Docker** - Container-based deployment

### Setup
1. Follow [DEPLOYMENT.md](DEPLOYMENT.md)
2. Update `.env` with production values
3. Configure database (PostgreSQL recommended)
4. Set up HTTPS/SSL
5. Configure firewall rules

---

## 🔐 Security

### Development
- Debug mode enabled
- SQLite database
- JWT secret: change in production

### Production Checklist
- [ ] Change `JWT_SECRET_KEY`
- [ ] Set `FLASK_ENV=production`
- [ ] Enable HTTPS/SSL
- [ ] Use PostgreSQL database
- [ ] Configure CORS origins
- [ ] Set strong database password
- [ ] Enable monitoring and logging
- [ ] Backup database regularly

---

## 📊 Data & Privacy

- **No external data transmission** during local deployment
- **HTTPS required** for production
- **Database encryption** recommended for sensitive data
- **User data** stored securely with hashed passwords

---

## 🤝 Contributing

To contribute to HeatGuard:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

This project is provided as-is for occupational safety purposes.

---

## 🆘 Support

### Getting Help
1. Check **[QUICKSTART.md](QUICKSTART.md)** for quick solutions
2. Review **[DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting)** for troubleshooting
3. Check **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** for API issues
4. Review **[SETUP_GUIDE.md](SETUP_GUIDE.md)** for detailed setup

### Common Issues
- **Port in use?** → See port reset commands above
- **Python not found?** → Reinstall Python, check PATH
- **npm not working?** → Reinstall Node.js
- **Database errors?** → Delete heatguard.db and restart

---

## 📈 Next Steps

1. **Get Started:** Run `.\start-heatguard.ps1` (Windows) or follow [QUICKSTART.md](QUICKSTART.md)
2. **Test System:** Create account, explore dashboards
3. **Read API Docs:** Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
4. **Deploy:** Follow [DEPLOYMENT.md](DEPLOYMENT.md) for production

---

## 🙏 Thank You

Thank you for using HeatGuard! For worker safety in extreme heat conditions.

---

**Ready to start?** Head to [QUICKSTART.md](QUICKSTART.md) or run:
```bash
.\start-heatguard.ps1    # Windows PowerShell
start-heatguard.bat      # Windows Command Prompt
```

**Questions?** Check the [documentation](DEPLOYMENT.md) or the [API reference](API_DOCUMENTATION.md).
