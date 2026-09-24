#!/usr/bin/env bash
# 程式更新後，在 EC2 上執行：bash /opt/toddler-music-box/deploy/update.sh
set -euo pipefail
cd /opt/toddler-music-box
git pull
.venv/bin/pip install -r requirements.txt -q
.venv/bin/python generate_assets.py
sudo systemctl restart toddler-music-box
sudo systemctl reload nginx
echo "✓ 已更新。記得：前端有改動時，要把 static/sw.js 的 VERSION 加 1。"
