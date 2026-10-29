# 🐈 CattenDock

A minimal, CasaOS-inspired homelab dashboard for **Debian 12**.
Manage Docker containers, deploy curated apps, and watch system stats from one web UI.

## Status
🚧 v0.1 — early prototype.

## Features
- [x] Web dashboard (React)
- [x] Container list / start / stop / remove
- [x] One-click deploy from YAML app catalog
- [x] CPU / RAM / disk / uptime stats
- [ ] Auth & multi-user
- [ ] File browser
- [ ] Storage / SMB management
- [ ] Custom `.deb` and ISO builds

## Quick start (dev)
```bash
# backend
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload

# frontend (separate terminal)
cd frontend
npm install
npm run dev
