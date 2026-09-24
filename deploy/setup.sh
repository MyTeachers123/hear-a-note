#!/usr/bin/env bash
# 在全新的 EC2 (Ubuntu 24.04) 上執行一次即可：
#   curl -fsSL https://raw.githubusercontent.com/MyTeachers123/toddler-music-box/main/deploy/setup.sh | bash
# 會完成：安裝套件 → 下載程式 → 產生音檔 → 啟動 Python 後端 → 設定 Nginx → 申請免費 HTTPS 憑證
set -euo pipefail

DOMAIN="${DOMAIN:-kids.myteachers123.com}"
EMAIL="${EMAIL:-info@myteachers123.com}"
REPO="${REPO:-https://github.com/MyTeachers123/toddler-music-box.git}"
APP_DIR="/opt/toddler-music-box"

echo "==> 1/6 安裝系統套件"
sudo apt-get update -y
sudo apt-get install -y git nginx python3-venv certbot python3-certbot-nginx

echo "==> 2/6 下載程式碼到 $APP_DIR"
if [ -d "$APP_DIR/.git" ]; then
  sudo git -C "$APP_DIR" pull
else
  sudo git clone "$REPO" "$APP_DIR"
fi
sudo chown -R ubuntu:ubuntu "$APP_DIR"
sudo chmod 755 /opt "$APP_DIR"

echo "==> 3/6 建立 Python 環境並產生音檔/圖示"
cd "$APP_DIR"
python3 -m venv .venv
.venv/bin/pip install --upgrade pip -q
.venv/bin/pip install -r requirements.txt -q
.venv/bin/python generate_assets.py

echo "==> 4/6 啟動 Python 後端 (systemd)"
sed "s|__APP_DIR__|$APP_DIR|g" deploy/toddler-music-box.service \
  | sudo tee /etc/systemd/system/toddler-music-box.service > /dev/null
sudo systemctl daemon-reload
sudo systemctl enable --now toddler-music-box
sudo systemctl restart toddler-music-box

echo "==> 5/6 設定 Nginx"
sed "s|__DOMAIN__|$DOMAIN|g; s|__APP_DIR__|$APP_DIR|g" deploy/nginx.conf \
  | sudo tee /etc/nginx/sites-available/toddler-music-box > /dev/null
sudo ln -sf /etc/nginx/sites-available/toddler-music-box /etc/nginx/sites-enabled/toddler-music-box
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx

echo "==> 6/6 申請 HTTPS 憑證 (Let's Encrypt，免費，自動續約)"
if sudo certbot --nginx -d "$DOMAIN" -m "$EMAIL" --agree-tos --redirect --non-interactive; then
  echo "✓ HTTPS 完成"
else
  echo "⚠ 憑證申請失敗：通常是 DNS 還沒生效。等 DNS 指向這台主機後，重新執行本腳本即可。"
fi

echo
echo "完成！檢查："
curl -s http://127.0.0.1:8000/api/health && echo
echo "打開 https://$DOMAIN"
