#!/usr/bin/env bash
# Run once on a fresh EC2 instance (Ubuntu 24.04 or 26.04 LTS):
#   curl -fsSL https://raw.githubusercontent.com/MyTeachers123/hear-a-note/main/deploy/setup.sh | bash
# It installs packages → downloads the code → generates sounds → starts the Python backend → configures Nginx → sets up HTTPS
#
# Two HTTPS modes (SSL_MODE):
#   cloudflare (default): domain on Cloudflare with the orange cloud on. First save the Cloudflare Origin Certificate
#                         to /etc/ssl/cloudflare/origin.pem and origin.key
#   letsencrypt         : DNS points straight at EC2 (grey cloud); a Let's Encrypt certificate is requested automatically
#     SSL_MODE=letsencrypt bash setup.sh
set -euo pipefail

DOMAIN="${DOMAIN:-kids.myteachers123.com}"
EMAIL="${EMAIL:-info@myteachers123.com}"
REPO="${REPO:-https://github.com/MyTeachers123/hear-a-note.git}"
APP_DIR="/opt/hear-a-note"
SSL_MODE="${SSL_MODE:-cloudflare}"

echo "==> 1/6 Installing system packages"
sudo apt-get update -y
sudo apt-get install -y git nginx python3-venv
if [ "$SSL_MODE" = "letsencrypt" ]; then sudo apt-get install -y certbot python3-certbot-nginx; fi

echo "==> 2/6 Downloading code to $APP_DIR"
if [ -d "$APP_DIR/.git" ]; then
  sudo git -C "$APP_DIR" pull
else
  sudo git clone "$REPO" "$APP_DIR"
fi
sudo chown -R ubuntu:ubuntu "$APP_DIR"
sudo chmod 755 /opt "$APP_DIR"

echo "==> 3/6 Creating the Python environment and generating sounds/icons"
cd "$APP_DIR"
python3 -m venv .venv
.venv/bin/pip install --upgrade pip -q
.venv/bin/pip install -r requirements.txt -q
.venv/bin/python generate_assets.py

echo "==> 4/6 Starting the Python backend (systemd, low-privilege user toddler)"
id toddler &>/dev/null || sudo useradd --system --no-create-home --shell /usr/sbin/nologin toddler
sudo chmod -R go-w "$APP_DIR"
sed "s|__APP_DIR__|$APP_DIR|g" deploy/hear-a-note.service \
  | sudo tee /etc/systemd/system/hear-a-note.service > /dev/null
sudo systemctl daemon-reload
sudo systemctl enable --now hear-a-note
sudo systemctl restart hear-a-note

echo "==> 5/6 Configuring Nginx (mode: $SSL_MODE)"
sudo mkdir -p /etc/nginx/snippets
sudo cp deploy/security-headers.conf /etc/nginx/snippets/hear-a-note-security.conf
sed "s|__APP_DIR__|$APP_DIR|g" deploy/app-locations.conf \
  | sudo tee /etc/nginx/snippets/hear-a-note-app.conf > /dev/null
if [ "$SSL_MODE" = "cloudflare" ]; then
  if [ ! -s /etc/ssl/cloudflare/origin.pem ] || [ ! -s /etc/ssl/cloudflare/origin.key ]; then
    echo "✗ Cloudflare Origin certificate not found. Create it first:"
    echo "    sudo mkdir -p /etc/ssl/cloudflare"
    echo "    sudo nano /etc/ssl/cloudflare/origin.pem   # paste the Origin Certificate"
    echo "    sudo nano /etc/ssl/cloudflare/origin.key   # paste the Private Key"
    echo "  Then run this script again."
    exit 1
  fi
  sudo chmod 600 /etc/ssl/cloudflare/origin.key
  CONF=deploy/nginx-cloudflare.conf
else
  CONF=deploy/nginx.conf
fi
sed "s|__DOMAIN__|$DOMAIN|g" "$CONF" \
  | sudo tee /etc/nginx/sites-available/hear-a-note > /dev/null
sudo ln -sf /etc/nginx/sites-available/hear-a-note /etc/nginx/sites-enabled/hear-a-note
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx

echo "==> 6/6 HTTPS"
if [ "$SSL_MODE" = "cloudflare" ]; then
  echo "✓ Using the Cloudflare Origin certificate. Make sure Cloudflare → SSL/TLS mode is Full (strict)."
elif sudo certbot --nginx -d "$DOMAIN" -m "$EMAIL" --agree-tos --redirect --non-interactive; then
  echo "✓ Let's Encrypt HTTPS done"
else
  echo "⚠ Certificate request failed — usually DNS has not propagated yet. Once DNS points to this server, run this script again."
fi

echo
echo "Done! Checks:"
curl -s http://127.0.0.1:8000/api/health && echo
echo "Open https://$DOMAIN"
echo "Recommended next step — security hardening: bash $APP_DIR/deploy/harden.sh"
