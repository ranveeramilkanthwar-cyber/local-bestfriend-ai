---
name: Cozy Artisanal Café AI
colors:
  surface: '#fff8f7'
  surface-dim: '#fcd0cb'
  surface-bright: '#fff8f7'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fff0ee'
  surface-container: '#ffe9e6'
  surface-container-high: '#ffe2de'
  surface-container-highest: '#ffdad6'
  on-surface: '#2d1513'
  on-surface-variant: '#544245'
  inverse-surface: '#442926'
  inverse-on-surface: '#ffedea'
  outline: '#877275'
  outline-variant: '#d9c0c4'
  surface-tint: '#99415a'
  primary: '#99415a'
  on-primary: '#ffffff'
  primary-container: '#f78da7'
  on-primary-container: '#73243c'
  inverse-primary: '#ffb1c2'
  secondary: '#805345'
  on-secondary: '#ffffff'
  secondary-container: '#fdc1af'
  on-secondary-container: '#794d3f'
  tertiary: '#4e6446'
  on-tertiary: '#ffffff'
  tertiary-container: '#9cb491'
  on-tertiary-container: '#32462b'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffd9e0'
  primary-fixed-dim: '#ffb1c2'
  on-primary-fixed: '#3f0018'
  on-primary-fixed-variant: '#7b2a42'
  secondary-fixed: '#ffdbd0'
  secondary-fixed-dim: '#f4b9a7'
  on-secondary-fixed: '#321208'
  on-secondary-fixed-variant: '#653c2f'
  tertiary-fixed: '#d1eac4'
  tertiary-fixed-dim: '#b5cea9'
  on-tertiary-fixed: '#0d2008'
  on-tertiary-fixed-variant: '#374c30'
  background: '#fff8f7'
  on-background: '#2d1513'
  surface-variant: '#ffdad6'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 48px
    fontWeight: '800'
    lineHeight: 56px
    letterSpacing: -0.03em
  display-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 34px
    fontWeight: '800'
    lineHeight: 42px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 20px
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '700'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 10px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.04em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  gutter: 1.25rem
  gutter-desktop: 2rem
  margin: 1rem
  margin-tablet: 1.5rem
  margin-desktop: 3rem
  space-xs: 0.375rem
  space-sm: 0.75rem
  space-md: 1.25rem
  space-lg: 1.75rem
  space-xl: 2.5rem
---

## Brand & Style
The design system envisions a deeply comforting, tactile sanctuary—bridging the intimate hospitality of an artisanal neighborhood café with the intelligent companionship of a thoughtful conversational partner. It is created for mindful individuals seeking a calmer, slower digital ambiance away from clinical or hyper-corporate interfaces. 

The aesthetic philosophy fuses **Claymorphism** and **Glassmorphism**:
- Soft, pillowy, extruded clay surfaces establish tactile presence and emotional safety.
- Airy, frosted milk-glass overlays (`backdrop-filter: blur(24px)`) provide luminous contrast, preventing the interface from feeling dense or heavy.
- Warm specular highlights evoke porcelain cups, steamed milk foam, and natural daylight filtering through café windowpanes.

## Colors
The core palette mimics the sensory experience of a pastry kitchen and specialty roastery:

- **Primary (`#F78DA7`):** Strawberry cream syrup; utilized for high-emphasis interactive triggers, playful badges, and warm voice wave pulses.
- **Secondary (`#784C3E`):** Steamed mocha espresso; grounds interactive accents, structural outlines, and key icon states.
- **Tertiary (`#98B08D`):** Ceremonial matcha green; signals positive verification, natural balance, and serene focus modes.
- **Neutral (`#4A2E2B`):** Deep roasted dark chocolate beans; replaces standard pitch-black to deliver human-readable contrast without optical fatigue.
- **Canvas Base:** Soft milky white (`#FCF9F6`), blended with warm strawberry foam (`#FFF0F3`) and frosted translucent whites (`rgba(255, 255, 255, 0.72)`).
- **Secondary Accent:** Caramel drizzle (`#B5835A`), reserved for warm highlight trims and notifications.

### Multi-Theme Dynamic Adaptations
- **Strawberry Latte (Default):** Canvas tint of `#FFF0F3` with `#F78DA7` highlights.
- **Roasted Mocha:** Canvas shifts to deep oatmeal (`#F5EFEB`) with dominant mocha (`#4A2E2B`) and caramel (`#B5835A`) clay surfaces.
- **Vanilla Cream:** Monochromatic whipped cream foundations (`#FCF9F6`, `#FFFFFF`) with muted cocoa-butter accents.
- **Matcha Breeze:** Canvas tint of soft matcha foam (`#F2F6F1`) paired with calming matcha-leaf tones (`#98B08D`).

## Typography
Plus Jakarta Sans was selected for its geometric softness, wide open counters, and human-friendly terminal shapes that emulate organic signage and rounded chalkboards. 

