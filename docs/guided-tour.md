# Guided Tour & Wayfinding System

## Tour Overview
The guided museum experience consists of **16 sequential tour stops** spanning both floors. The tour follows a logical narrative:

```
Entrance & Foundations (Floor 1) ──► Academics & Campus Core (Floor 1) ──► Grand Staircase Transition
                                                                                     │
Tour Finale & Vision 2030 (Floor 2) ◄── Student Vibrance & Culture (Floor 2) ◄── Research & Achievements (Floor 2)
```

## Tour Stops Manifest
Stored in [src/data/tourStops.json](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/src/data/tourStops.json):

| Stop | Title | Floor | Coordinates (X, Y, Z) | Narrative Focus |
|---|---|---|---|---|
| **01** | Welcome to VIT Vellore | 1 | `(0.0, 0.0, 14.5)` | Grand Entrance & 4-Decade Overview |
| **02** | The Beginning & 1984 Foundation | 1 | `(-14.0, 0.0, -12.0)` | Vellore Engineering College Genesis |
| **03** | Founder & Chancellor Dr. G. Viswanathan | 1 | `(-14.0, 0.0, -9.0)` | Visionary leadership & public service |
| **04** | Four Decades of Institutional Evolution | 1 | `(-14.0, 0.0, -1.0)` | Deemed University, ABET, IoE milestones |
| **05** | Academic Schools & Multidisciplinary Wings | 1 | `(14.0, 0.0, -11.0)` | SCOPE, SENSE, SELECT, SMEC faculties |
| **06** | Curricular Innovation: FFCS & Central Library | 1 | `(14.0, 0.0, -4.0)` | Flexible credits and library research |
| **07** | Campus Miniature Model & Masterplan | 1 | `(0.0, 0.0, 6.5)` | 372-acre campus interactive overview |
| **08** | Central VIT Monument & Iconic Gateway | 1 | `(0.0, 0.0, 1.5)` | University motto and main entrance arch |
| **09** | Grand Staircase & Transition to Floor 2 | 1 | `(8.5, 0.0, 9.0)` | Transition core leading upstairs |
| **10** | Research & Innovation Ecosystem | 2 | `(-13.0, 5.0, -3.0)` | 50,000+ publications & NIRF #14 Research |
| **11** | Research Centres & Interactive Table | 2 | `(-11.0, 5.0, -6.5)` | Nanotechnology, ARC, CBCMT, VITTBI |
| **12** | Wall of Achievements & Recognition | 2 | `(8.0, 5.0, -12.0)` | NAAC A++ (3.66/4), NIRF #14, QS rankings |
| **13** | VIT Around the World — Global Connections | 2 | `(0.0, 5.0, 6.5)` | 300+ partner universities, SAP programs |
| **14** | Life at VIT — Riviera & Cultural Vibrance | 2 | `(13.0, 5.0, -6.0)` | ISO 9001:2015 carnival, student sports |
| **15** | Technical Culture — graVITas & Racing Teams | 2 | `(13.0, 5.0, 2.0)` | 120+ clubs, SAE Formula racing cars |
| **16** | VIT Today & The Future — The Journey Continues | 2 | `(0.0, 5.0, 1.0)` | 200K+ alumni & Vision 2030 sustainable finale |

## 3D Tour Stop Visual Markers
Each tour stop is marked in the 3D scene by an illuminated golden ring (`a-ring`) at floor level (`Y = 0.02m` on Floor 1, `Y = 5.02m` on Floor 2). Approaching or clicking any ring automatically aligns the tour guide controller.

## Tour Controller Navigation State
- **Current Stop Tracking**: Displayed at top center in `#tourProgress` (`01 / 16` through `16 / 16`).
- **Smooth Automated Waypoint Navigation**: Uses quadratic easing (`dur: 1400-1600ms`) with smooth yaw and pitch alignment to the exhibit focal point.
- **Interruption Tolerance**: If a visitor presses a movement key or clicks 'Exit', automated camera animations gracefully cancel, restoring full manual WASD control immediately.
