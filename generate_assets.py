"""
generate_assets.py — generates every asset the PWA needs, with Python
    1. static/sounds/*.wav  : 25 piano notes synthesized with numpy (C3 to C5, including black keys)
    2. static/icons/*.png   : app icons made from assets/logo.png with Pillow (circle-safe)
    3. static/songs.json    : nursery song melodies (public-domain tunes)
    4. static/i18n.json     : UI text in 12 languages (source: i18n.py)
    5. static/staff/*.svg   : staff notation image for every note (engraved with verovio)

Run: python generate_assets.py
"""
import json
import re
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import i18n

ROOT = Path(__file__).parent / "static"
SAMPLE_RATE = 22050      # a toddler app does not need 44.1 kHz; half the file size
DURATION = 1.6           # each note lasts 1.6 s

# White keys: one octave of C major + high C
WHITE = {
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23,
    "G4": 392.00, "A4": 440.00, "B4": 493.88, "C5": 523.25,
}
# Black keys (sharps). File names use "s" instead of "#", because "#" is special in URLs: C#4 → Cs4
BLACK = {
    "Cs4": 277.18, "Ds4": 311.13, "Fs4": 369.99, "Gs4": 415.30, "As4": 466.16,
}
# One octave lower for the bass clef (C3–B3, including sharps): exactly half the frequency
LOW = {n[:-1] + "3": round(f / 2, 2) for n, f in {**WHITE, **BLACK}.items() if n != "C5"}
NOTES = {**WHITE, **BLACK, **LOW}


# ---------------------------------------------------------------- 1. Sound
def synth_piano(freq: float) -> np.ndarray:
    """Additive synthesis: fundamental + overtones, each decaying at a different rate.
    Higher overtones fade faster → sounds like a gentle piano/glockenspiel "ding", not an electronic beep."""
    t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)
    harmonics = [(1, 1.0, 3.0), (2, 0.45, 4.5), (3, 0.22, 6.0),
                 (4, 0.12, 8.0), (5, 0.06, 10.0)]     # (multiple, volume, decay rate)
    tone = np.zeros_like(t)
    for n, amp, decay in harmonics:
        # Slight inharmonicity makes it sound more natural
        f = freq * n * (1 + 0.0004 * n * n)
        tone += amp * np.exp(-decay * t) * np.sin(2 * np.pi * f * t)

    attack = np.minimum(t / 0.005, 1.0)                  # 5 ms attack avoids a "click"
    release = np.clip((DURATION - t) / 0.15, 0.0, 1.0)   # fade out at the end
    tone *= attack * release
    return tone / np.max(np.abs(tone)) * 0.8             # normalize and keep headroom


