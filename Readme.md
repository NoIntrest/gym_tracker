# 🏋 IronForge — Advanced Gym Tracker

A full-featured gym tracking web app built with Python + Streamlit.

## Features
- 60 exercises across 12 muscle groups
- XP & level system (7 levels: Novice → Legend)
- Rest timer with presets
- Body weight tracker with progress chart
- Workout history & statistics with charts
- 20 unlockable badges
- 8 pre-built workout plans
- Personal records per exercise
- Data export/import (JSON)

---

## 🚀 Deploy on Render (Step by Step)

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "IronForge gym tracker"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ironforge.git
git push -u origin main
```

### 2. Deploy on Render
1. Go to **[render.com](https://render.com)** and sign in (free account works)
2. Click **New → Web Service**
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` — click **Create Web Service**
5. Wait ~2 minutes for the build to finish
6. Your app is live at `https://ironforge-gym-tracker.onrender.com`

### Manual settings (if not using render.yaml)
| Setting | Value |
|---|---|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true` |

---

## 💾 Data Persistence Note
Render's **free tier** has an ephemeral filesystem — data resets on redeploy.

**Options to keep data permanently:**
- **Render Paid Tier** → Add a Persistent Disk in the service settings
- **Use a database** → Replace JSON file storage with SQLite + SQLAlchemy or a free PostgreSQL instance (Render offers one free Postgres DB)

---

## 🏃 Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
App opens at `http://localhost:8501`