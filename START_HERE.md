# 🚀 START HERE - HeatGuard System

> **Everything is already set up for you. Just follow these 3 steps.**

---

## ⚡ STEP 1: Check You Have What You Need

Open PowerShell and run these commands:

```powershell
python --version
node --version
npm --version
```

**All show version numbers?** ✅ Go to Step 2

**One says "not found"?**
- Python not found? → https://www.python.org/
- Node not found? → https://nodejs.org/ (includes npm)

---

## ⚡ STEP 2: Install Dependencies (First Time Only)

```powershell
cd frontend
npm install
cd..
```

This downloads required packages. Should take ~2-3 minutes.

---

## ⚡ STEP 3: Start Everything!

```powershell
.\start-heatguard.ps1
```

**What happens:**
- ✅ Backend starts on http://localhost:5000
- ✅ Frontend starts on http://localhost:5173  
- ✅ Browser opens automatically

---

## 🎮 Login & Test

Browser should open automatically. If not:
👉 Go to: **http://localhost:5173**

**Use these credentials:**
- Username: **worker1**
- Password: **password123**

**Or register a new account!**

---

## ✅ You're Done!

You now have:
- ✅ Web-based worker heat monitoring
- ✅ Real-time risk assessment
- ✅ AI-powered predictions
- ✅ Multi-user dashboards
- ✅ Supervisor controls

---

## 🆘 Quick Fixes

### "Port already in use?"
```powershell
netstat -ano | findstr :5000
taskkill /PID <number> /F
```

### "Python/npm not found?"
- Reinstall from links above
- Restart PowerShell after install

### "npm install failed?"
```powershell
npm cache clean --force
cd frontend
npm install
```

---

## 📚 Need More Info?

| Want | Read |
|------|------|
| Quick setup guide | [QUICKSTART.md](QUICKSTART.md) |
| How to run system | [RUN.md](RUN.md) |
| API reference | [API_DOCUMENTATION.md](API_DOCUMENTATION.md) |
| Deployment guide | [DEPLOYMENT.md](DEPLOYMENT.md) |
| All documentation | [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) |

---

## 🎯 Next Steps

1. **Just Started?** Explore the dashboards after login
2. **Want to test predictions?** Try the Digital Twin simulator
3. **Want to deploy?** See [DEPLOYMENT.md](DEPLOYMENT.md)
4. **Want to customize?** Edit `.env` file

---

## 🎉 That's It!

**Everything is ready to go.** Just run:

```powershell
.\start-heatguard.ps1
```

**Good luck! 🔥**

---

For detailed information, see [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