def write_wav(path: Path, data: np.ndarray) -> None:
    pcm = (data * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(pcm.tobytes())


# ---------------------------------------------------------------- 2. Icons
# Every icon is made from the transparent logo in assets/logo.png.
# Launchers often crop icons to a circle, so the logo is always scaled down until its whole
# bounding box (corners included) fits inside the circle — nothing of the logo is ever cut off.
LOGO = Path(__file__).parent / "assets" / "logo.png"
ICON_BG = (255, 255, 255, 255)   # background for icons that must be opaque (maskable, Apple)


def load_logo() -> Image.Image:
    """Loads the logo and trims the transparent border around it"""
    logo = Image.open(LOGO).convert("RGBA")
    return logo.crop(logo.getchannel("A").getbbox())


def make_icon(logo: Image.Image, size: int, circle: float, opaque: bool) -> Image.Image:
    """Centers the logo on a square canvas so its bounding box fits in a circle.

    circle = diameter of the circle as a fraction of the icon size
             (0.80 = maskable safe zone, 0.94 = a plain round frame with a small margin)
    """
    w, h = logo.size
    d = circle * size                      # circle diameter in pixels
    scale = d / (w * w + h * h) ** 0.5     # the box diagonal must fit the diameter
    lw, lh = max(1, round(w * scale)), max(1, round(h * scale))
    canvas = Image.new("RGBA", (size, size), ICON_BG if opaque else (0, 0, 0, 0))
    small = logo.resize((lw, lh), Image.Resampling.LANCZOS)
    canvas.alpha_composite(small, ((size - lw) // 2, (size - lh) // 2))
    return canvas.convert("RGB") if opaque else canvas


ICONS = [   # file name, size, circle, opaque
    ("icon-192.png",          192, 0.94, False),   # manifest "any"
    ("icon-512.png",          512, 0.94, False),   # manifest "any"
    ("icon-maskable-512.png", 512, 0.80, True),    # manifest "maskable" (Android adaptive icons)
    ("apple-touch-icon.png",  180, 0.80, True),    # iPhone / iPad home screen (no transparency)
    ("favicon-32.png",         32, 0.98, False),   # browser tab
]


def write_icons() -> None:
    logo = load_logo()
    for name, size, circle, opaque in ICONS:
        make_icon(logo, size, circle, opaque).save(ROOT / "icons" / name, optimize=True)
    print(f"✓ {len(ICONS)} icons from assets/logo.png → static/icons/")


# ---------------------------------------------------------------- 3. Songs
def song(sid: str, notes: str, beats: str) -> dict:
    """notes and beats are space-separated; one beat = one quarter note. Every note must be a white key C4–C5."""
    n, b = notes.split(), [float(x) for x in beats.split()]
    assert len(n) == len(b), (sid, len(n), len(b))
    assert all(x in WHITE for x in n), sid                 # stays inside the 8 white keys
    return {"id": sid, "title": sid, "notes": n, "beats": b}   # title = i18n key


# Public-domain tunes that fit the 8 white keys (C4–C5). Written for treble clef; the app moves them
# down one octave for bass clef. "beats" drives the slow "Play" demo.
SONGS = [
    song("twinkle",                                    # Twinkle Twinkle Little Star (traditional)
         "C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4 "
         "G4 G4 F4 F4 E4 E4 D4 G4 G4 F4 F4 E4 E4 D4 "
         "C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4",
         "1 1 1 1 1 1 2 1 1 1 1 1 1 2 "
         "1 1 1 1 1 1 2 1 1 1 1 1 1 2 "
         "1 1 1 1 1 1 2 1 1 1 1 1 1 2"),
    song("mary",                                       # Mary Had a Little Lamb (traditional)
         "E4 D4 C4 D4 E4 E4 E4 D4 D4 D4 E4 G4 G4 "
         "E4 D4 C4 D4 E4 E4 E4 E4 D4 D4 E4 D4 C4",
         "1 1 1 1 1 1 2 1 1 2 1 1 2 "
         "1 1 1 1 1 1 1 1 1 1 1 1 4"),
    song("ode",                                        # Ode to Joy (Beethoven, Symphony No. 9, 1824)
         "E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4 "
         "E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 D4 C4 C4",
         "1 1 1 1 1 1 1 1 1 1 1 1 1.5 0.5 2 "
         "1 1 1 1 1 1 1 1 1 1 1 1 1.5 0.5 2"),
    song("jingle",                                     # Jingle Bells chorus (James Lord Pierpont, 1857)
         "E4 E4 E4 E4 E4 E4 E4 G4 C4 D4 E4 "
         "F4 F4 F4 F4 F4 E4 E4 E4 E4 E4 D4 D4 E4 D4 G4 "
         "E4 E4 E4 E4 E4 E4 E4 G4 C4 D4 E4 "
         "F4 F4 F4 F4 F4 E4 E4 E4 E4 G4 G4 F4 D4 C4",
         "1 1 2 1 1 2 1 1 1.5 0.5 4 "
         "1 1 1.5 0.5 1 1 1 0.5 0.5 1 1 1 1 2 2 "
         "1 1 2 1 1 2 1 1 1.5 0.5 4 "
         "1 1 1 1 1 1 1 0.5 0.5 1 1 1 1 4"),
]


# ---------------------------------------------------------------- 1b. Wrong-note sound: a soft kitten "mew"
def _lowpass(x: np.ndarray, fc: float) -> np.ndarray:
    """One-pole low-pass filter: takes off any sharp edge."""
    a = np.exp(-2 * np.pi * fc / SAMPLE_RATE)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def synth_oops() -> np.ndarray:
    """Wrong-note sound (sounds/oops.wav): a soft, low, "questioning" kitten mew — "mew?".
    Chosen by the parent from 10 versions (#6).
      * pitch 430 Hz → dips to 380 Hz → rises to 610 Hz at the end, like asking "is this one?"
      * it glides the whole time, so it never sounds like a piano note
      * only a few gentle overtones + a 1.8 kHz low-pass: round, never shrill (sound centre ~530 Hz)
      * short (0.36 s) and quiet (32 % volume); app.js never stacks two mews"""
    dur = 0.36
    n = int(SAMPLE_RATE * dur)
    t = np.arange(n) / SAMPLE_RATE
    x = t / dur
    # Smooth pitch curve through (0, 430 Hz), (0.45, 380 Hz), (1, 610 Hz), interpolated on a log scale
    f0 = np.exp(np.interp(x, [0, 0.45, 1], np.log([430, 380, 610])))
    k = max(3, n // 60)
    f0 = np.convolve(np.pad(f0, k, mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), "valid")
    f0 *= 1 + 0.006 * np.sin(2 * np.pi * 6 * t)                # tiny purr-like wobble
    phase = 2 * np.pi * np.cumsum(f0) / SAMPLE_RATE
    bright = 0.3 * np.sin(np.pi * np.clip(x * 1.4, 0, 1))     # "ee" a little brighter in the middle
    tone = (np.sin(phase) + 0.55 * bright * np.sin(2 * phase)
            + 0.25 * bright * np.sin(3 * phase) + 0.08 * bright * np.sin(4 * phase))
    env = np.minimum(t / 0.035, 1) * np.sin(np.pi * np.clip(x, 0, 1)) ** 0.6   # soft start and end
    out = _lowpass(tone * env, 1800)
    return out / np.max(np.abs(out)) * 0.32


# ---------------------------------------------------------------- 5. Staff notation
# Colors: everything pink in treble clef, light blue in bass clef (same families as CLEF_LINE in app.js)
CLEF_COLOR = {"G": "#C04877", "F": "#2A78A8"}   # "Sakura Sky" outline colors for the note heads (4.7:1 / 4.8:1 on white)
# Notes drawn for each clef: treble C4–C5, bass C3–C4 (middle C appears in both)
CLEF_NOTES = {
    "G": ["C4", "Cs4", "D4", "Ds4", "E4", "F4", "Fs4", "G4", "Gs4", "A4", "As4", "B4", "C5"],
    "F": ["C3", "Cs3", "D3", "Ds3", "E3", "F3", "Fs3", "G3", "Gs3", "A3", "As3", "B3", "C4"],
}


def staff_mei(note, clef_name: str) -> str:
    """Converts a note like 'Cs4' into MEI music notation (one whole note); note=None draws only the clef"""
    clef = ("G", 2) if clef_name == "G" else ("F", 4)     # treble clef on line 2, bass clef on line 4
    if note is None:
        body = '<space dur="1"/>'
    else:
        pname, accid, octave = note[0].lower(), ("s" if note[1] == "s" else ""), int(note[-1])
        # Middle C (C4) is always pink, reminding kids "this is middle C" on the bass staff too
        color = CLEF_COLOR["G"] if note == "C4" else CLEF_COLOR[clef_name]
        acc = f' accid="{accid}"' if accid else ""
        body = f'<note pname="{pname}" oct="{octave}" dur="1"{acc} color="{color}"/><space dur="8"/>'
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<mei xmlns="http://www.music-encoding.org/ns/mei" meiversion="5.1"><meiHead><fileDesc><titleStmt><title/></titleStmt><pubStmt/></fileDesc></meiHead>
<music><body><mdiv><score><scoreDef><staffGrp><staffDef n="1" lines="5" clef.shape="{clef[0]}" clef.line="{clef[1]}"/></staffGrp></scoreDef>
<section><measure n="1" right="invis"><staff n="1"><layer n="1">
{body}
</layer></staff></measure></section></score></mdiv></body></music></mei>"""


def plain_staff(svg: str) -> str:
    """Same staff picture without the clef, as a square cropped around the note (used by the right-note reward).
    Works on the verovio SVG text: drop the clef group, fit the five staff lines to the window, square view box
    that still holds the ledger-line notes (treble C4 below, bass C4 above)."""
    svg = re.sub(r'<g[^>]*class="clef"[^>]*>.*?</g>', "", svg, count=1, flags=re.S)
    layer = svg[svg.find('class="layer"'):]
    xs = [int(x) for x in re.findall(r'translate\((\d+), \d+\)', layer)] or [825]
    ORIGIN, SIZE, HEAD = 100, 1440, 300                    # page margin (x and y 100/200), window size, notehead
    mid = (min(xs) + max(xs) + HEAD) / 2                    # center of the note (+ its sharp), staff coordinates
    x0 = int(mid - SIZE / 2)
    ys = [int(y) for y in re.findall(r'M0 (\d+) L\d+ \1" stroke-width="13"', svg)] or [240, 960]
    top = int(200 + (min(ys) + max(ys)) / 2 - SIZE / 2)     # the five lines sit in the middle of the square
    svg = re.sub(r'M0 (\d+) L(\d+) \1" stroke-width="13"',
                 lambda m: f'M{x0} {m.group(1)} L{x0 + SIZE} {m.group(1)}" stroke-width="13"', svg)
    svg = re.sub(r'<svg viewBox="0 0 \d+ \d+"', '<svg viewBox="0 0 144 144"', svg, count=1)
    return re.sub(r'(class="definition-scale"[^>]*viewBox=")0 0 \d+ \d+"',
                  lambda m: f'{m.group(1)}{x0 + ORIGIN} {top} {SIZE} {SIZE}"', svg, count=1)


def write_staff() -> None:
    try:
        import verovio
    except ImportError:
        print("⚠ verovio is not installed — skipping staff images (keeping existing static/staff/*.svg)")
        return
    verovio.enableLog(verovio.LOG_OFF) if hasattr(verovio, "enableLog") else None
    tk = verovio.toolkit()
    tk.setOptions({"adjustPageHeight": True, "adjustPageWidth": True, "scale": 100,
                   "header": "none", "footer": "none", "svgViewBox": True, "svgRemoveXlink": True,
                   "pageMarginTop": 20, "pageMarginBottom": 20, "pageMarginLeft": 10,
                   "pageMarginRight": 20, "removeIds": True,
                   "spacingLinear": 0.12, "spacingNonLinear": 0.5, "spacingStaff": 4})
    total = 0
    for clef_name, notes in CLEF_NOTES.items():
        folder = ROOT / "staff" / clef_name
        folder.mkdir(parents=True, exist_ok=True)
        for n in [None] + notes:                          # None = clef-only image (used as the menu icon)
            tk.loadData(staff_mei(n, clef_name))
            svg = tk.renderToSVG(1)
            (folder / f"{n or 'clef'}.svg").write_text(svg, encoding="utf-8")
            total += 1
            if n:                                         # plain/<note>.svg: no clef, for the reward
                (folder / "plain").mkdir(exist_ok=True)
                (folder / "plain" / f"{n}.svg").write_text(plain_staff(svg), encoding="utf-8")
                total += 1
    print(f"✓ {total} staff images (treble staff/G, bass staff/F) → static/staff/")


def main() -> None:
    (ROOT / "sounds").mkdir(parents=True, exist_ok=True)
    (ROOT / "icons").mkdir(parents=True, exist_ok=True)

    for name, freq in NOTES.items():
        write_wav(ROOT / "sounds" / f"{name}.wav", synth_piano(freq))
    write_wav(ROOT / "sounds" / "oops.wav", synth_oops())
    print(f"✓ {len(NOTES)} sound files + oops.wav → static/sounds/")

    write_icons()

    (ROOT / "songs.json").write_text(
        json.dumps({"notes": list(WHITE), "black": list(BLACK), "songs": SONGS}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"✓ {len(SONGS)} songs → static/songs.json")

    i18n.check()
    (ROOT / "i18n.json").write_text(
        json.dumps({"langs": i18n.LANGS, "strings": i18n.STRINGS}, ensure_ascii=True, indent=1),
        encoding="utf-8")
    print(f"✓ {len(i18n.LANGS)} languages → static/i18n.json")

    write_staff()


if __name__ == "__main__":
    main()
