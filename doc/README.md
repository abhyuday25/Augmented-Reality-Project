# Academic Project Documentation Dossier

**Project Title**: VIT Vellore Virtual Museum — Two-Floor Interactive 3D Digital Twin  
**Software Version**: 2.0.0 (React 18, React Three Fiber, Three.js, Zustand)  
**Documentation Purpose**: Comprehensive technical, architectural, curatorial, and empirical report reference dossier.  

---

## Document Index & Chapter Directory

This directory (`doc/`) contains four academic-grade technical specification and evaluation documents prepared for formal project reporting, research publication, thesis documentation, and institutional presentation:

```
doc/
├── README.md                                  # Documentation index & project executive summary
├── 1_project_architecture.md                  # System architecture, multi-tier pipeline, mathematical models & Mermaid diagrams
├── 2_working_and_components.md                # System runtime lifecycle, 3D graphics components, 2D UI components & state store
├── 3_references_and_citations.md              # Curatorial provenance manifest, institutional sources & formal IEEE/APA citations
└── 4_results_and_performance_benchmarks.md     # Empirical profiling, frame-time latency, memory footprints & comparative metrics
```

---

## Chapter Summaries

### [1. Project Architecture (`1_project_architecture.md`)](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/doc/1_project_architecture.md)
- **High-Level Paradigm**: Decoupled Model-View-Controller (MVC) spatial architecture for 3D web applications.
- **5-Tier Architectural Model**:
  - *Tier 1*: Declarative React 18 UI & Glassmorphism presentation layer.
  - *Tier 2*: Zustand reactive state broker and micro-store event bus.
  - *Tier 3*: React Three Fiber / WebGL 2.0 scene graph and first-person camera controller.
  - *Tier 4*: Static JSON data layer, binary GLB assets, and procedural canvas texture generators.
  - *Tier 5*: In-memory Web Audio oscillator synthesizer and W3C Web Speech API TTS engine.
- **Visualizations**: End-to-end system flowchart, spatial hierarchy class diagram, render-loop sequence diagram, and layout schematics using Mermaid.
- **Mathematical Formulations**: First-person Euler yaw velocity projections, Hermite polynomial S-curve staircase elevation, and 2D AABB mezzanine atrium boundary containment.

### [2. Project Working & Component Inventory (`2_working_and_components.md`)](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/doc/2_working_and_components.md)
- **Operational Workflow**: Application initialization, asynchronous GLB hydration, and dual-mode exploration (Autonomous Free Exploration vs. 17-Stop Curated Guided Tour).
- **3D Graphics Components**: Detailed technical breakdown of `MuseumScene.jsx`, `CameraController.jsx`, `MuseumArchitecture.jsx`, `SchoolsBackWall.jsx`, `CampusMasterplanDiorama.jsx`, `BotanicalPlant.jsx`, `MuseumBench.jsx`, and `SpatialHotspots.jsx`.
- **2D User Interface Components**: Design rationale and event bindings for `TopHUD.jsx`, `DockToolbar.jsx`, `ExhibitDrawer.jsx`, `TourStopCard.jsx`, `MapModal.jsx`, `VisitorGuideModal.jsx`, and `VirtualJoystick.jsx`.
- **Side-by-Side Zero-Overlap Architecture**: Pinned Left Exhibit Drawer ($420\,\text{px}$) and Pinned Right Tour Card ($380\,\text{px}$) preventing view occlusion during guided navigation.

### [3. Curatorial Provenance & Academic Citations (`3_references_and_citations.md`)](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/doc/3_references_and_citations.md)
- **Curatorial Methodology**: Verification protocols utilizing official Vellore Institute of Technology archives, Ministry of Education (GoI) gazettes, NIRF, NAAC, and ABET records.
- **Exhibit Registry**: Complete tabular mapping for all 27+ institutional exhibits, including physical world coordinates $(X, Y, Z)$, official source titles, and live reference URLs.
- **Asset Manifest**: Verified local photographic and cartographic assets stored in `src/assets/images/vit/`.
- **Technical Standards**: Formal citations for glTF 2.0, WebGL 2.0, Three.js, React Three Fiber, Zustand, Web Audio API, and Web Speech API.
- **Bibliography**: Academic literature review formatted in both **IEEE** and **APA 7th Edition** citation styles.

### [4. Experimental Results & Performance Benchmarks (`4_results_and_performance_benchmarks.md`)](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/doc/4_results_and_performance_benchmarks.md)
- **Frame Rate & Latency Profiling**: Frame rate stability across dedicated GPUs (NVIDIA RTX 3070), integrated GPUs (Intel Iris Xe), Apple Silicon (M2), and mobile SoCs (Snapdragon 778G).
- **Analytical vs. Mesh Raycasting**: Closed-form S-curve polynomial achieved **$0.018\,\text{ms}$** query latency vs **$4.850\,\text{ms}$** for mesh raycasting (**$269.4\times$ speedup, $99.63\%$ reduction in collision overhead**).
- **Audio & TTS Latency**: Synthetic oscillator sounds initialized in **$1.20\,\text{ms}$** compared to $180\,\text{ms} - 320\,\text{ms}$ for conventional remote MP3 streaming.
- **Memory & VRAM Allocation**: Stable JS heap footprint ($62.4\,\text{MB}$) and GPU VRAM footprint ($384\,\text{MB}$).
- **Network Transfer & Web Vitals**: Total compressed delivery payload of **$15.29\,\text{MB}$**, achieving **Google Lighthouse Score of 96/100** with an LCP of $2.15\,\text{s}$ and INP of $38\,\text{ms}$.
- **Comparative Matrix**: Empirical benchmark table evaluating R3F v2.0 against the legacy A-Frame v1.0 prototype.
