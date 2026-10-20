/**
 * Modern Experience Layer for VIT Vellore Virtual Museum
 * Implements:
 * 1. Cinema-grade Tone Mapping & Color Calibration (Three.js ACESFilmic)
 * 2. GSAP Camera Choreography & Smooth Bezier Transitions
 * 3. Spatial 3D World-to-Screen Interactive Radar Hotspots
 * 4. Lucide Icons & Enhanced Apple-style Glassmorphism Dock
 */

(function () {
  "use strict";

  const Modern3D = {
    scene: null,
    camera: null,
    renderer: null,
    rig: null,
    hotspotsEnabled: true,
    hotspotElements: [],
    landmarks: [
      { id: "campus-model", name: "Campus Masterplan Diorama", pos: [0, 1.4, 4.2], floor: 1, stopIdx: 6, icon: "map-pin" },
      { id: "monument", name: "Central Heritage Monument", pos: [0, 2.5, -2.0], floor: 1, stopIdx: 7, icon: "award" },
      { id: "history", name: "VIT History Timeline", pos: [-18.0, 2.5, -4.0], floor: 1, stopIdx: 1, icon: "clock" },
      { id: "academics", name: "Academic Schools & Tech", pos: [18.0, 2.5, -4.0], floor: 1, stopIdx: 4, icon: "book-open" },
      { id: "staircase", name: "Grand Staircase to Floor 2", pos: [12.5, 2.0, 8.5], floor: 1, stopIdx: 8, icon: "layers" },
      { id: "research", name: "Research & Innovation Wing", pos: [-18.0, 7.5, -4.0], floor: 2, stopIdx: 9, icon: "flask-conical" },
      { id: "achievements", name: "Wall of Achievements", pos: [8.5, 7.5, -16.0], floor: 2, stopIdx: 11, icon: "trophy" },
      { id: "student-life", name: "Life at VIT & Motorsports", pos: [18.0, 7.5, -4.0], floor: 2, stopIdx: 13, icon: "users" },
      { id: "global-vit", name: "Global VIT Partnerships", pos: [0.0, 7.5, 14.0], floor: 2, stopIdx: 12, icon: "globe" }
    ],

    init() {
      const sceneEl = document.querySelector("a-scene");
      if (!sceneEl) return;

      if (sceneEl.hasLoaded) {
        this.onSceneReady(sceneEl);
      } else {
        sceneEl.addEventListener("loaded", () => this.onSceneReady(sceneEl), { once: true });
      }

      this.initLucideIcons();
      this.initHotspotsDOM();
    },

    onSceneReady(sceneEl) {
      this.scene = sceneEl;
      this.renderer = sceneEl.renderer;
      this.rig = document.querySelector("#rig");
      const camEl = document.querySelector("#cam");
      this.camera = camEl?.getObject3D("camera");

      this.setupCinemaShading();
      this.setupCameraChoreography();
      this.startSpatialHotspotsLoop();
    },

    // --- 1. Cinema-grade Tone Mapping & Color Calibration ---
    setupCinemaShading() {
      if (!this.renderer) return;

      try {
        const THREE = window.THREE || window.AFRAME?.THREE;
        if (!THREE) return;

        // ACES Filmic Tone Mapping for photorealistic dynamic range
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1.18;

        // Color Space
        if (THREE.SRGBColorSpace) {
          this.renderer.outputColorSpace = THREE.SRGBColorSpace;
        }

        // Shadow quality
        if (this.renderer.shadowMap) {
          this.renderer.shadowMap.enabled = true;
          this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        }

        // Emissive enhancement on materials
        const museumModel = document.querySelector("#museu");
        if (museumModel) {
          museumModel.addEventListener("model-loaded", (e) => {
            const root = e.detail?.model;
            if (!root) return;
            root.traverse((node) => {
              if (node.isMesh && node.material) {
                const mat = node.material;
                // Add soft gloss to marble & trims
                if (mat.name && mat.name.includes("Gold")) {
                  mat.roughness = 0.22;
                  mat.metalness = 0.88;
                } else if (mat.name && mat.name.includes("Floor")) {
                  mat.roughness = 0.20;
                }
              }
            });
          });
        }
      } catch (err) {
        console.warn("Tone mapping setup failed", err);
      }
    },

    // --- 2. GSAP Camera Choreography & Smooth Bezier Transitions ---
    setupCameraChoreography() {
      const self = this;
      const rig = this.rig;
      const THREE = window.THREE || window.AFRAME?.THREE;

      // Expose smooth flight API for interactive navigation
      window.VirtuMuseum = window.VirtuMuseum || {};
      window.VirtuMuseum.smoothFlyTo = function (destPos, destYawDeg = null, durationSec = 1.6, onComplete = null) {
        if (!rig || !window.gsap) return;

        const currentPos = rig.object3D.position;
        const targetPos = Array.isArray(destPos) ? { x: destPos[0], y: destPos[1], z: destPos[2] } : destPos;

        // Animate position with smooth cubic bezier curve
        window.gsap.to(currentPos, {
          x: targetPos.x,
          y: targetPos.y,
          z: targetPos.z,
          duration: durationSec,
          ease: "power2.inOut",
          onUpdate: () => {
            rig.setAttribute("position", `${currentPos.x} ${currentPos.y} ${currentPos.z}`);
          },
          onComplete: () => {
            if (typeof onComplete === "function") onComplete();
          }
        });

        // Animate orientation if provided
        if (destYawDeg !== null) {
          const currentRot = rig.getAttribute("rotation") || { x: 0, y: 0, z: 0 };
          const startYaw = currentRot.y;
          // Shortest angular path
          let diff = (destYawDeg - startYaw) % 360;
          if (diff > 180) diff -= 360;
          if (diff < -180) diff += 360;
          const endYaw = startYaw + diff;

          const rotObj = { y: startYaw };
          window.gsap.to(rotObj, {
            y: endYaw,
            duration: durationSec * 0.8,
            ease: "power2.out",
            onUpdate: () => {
              rig.setAttribute("rotation", `0 ${rotObj.y} 0`);
            }
          });
        }
      };

      // Wrap jumpToTourStop to use GSAP flight
      const origJump = window.VirtuMuseum.jumpToTourStop;
      window.VirtuMuseum.jumpToTourStop = function (stopIdx) {
        const tourC = document.querySelector("#tour")?.components?.["tour-guide"];
        if (tourC && tourC.stops && tourC.stops[stopIdx]) {
          const stop = tourC.stops[stopIdx];
          const pos = stop.targetPosition || stop.pos;
          if (pos && window.gsap) {
            let parsed = Array.isArray(pos) ? { x: pos[0], y: pos[1], z: pos[2] } : null;
            if (!parsed && typeof pos === "string") {
              const parts = pos.trim().split(/\s+/).map(Number);
              if (parts.length === 3) parsed = { x: parts[0], y: parts[1], z: parts[2] };
            }
            if (parsed) {
              tourC.idx = stopIdx;
              if (tourC._applyPanel) tourC._applyPanel(stop);
              window.VirtuMuseum.smoothFlyTo(parsed, null, 1.4);
              return;
            }
          }
        }
        if (typeof origJump === "function") origJump(stopIdx);
      };
    },

    // --- 3. Spatial 3D World-to-Screen Interactive Radar Hotspots ---
    initHotspotsDOM() {
      let container = document.querySelector("#spatialHotspotsContainer");
      if (!container) {
        container = document.createElement("div");
        container.id = "spatialHotspotsContainer";
        container.className = "spatialHotspots";
        document.body.appendChild(container);
      }

      this.hotspotElements = this.landmarks.map((landmark) => {
        const el = document.createElement("div");
        el.className = "spatialPin";
        el.dataset.id = landmark.id;
        el.innerHTML = `
          <div class="spatialPin__radar"></div>
          <div class="spatialPin__core">
            <svg class="spatialPin__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M12 2v3m0 14v3M2 12h3m14 0h3"></path>
            </svg>
          </div>
          <div class="spatialPin__badge">
            <span class="spatialPin__name">${landmark.name}</span>
            <span class="spatialPin__dist">-- m</span>
          </div>
        `;

        el.addEventListener("click", () => {
          if (landmark.stopIdx !== undefined && window.VirtuMuseum?.jumpToTourStop) {
            window.VirtuMuseum.jumpToTourStop(landmark.stopIdx);
          } else {
            window.VirtuMuseum?.smoothFlyTo?.(landmark.pos);
          }
        });

        container.appendChild(el);
        return { landmark, el, posVec: null };
      });
    },

    startSpatialHotspotsLoop() {
      const THREE = window.THREE || window.AFRAME?.THREE;
      if (!THREE) return;

      const vCam = new THREE.Vector3();
      const vLandmark = new THREE.Vector3();
      const vProj = new THREE.Vector3();

      const updateLoop = () => {
        requestAnimationFrame(updateLoop);

        if (!this.hotspotsEnabled || !this.camera) return;

        this.camera.getWorldPosition(vCam);
        const w = window.innerWidth;
        const h = window.innerHeight;

        this.hotspotElements.forEach((item) => {
          const { landmark, el } = item;
          vLandmark.set(landmark.pos[0], landmark.pos[1], landmark.pos[2]);

          const dist = vCam.distanceTo(vLandmark);

          // Project to screen coordinates
          vProj.copy(vLandmark).project(this.camera);

          // Check if landmark is in front of camera
          const inFront = vProj.z < 1.0;
          const inScreenBounds = vProj.x >= -1.1 && vProj.x <= 1.1 && vProj.y >= -1.1 && vProj.y <= 1.1;

          if (inFront && inScreenBounds && dist < 45) {
            const screenX = (vProj.x * 0.5 + 0.5) * w;
            const screenY = (-vProj.y * 0.5 + 0.5) * h;

            el.style.transform = `translate3d(${screenX}px, ${screenY}px, 0)`;
            el.classList.remove("is-hidden");

            // Update distance badge
            const distBadge = el.querySelector(".spatialPin__dist");
            if (distBadge) distBadge.textContent = `${Math.round(dist)}m`;

            // Distance attenuation
            if (dist > 28) {
              el.style.opacity = Math.max(0.2, (45 - dist) / 17);
            } else {
              el.style.opacity = 1.0;
            }
          } else {
            el.classList.add("is-hidden");
          }
        });
      };

      requestAnimationFrame(updateLoop);
    },

    // --- 4. Lucide Vector Icon Initializer ---
    initLucideIcons() {
      if (window.lucide && typeof window.lucide.createIcons === "function") {
        window.lucide.createIcons();
      } else {
        window.addEventListener("load", () => {
          if (window.lucide && typeof window.lucide.createIcons === "function") {
            window.lucide.createIcons();
          }
        });
      }
    }
  };

  window.Modern3D = Modern3D;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => Modern3D.init());
  } else {
    Modern3D.init();
  }
})();
