#!/usr/bin/env bash
# 在全新的 EC2 (Ubuntu 24.04 或 26.04 LTS) 上執行一次即可：
#   curl -fsSL https://raw.githubusercontent.com/MyTeachers123/toddler-music-box/main/deploy/setup.sh | bash
# 會完成：安裝套件 → 下載程式 → 產生音檔 → 啟動 Python 後端 → 設定 Nginx → 設定 HTTPS
#
# HTTPS 有兩種模式（SSL_MODE）：
#   cloudflare（預設）：網域在 Cloudflare、橘色雲朵開啟。需先把 Cloudflare Origin Certificate
#                       存到 /etc/ssl/cloudflare/origin.pem 與 origin.key
#   letsencrypt       ：DNS 直接指向 EC2（灰色雲朵），自動申請 Let's Encrypt 憑證
#     SSL_MODE=letsencrypt bash setup.sh
set -euo pipefail

DOMAIN="${DOMAIN:-kids.myteachers123.com}"
EMAIL="${EMAIL:-info@myteachers123.com}"
REPO="${REPO:-https://github.com/MyTeachers123/toddler-music-box.git}"
APP_DIR="/opt/toddler-music-box"
SSL_MODE="${SSL_MODE:-cloudflare}"

echo "==> 1/6 安裝系統套件"
sudo apt-get update -y
sudo apt-get install -y git nginx python3-venv
if [ "$SSL_MODE" = "letsencrypt" ]; then sudo apt-get install -y certbot python3-certbot-nginx; fi

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

echo "==> 4/6 啟動 Python 後端 (systemd，低權限帳號 toddler)"
id toddler &>/dev/null || sudo useradd --system --no-create-home --shell /usr/sbin/nologin toddler
sudo chmod -R go-w "$APP_DIR"
sed "s|__APP_DIR__|$APP_DIR|g" deploy/toddler-music-box.service \
  | sudo tee /etc/systemd/system/toddler-music-box.service > /dev/null
sudo systemctl daemon-reload
sudo systemctl enable --now toddler-music-box
sudo systemctl restart toddler-music-box

echo "==> 5/6 設定 Nginx（模式：$SSL_MODE）"
sudo mkdir -p /etc/nginx/snippets
sudo cp deploy/security-headers.conf /etc/nginx/snippets/toddler-music-box-security.conf
sed "s|__APP_DIR__|$APP_DIR|g" deploy/app-locations.conf \
  | sudo tee /etc/nginx/snippets/toddler-music-box-app.conf > /dev/null
if [ "$SSL_MODE" = "cloudflare" ]; then
  if [ ! -s /etc/ssl/cloudflare/origin.pem ] || [ ! -s /etc/ssl/cloudflare/origin.key ]; then
    echo "✗ 找不到 Cloudflare Origin 憑證。請先建立："
    echo "    sudo mkdir -p /etc/ssl/cloudflare"
    echo "    sudo nano /etc/ssl/cloudflare/origin.pem   # 貼上 Origin Certificate"
    echo "    sudo nano /etc/ssl/cloudflare/origin.key   # 貼上 Private Key"
    echo "  然後重新執行本腳本。"
    exit 1
  fi
  sudo chmod 600 /etc/ssl/cloudflare/origin.key
  CONF=deploy/nginx-cloudflare.conf
else
  CONF=deploy/nginx.conf
fi
sed "s|__DOMAIN__|$DOMAIN|g" "$CONF" \
  | sudo tee /etc/nginx/sites-available/toddler-music-box > /dev/null
sudo ln -sf /etc/nginx/sites-available/toddler-music-box /etc/nginx/sites-enabled/toddler-music-box
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx

echo "==> 6/6 HTTPS"
if [ "$SSL_MODE" = "cloudflare" ]; then
  echo "✓ 使用 Cloudflare Origin 憑證。請確認 Cloudflare → SSL/TLS 模式為 Full (strict)。"
elif sudo certbot --nginx -d "$DOMAIN" -m "$EMAIL" --agree-tos --redirect --non-interactive; then
  echo "✓ Let's Encrypt HTTPS 完成"
else
  echo "⚠ 憑證申請失敗：通常是 DNS 還沒生效。等 DNS 指向這台主機後，重新執行本腳本即可。"
fi

echo
echo "完成！檢查："
curl -s http://127.0.0.1:8000/api/health && echo
echo "打開 https://$DOMAIN"
echo "建議接著執行安全強化：bash $APP_DIR/deploy/harden.sh"
