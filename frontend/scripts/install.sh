#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${CATTENDOCK_REPO:-https://github.com/Xerone0/CattenDock.git}"
INSTALL_DIR=/opt/cattendock

if [[ $EUID -ne 0 ]]; then
  echo "Please run as root (sudo $0)"; exit 1
fi

echo ">> Installing dependencies"
apt-get update
apt-get install -y python3 python3-venv python3-pip docker.io nodejs npm git

echo ">> Fetching CattenDock"
rm -rf "$INSTALL_DIR"
git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
chown -R root:root "$INSTALL_DIR"

echo ">> Building frontend"
cd "$INSTALL_DIR/frontend"
npm install
npm run build
rm -rf "$INSTALL_DIR/backend/app/static"
cp -r dist "$INSTALL_DIR/backend/app/static"

echo ">> Setting up backend venv"
cd "$INSTALL_DIR/backend"
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

echo ">> Installing systemd service"
cp "$INSTALL_DIR/scripts/cattendock.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now cattendock

echo ">> Done. Open http://$(hostname -I | awk '{print $1}'):8000"
