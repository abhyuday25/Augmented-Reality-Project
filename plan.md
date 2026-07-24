# Plan & Instructions: Model Cleanup and Image Replacement

This document outlines the model cleanup changes performed on the project and provides instructions on how to customize the museum with your own images.

---

## 1. Changes Completed

- **Deleted Unused 3D Models**: Removed all models from `src/assets/models/` except for the active `q.glb` model.
  - Deleted folder: `src/assets/models/01/`
  - Deleted files:
    - `21-5.glb`
    - `Camadas.glb`
    - `TexturaQuadroTodos.glb`
    - `branco.glb`
    - `q.glb.bak`
    - `q_structure.json`
    - `q_test.glb`
- **Updated Codebase References**:
  - Updated [README.md](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/README.md) to reference `src/assets/models/q.glb` instead of the non-existent `museu.glb`.
  - Confirmed [index.html](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/index.html) references and uses `src/assets/models/q.glb`.
- **Fixed Image Loading & Cache Issues**:
  - Modified [index.html](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/index.html) to dynamically load the 3D plane textures from their designated room directories (`room1`, `room2`, `room3`, `room4`) rather than hardcoding to `test/`.
  - Fixed the type-to-folder mapping bug in `imageUrlForPainting` in [app.js](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/src/js/app.js) (mapped `"Baroque"`, `"Romanticism"`, etc. to `room1`, `room2`, etc. so info cards load the correct images).
  - Added a cache-busting timestamp query parameter (`?t=timestamp`) to all image loading logic to ensure that modified/overwritten images reflect instantly on localhost without browser caching.

---

## 2. Instruction: How to Replace Images in the Museum

The museum uses the `q.glb` model, which contains 3D planes serving as anchors for paintings. These anchors are named `PLANE_001` through `PLANE_031`.

The paintings are structured into folders by room/genre:
- **Room 1 (`room1/`)**: Paintings `001` to `010` (Baroque)
- **Room 2 (`room2/`)**: Paintings `011` to `020` (Romanticism)
- **Room 3 (`room3/`)**: Paintings `021` to `030` (Cubism)
- **Room 4 (`room4/`)**: Painting `031` (Impressionism)

### Option A: Overwrite Existing Image Files (Recommended)

1. **Locate room folder**: Go to the corresponding room folder in `src/assets/images/` (e.g. `src/assets/images/room3/` for paintings 21 to 30).
2. **Prepare your images**: Save your images as JPEG files (or `.jpeg` for painting `038`).
3. **Rename and replace**: Name your images to match the painting slot you want to replace (e.g. `028.jpg`).
4. **Overwrite the existing file** in the corresponding room folder with your new file.

### Option B: Use Custom File Paths or Formats

If you want to use different filenames, subfolders, or image formats (such as `.png`):

1. **Place your images** in `src/assets/images/`.
2. **Modify the image loading logic** in [index.html](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/index.html#L609):
   - Locate the `material` attribute setup for `quadro` inside the script tag (around line 609):
     ```javascript
     quadro.setAttribute(
       "material",
       `
       src: url(src/assets/images/${folder}/${code}.${ext}${cacheBuster});
       side: double;
       roughness: 1;
       metalness: 0;
       `,
     );
     ```
   - Customize the path format to fit your structure.

### Update Painting Metadata (Titles & Descriptions)

When you replace the images, you should also update the text displayed in the museum UI (onboards, hotspots, and panels):

1. **Open the metadata file**: [paintings.json](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/src/data/paintings.json).
2. **Modify the details**: Edit the `title`, `author`, `year`, `materials`, `description`, `history`, `symbolism`, and `type` fields for each painting code (e.g. `"code": "001"`).
3. **Open the tour stops file**: [tourStops.json](file:///c:/Users/Abhyuday/Documents/..PROJECTS/virtumuseum/src/data/tourStops.json) to edit the titles and descriptions of the guided tour stops.
