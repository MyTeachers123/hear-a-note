#!/usr/bin/env bash
# After updating the code, run on EC2: bash /opt/toddler-music-box/deploy/update.sh
set -euo pipefail
cd /opt/toddler-music-box
git pull
.venv/bin/pip install -r requirements.txt -q
.venv/bin/python generate_assets.py
id toddler &>/dev/null || sudo useradd --system --no-create-home --shell /usr/sbin/nologin toddler
sudo chmod -R go-w /opt/toddler-music-box
sudo cp deploy/security-headers.conf /etc/nginx/snippets/toddler-music-box-security.conf
sed "s|__APP_DIR__|/opt/toddler-music-box|g" deploy/app-locations.conf | sudo tee /etc/nginx/snippets/toddler-music-box-app.conf > /dev/null
sed "s|__APP_DIR__|/opt/toddler-music-box|g" deploy/toddler-music-box.service | sudo tee /etc/systemd/system/toddler-music-box.service > /dev/null
sudo systemctl daemon-reload
sudo systemctl restart toddler-music-box
sudo nginx -t && sudo systemctl reload nginx
echo "✓ Updated. Remember: after frontend changes, bump VERSION in static/sw.js."
