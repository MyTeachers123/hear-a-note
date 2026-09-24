#!/usr/bin/env bash
# EC2 安全強化（網站上線後執行一次）：bash /opt/toddler-music-box/deploy/harden.sh
#
#  1. SSH：只允許金鑰登入、禁止 root、禁止密碼、只允許 ubuntu 帳號
#  2. 防火牆 (ufw)：80/443 只接受 Cloudflare 的連線（別人無法繞過 Cloudflare 直連主機）
#  3. fail2ban：SSH 連續輸錯就封鎖該 IP
#  4. 自動安裝安全性更新
#  5. 程式唯讀：後端改用低權限帳號 toddler 執行，程式檔案它只能讀不能寫
#  6. 憑證私鑰只有 root 能讀
#
# ⚠ 執行前：保持目前這個 SSH 視窗不要關；執行後另開一個新視窗測試能否登入。
set -euo pipefail
APP_DIR="/opt/toddler-music-box"

echo "==> 1/6 SSH 強化"
# 檔名用 00- 開頭：sshd 採用「第一個讀到的值」，要比 cloud-init 的 50- 設定優先
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
sudo sshd -t                       # 設定有錯就停止，不會把自己鎖在外面
sudo systemctl reload ssh || sudo systemctl restart ssh

echo "==> 2/6 防火牆：80/443 只允許 Cloudflare"
sudo apt-get install -y ufw curl > /dev/null
sudo ufw --force reset > /dev/null
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp comment 'SSH (AWS Security Group 再限制來源 IP)'
CF_V4=$(curl -fsSL https://www.cloudflare.com/ips-v4)
CF_V6=$(curl -fsSL https://www.cloudflare.com/ips-v6)
for ip in $CF_V4 $CF_V6; do
  sudo ufw allow proto tcp from "$ip" to any port 80,443 comment 'Cloudflare' > /dev/null
done
sudo ufw --force enable
echo "   已加入 $(echo $CF_V4 $CF_V6 | wc -w) 個 Cloudflare 網段"

echo "==> 3/6 fail2ban（SSH 防暴力破解）"
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

echo "==> 4/6 自動安全性更新"
sudo apt-get install -y unattended-upgrades > /dev/null
sudo tee /etc/apt/apt.conf.d/20auto-upgrades > /dev/null <<'EOF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
EOF

echo "==> 5/6 程式唯讀 + 低權限帳號"
id toddler &>/dev/null || sudo useradd --system --no-create-home --shell /usr/sbin/nologin toddler
sudo chown -R ubuntu:ubuntu "$APP_DIR"
sudo chmod -R go-w "$APP_DIR"            # 只有 ubuntu 能改檔案；toddler 和 nginx 只能讀
sed "s|__APP_DIR__|$APP_DIR|g" "$APP_DIR/deploy/toddler-music-box.service" \
  | sudo tee /etc/systemd/system/toddler-music-box.service > /dev/null
sudo systemctl daemon-reload
sudo systemctl restart toddler-music-box

echo "==> 6/6 憑證私鑰權限"
if [ -d /etc/ssl/cloudflare ]; then
  sudo chown -R root:root /etc/ssl/cloudflare
  sudo chmod 700 /etc/ssl/cloudflare
  sudo chmod 600 /etc/ssl/cloudflare/*.key
  sudo chmod 644 /etc/ssl/cloudflare/*.pem
fi

sleep 2
echo
echo "================ 檢查結果 ================"
printf "後端健康檢查：    "; curl -s http://127.0.0.1:8000/api/health; echo
printf "後端執行帳號：    "; ps -o user= -p "$(systemctl show -p MainPID --value toddler-music-box)"
printf "toddler 能寫程式嗎："; sudo -u toddler touch "$APP_DIR/test" 2>/dev/null && { echo "能 ✗"; rm -f "$APP_DIR/test"; } || echo "不能 ✓（唯讀）"
printf "SSH 密碼登入：    "; sudo sshd -T | grep -i '^passwordauthentication'
printf "SSH root 登入：   "; sudo sshd -T | grep -i '^permitrootlogin'
printf "fail2ban：        "; sudo fail2ban-client status sshd | grep 'Currently banned' | xargs
printf "systemd 安全評分："; systemd-analyze security toddler-music-box --no-pager 2>/dev/null | tail -1
sudo ufw status | head -5
echo
echo "⚠ 現在請另開一個新的 PowerShell 視窗，用同樣的 ssh 指令測試能否登入，成功後才關閉這個視窗。"
