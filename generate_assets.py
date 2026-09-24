"""
generate_assets.py — 用 Python 產生 PWA 需要的所有素材
  1. static/sounds/*.wav  : 用 numpy 合成的 8 個鋼琴音 (C4 ~ C5)
  2. static/icons/*.png   : App 圖示 (192 / 512 / maskable)，不需要 Pillow
  3. static/songs.json    : 兒歌旋律資料 (公領域曲目)

執行：python generate_assets.py
"""
import json
import struct
import wave
import zlib
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent / "static"
SAMPLE_RATE = 22050      # 幼兒 App 不需要 44.1kHz，檔案小一半
DURATION = 1.6           # 每個音 1.6 秒

# 白鍵 C 大調一個八度 + 高音 C（幼兒最友善：沒有黑鍵）
NOTES = {
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23,
    "G4": 392.00, "A4": 440.00, "B4": 493.88, "C5": 523.25,
}


# ---------------------------------------------------------------- 1. 聲音
def synth_piano(freq: float) -> np.ndarray:
    """加法合成 (additive synthesis)：基頻 + 泛音，每個泛音衰減速度不同，
    高泛音衰減較快 → 聽起來像「叮～」的鋼琴/鐵琴，而不是電子嗶聲。"""
    t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)
    harmonics = [(1, 1.0, 3.0), (2, 0.45, 4.5), (3, 0.22, 6.0),
                 (4, 0.12, 8.0), (5, 0.06, 10.0)]     # (倍數, 音量, 衰減率)
    tone = np.zeros_like(t)
    for n, amp, decay in harmonics:
        # 輕微走音 (inharmonicity) 讓聲音更自然
        f = freq * n * (1 + 0.0004 * n * n)
        tone += amp * np.exp(-decay * t) * np.sin(2 * np.pi * f * t)

    attack = np.minimum(t / 0.005, 1.0)                  # 5ms 起音，避免「啪」聲
    release = np.clip((DURATION - t) / 0.15, 0.0, 1.0)   # 尾巴淡出
    tone *= attack * release
    return tone / np.max(np.abs(tone)) * 0.8             # 正規化並留 headroom


def write_wav(path: Path, data: np.ndarray) -> None:
    pcm = (data * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(pcm.tobytes())


# ---------------------------------------------------------------- 2. 圖示
def write_png(path: Path, rgb: np.ndarray) -> None:
    """用標準函式庫 zlib 手寫 PNG（教學重點：PNG 就是 header + 壓縮過的像素）"""
    h, w, _ = rgb.shape
    raw = b"".join(b"\x00" + rgb[y].astype(np.uint8).tobytes() for y in range(h))

    def chunk(tag: bytes, body: bytes) -> bytes:
        return (struct.pack(">I", len(body)) + tag + body
                + struct.pack(">I", zlib.crc32(tag + body) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    path.write_bytes(png)


def make_icon(size: int, maskable: bool = False) -> np.ndarray:
    """畫一個 8 色琴鍵的圖示"""
    img = np.zeros((size, size, 3), dtype=np.uint8)
    img[:] = (255, 248, 231)                              # 奶油色背景
    colors = [(239, 83, 80), (255, 167, 38), (255, 213, 79), (102, 187, 106),
              (38, 198, 218), (66, 165, 245), (171, 71, 188), (236, 64, 122)]
    pad = int(size * (0.22 if maskable else 0.12))        # maskable 要留安全區
    top, bottom = pad + int(size * 0.08), size - pad - int(size * 0.08)
    key_w = (size - 2 * pad) / 8
    for i, c in enumerate(colors):
        x0 = int(pad + i * key_w + key_w * 0.08)
        x1 = int(pad + (i + 1) * key_w - key_w * 0.08)
        img[top:bottom, x0:x1] = c
    return img


# ---------------------------------------------------------------- 3. 兒歌
SONGS = [
    {
        "id": "twinkle",
        "title": "小星星 Twinkle Twinkle",
        "notes": "C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4 "
                 "G4 G4 F4 F4 E4 E4 D4 G4 G4 F4 F4 E4 E4 D4 "
                 "C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4".split(),
    },
    {
        "id": "mary",
        "title": "瑪莉有隻小綿羊 Mary Had a Little Lamb",
        "notes": "E4 D4 C4 D4 E4 E4 E4 D4 D4 D4 E4 G4 G4 "
                 "E4 D4 C4 D4 E4 E4 E4 E4 D4 D4 E4 D4 C4".split(),
    },
    {
        "id": "scale",
        "title": "音階 Do Re Mi",
        "notes": list(NOTES) + list(reversed(NOTES)),
    },
]


def main() -> None:
    (ROOT / "sounds").mkdir(parents=True, exist_ok=True)
    (ROOT / "icons").mkdir(parents=True, exist_ok=True)

    for name, freq in NOTES.items():
        write_wav(ROOT / "sounds" / f"{name}.wav", synth_piano(freq))
    print(f"✓ {len(NOTES)} 個音檔 → static/sounds/")

    write_png(ROOT / "icons" / "icon-192.png", make_icon(192))
    write_png(ROOT / "icons" / "icon-512.png", make_icon(512))
    write_png(ROOT / "icons" / "icon-maskable-512.png", make_icon(512, maskable=True))
    print("✓ 3 個圖示 → static/icons/")

    (ROOT / "songs.json").write_text(
        json.dumps({"notes": list(NOTES), "songs": SONGS}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"✓ {len(SONGS)} 首兒歌 → static/songs.json")


if __name__ == "__main__":
    main()
