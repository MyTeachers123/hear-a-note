"""
app.py — Toddler Music Box 的 Python 後端 (FastAPI)

  GET /              → 前端 PWA (static/index.html)
  GET /api/songs     → 兒歌清單 (之後可換成 VAE 生成的旋律)
  GET /api/health    → 健康檢查
  GET /sw.js         → Service Worker（必須從根目錄提供，才能控制整個網站）

本機執行：uvicorn app:app --reload --port 8000
然後打開 http://localhost:8000
"""
import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

STATIC = Path(__file__).parent / "static"

app = FastAPI(title="Toddler Music Box API", version="1.0.0")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/songs")
def songs():
    # Week 1 延伸：之後可以把這裡改成回傳 VAE 生成的新旋律
    return json.loads((STATIC / "songs.json").read_text(encoding="utf-8"))


@app.get("/sw.js", include_in_schema=False)
def service_worker():
    return FileResponse(
        STATIC / "sw.js",
        media_type="application/javascript",
        headers={"Cache-Control": "no-cache", "Service-Worker-Allowed": "/"},
    )


@app.get("/manifest.webmanifest", include_in_schema=False)
def manifest():
    return FileResponse(STATIC / "manifest.webmanifest",
                        media_type="application/manifest+json")


# 其他靜態檔 (index.html, app.js, sounds/…) — 放最後，避免蓋掉 /api
app.mount("/", StaticFiles(directory=STATIC, html=True), name="static")
