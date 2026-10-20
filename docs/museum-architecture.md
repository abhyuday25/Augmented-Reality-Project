# Two-Floor Museum Architecture — VIT Vellore Virtual Museum

## Overview
The VIT Vellore Virtual Museum is designed as a **two-floor, open-atrium university heritage and technology museum**. It blends classical academic prestige (rich navy marble, warm brushed brass, illuminated architectural pylons) with contemporary digital museum interactive installations.

## Floor Layout & Spatial Hierarchy

```
VIT Virtual Museum (36.4m x 32.4m x 10.0m)
│
├── Floor 1 (Y = 0.0m): "The VIT Journey & Academic Foundations"
│   ├── Zone A: Grand Entrance & Welcome Lobby (Z in [8.0, 16.2])
│   ├── Zone B: Origins & History Timeline (X in [-18.2, -7.0], Z in [-15.0, 6.0])
│   ├── Zone C: Academics, Schools & FFCS Wing (X in [7.0, 18.2], Z in [-15.0, 6.0])
│   ├── Zone D: Central Atrium & Heritage Landmarks (X in [-7.0, 7.0], Z in [-6.0, 5.0])
│   │   ├── Miniature 3D Interactive Campus Model (Z = 4.2m)
│   │   └── Central VIT Monolith Monument (Z = -2.0m)
│   └── Zone E: Grand Staircase & Accessible Elevator Transition Core (X in [10.5, 17.5], Z in [6.8, 14.8])
│
├── Grand Staircase & Ramp Collision Core
│   ├── Visual: 16 graduated steps with brass safety handrails and directional signage
│   └── Collision: Smooth incline ramp elevating Y from 0.0m to 5.0m across Z in [6.8, 14.5]
│
└── Floor 2 (Y = 5.0m): "Research, Global Impact & Campus Life"
    ├── Zone F: Central Atrium Void & Glass Guardrail Perimeter (Overlooking Floor 1)
    ├── Zone G: Strategic Research Clusters & Innovation Wing (West Gallery)
    ├── Zone H: Interactive Digital Research Table (Center-West)
    ├── Zone I: Wall of Achievements & Recognitions (North Gallery Wall)
    ├── Zone J: VIT Around the World Global Partnership Wall (South Gallery Wall)
    ├── Zone K: Student Life, Riviera & graVITas Photo Gallery Wall (East Gallery)
    └── Zone L: Tour Finale & Vision 2030 Sustainable Installation (Overlooking Lobby)
```

## Architectural Dimensions & Coordinate Frame
- **World Origin (0, 0, 0)**: Ground level center of the main atrium monument.
- **Player Spawn Point**: `(0.00, 0.00, 15.00)` facing `(0, 180, 0)` towards the welcome reception wall.
- **Floor 1 Floor Plane**: `Y = 0.00m`, Ceiling height = `4.80m`.
- **Floor 2 Mezzanine Slab**: `Y = 5.00m`, Ceiling height = `9.60m` (total building height = `10.0m`).
- **Outer Building Perimeter Bounds**: `X ∈ [-18.2, 18.2]`, `Z ∈ [-16.2, 16.2]`.
- **Floor 2 Atrium Opening**: `X ∈ [-7.2, 7.2]`, `Z ∈ [-6.2, 5.2]`. Protected by 1.1m tempered glass railings and player boundary collision.

## Staircase & Accessible Floor Transition
1. **Physical Staircase Walkway**:
   - Location: `X ∈ [10.5, 14.5], Z ∈ [6.8, 14.8]`.
   - Continuous slope equation:
     $$\Delta Z = 14.5 - 6.8 = 7.7\text{m}$$
     $$Y(z) = \text{clamp}\left(\frac{z - 6.8}{7.7}, 0, 1\right) \times 5.0\text{m}$$
   - Walking along WASD seamlessly raises player eye-height without stutter or camera clipping.
2. **Accessible One-Click Elevator**:
   - Accessible from both the HUD bar ("Switch Floor"), side menu, and direct click on elevator shaft door (`INTERACT_GrandStaircase`).
   - Smoothly teleports rig between Floor 1 spawn `(12.5, 0.0, 7.5)` and Floor 2 spawn `(12.5, 5.0, 14.0)`.

## Layered Museum Lighting Architecture
1. **Ambient Light**: Soft cool white `(#f1f5f9)` at `0.85` intensity.
2. **Directional Skylight**: Primary warm daylight `(#fef3c7)` casting soft shadows through the glass roof at `position="6 14 8"`.
3. **Directional Gallery Light**: Secondary fill light for Floor 2 North Wall at `position="-6 12 -8"`.
4. **Transition Accent Light**: Warm golden point light `(#fbbf24)` illuminating the staircase and elevator at `position="12.5 6.0 10.5"`.
5. **Central Monument Spotlight**: Focused gallery spotlight `(#fef08a)` highlighting the central VIT monolith at `position="0 6.5 -2.0"`.
