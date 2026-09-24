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
│   ├── nginx.conf          # Nginx 設定
│   └── toddler-music-box.service   # systemd：開機自動啟動後端
└── static/                 # 前端（PWA）
    ├── index.html  style.css  app.js
    ├── sw.js               # Service Worker：離線快取
    ├── manifest.webmanifest
    ├── songs.json  sounds/*.wav  icons/*.png   # ← generate_assets.py 產生
```

```
使用者 ──HTTPS──> Nginx (EC2) ──┬── 靜態檔 static/（網頁、音檔、圖示）
                                └── /api/* ──> uvicorn + FastAPI (127.0.0.1:8000)
```

## 本機執行

```bash
pip install -r requirements.txt
python generate_assets.py
uvicorn app:app --reload --port 8000
```
打開 http://localhost:8000

## 部署到 AWS EC2

1. 開 EC2（Ubuntu 24.04），安全群組開 22 / 80 / 443。
2. 綁定 Elastic IP，在網域 DNS 加 A 記錄：`kids` → Elastic IP。
3. 連線到 EC2 後執行：
   ```bash
   curl -fsSL https://raw.githubusercontent.com/MyTeachers123/toddler-music-box/main/deploy/setup.sh | bash
   ```
4. 之後更新：`bash /opt/toddler-music-box/deploy/update.sh`

## 功能

- 8 個彩色大琴鍵（Do～高音 Do），每鍵不同形狀
- 低延遲 Web Audio、多指同按
- 跟唱模式：小星星、小綿羊、音階（公領域曲目）
- 音量上限 70%、防誤觸（禁止縮放 / 長按選單）
- 電腦鍵盤 A S D F G H J K 也能彈

## 更新前端時

修改 `static/` 內任何檔案後，把 `sw.js` 的 `VERSION` 改成下一版（例如 `toddler-music-box-v2`）。

## 兒童隱私（COPPA）

不收集個資、沒有帳號、沒有廣告、沒有第三方追蹤。

## License

MIT
