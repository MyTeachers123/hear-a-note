# Toddler Music Box

A colorful piano app that helps toddlers learn to read music — the **treble clef** and the **bass clef** — by playing.
No letters or numbers on the keys: kids learn from **shapes, colors and the notes on the staff**.

Free, no ads, no accounts, no data collected. Works offline once it has been opened.

**Open the app:** https://kids.myteachers123.com

---

## Getting started

1. Open the app in a browser on a phone, tablet or computer.
2. Tap the big green **▶** button. The app goes fullscreen and turns sideways (landscape).
3. Tap the keys and play!

**Install it like an app (recommended)**
- **iPhone / iPad (Safari):** Share button → **Add to Home Screen**
- **Android (Chrome):** ⋮ menu → **Add to Home screen** / **Install app**

Opened from the home-screen icon, it runs fullscreen and works without internet.

## How to play

### The keys
- Black and white keys, just like a real piano.
- Each white key shows a **shape** and **its note on the staff**.
- **Middle C** is always a **circle**. The C one octave higher is an **up arrow ↑**; the C one octave lower is a **down arrow ↓**.

### Treble clef and bass clef
Use the **clef menu** (top left) to switch:

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

### 🎹 Play on my piano
Have a real piano or keyboard at home? Choose a song, tap **🎹**, and play on your own instrument.
Each correct note moves the song forward until it's finished.

| Your instrument | How the app listens |
|---|---|
| Digital piano / keyboard (USB or Bluetooth MIDI) | Connects automatically — the most accurate. Works in Chrome, Edge and on Android. |
| Acoustic piano | Uses the microphone. Works on every device, including iPhone and iPad. |

The first time, the browser asks for microphone permission. If it was blocked, the app shows how to turn it back on.

### 🎯 Quiz
Tap **🎯** to test reading notes in the selected clef:
- The app picks **3 random notes**. The card shows the note on the staff; the pictures on the keys are hidden, so the child has to read the staff.
- Answer on a keyboard, a real piano, or the on-screen keys.
- Wrong → the correct key flashes. Right → next note.
- All 3 done → ⭐⭐⭐ Well done!
- Five wrong answers in a row → the quiz ends gently. Try again anytime.

### Languages
Choose from the language menu (top right): English, Spanish, Traditional Chinese, Simplified Chinese, Korean, Japanese, Vietnamese, French, Italian, Russian, German and Hindi.
The app picks your device language automatically and remembers your choice.

## Tips for parents

The app goes fullscreen, stays in landscape, blocks zooming and the back button, and caps the volume at 70%.
A web app can't block the phone's "home" gesture, so for full lock-down:

- **iPhone / iPad — Guided Access:** Settings → Accessibility → Guided Access → On (set a passcode).
  Open the app and triple-click the side button to start. Triple-click again and enter the passcode to finish.
- **Android — App pinning:** Settings → Security → App pinning → On.
  Open the app, go to Recent apps, tap the app icon → **Pin**.

## Privacy

- No accounts, no personal data, no ads, no tracking.
- The microphone is only used after you tap 🎹 or start a quiz. Sound is analyzed **on your device only** — it is never recorded, stored or uploaded.

## For developers

```bash
pip install -r requirements.txt
python generate_assets.py      # generates sounds, staff images, icons and translations
uvicorn app:app --reload --port 8000
```

Then open http://localhost:8000. All UI text is in `i18n.py` (12 languages).

## License

MIT
