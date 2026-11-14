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

## Install on Debian 12

Grab the latest `.deb` from [Releases](../../releases) and install:

```bash
sudo apt install ./cattendock_0.2.0_amd64.deb
```

Open `http://<your-host>:8000`, create the admin account, done.

```bash
cattendock status    # service health
cattendock logs      # tail logs
cattendock url       # print dashboard URL
```

- Config: `/etc/cattendock/cattendock.env`
- Data:   `/opt/cattendock/data/`
- `apt remove` keeps data; `apt purge` wipes it.

### Build the package yourself

```bash
# on Debian 12 (or `docker run --rm -it -v $PWD:/src -w /src debian:bookworm`)
sudo apt install python3-venv python3-pip python3-dev nodejs npm dpkg-dev build-essential
make deb        # → build/cattendock_0.2.0_amd64.deb
```
