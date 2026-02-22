# Navigation Reference

Complete JavaScript and CSS for both navigation modes. Copy the appropriate mode into the presentation HTML.

## Table of Contents

1. [Horizontal Mode (Reveal.js)](#horizontal-mode-revealjs)
2. [Vertical Scroll Mode](#vertical-scroll-mode)

---

## Horizontal Mode (Reveal.js)

Uses Reveal.js for slide navigation. Slides go left-to-right. Arrow keys, mouse wheel, swipe, and click controls all work.

### CDN Includes (in `<head>`)

```html
<!-- Reveal.js CSS -->
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.css"
/>

<!-- Syntax highlighting theme (only if code blocks present) -->
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/highlight/monokai.css"
/>
```

### Scripts (before `</body>`)

```html
<!-- Reveal.js Core -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.js"></script>

<!-- Highlight plugin (only if code blocks present) -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/highlight/highlight.js"></script>

<!-- Lucide Icons -->
<script src="https://unpkg.com/lucide@latest"></script>

<script>
  Reveal.initialize({
    hash: true,
    slideNumber: true,
    controls: true,
    controlsLayout: "bottom-right",
    controlsBackArrows: "faded",
    progress: true,
    center: false,
    transition: "slide",
    backgroundTransition: "fade",
    width: "100%",
    height: "100%",
    margin: 0.04,
    minScale: 0.2,
    maxScale: 2,
    autoAnimate: true,
    autoAnimateDuration: 0.7,
    navigationMode: "linear",
    disableLayout: false,
    // Enable mouse wheel navigation
    mouseWheel: true,
    // Include highlight plugin only if code blocks are present
    plugins: [RevealHighlight],
  });

  // Initialize Lucide icons
  lucide.createIcons();
</script>
```

**Important:** If no code blocks exist in the presentation, remove the highlight CSS, the highlight JS script, and `RevealHighlight` from the plugins array.

### Mouse Wheel

Reveal.js has built-in mouse wheel support. Set `mouseWheel: true` in the config. Each scroll tick advances or retreats one slide/fragment.

---

## Vertical Scroll Mode

Zero dependency on Reveal.js. Pure CSS scroll-snap + vanilla JS. Slides go top-to-bottom.

### HTML Structure

```html
<body>
  <div class="presentation-viewport" id="presentation">
    <section class="v-slide" id="slide-1">
      <div class="slide slide--section slide--center">
        <!-- slide content -->
      </div>
    </section>
    <section class="v-slide" id="slide-2">
      <div class="slide">
        <!-- slide content -->
      </div>
    </section>
    <!-- more slides... -->
  </div>

  <!-- Progress bar -->
  <div class="scroll-progress-track">
    <div class="scroll-progress-bar" id="progressBar"></div>
  </div>

  <!-- Slide counter -->
  <div class="slide-counter" id="slideCounter">1 / N</div>

  <!-- Navigation arrows -->
  <div class="nav-arrows">
    <button
      class="nav-arrow nav-arrow--up"
      id="navUp"
      aria-label="Previous slide"
    >
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <polyline points="18 15 12 9 6 15" />
      </svg>
    </button>
    <button
      class="nav-arrow nav-arrow--down"
      id="navDown"
      aria-label="Next slide"
    >
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <polyline points="6 9 12 15 18 9" />
      </svg>
    </button>
  </div>

  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <script>
    lucide.createIcons();
  </script>
</body>
```

### CSS for Vertical Scroll

Add this INSTEAD of the Reveal.js CSS and overrides:

```css
/* === VERTICAL SCROLL NAVIGATION === */
.presentation-viewport {
  height: 100vh;
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}

.v-slide {
  height: 100vh;
  width: 100%;
  scroll-snap-align: start;
  scroll-snap-stop: always;
  position: relative;
  overflow: hidden;
}

/* Fragment animations via IntersectionObserver */
.v-slide .fragment {
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity 0.5s ease,
    transform 0.5s ease;
}

.v-slide .fragment.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Stagger fragment animations */
.v-slide .fragment:nth-child(1) {
  transition-delay: 0.1s;
}
.v-slide .fragment:nth-child(2) {
  transition-delay: 0.2s;
}
.v-slide .fragment:nth-child(3) {
  transition-delay: 0.3s;
}
.v-slide .fragment:nth-child(4) {
  transition-delay: 0.4s;
}
.v-slide .fragment:nth-child(5) {
  transition-delay: 0.5s;
}
.v-slide .fragment:nth-child(6) {
  transition-delay: 0.6s;
}
.v-slide .fragment:nth-child(7) {
  transition-delay: 0.7s;
}
.v-slide .fragment:nth-child(8) {
  transition-delay: 0.8s;
}
.v-slide .fragment:nth-child(9) {
  transition-delay: 0.9s;
}

/* Progress bar */
.scroll-progress-track {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: var(--border);
  z-index: 1000;
}

.scroll-progress-bar {
  height: 100%;
  background: var(--accent);
  width: 0%;
  transition: width 0.15s ease;
}

/* Slide counter */
.slide-counter {
  position: fixed;
  bottom: 16px;
  right: 20px;
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-muted);
  z-index: 1000;
}

/* Navigation arrows */
.nav-arrows {
  position: fixed;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 1000;
}

.nav-arrow {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0;
}

.nav-arrow:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.nav-arrow:disabled {
  opacity: 0.3;
  cursor: default;
}

/* Hide nav arrows on mobile */
@media (max-width: 768px) {
  .nav-arrows {
    display: none;
  }
}
```

### JavaScript for Vertical Scroll

```javascript
(function () {
  const viewport = document.getElementById("presentation");
  const slides = document.querySelectorAll(".v-slide");
  const progressBar = document.getElementById("progressBar");
  const slideCounter = document.getElementById("slideCounter");
  const navUp = document.getElementById("navUp");
  const navDown = document.getElementById("navDown");
  const totalSlides = slides.length;
  let currentSlide = 0;
  let isScrolling = false;
  let scrollTimeout;

  // ── Navigate to slide ──
  function goToSlide(index) {
    if (index < 0 || index >= totalSlides || isScrolling) return;
    isScrolling = true;
    currentSlide = index;
    slides[index].scrollIntoView({ behavior: "smooth" });
    updateUI();
    // Debounce: prevent rapid navigation
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
      isScrolling = false;
    }, 600);
  }

  function nextSlide() {
    goToSlide(currentSlide + 1);
  }
  function prevSlide() {
    goToSlide(currentSlide - 1);
  }

  // ── Update progress bar, counter, nav arrows ──
  function updateUI() {
    const progress = ((currentSlide + 1) / totalSlides) * 100;
    progressBar.style.width = progress + "%";
    slideCounter.textContent = currentSlide + 1 + " / " + totalSlides;
    navUp.disabled = currentSlide === 0;
    navDown.disabled = currentSlide === totalSlides - 1;
  }

  // ── Keyboard navigation ──
  document.addEventListener("keydown", function (e) {
    switch (e.key) {
      case "ArrowDown":
      case "ArrowRight":
      case " ":
      case "PageDown":
        e.preventDefault();
        nextSlide();
        break;
      case "ArrowUp":
      case "ArrowLeft":
      case "PageUp":
        e.preventDefault();
        prevSlide();
        break;
      case "Home":
        e.preventDefault();
        goToSlide(0);
        break;
      case "End":
        e.preventDefault();
        goToSlide(totalSlides - 1);
        break;
    }
  });

  // ── Mouse wheel navigation (debounced) ──
  let wheelTimeout;
  viewport.addEventListener(
    "wheel",
    function (e) {
      e.preventDefault();
      clearTimeout(wheelTimeout);
      wheelTimeout = setTimeout(() => {
        if (e.deltaY > 0) nextSlide();
        else if (e.deltaY < 0) prevSlide();
      }, 50);
    },
    { passive: false },
  );

  // ── Touch swipe navigation ──
  let touchStartY = 0;
  let touchEndY = 0;

  viewport.addEventListener(
    "touchstart",
    function (e) {
      touchStartY = e.changedTouches[0].screenY;
    },
    { passive: true },
  );

  viewport.addEventListener(
    "touchend",
    function (e) {
      touchEndY = e.changedTouches[0].screenY;
      const diff = touchStartY - touchEndY;
      if (Math.abs(diff) > 50) {
        // minimum swipe distance
        if (diff > 0) nextSlide();
        else prevSlide();
      }
    },
    { passive: true },
  );

  // ── Click navigation arrows ──
  navUp.addEventListener("click", prevSlide);
  navDown.addEventListener("click", nextSlide);

  // ── Scroll-based current slide detection ──
  // Uses IntersectionObserver to track which slide is in view
  const slideObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && entry.intersectionRatio > 0.5) {
          const index = Array.from(slides).indexOf(entry.target);
          if (index !== -1) {
            currentSlide = index;
            updateUI();
          }
        }
      });
    },
    {
      root: viewport,
      threshold: 0.5,
    },
  );

  slides.forEach((slide) => slideObserver.observe(slide));

  // ── Fragment animations via IntersectionObserver ──
  const fragmentObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          // Find all fragments in this slide and reveal them
          const fragments = entry.target.querySelectorAll(".fragment");
          fragments.forEach((frag, i) => {
            setTimeout(() => frag.classList.add("visible"), i * 150);
          });
        } else {
          // Reset fragments when slide leaves viewport
          const fragments = entry.target.querySelectorAll(".fragment");
          fragments.forEach((frag) => frag.classList.remove("visible"));
        }
      });
    },
    {
      root: viewport,
      threshold: 0.3,
    },
  );

  slides.forEach((slide) => fragmentObserver.observe(slide));

  // ── Initialize ──
  updateUI();
})();
```

### Important Notes for Vertical Mode

1. **No Reveal.js CDN needed** — do not include `reveal.css` or `reveal.js`
2. **Do not use** `.reveal` or `.slides` wrapper divs — use `.presentation-viewport` and `.v-slide`
3. **The `.slide` inner div** is still used for content layout — it's the same as horizontal mode
4. **Fragment class** still works but is triggered by IntersectionObserver instead of Reveal.js
5. **All CSS component classes** (`.card`, `.metric`, `.split`, etc.) work identically in both modes
6. **Links are naturally clickable** — no pointer-events hacks needed
7. **URL hash navigation** — add `id="slide-N"` to each v-slide for bookmarkable URLs
