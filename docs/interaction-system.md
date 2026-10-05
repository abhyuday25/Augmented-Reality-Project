# Interaction System & Registry

## Architecture Overview
The interaction system connects 3D GLB scene nodes, 2D HTML/SVG user interfaces, and the central data layer. It completely decouples 3D rendering geometry from presentation logic.

```
3D GLB Scene Nodes (INTERACT_* / PLANE_*)
                │
                ▼ (Raycasting / Click / Keyboard E)
    INTERACTION_REGISTRY
                │
                ├─► "exhibit"          ──► openExhibit(exhibit) [ExhibitDrawer]
                ├─► "campus-model"     ──► setCampusModalOpen(true)
                ├─► "research-table"   ──► setResearchModalOpen(true)
                ├─► "global-map"       ──► openExhibitById("global-vit")
                ├─► "monument"         ──► openExhibitById("central-monument")
                ├─► "floor-transition" ──► switchFloor()
                └─► "finale"           ──► openExhibitById("vit-future")
```

## Central Registry Mapping
Defined in [src/data/museumContent.js](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/src/data/museumContent.js):

| GLB Node Name | Type | Target Entity / Exhibit ID |
|---|---|---|
| `INTERACT_Welcome` | `exhibit` | `exhibit-welcome` |
| `INTERACT_History_1984` | `exhibit` | `history-1984` |
| `INTERACT_Founder` | `exhibit` | `founder-viswanathan` |
| `INTERACT_History_UniversityStatus` | `exhibit` | `history-university` |
| `INTERACT_CampusPhoto_TechnologyTower` | `exhibit` | `campus-tt` |
| `INTERACT_History_ABET` | `exhibit` | `history-abet` |
| `INTERACT_History_IoE` | `exhibit` | `history-ioe` |
| `INTERACT_Campus_Model` | `campus-model` | `campus-model` |
| `INTERACT_Central_Sculpture` | `monument` | `central-monument` |
| `INTERACT_Academics` | `exhibit` | `acad-schools` |
| `INTERACT_FFCS` | `exhibit` | `acad-ffcs` |
| `INTERACT_CampusPhoto_Library` | `exhibit` | `campus-library` |
| `INTERACT_CampusPhoto_MainBuilding` | `exhibit` | `campus-admin` |
| `INTERACT_GrandStaircase` | `floor-transition` | `grand-staircase` |
| `INTERACT_Research` | `exhibit` | `research-ecosystem` |
| `INTERACT_ResearchCentres` | `exhibit` | `research-centres` |
| `INTERACT_Research_Table` | `research-table` | `research-table` |
| `INTERACT_VITTBI` | `exhibit` | `vittbi-incubator` |
| `INTERACT_Achievements` | `exhibit` | `wall-achievements` |
| `INTERACT_Global` | `global-map` | `global-vit` |
| `INTERACT_StudentLife` | `exhibit` | `student-life` |
| `INTERACT_Riviera` | `exhibit` | `riviera-fest` |
| `INTERACT_graVITas` | `exhibit` | `gravitas-fest` |
| `INTERACT_StudentChapters` | `exhibit` | `student-chapters` |
| `INTERACT_CampusPhoto_Hostels` | `exhibit` | `campus-hostels` |
| `INTERACT_Convocation` | `exhibit` | `convocation-alumni` |
| `INTERACT_Finale` | `finale` | `vit-future` |

## Legacy Backward Compatibility
For compatibility with earlier versions, anchor planes `PLANE_001` through `PLANE_031` are detected on model load. Each creates a transparent click hitbox bound to `openExhibitByCode(code)`, ensuring all 31 original wall frames remain fully interactive without broken links.

## User Input Mapping
- **`WASD` / `Arrow Keys`**: Free first-person movement.
- **`Mouse Look`**: Smooth 360-degree viewpoint control.
- **`E` / `Click`**: Inspect exhibit / interact with closest object / advance tour stop.
- **`M`**: Open / Close 2-Floor Interactive Map.
- **`T`**: Enter Guided Tour mode.
- **`H`**: Toggle minimal HUD on / off.
- **`Esc`**: Close any open drawer, modal, or exit guided tour.
