// UI/UX CHANGE: Dedicated UI/UX Enhancement Layer for VIT Vellore Virtual Museum
// Strictly non-invasive: does not modify or overwrite core app.js logic

(function () {
  "use strict";

  // --- 1. Synthesized Audio Feedback & Haptics (UI/UX CHANGE) ---
  const AudioFeedback = {
    ctx: null,
    init() {
      if (!this.ctx && (window.AudioContext || window.webkitAudioContext)) {
        try {
          const AudioCtx = window.AudioContext || window.webkitAudioContext;
          this.ctx = new AudioCtx();
        } catch (e) {
          console.warn("AudioContext not supported", e);
        }
      }
      if (this.ctx && this.ctx.state === "suspended") {
        this.ctx.resume().catch(() => {});
      }
    },
    playTone(freq = 440, type = "sine", duration = 0.12, gainLevel = 0.08) {
      try {
        this.init();
        if (!this.ctx) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
        gain.gain.setValueAtTime(gainLevel, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + duration);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + duration);
      } catch {}
    },
    click() {
      this.playTone(800, "triangle", 0.06, 0.05);
      HapticFeedback.trigger(12);
    },
    success() {
      try {
        this.init();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        [523.25, 659.25, 783.99].forEach((freq, idx) => {
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = "sine";
          osc.frequency.setValueAtTime(freq, now + idx * 0.06);
          gain.gain.setValueAtTime(0.06, now + idx * 0.06);
          gain.gain.exponentialRampToValueAtTime(0.0001, now + idx * 0.06 + 0.18);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(now + idx * 0.06);
          osc.stop(now + idx * 0.06 + 0.18);
        });
      } catch {}
      HapticFeedback.trigger([15, 40, 20]);
    },
    floorSwitch() {
      try {
        this.init();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        [440, 554.37, 659.25].forEach((freq, idx) => {
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = "triangle";
          osc.frequency.setValueAtTime(freq, now + idx * 0.08);
          gain.gain.setValueAtTime(0.08, now + idx * 0.08);
          gain.gain.exponentialRampToValueAtTime(0.0001, now + idx * 0.08 + 0.25);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(now + idx * 0.08);
          osc.stop(now + idx * 0.08 + 0.25);
        });
      } catch {}
      HapticFeedback.trigger([25, 30, 45]);
    },
    exhibitOpen() {
      this.playTone(660, "sine", 0.16, 0.08);
      HapticFeedback.trigger(22);
    }
  };

  const HapticFeedback = {
    trigger(pattern = 15) {
      try {
        if ("vibrate" in navigator && typeof navigator.vibrate === "function") {
          navigator.vibrate(pattern);
        }
      } catch {}
    }
  };

  // --- 2. Toast & Alert Interceptor (UI/UX CHANGE) ---
  function showModernToast(msg, type = "info") {
    let toast = document.querySelector("#appToast");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "appToast";
      toast.className = "toast";
      document.body.appendChild(toast);
    }
    toast.className = `toast toast--${type}`;
    toast.innerHTML = `
      <span class="toast__icon">${type === "error" ? "⚠️" : type === "success" ? "✓" : "✦"}</span>
      <span class="toast__msg">${msg}</span>
    `;
    toast.style.display = "flex";
    toast.style.animation = "none";
    void toast.offsetWidth; // trigger reflow
    toast.style.animation = "toastIn 0.28s cubic-bezier(0.16, 1, 0.3, 1) forwards";

    if (window._toastTimeout) clearTimeout(window._toastTimeout);
    window._toastTimeout = setTimeout(() => {
      toast.style.animation = "toastOut 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards";
      setTimeout(() => {
        toast.style.display = "none";
      }, 250);
    }, 3200);
  }

  // Intercept window.alert to never disrupt user with standard alert boxes
  const nativeAlert = window.alert;
  window.alert = function (message) {
    showModernToast(message, "info");
    console.info("Intercepted alert():", message);
  };

  // --- 3. Loading Experience & Splash Screen (UI/UX CHANGE) ---
  function initLoadingExperience() {
    const splash = document.querySelector("#splashScreen");
    const bar = document.querySelector("#splashProgressBar");
    const percentEl = document.querySelector("#splashProgressPercent");
    const statusEl = document.querySelector("#splashProgressText");
    const museuEl = document.querySelector("#museuModel");

    if (!splash) return;

    let progress = 10;
    const progressInterval = setInterval(() => {
      if (progress < 85) {
        progress += Math.floor(Math.random() * 8) + 3;
        if (progress > 85) progress = 85;
        updateProgress(progress, "Loading Museum Architecture & Assets...");
      }
    }, 180);

    function updateProgress(val, status) {
      if (bar) bar.style.width = `${val}%`;
      if (percentEl) percentEl.textContent = `${Math.min(100, Math.floor(val))}%`;
      if (statusEl && status) statusEl.textContent = status;
    }

    function completeLoading() {
      clearInterval(progressInterval);
      updateProgress(100, "Museum Ready. Welcome!");
      AudioFeedback.success();

      // Trigger smooth scale-in & presentation animation for 3D model
      animateModelPresentation();

      setTimeout(() => {
        splash.classList.add("is-dismissed");
        setTimeout(() => {
          splash.remove();
        }, 650);
      }, 400);
    }

    if (museuEl) {
      museuEl.addEventListener("model-loaded", () => {
        completeLoading();
      });
      museuEl.addEventListener("model-error", () => {
        updateProgress(100, "Starting Exhibition...");
        setTimeout(completeLoading, 500);
      });
    }

    // Safety fallback if model takes long or event already fired
    setTimeout(() => {
      if (document.querySelector("#splashScreen")) {
        completeLoading();
      }
    }, 4500);
  }

  // --- 4. Model Presentation & Smooth Entrance (UI/UX CHANGE) ---
  function animateModelPresentation() {
    const museuEl = document.querySelector("#museuModel");
    if (!museuEl) return;

    // Soft scale-in animation without changing base transforms
    try {
      museuEl.setAttribute("animation__scalein", {
        property: "scale",
        from: "0.96 0.96 0.96",
        to: "1 1 1",
        dur: 1000,
        easing: "easeOutCubic"
      });
    } catch {}

    // Trigger subtle spawn glow effect
    triggerSpawnGlow();
  }

  // Particle & Glow Spawning Burst (UI/UX CHANGE)
  function triggerSpawnGlow() {
    const glow = document.createElement("div");
    glow.className = "spawnGlowEffect";
    document.body.appendChild(glow);
    setTimeout(() => {
      glow.classList.add("is-active");
    }, 50);
    setTimeout(() => {
      glow.remove();
    }, 1800);
  }

  // --- 5. Reticle Interactive Hover Feedback (UI/UX CHANGE) ---
  function initReticleFeedback() {
    const cursor = document.querySelector("a-cursor");
    if (!cursor) return;

    cursor.addEventListener("raycaster-intersection", (e) => {
      const els = e.detail.els;
      const hasInteractable = els.some((el) =>
        el.classList && (
          el.classList.contains("interactable") ||
          el.classList.contains("quadroHitbox") ||
          el.classList.contains("hotspot")
        )
      );
      if (hasInteractable) {
        cursor.setAttribute("material", "color: #10b981; shader: flat"); // Valid interactive target green
        cursor.setAttribute("geometry", "radiusInner: 0.004; radiusOuter: 0.008");
      }
    });

    cursor.addEventListener("raycaster-intersection-cleared", () => {
      cursor.setAttribute("material", "color: #4F8CFF; shader: flat"); // Idle accent color
      cursor.setAttribute("geometry", "radiusInner: 0.003; radiusOuter: 0.006");
    });
  }

  // --- 6. Onboarding 3-Step Guide Modal (UI/UX CHANGE) ---
  function initOnboardingGuide() {
    const guide = document.querySelector("#onboardingGuide");
    const btnDismiss = document.querySelector("#btnOnboardingDismiss");
    const backdrop = document.querySelector("#onboardingBackdrop");
    const btnHelp = document.querySelector("#btnDockHelp");

    function openGuide() {
      AudioFeedback.click();
      guide?.classList.remove("is-hidden");
    }

    function closeGuide() {
      AudioFeedback.click();
      guide?.classList.add("is-hidden");
      localStorage.setItem("virtumuseum.onboarded", "1");
    }

    btnDismiss?.addEventListener("click", closeGuide);
    backdrop?.addEventListener("click", closeGuide);
    btnHelp?.addEventListener("click", openGuide);

    // Auto-open on first visit if not seen
    const seen = localStorage.getItem("virtumuseum.onboarded") === "1";
    if (!seen) {
      // Allow user to explore welcome screen first, guide is ready via ?
    }
  }

  // --- 7. Glassmorphic Bottom Toolbar (UI/UX CHANGE) ---
  function initBottomToolbar() {
    const toolbar = document.querySelector("#bottomToolbar");
    const btnDockMap = document.querySelector("#btnDockMap");
    const btnDockTour = document.querySelector("#btnDockTour");
    const btnDockFloor = document.querySelector("#btnDockFloor");
    const btnDockReset = document.querySelector("#btnDockReset");
    const btnDockAudio = document.querySelector("#btnDockAudio");
    const btnDockScreenshot = document.querySelector("#btnDockScreenshot");

    // Hook Map
    btnDockMap?.addEventListener("click", () => {
      AudioFeedback.click();
      const mapBtn = document.querySelector("#btnMap");
      mapBtn?.click();
    });

    // Hook Tour
    btnDockTour?.addEventListener("click", () => {
      AudioFeedback.click();
      const tourProgress = document.querySelector("#tourProgress");
      const isTourActive = tourProgress && !tourProgress.classList.contains("is-hidden");
      if (isTourActive) {
        document.querySelector("#btnTourEndBar")?.click();
        btnDockTour.classList.remove("is-active");
      } else {
        const tourBtn = document.querySelector("#btnTourBar") || document.querySelector("#btnEnterTour");
        tourBtn?.click();
        btnDockTour.classList.add("is-active");
      }
    });

    // Hook Floor Switch
    btnDockFloor?.addEventListener("click", () => {
      AudioFeedback.floorSwitch();
      const elevatorBtn = document.querySelector("#btnElevatorQuick");
      elevatorBtn?.click();
      updateFloorBadgeInToolbar();
    });

    // Hook Reset Position
    btnDockReset?.addEventListener("click", () => {
      AudioFeedback.click();
      const resetBtn = document.querySelector("#btnReset");
      if (resetBtn) {
        resetBtn.click();
      } else {
        const rig = document.querySelector("#rig");
        if (rig) {
          rig.setAttribute("position", "0.00 0.00 15.00");
          rig.setAttribute("rotation", "0 0 0");
        }
      }
      showModernToast("Position reset to Grand Lobby entrance.", "info");
    });

    // Hook Audio Toggle
    btnDockAudio?.addEventListener("click", () => {
      AudioFeedback.click();
      const chk = document.querySelector("#chkAmbient");
      if (chk) {
        chk.checked = !chk.checked;
        chk.dispatchEvent(new Event("change"));
        btnDockAudio.classList.toggle("is-active", chk.checked);
        showModernToast(chk.checked ? "Ambient sound turned ON" : "Ambient sound muted", "info");
      }
    });

    // Hook Screenshot
    btnDockScreenshot?.addEventListener("click", () => {
      AudioFeedback.click();
      takeSceneScreenshot();
    });

    // Sync Floor indicator state
    function updateFloorBadgeInToolbar() {
      setTimeout(() => {
        const hudNum = document.querySelector("#hudFloorNum")?.textContent;
        const label = document.querySelector("#dockFloorLabel");
        if (label && hudNum) {
          label.textContent = hudNum.includes("2") ? "Floor 2" : "Floor 1";
        }
      }, 150);
    }

    // Observe HUD floor changes
    const hudFloor = document.querySelector("#hudFloorIndicator");
    if (hudFloor) {
      hudFloor.addEventListener("click", () => {
        AudioFeedback.floorSwitch();
        updateFloorBadgeInToolbar();
      });
    }

    // Attach click feedback to all interactive buttons
    document.querySelectorAll("button").forEach((btn) => {
      btn.addEventListener("click", () => {
        AudioFeedback.click();
      });
    });

    // Attach exhibit click feedback
    window.addEventListener("click", (e) => {
      if (e.target.closest && (e.target.closest(".quadroHitbox") || e.target.closest("#btnExhibitClose"))) {
        AudioFeedback.exhibitOpen();
      }
    });
  }

  // --- 8. High-Res Canvas Screenshot (UI/UX CHANGE) ---
  function takeSceneScreenshot() {
    try {
      const scene = document.querySelector("a-scene");
      if (!scene) return;
      const canvas = scene.canvas || scene.querySelector("canvas");
      if (!canvas) {
        showModernToast("Unable to capture scene canvas.", "error");
        return;
      }
      const dataURL = canvas.toDataURL("image/png");
      const a = document.createElement("a");
      a.href = dataURL;
      a.download = `vit-vellore-museum-${Date.now()}.png`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      showModernToast("Screenshot saved to downloads! 📸", "success");
      AudioFeedback.success();
    } catch (err) {
      console.warn("Screenshot capture failed:", err);
      showModernToast("Screenshot error. Please check permissions.", "error");
    }
  }

  // Initialize all enhancements on DOM ready
  function initEnhancements() {
    initLoadingExperience();
    initOnboardingGuide();
    initBottomToolbar();
    initReticleFeedback();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initEnhancements);
  } else {
    initEnhancements();
  }
})();
