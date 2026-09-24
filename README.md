# Toddler Music Box 寶寶音樂盒

給幼兒的彩色鋼琴 PWA。Python 後端 (FastAPI) + HTML/JS 前端。
可離線、可加到主畫面、無廣告、不收集任何資料。

正式網址：https://kids.myteachers123.com

## 架構

```
toddler-music-box/
├── generate_assets.py      # Python：numpy 合成 8 個琴音、手寫 PNG 圖示、輸出兒歌 JSON
├── app.py                  # Python：FastAPI 後端（/api/songs、/api/health）
├── requirements.txt
├── deploy/
│   ├── setup.sh            # EC2 一鍵安裝（Nginx + Python + HTTPS）
│   ├── update.sh           # 更新程式用
│   ├── harden.sh           # 安全強化（SSH、防火牆、唯讀權限）
│   ├── security-headers.conf  # Nginx 安全標頭（CSP 等）
│   ├── app-locations.conf  # Nginx 共用設定（靜態檔、/api、快取）
│   ├── nginx-cloudflare.conf  # HTTPS 模式：Cloudflare Origin 憑證（預設）
│   ├── nginx.conf          # HTTPS 模式：Let's Encrypt
│   └── toddler-music-box.service   # systemd：開機自動啟動後端
└── static/                 # 前端（PWA）
    ├── index.html  style.css  app.js
    ├── sw.js               # Service Worker：離線快取
    ├── manifest.webmanifest
    ├── songs.json  sounds/*.wav  icons/*.png   # ← generate_assets.py 產生
```

```
使用者 ──HTTPS──> Cloudflare ──> Nginx (EC2) ──┬── 靜態檔 static/（網頁、音檔、圖示）
                                └── /api/* ──> uvicorn + FastAPI (127.0.0.1:8000)
```

## 本機執行

```bash
pip install -r requirements.txt
python generate_assets.py
uvicorn app:app --reload --port 8000
```
打開 http://localhost:8000

## 部署到 AWS EC2（Cloudflare SSL）

```
使用者 ──HTTPS──> Cloudflare（橘色雲朵）──HTTPS(Origin 憑證)──> EC2 Nginx ──> uvicorn
```

1. 開 EC2（Ubuntu 26.04 LTS），安全群組開 22 / 80 / 443，綁定 Elastic IP。
2. Cloudflare DNS：A 記錄 `kids` → Elastic IP，**Proxied（橘色雲朵）**。
3. Cloudflare → SSL/TLS → Origin Server → Create Certificate，把憑證和私鑰存到 EC2：
   `/etc/ssl/cloudflare/origin.pem`、`/etc/ssl/cloudflare/origin.key`
4. Cloudflare → SSL/TLS → Overview → 加密模式選 **Full (strict)**。
5. 在 EC2 執行：
   ```bash
   curl -fsSL https://raw.githubusercontent.com/MyTeachers123/toddler-music-box/main/deploy/setup.sh | bash
   ```
6. 安全強化（上線後執行一次）：`bash /opt/toddler-music-box/deploy/harden.sh`
7. 之後更新：`bash /opt/toddler-music-box/deploy/update.sh`，前端有改動時到 Cloudflare 清除快取（Caching → Purge Everything）。

不用 Cloudflare Proxy 時（灰色雲朵），改用 Let's Encrypt：
`curl -fsSL .../setup.sh | SSL_MODE=letsencrypt bash`

## 功能

- 8 個彩色大琴鍵（Do～高音 Do），每鍵不同形狀；高音 Do 同色＋向上箭頭＋頭頂一點
- 5 個黑鍵圖層（Do♯ Re♯ Fa♯ Sol♯ La♯），位置依白鍵動態計算，可用「♯ 黑鍵」開關顯示／隱藏
- 低延遲 Web Audio、多指同按
- 跟唱模式：小星星、小綿羊、音階（公領域曲目）
- 音量上限 70%、防誤觸（禁止縮放 / 長按選單）
- 電腦鍵盤：白鍵 A S D F G H J K，黑鍵 W E T Y U

## 更新前端時

修改 `static/` 內任何檔案後，把 `sw.js` 的 `VERSION` 改成下一版（例如 `toddler-music-box-v2`）。

## 防止寶寶誤觸退出

App 會自動做：
- 點開始時進入**全螢幕**（隱藏網址列和瀏覽器按鈕），並鎖定**橫向**（Android）
- 直立的手機／iPhone：畫面自動轉 90 度橫向顯示
- 攔截「返回」按鈕／手勢，不會離開 App
- 被滑出全螢幕時，蓋上「點一下繼續」畫面

網頁無法擋住系統的「回主畫面」手勢，建議家長再做：
- **加到主畫面**：用主畫面圖示開啟，完全沒有瀏覽器介面
- **iPhone / iPad：引導使用模式（Guided Access）**
  設定 → 輔助使用 → 引導使用模式 → 開啟並設密碼；打開 App 後連按三下側邊鍵開始，再連按三下輸入密碼結束
- **Android：固定應用程式（App pinning / 螢幕固定）**
  設定 → 安全性 → 固定應用程式 → 開啟；打開 App 後在「最近使用的應用程式」點圖示 → 固定

## 兒童隱私（COPPA）

不收集個資、沒有帳號、沒有廣告、沒有第三方追蹤。

## License

MIT
