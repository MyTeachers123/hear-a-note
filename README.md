# Toddler Music Box

A colorful piano app that helps toddlers learn to read music — the **treble clef** and the **bass clef** — by playing.
No letters or numbers on the keys: kids learn from **shapes, colors and the notes on the staff**.

Free, no ads, no accounts, no data collected. Works offline once it has been opened.

**Open the app:** https://kids.myteachers123.com

---

## Getting started

1. Open the app in a browser on a phone, tablet or computer.
2. Tap anywhere — the first tap turns the sound on, goes fullscreen and turns the screen sideways (landscape).
3. Tap the keys and play!

**Install it like an app (recommended)**
- **iPhone / iPad (Safari):** Share button → **Add to Home Screen**
- **Android (Chrome):** ⋮ menu → **Add to Home screen** / **Install app**

Opened from the home-screen icon, it runs fullscreen and works without internet.

## How to play

### The keys
- Black and white keys, just like a real piano.
- Each white key shows one big, simple **shape** (circle, square, triangle, star, hexagon, diamond, heart, arrow) — all the same size.
- The **current note card** above the keys shows the note on the staff, so children learn to match the staff to the shape.
- **Middle C** is always a **circle**. The C one octave higher is an **up arrow ↑**; the C one octave lower is a **down arrow ↓**.

### Treble clef and bass clef
Use the **clef menu** (top right) to switch. The whole screen changes color too — pink for treble clef, light blue for bass clef:

| | Treble clef | Bass clef |
|---|---|---|
| Keys | Middle C up to the next C | The C below up to middle C |
| Color | Pink | Light blue |
| Middle C | Pink circle | **Pink** circle (so kids can always find middle C) |

The keys, the sounds and the pictures all change together.

### "Current note" card
The card above the keys shows **the note on the staff → the key to press**.
- In **Free play**, it shows the note you just played.
- In a **song**, it shows the next note to play.

### Songs
Pick a song from the **song menu**: *Twinkle Twinkle Little Star* or *Mary Had a Little Lamb*.
The next key to press bounces. Wrong notes are never punished — the song simply waits for the right one.
Both songs work in treble clef and in bass clef.

### Play mode: on-screen keys or a real piano
Use the **play mode menu** (top right):

| Play mode | What happens |
|---|---|
| 🎹 **Play on-screen keys** (default) | Tap the keys on the screen. The microphone is never used. |
| 🎤 **Play a real piano** | Have a real piano or keyboard at home? The app listens through the microphone (on every device, including iPhone and iPad). Each correct note moves the song or the quiz forward. |

The microphone is only requested when you choose **Play a real piano**. The first time, the browser asks for permission; if it was blocked, the app shows how to turn it back on.
Switch back to **Play on-screen keys** to turn the microphone off.

### 🎯 Quiz
Tap **🎯** to test reading notes in the selected clef:
- The app picks **3 random notes**. The card shows only the note on the staff (the answer is a "?"), so the child has to read the staff.
- Answer on the on-screen keys, or on a real piano when the play mode is **Play a real piano**.
- Wrong → the correct key flashes. Right → next note.
- All 3 done → ⭐⭐⭐ Well done!
- Five wrong answers in a row → the quiz ends gently. Try again anytime.

### Languages
Choose from the language menu (top right): English, Spanish, Traditional Chinese, Simplified Chinese, Korean, Japanese, Vietnamese, French, Italian, Russian, German and Hindi.
The app picks your device language automatically and remembers your choice.

## Tips for parents

The app goes fullscreen (and back again after a swipe out, on the next tap), stays in landscape, blocks zooming and the back button, and caps the volume at 70%.
A web app can't block the phone's "home" gesture, so for full lock-down:

- **iPhone / iPad — Guided Access:** Settings → Accessibility → Guided Access → On (set a passcode).
  Open the app and triple-click the side button to start. Triple-click again and enter the passcode to finish.
- **Android — App pinning:** Settings → Security → App pinning → On.
  Open the app, go to Recent apps, tap the app icon → **Pin**.

## Privacy

- No accounts, no personal data, no ads, no tracking.
- The microphone is only used when the play mode is set to **Play a real piano**. Sound is analyzed **on your device only** — it is never recorded, stored or uploaded.

## For developers

```bash
pip install -r requirements.txt
python generate_assets.py      # generates sounds, staff images, icons and translations
uvicorn app:app --reload --port 8000
```

Then open http://localhost:8000. All UI text is in `i18n.py` (12 languages).

## License

MIT
