#!/usr/bin/env bash
# One-time move of an existing server to the new name (folder, systemd service, Nginx files).
# Run once on EC2, then keep using update.sh as usual:
#   cd /opt/toddler-music-box && git remote set-url origin https://github.com/MyTeachers123/hear-a-note.git \
#     && git fetch origin && git reset --hard origin/main && bash deploy/migrate-server.sh
# The site is unavailable for about a minute while the folder moves and the Python environment is rebuilt.
set -euo pipefail
# Everything is inside main() so bash reads the whole script before the folder is moved
main() {
  local OLD_NAME="toddler-music-box" NEW_NAME="hear-a-note"
  local OLD="/opt/$OLD_NAME" NEW="/opt/$NEW_NAME"
  if [ -d "$NEW/.git" ]; then echo "✓ $NEW already exists — nothing to migrate. Use: bash $NEW/deploy/update.sh"; exit 0; fi
  [ -d "$OLD/.git" ] || { echo "✗ $OLD not found"; exit 1; }
  git -C "$OLD" remote set-url origin "https://github.com/MyTeachers123/$NEW_NAME.git"

  echo "==> 1/5 Stopping the old service"
  sudo systemctl disable --now "$OLD_NAME" 2>/dev/null || true

  echo "==> 2/5 Moving $OLD → $NEW"
  sudo mv "$OLD" "$NEW"
  sudo chown -R ubuntu:ubuntu "$NEW"
  cd "$NEW"

  echo "==> 3/5 Rebuilding the Python environment (a venv contains its absolute path)"
  rm -rf .venv
  python3 -m venv .venv
  .venv/bin/pip install --upgrade pip -q

  echo "==> 4/5 Renaming the Nginx site"
  if [ -f "/etc/nginx/sites-available/$OLD_NAME" ]; then
    sudo sed "s|$OLD_NAME|$NEW_NAME|g" "/etc/nginx/sites-available/$OLD_NAME" \
      | sudo tee "/etc/nginx/sites-available/$NEW_NAME" > /dev/null
    sudo ln -sf "/etc/nginx/sites-available/$NEW_NAME" "/etc/nginx/sites-enabled/$NEW_NAME"
    sudo rm -f "/etc/nginx/sites-enabled/$OLD_NAME"
  fi

  echo "==> 5/5 Installing the new service and Nginx snippets"
  bash "$NEW/deploy/update.sh"          # pip install, assets, snippets, systemd unit, restart, nginx reload
  sudo systemctl enable "$NEW_NAME"
  sudo rm -f "/etc/nginx/sites-available/$OLD_NAME" \
             "/etc/nginx/snippets/$OLD_NAME-app.conf" "/etc/nginx/snippets/$OLD_NAME-security.conf" \
             "/etc/systemd/system/$OLD_NAME.service"
  sudo systemctl daemon-reload
  sudo nginx -t && sudo systemctl reload nginx

  sleep 2
  printf "Backend health: "; curl -s http://127.0.0.1:8000/api/health || printf "not answering yet — check: sudo journalctl -u hear-a-note -n 50"; echo
  printf "Service:        "; systemctl is-active "$NEW_NAME" || true
  echo "✓ Done. From now on: bash $NEW/deploy/update.sh and bash $NEW/deploy/indexnow.sh"
}
main "$@"
exit
