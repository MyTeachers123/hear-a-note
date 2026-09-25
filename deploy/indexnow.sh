#!/usr/bin/env bash
# Tell Bing (Copilot, Yahoo, DuckDuckGo use its index), Yandex, Seznam and Naver that pages changed.
# Run after each deploy:  bash /opt/hear-a-note/deploy/indexnow.sh
set -euo pipefail
main() {
  local host="kids.myteachers123.com"
  local key
  key=$(python3 -c "import sys; sys.path.insert(0, '$(dirname "$0")/..'); import seo_pages; print(seo_pages.INDEXNOW_KEY)")
  local urls='"https://'"$host"'/"'
  for l in en es zh-hant zh-hans ko ja vi fr it ru de hi; do
    urls="$urls,\"https://$host/learn/$l/\""
  done
  curl -sS -o /dev/null -w "IndexNow: HTTP %{http_code} (200 or 202 = accepted)\n" \
    -H "Content-Type: application/json; charset=utf-8" \
    -d "{\"host\":\"$host\",\"key\":\"$key\",\"keyLocation\":\"https://$host/$key.txt\",\"urlList\":[${urls}]}" \
    https://api.indexnow.org/indexnow
}
main "$@"
