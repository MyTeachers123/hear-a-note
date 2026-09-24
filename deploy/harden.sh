#!/usr/bin/env bash
# EC2 security hardening (run once after the site is live): bash /opt/toddler-music-box/deploy/harden.sh
#
#  1. SSH: key-only login, no root, no passwords, only the ubuntu user
#  2. Firewall (ufw): ports 80/443 only accept Cloudflare (nobody can bypass Cloudflare to hit the server)
#  3. fail2ban: bans IPs after repeated failed SSH logins
#  4. Automatic security updates
#  5. Read-only app: the backend runs as the low-privilege user "toddler", which can read but not write the code
#  6. Only root can read the certificate private key
#
# ⚠ Before running: keep this SSH window open; afterwards, test logging in from a NEW window.
set -euo pipefail
APP_DIR="/opt/toddler-music-box"

echo "==> 1/6 Hardening SSH"
# File name starts with 00-: sshd uses the first value it reads, so this must win over cloud-init's 50- file
sudo tee /etc/ssh/sshd_config.d/00-hardening.conf > /dev/null <<'EOF'
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
AuthenticationMethods publickey
AllowUsers ubuntu
MaxAuthTries 3
LoginGraceTime 30
X11Forwarding no
AllowAgentForwarding no
AllowTcpForwarding no
ClientAliveInterval 300
ClientAliveCountMax 2
EOF
sudo sshd -t                       # stop if the config is invalid, so you cannot lock yourself out
sudo systemctl reload ssh || sudo systemctl restart ssh

echo "==> 2/6 Firewall: ports 80/443 from Cloudflare only"
sudo apt-get install -y ufw curl > /dev/null
sudo ufw --force reset > /dev/null
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp comment 'SSH (restrict source IPs in the AWS Security Group)'
CF_V4=$(curl -fsSL https://www.cloudflare.com/ips-v4)
CF_V6=$(curl -fsSL https://www.cloudflare.com/ips-v6)
for ip in $CF_V4 $CF_V6; do
  sudo ufw allow proto tcp from "$ip" to any port 80,443 comment 'Cloudflare' > /dev/null
done
sudo ufw --force enable
echo "   Added $(echo $CF_V4 $CF_V6 | wc -w) Cloudflare IP ranges"

echo "==> 3/6 fail2ban (SSH brute-force protection)"
sudo apt-get install -y fail2ban python3-systemd > /dev/null
sudo tee /etc/fail2ban/jail.d/sshd.local > /dev/null <<'EOF'
[sshd]
enabled  = true
backend  = systemd
maxretry = 5
findtime = 10m
bantime  = 1h
EOF
sudo systemctl enable --now fail2ban
sudo systemctl restart fail2ban

echo "==> 4/6 Automatic security updates"
sudo apt-get install -y unattended-upgrades > /dev/null
sudo tee /etc/apt/apt.conf.d/20auto-upgrades > /dev/null <<'EOF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
EOF

echo "==> 5/6 Read-only app + low-privilege user"
id toddler &>/dev/null || sudo useradd --system --no-create-home --shell /usr/sbin/nologin toddler
sudo chown -R ubuntu:ubuntu "$APP_DIR"
sudo chmod -R go-w "$APP_DIR"            # only ubuntu can change files; toddler and nginx can only read
sed "s|__APP_DIR__|$APP_DIR|g" "$APP_DIR/deploy/toddler-music-box.service" \
  | sudo tee /etc/systemd/system/toddler-music-box.service > /dev/null
sudo systemctl daemon-reload
sudo systemctl restart toddler-music-box

echo "==> 6/6 Certificate private key permissions"
if [ -d /etc/ssl/cloudflare ]; then
  sudo chown -R root:root /etc/ssl/cloudflare
  sudo chmod 700 /etc/ssl/cloudflare
  # the glob must run as root: after chmod 700 the ubuntu user can no longer list this folder
  sudo find /etc/ssl/cloudflare -type f -name '*.key' -exec chmod 600 {} +
  sudo find /etc/ssl/cloudflare -type f -name '*.pem' -exec chmod 644 {} +
fi

sleep 2
echo
echo "================ Results ================"
printf "Backend health:        "; curl -s http://127.0.0.1:8000/api/health; echo
printf "Backend runs as:       "; ps -o user= -p "$(systemctl show -p MainPID --value toddler-music-box)"
printf "Can toddler write code? "; sudo -u toddler touch "$APP_DIR/test" 2>/dev/null && { echo "yes ✗"; rm -f "$APP_DIR/test"; } || echo "no ✓ (read-only)"
printf "SSH password login:    "; sudo sshd -T | grep -i '^passwordauthentication'
printf "SSH root login:        "; sudo sshd -T | grep -i '^permitrootlogin'
printf "fail2ban:              "; sudo fail2ban-client status sshd | grep 'Currently banned' | xargs
printf "systemd security score: "; systemd-analyze security toddler-music-box --no-pager 2>/dev/null | tail -1
sudo ufw status | head -5
echo
echo "⚠ Now open a NEW PowerShell window and log in with the same ssh command. Only close this window after that works."