To maintain legibility against frosted glass layers and puffy clay surfaces:
- Conversational chat turns utilize `body-lg` (18px) for assistant replies, ensuring comfortable, conversational pacing without straining eyes.
- User input states prioritize `body-md` (15px).
- Labels, meta timestamps, and vocal transcript flags rely on medium and semibold weights (`600`–`700`) to guarantee high clarity across non-flat, textured surfaces.

## Layout & Spacing
The layout follows a centered, comfortable fluid grid that hugs conversations like an intimate two-top café booth.

- **Grid Architecture:** Desktop displays standard 12-column layouts with maximum conversational widths capped at `840px` to maintain optimal line-lengths and reading intimacy. Tablets employ an 8-column layout, and mobile devices operate on a responsive 4-column flow.
- **Rhythm & Padding:** Spacing tokens intentionally lean larger than traditional utility platforms to support the puffy geometry of clay surfaces. Touch targets demand generous margins (`margin: 1rem` on mobile, expanding to `3rem` on desktop canvas boundaries).
- **Conversational Air:** Bubble clusters preserve a strict `space-xs` (6px) sibling separation within grouped thoughts, and `space-md` (20px) between alternate speaker turns.

## Elevation & Depth
Elevation is expressed through physical extrusion (Claymorphism) paired with light refraction (Glassmorphism), never through raw flat dropshadows.

1. **Clay Depth (Extruded Surfaces):**
   - **Resting Clay:** Dual shadow structure comprising a top-left inner light bounce (`inset 2px 2px 4px rgba(255, 255, 255, 0.9)`) combined with an underside ambient drop cushion (`0 8px 20px -4px rgba(74, 46, 43, 0.08), inset -2px -3px 6px rgba(120, 76, 62, 0.12)`).
   - **Pressed / Squished Clay:** Inset shadow flips downwards (`inset 2px 3px 6px rgba(74, 46, 43, 0.18)`), while drop elevation flattens (`0 2px 6px rgba(74, 46, 43, 0.06)`), producing a responsive silicone-like squeeze.

2. **Frosted Milk-Glass (Translucent Overlays):**
   - Backdrop filter applied at `blur(20px) saturate(160%)`.
   - Surface color utilizes `rgba(255, 255, 255, 0.72)` during day light and `rgba(252, 249, 246, 0.85)` in warmer themes.
   - Finished with a soft 1px border perimeter of `rgba(255, 255, 255, 0.8)`.

3. **Floating Audio / Action Nodes:**
   - Pill and circular interactive hubs utilize elevated floating tiers (`0 14px 28px -6px rgba(247, 141, 167, 0.35)`).

## Shapes
The shape language relies entirely on full pill geometry and organic, dough-like rounded silhouettes:

- Buttons, vocal visualizers, and system prompts adopt hyper-rounded pill styling (`border-radius: 9999px`).
- Card containers, dialogue bubbles, and floating panels embrace deep squircle curvature (starting at `2rem` and scaling up to `3rem` on overarching cards).
- Corners are deliberately non-rigid to simulate clay and hand-crafted ceramics. No sharp corners exist within the core interactive view.

## Components

### Buttons
- **Clay Primary:** Thick strawberry pink pill (`#F78DA7`), white text, warm specular highlight along the upper rim, deep shaded cushion at the base. Depresses smoothly on click with a tactile 2px translation.
- **Glass Secondary:** Translucent milk glass (`rgba(255,255,255,0.65)`) with an espresso icon or label (`#4A2E2B`), surrounded by a delicate semi-translucent perimeter.

### Conversational Bubbles
- **AI Persona (Barista):** Cloud-white clay card with soft mocha typography. Includes a micro-embossed coffee steam motif or mood avatar at the header.
- **User Turn:** Strawberry cream clay bubble right-aligned, using darker berry-espresso text for high-contrast accessibility.

### Speech & Sound Voice Hub
- Floating bottom-docked clay capsule housing a real-time waveform visualizer styled after gentle ripples in steamed latte foam.
- Microphone toggles feature an animated pulse ring transitioning from pastel matcha (`#98B08D`) when listening, to strawberry pink (`#F78DA7`) during AI synthesis.

### Theme Switcher Carousel
- Segmented pill tray styled in frosted glass containing squishy miniature ceramic-style buttons representing each flavor blend: Strawberry Latte, Roasted Mocha, Vanilla Cream, and Matcha Breeze.

### Input Bar & Text Fields
- Recessed pill trough with an inset shadow (`inset 2px 2px 5px rgba(74, 46, 43, 0.08)`), filled with milky white tone (`#FFFFFF`), featuring strawberry-tinted cursor carats and caramel placeholder text.

### Cards & Drawers
- Elevated panels showcase a frosted glass base framed with 1.5px soft white borders, crowned with squishy clay category headers and badge pills.