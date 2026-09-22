## Interactive Virtual Museum (A‑Frame) — VirtuMuseum

Project for the course **Interaction and User Experience (VR/AR)**.


### Goal (summary)

Create a **desktop/mobile VR** virtual museum experience with an **automatic guided tour**, **free exploration**, informative **hotspots**, and **multimedia** (3D + audio + 360 panorama/video).

### Key features

- **Guided tour** with stops (movement + orientation) and panel text.
- **Free exploration** with WASD (desktop) and look-controls (mouse/touch).
- Clickable **hotspots** with information + audio/feedback.
- **Menu/overlay** with:
  - Start/Pause/Resume/Stop
  - Teleport to stops
  - Volume / ambient music
  - **360 Panorama** and **360 Video** mode
  - Help (shortcuts) + accessibility (reduced motion)
- **Voice (Web Speech)**: commands like “start tour”, “pause”, “resume”, “stop”, “next”, “help”.
- **Audio without required local files**: ambient music

### Use cases (1–2)

1. **Guided tour**: a user enters the museum and follows a route with stops and contextual information.
2. **Explore + discover**: a user explores freely and clicks hotspots to get details and hear narration.

### Tested hardware/tech (suggestion for the report)

- **Desktop**: keyboard + mouse (WASD + click; shortcuts).
- **Smartphone/tablet**: touch (look-controls) + UI; (optional) gyroscope via browser.
- **Software**: A‑Frame 1.5; WebAudio/Tone.js; Web Speech API (when supported).

### How to Run

#### 1. (Optional) Re-generate the 3D GLB Model
If you made changes to the museum procedural code or 3D assets:
```bash
python scripts/generate_vit_museum.py
```

#### 2. Start a Local HTTP Server
Run from the project root directory:

**Option A (Python):**
```bash
python -m http.server 8000
```

**Option B (Node.js - Disables caching automatically):**
```bash
npx http-server -c-1 -p 8000
```

Then open `http://localhost:8000/` in your browser.

---

### Fixing "Updated Code / Assets Not Showing" (Browser Cache Issue)

Web browsers heavily cache 3D `.glb` models, JavaScript, and JSON files in memory. If your changes are not appearing on `localhost:8000`:

1. **Hard Refresh the Browser:**
   - Windows/Linux: Press **`Ctrl + F5`** or **`Ctrl + Shift + R`**
   - Mac: Press **`Cmd + Shift + R`**
2. **Disable Cache via DevTools (Recommended):**
   - Open Developer Tools (**`F12`** or Right Click → **Inspect**).
   - Go to the **Network** tab.
   - Check the **"Disable cache"** checkbox.
   - Keep DevTools open while developing and refreshing.
3. **Open in Private / Incognito Window:**
   - Press **`Ctrl + Shift + N`** (Chrome/Edge) or **`Ctrl + Shift + P`** (Firefox) and visit `http://localhost:8000/`.
4. **Kill Stale Server Processes:**
   - Ensure an old background server instance isn't occupying port 8000 from another directory.

---

### Project structure

- `index.html`: Main entry page (A‑Frame 3D scene + UI overlay).
- `scripts/generate_vit_museum.py`: Procedural GLB model generator.
- `src/css/style.css`: UI styles & layout.
- `src/js/app.js`: Museum application logic (A-Frame components, guided tour, audio, interaction).
- `src/data/tourStops.json`: Guided tour stops, camera coordinates, and narration text.
- `src/data/paintings.json`: Exhibit descriptions, historical archives, and metadata.
- `src/assets/models/vit_vellore_virtual_museum.glb`: 3D museum model asset.
- `vit_vellore_virtual_museum.glb`: Root 3D museum GLB bundle.

### Credits / references

- A‑Frame: `https://aframe.io/`
- VR heuristics (NN/g): `https://www.nngroup.com/articles/usability-heuristics-virtual-reality/`


### Instructions

Model Regeneration:
bash
python scripts/generate_vit_museum.py
Local HTTP Server Commands:
python -m http.server 8000
npx http-server -c-1 -p 8000 (auto cache disable)
Browser Cache Bypassing:
Hard reload: Ctrl + F5 / Ctrl + Shift + R (Cmd + Shift + R on Mac).
DevTools: F12 → Network tab → check Disable cache.
Incognito mode.
Updated File Structure.
