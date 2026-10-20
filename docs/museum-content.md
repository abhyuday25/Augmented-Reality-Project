# Museum Content & Exhibit Data Layer

## Architecture
All museum exhibits are defined in a centralized, strongly typed data layer:
- ES Module: [src/data/museumContent.js](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/src/data/museumContent.js)
- JSON Export: [src/data/museumContent.json](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/src/data/museumContent.json)
- Tour Stops: [src/data/tourStops.json](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/src/data/tourStops.json)
- Provenance Manifest: [src/data/sources.json](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/src/data/sources.json)

## Exhibit Data Schema
```typescript
interface MuseumExhibit {
  id: string;                    // Unique identifier (e.g., "history-1984")
  tourStop?: number;             // Assigned tour stop order (1-16)
  floor: 1 | 2;                  // Museum floor level
  section: string;               // Wing / section category
  code: string;                  // 3-digit code mapping to legacy planes (001-031)
  title: string;                 // Curated exhibit title
  subtitle?: string;             // Secondary subtitle
  shortDescription: string;      // Concise teaser description
  description: string;           // Comprehensive verified museum description
  image: string;                 // Relative path to local optimized image asset
  imageAlt: string;              // Descriptive accessibility alt text
  year?: string;                 // Applicable year or timeframe
  location?: string;             // Physical museum wing location
  facts?: string[];              // Bulleted list of verified institutional facts
  sourceTitle?: string;          // Official source title
  sourceUrl?: string;            // Verified external official source URL
  nodeName: string;              // Corresponding GLB 3D scene node name
  position?: [number, number, number]; // World coordinates [x, y, z]
}
```

## Curated Museum Exhibits Roster

### Floor 1: The VIT Journey & Academics (14 Exhibits)
1. **`exhibit-welcome`** (Stop 01): Welcome to VIT Vellore (1984–Present)
2. **`history-1984`** (Stop 02): Founding of Vellore Engineering College (1984)
3. **`founder-viswanathan`** (Stop 03): Dr. G. Viswanathan — Founder & Chancellor
4. **`history-university`** (Stop 04): Conferment of Deemed University Status (2001)
5. **`campus-tt`** (Stop 04): Technology Tower (TT) Landmark (2008)
6. **`history-abet`** (Stop 04): Pioneering ABET USA Accreditations (2010–2015)
7. **`history-ioe`** (Stop 04): Institution of Eminence (IoE) Recognition (2019)
8. **`campus-model`** (Stop 07): Miniature 3D Interactive Campus Model (372 Acres)
9. **`central-monument`** (Stop 08): Central VIT Heritage & Main Gateway Monolith
10. **`acad-schools`** (Stop 05): Academic Schools & Multidisciplinary Faculties (SCOPE, SENSE, SMEC, etc.)
11. **`acad-ffcs`** (Stop 06): Fully Flexible Credit System (FFCS)
12. **`campus-library`** (Stop 06): Periyar E.V.R. Central Library (6 Floors, 300K+ Books)
13. **`campus-admin`** (Stop 06): Main Administrative Building & Governance Quad
14. **`grand-staircase`** (Stop 09): Grand Architectural Staircase & Accessible Elevator Transition

### Floor 2: Research, Achievements & Campus Life (13 Exhibits)
15. **`research-ecosystem`** (Stop 10): Research & Innovation Ecosystem (50,000+ Scopus Papers)
16. **`research-centres`** (Stop 11): Specialized Advanced Research Centres (CNR, CBCMT, ARC)
17. **`research-table`** (Stop 11): Interactive Digital Research Table (4 Thematic Pillars)
18. **`vittbi-incubator`** (Stop 11): VITTBI Technology Business Incubator (150+ Startups)
19. **`wall-achievements`** (Stop 12): Wall of Achievements & Recognition (NIRF 2025, NAAC A++ 3.66/4)
20. **`global-vit`** (Stop 13): VIT Around the World (300+ Partner Universities, Semester Abroad)
21. **`student-life`** (Stop 14): Vibrant Campus Community & Student Welfare (40,000+ Students)
22. **`riviera-fest`** (Stop 14): Riviera International Sports & Cultural Carnival (ISO 9001:2015)
23. **`gravitas-fest`** (Stop 15): graVITas Annual Techno-Management Festival
24. **`student-chapters`** (Stop 15): 120+ Student Clubs, Professional Chapters & Formula Racing Teams
25. **`campus-hostels`** (Stop 15): Student Residential High-Rise Towers (25,000+ Resident Scholars)
26. **`convocation-alumni`** (Stop 16): Ceremonial Convocations & 200,000+ Global Alumni
27. **`vit-future`** (Stop 16): VIT Today & Vision 2030 Sustainable Future Finale
