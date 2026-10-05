# VIT Vellore Virtual Museum — Two-Floor Interactive Tour

An immersive, browser-based 3D digital museum dedicated to **Vellore Institute of Technology (VIT), Vellore**. Built with A-Frame 1.5.0, Three.js, and procedural glTF architecture, the experience allows visitors to explore two floors, follow a 16-stop guided tour, inspect authentic campus photographs, explore strategic research clusters, and learn verified institutional milestones.

---

## Key Features

1. **Two-Floor Open-Atrium Building**:
   - **Floor 1 (Ground Level)**: "The VIT Journey & Academic Foundations" — Grand Lobby, 1984 Foundation, Dr. G. Viswanathan Founder Feature, 4-Decade Milestone Timeline, Academic Schools, FFCS Innovation, Periyar Central Library, Main Admin Quadrangle, and Miniature 3D Campus Model.
   - **Grand Staircase & Elevator Transition**: Walk up the 16-step architectural staircase with smooth collision ramp or use the accessible elevator transition.
   - **Floor 2 (Mezzanine Level)**: "Research, Impact & Campus Life" — Research & Innovation Wing, Strategic Research Table, VITTBI Technology Incubator, Wall of Achievements (NIRF 2025, NAAC A++), Global Partnerships World Map, Student Life Photo Gallery (Riviera, graVITas, 120+ clubs, Formula racing), and Vision 2030 Finale.
2. **16-Stop Curated Guided Tour**:
   - Sequential progression (`01 / 16` through `16 / 16`).
   - Smooth waypoint camera navigation with quadratic easing.
   - Waypoint guidance with top progress bar, previous/next controls, and map integration.
3. **Interactive 2-Floor Vector Map**:
   - Press **`M`** or click **Map** in the top bar to open the vector SVG blueprint.
   - Live "You Are Here" player beacon tracking current coordinates.
   - Tab switching between Floor 1 and Floor 2.
   - Direct click-to-teleport on any wing or numbered tour pin.
4. **Clickable Exhibits & Responsive Drawer**:
   - 27 curated exhibits mapped across `INTERACT_*` and legacy `PLANE_*` nodes.
   - Slide-out information drawer displaying title, verified year, description, key fact bullets, and external official source attribution links (`vit.ac.in`).
5. **Real Researched VIT Data & Provenance**:
   - All factual data and images verified from official university sources ([https://vit.ac.in/](https://vit.ac.in/)).
   - Documented in [src/data/sources.json](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/src/data/sources.json).
6. **Optimized Web Delivery**:
   - Lightweight GLB model (3.40 MB, 95 nodes, 46 materials).
   - Stable 60 FPS in standard desktop and mobile browsers.

---

## User Controls & Key Bindings

| Control | Action |
|---|---|
| **`W` / `A` / `S` / `D`** or **Arrow Keys** | Walk / Move through the museum |
| **Mouse Drag** | Look around (360° viewpoint) |
| **`E` / Left Click** | Inspect exhibit / Interact with closest landmark / Advance tour stop |
| **`M`** | Toggle Interactive 2-Floor Map |
| **`T`** | Start Guided Tour |
| **`H`** | Toggle Minimal HUD mode |
| **`Esc`** | Close exhibit drawer, close modals, or exit guided tour |
| **`Enter`** | Start Tour from Welcome screen |
| **Touch / Virtual Joystick** | Mobile navigation and tap-to-inspect |

---

## How to Run Locally

### 1. Start a Local HTTP Server
Run from the repository root:

**Using Python:**
```bash
python -m http.server 8000
```
*(Or `py -3.13 -m http.server 8000`)*

**Using Node.js:**
```bash
npx http-server -c-1 -p 8000
```

Open `http://localhost:8000/` in Google Chrome, Microsoft Edge, Mozilla Firefox, or Safari.

---

## How to Add or Replace an Exhibit

Another developer can easily add or update exhibits without modifying core 3D scene code:

### Step 1: Add or Replace Image
1. Place an optimized `.jpg` or `.png` into `src/assets/images/vit/`.
2. Keep file size under 300 KB for optimal web delivery.

### Step 2: Add Entry in `src/data/museumContent.js`
Add your exhibit to `MUSEUM_EXHIBITS`:
```javascript
{
  id: "my-new-exhibit",
  tourStop: 17,
  floor: 2,
  section: "Research & Innovation",
  code: "032",
  title: "Frontier Quantum Computing Lab",
  subtitle: "Next-Gen Quantum Information Science",
  shortDescription: "Pioneering quantum algorithms and cryptography.",
  description: "Detailed museum description...",
  image: "src/assets/images/vit/my_image.jpg",
  imageAlt: "Quantum Computing Lab",
  year: "2026",
  location: "Floor 2 • West Wing",
  facts: [
    "Key fact 1",
    "Key fact 2"
  ],
  sourceTitle: "Official VIT Quantum Lab",
  sourceUrl: "https://vit.ac.in/research",
  nodeName: "INTERACT_QuantumLab",
  position: [-18.1, 7.5, 3.0]
}
```

### Step 3: Map in `INTERACTION_REGISTRY`
In [src/data/museumContent.js](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/src/data/museumContent.js):
```javascript
export const INTERACTION_REGISTRY = {
  ...
  INTERACT_QuantumLab: { type: "exhibit", exhibitId: "my-new-exhibit" }
};
```

### Step 4: Record Source in `src/data/sources.json`
Add the factual source and image attribution to ensure provenance integrity.

### Step 5: (Optional) Re-export JSON or Re-generate 3D GLB
```bash
node scripts/export_json.mjs
py -3.13 scripts/generate_vit_museum.py
```

---

## Project Structure & Documentation

```
virtumuseum/
├── index.html                           # Main entry HTML, 3D A-Frame scene, HUD & Modals
├── vit_vellore_virtual_museum.glb       # Optimized two-floor 3D museum GLB bundle (3.4 MB)
├── README.md                            # Project overview & running instructions
├── docs/                                # Technical Documentation
│   ├── museum-architecture.md           # Two-floor architectural layout, coordinates, lighting
│   ├── museum-content.md                # 27 curated exhibits, schemas, and floor assignments
│   ├── content-sources.md               # Research methodology, provenance, source URLs
│   ├── interaction-system.md            # Interaction registry, raycasting, key bindings
│   ├── guided-tour.md                   # 16-stop tour manifest, waypoints, camera easing
│   └── performance.md                   # Performance budget, draw calls, memory benchmarks
├── scripts/
│   ├── generate_vit_museum.py           # Procedural 3D GLB model generator (pygltflib + trimesh)
│   ├── prepare_vit_assets_and_data.py   # Asset optimizer and data synchronization
│   └── export_json.mjs                  # ESM to JSON content exporter
├── src/
│   ├── css/style.css                    # Academic prestige UI design system & responsive layout
│   ├── js/app.js                        # Core application engine, 2-floor bounds, tour & modal controllers
│   ├── data/
│   │   ├── museumContent.js             # Centralized museum content data layer & registry
│   │   ├── museumContent.json           # JSON export of museum exhibits
│   │   ├── tourStops.json               # 16 tour stop waypoints & camera orientations
│   │   ├── sources.json                 # Provenance manifest with official URLs & image credits
│   │   └── paintings.json               # Legacy compatibility metadata
│   └── assets/
│       ├── images/vit/                  # Authentic optimized VIT campus & leadership photos
│       └── models/                      # Model assets directory
```
