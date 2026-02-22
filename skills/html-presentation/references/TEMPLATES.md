# Slide Template Reference

HTML patterns for each slide layout type. Copy and adapt these when building slides.

All templates work in both horizontal (Reveal.js) and vertical (scroll) modes. In horizontal mode, each slide is a `<section>`. In vertical mode, each slide is a `<section class="v-slide">`.

## Table of Contents

1. [Title Slide](#title-slide)
2. [Section Divider](#section-divider)
3. [Split Layout](#split-layout)
4. [Grid Cards](#grid-cards)
5. [Metrics / Stats](#metrics--stats)
6. [Quote Slide](#quote-slide)
7. [Workflow / Pipeline](#workflow--pipeline)
8. [Comparison Table](#comparison-table)
9. [Timeline](#timeline)
10. [Numbered List](#numbered-list)
11. [Code Slide](#code-slide)
12. [CTA / Closing](#cta--closing)
13. [Assembling the Full Deck](#assembling-the-full-deck)

---

## Title Slide

The opening slide. Centered, large text, optional badge and subtitle.

```html
<section>
  <div class="slide slide--section slide--center">
    <div
      class="content flex-center"
      style="flex-direction: column; text-align: center;"
    >
      <p class="kicker" style="justify-content: center;">
        SUBTITLE OR CONTEXT LINE
      </p>
      <h1>Main Title<br /><span class="accent-text">Accent Phrase</span></h1>
      <p class="lead" style="max-width: 700px; margin: 0 auto;">
        A brief description or tagline that sets the stage for the presentation.
      </p>
      <div style="margin-top: 40px;">
        <span class="badge">BADGE LABEL</span>
      </div>
    </div>
  </div>
</section>
```

---

## Section Divider

Used between major parts of the presentation. Centered text with glow background.

```html
<section>
  <div class="slide slide--section slide--center">
    <p class="kicker" style="justify-content: center;">## // SECTION NAME</p>
    <h2>Section Title</h2>
    <p class="lead muted" style="max-width: 700px;">
      Brief description of what this section covers.
    </p>
    <div style="margin-top: 40px;">
      <span class="badge badge--success">ACTION LABEL</span>
    </div>
  </div>
</section>
```

---

## Split Layout

Left side: text (kicker, headline, lead). Right side: supporting content (list, cards, image placeholder).

```html
<section>
  <div class="slide">
    <div class="header">
      <div class="header__logo">
        <i data-lucide="ICON_NAME"></i>
        Section Label
      </div>
    </div>
    <div class="split">
      <div>
        <p class="kicker">## // KICKER TEXT</p>
        <h2>Headline<br />Second Line</h2>
        <p class="lead">Supporting paragraph text that provides context.</p>
      </div>
      <div>
        <ul class="list">
          <li class="fragment">
            <strong>Point One</strong><br /><span class="muted"
              >Description</span
            >
          </li>
          <li class="fragment">
            <strong>Point Two</strong><br /><span class="muted"
              >Description</span
            >
          </li>
          <li class="fragment">
            <strong>Point Three</strong><br /><span class="muted"
              >Description</span
            >
          </li>
        </ul>
      </div>
    </div>
  </div>
</section>
```

**Variants:**

- `split--60-40` — left column wider (for text-heavy left side)
- `split--40-60` — right column wider (for content-heavy right side)
- Right side can contain: `list`, `list--check`, `list--numbered`, cards, `quote-block`, or any HTML

---

## Grid Cards

For 2-6 equal items. Choose `grid-2`, `grid-3`, or `grid-4` based on item count.

```html
<section>
  <div class="slide">
    <div class="header">
      <div class="header__logo">
        <i data-lucide="ICON_NAME"></i>
        Section Label
      </div>
    </div>
    <div class="content">
      <p class="kicker">## // KICKER TEXT</p>
      <h2>Grid Headline</h2>
      <div class="grid-3" style="margin-top: 32px;">
        <div class="card fragment fade-up">
          <div class="card__icon"><i data-lucide="ICON"></i></div>
          <h4 class="card__title">Card Title</h4>
          <p class="card__text">Brief description of this item.</p>
        </div>
        <div class="card fragment fade-up">
          <div class="card__icon"><i data-lucide="ICON"></i></div>
          <h4 class="card__title">Card Title</h4>
          <p class="card__text">Brief description of this item.</p>
        </div>
        <div class="card fragment fade-up">
          <div class="card__icon"><i data-lucide="ICON"></i></div>
          <h4 class="card__title">Card Title</h4>
          <p class="card__text">Brief description of this item.</p>
        </div>
      </div>
    </div>
  </div>
</section>
```

**Card variants:**

- `card--danger` — red border (risks, problems)
- `card--success` — green border (solutions, benefits)
- `card--warning` — amber border (cautions, caveats)
- `card--featured` — accent border (highlighted item)

---

## Metrics / Stats

For showcasing key numbers. Use 3-4 metrics for best visual balance.

```html
<section>
  <div class="slide">
    <div class="header">
      <div class="header__logo">
        <i data-lucide="ICON_NAME"></i>
        Section Label
      </div>
    </div>
    <div class="content">
      <p class="kicker">## // KICKER TEXT</p>
      <h2>Key Numbers Headline</h2>
      <div class="metrics" style="margin-top: 48px;">
        <div class="metric fragment">
          <div class="metric__value">42K</div>
          <div class="metric__label">Metric Label</div>
        </div>
        <div class="metric fragment">
          <div class="metric__value">99.9%</div>
          <div class="metric__label">Metric Label</div>
        </div>
        <div class="metric fragment">
          <div class="metric__value">$2.5M</div>
          <div class="metric__label">Metric Label</div>
        </div>
        <div class="metric fragment">
          <div class="metric__value">< 5ms</div>
          <div class="metric__label">Metric Label</div>
        </div>
      </div>
      <div style="margin-top: 40px;" class="fragment">
        <p class="muted" style="font-size: 0.9rem;">
          Optional footnote or source citation.
        </p>
      </div>
    </div>
  </div>
</section>
```

**Variant:** Add `metric--danger` class for negative metrics (risks, losses).

---

## Quote Slide

For expert quotes, testimonials, or key statements. Works well in split layout.

```html
<section>
  <div class="slide">
    <div class="header">
      <div class="header__logo">
        <i data-lucide="message-circle"></i>
        Section Label
      </div>
    </div>
    <div class="split">
      <div>
        <p class="kicker">## // KICKER TEXT</p>
        <h2>Quote Headline</h2>
        <p class="lead">Context for why these quotes matter.</p>
      </div>
      <div>
        <div class="quote-block fragment" style="margin-bottom: 24px;">
          "The actual quote text goes here."
          <div class="quote-author">Author Name, Title, Organization</div>
        </div>
        <div class="quote-block fragment" style="margin-bottom: 24px;">
          "Another quote for contrast or reinforcement."
          <div class="quote-author">Author Name, Title, Organization</div>
        </div>
      </div>
    </div>
  </div>
</section>
```

---

## Workflow / Pipeline

For sequential processes. Uses arrow connectors between boxes.

```html
<section>
  <div class="slide">
    <div class="header">
      <div class="header__logo">
        <i data-lucide="git-branch"></i>
        Section Label
      </div>
    </div>
    <div class="content">
      <p class="kicker">## // KICKER TEXT</p>
      <h2>Process Headline</h2>
      <div class="workflow" style="margin-top: 48px;">
        <div class="workflow__step fragment">
          <div class="workflow__box">
            <div class="workflow__label">Step 1</div>
            <div class="workflow__sublabel">Detail</div>
          </div>
        </div>
        <div class="workflow__arrow">→</div>
        <div class="workflow__step fragment">
          <div class="workflow__box">
            <div class="workflow__label">Step 2</div>
            <div class="workflow__sublabel">Detail</div>
          </div>
        </div>
        <div class="workflow__arrow">→</div>
        <div class="workflow__step fragment">
          <div class="workflow__box">
            <div class="workflow__label">Step 3</div>
            <div class="workflow__sublabel">Detail</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
```

**Notes:** Keep to 3-5 steps max. For longer flows, break across multiple slides. Use `style="border-color: var(--success);"` on individual boxes to highlight key steps.

---

## Comparison Table

For feature comparisons, before/after, us vs. them.

```html
<section>
  <div class="slide">
    <div class="header">
      <div class="header__logo">
        <i data-lucide="ICON_NAME"></i>
        Section Label
      </div>
    </div>
    <div class="content">
      <p class="kicker">## // KICKER TEXT</p>
      <h2>Comparison Headline</h2>
      <table class="comparison-table" style="margin-top: 32px;">
        <thead>
          <tr>
            <th>Feature</th>
            <th>Option A</th>
            <th>Option B</th>
          </tr>
        </thead>
        <tbody>
          <tr class="fragment">
            <td>Feature Name</td>
            <td><span class="check">✓</span></td>
            <td><span class="cross">✗</span></td>
          </tr>
          <tr class="fragment">
            <td>Another Feature</td>
            <td><span class="cross">✗</span></td>
            <td><span class="check">✓</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</section>
```

---

## Timeline

For roadmaps, chronological events, project phases.

```html
<section>
  <div class="slide">
    <div class="header">
      <div class="header__logo">
        <i data-lucide="clock"></i>
        Section Label
      </div>
    </div>
    <div class="content">
      <p class="kicker">## // KICKER TEXT</p>
      <h2>Timeline Headline</h2>
      <div class="timeline" style="margin-top: 48px;">
        <div class="timeline__item fragment">
          <div class="timeline__year">Q1</div>
          <div class="timeline__dot"></div>
          <div class="timeline__content">Phase description</div>
        </div>
        <div class="timeline__item fragment">
          <div class="timeline__year">Q2</div>
          <div class="timeline__dot"></div>
          <div class="timeline__content">Phase description</div>
        </div>
        <div class="timeline__item fragment">
          <div class="timeline__year">Q3</div>
          <div class="timeline__dot"></div>
          <div class="timeline__content">Phase description</div>
        </div>
        <div class="timeline__item fragment">
          <div class="timeline__year">Q4</div>
          <div class="timeline__dot"></div>
          <div class="timeline__content">Phase description</div>
        </div>
      </div>
    </div>
  </div>
</section>
```

---

## Numbered List

For ordered items where sequence matters.

```html
<!-- Same as Split Layout but using list--numbered on the right side -->
<ul class="list list--numbered">
  <li class="fragment">
    <strong>First Item</strong><br />
    <span class="muted">Description of the first item</span>
  </li>
  <li class="fragment">
    <strong>Second Item</strong><br />
    <span class="muted">Description of the second item</span>
  </li>
</ul>
```

Other list variants: `list--check` (green checkmarks), `list--x` (red crosses).

---

## Code Slide

For showing code snippets with syntax highlighting. Requires the Reveal.js highlight plugin in horizontal mode.

```html
<section>
  <div class="slide">
    <div class="header">
      <div class="header__logo">
        <i data-lucide="code"></i>
        Code
      </div>
    </div>
    <div class="content">
      <p class="kicker">## // KICKER TEXT</p>
      <h2>Code Example</h2>
      <pre><code class="language-python">
def example():
    """Clean, readable code example."""
    return "Hello, Presentation"
      </code></pre>
    </div>
  </div>
</section>
```

---

## CTA / Closing

Final slide with call-to-action and contact links.

```html
<section>
  <div class="slide slide--section slide--center">
    <div class="content flex-center" style="flex-direction: column;">
      <h1>Closing<br /><span class="accent-text">Call to Action</span></h1>
      <p class="lead" style="margin-bottom: 40px;">
        Final message or instruction.
      </p>
      <div
        class="contact-grid"
        style="width: 100%; max-width: 700px;"
        data-prevent-swipe
      >
        <div class="contact-item">
          <div class="contact-item__label">Label</div>
          <a
            href="https://example.com"
            target="_blank"
            rel="noopener"
            class="contact-item__value"
            style="color: var(--accent); text-decoration: none;"
            data-prevent-swipe
            >Link Text</a
          >
        </div>
        <div class="contact-item">
          <div class="contact-item__label">Label</div>
          <span class="contact-item__value">Value</span>
        </div>
        <div class="contact-item">
          <div class="contact-item__label">Label</div>
          <span class="contact-item__value">Value</span>
        </div>
      </div>
    </div>
  </div>
</section>
```

---

## Assembling the Full Deck

### Horizontal Mode (Reveal.js)

```html
<div class="reveal">
  <div class="slides">
    <!-- Each <section> is one slide -->
    <section><!-- Title Slide --></section>
    <section><!-- Content Slide --></section>
    <section><!-- ... --></section>
  </div>
</div>
```

### Vertical Scroll Mode

```html
<div class="presentation-viewport">
  <!-- Each <section class="v-slide"> is one slide -->
  <section class="v-slide"><!-- Title Slide --></section>
  <section class="v-slide"><!-- Content Slide --></section>
  <section class="v-slide"><!-- ... --></section>

  <!-- Navigation UI -->
  <div class="scroll-progress"></div>
  <div class="slide-counter">1 / N</div>
</div>
```

### Lucide Icons

Always initialize after the slides HTML:

```html
<script src="https://unpkg.com/lucide@latest"></script>
<script>
  lucide.createIcons();
</script>
```

Common icons for headers: `sparkles`, `alert-triangle`, `shield-off`, `message-circle`, `bug`, `git-branch`, `phone-call`, `layers`, `compass`, `dollar-sign`, `code`, `zap`, `lock`, `rocket`, `target`, `brain`, `database`, `server`, `cloud`, `bar-chart`, `pie-chart`, `trending-up`, `check-circle`, `x-circle`, `clock`, `calendar`, `users`, `settings`, `globe`, `package`, `cpu`, `hard-drive`, `terminal`.
