# Product.md — Project **AETHER**

> A motion-first, 3D-driven production website where open-source 3D models are sourced, aligned, gradient-shaded, and brought to life with hover, scroll, and cursor-reactive rotation — engineered to a 60 FPS production bar and buildable end-to-end inside Claude Code.

| Field | Value |
|---|---|
| **Codename** | AETHER (rename per brand) |
| **Document** | Product / Technical Requirements (PRD + TDD hybrid) |
| **Version** | 1.0 |
| **Status** | Living draft — refined over multiple review passes |
| **Surface** | Marketing / portfolio / product-showcase website (single-page + sub-routes) |
| **Primary owner** | Frontend / Creative Technology |
| **Build environment** | Claude Code (+ installed skills) |
| **Quality bar** | "Pinnacle" — top ~1% of the web for craft, motion, and performance |

---

## 0. How to read this document

This is both a **product spec** (what we're building and why) and a **technical design doc** (how it gets built). It is opinionated on purpose: a "pinnacle" frontend is the product of hundreds of small, deliberate decisions, so the defaults here are concrete and ready to execute. Every default is overridable — the goal is to remove ambiguity, not creativity.

Sections are layered so they can be read independently:
- **§1–§5** — the *why* and the *feel* (vision, goals, audience, principles).
- **§6** — the **design language** (tokens: color, gradient, type, space, elevation, motion).
- **§7–§8** — the **core differentiator**: the 3D + motion system and the open-source asset pipeline (sourcing → alignment → optimization).
- **§9–§14** — the **build surface** (IA, components, performance, a11y, responsive, stack).
- **§15** — **building it in Claude Code** with skills.
- **§16–§22 + Appendices** — delivery, QA, infra, risks, and reference directories.

---

## 1. Vision & one-liner

**One-liner:** *A living, light-filled canvas where real 3D objects float, rotate, and respond to you — turning a website into a tactile space instead of a flat page.*

**Vision:** Most "3D websites" fall into one of two traps — a heavy, janky tech demo that punishes the visitor's GPU, or a tasteful-but-timid site that uses 3D as wallpaper. AETHER refuses both. It treats motion and three-dimensionality as a *narrative device*: objects appear with intent, react to attention (hover, cursor, scroll), and recede gracefully when the visitor wants to read. The result should feel less like "a website with a 3D widget" and more like *a small, considered world that happens to load in a browser* — and it should do so at 60 FPS on a mid-range laptop and degrade beautifully on a phone.

**The single thing people remember:** *"The objects felt alive — they noticed me."* Cursor-reactive parallax + hover-accelerated rotation + fresnel rim-light is the signature, and it's tuned to feel physical, not gimmicky.

---

## 2. Problem & opportunity

**Problem.** Production websites that want to feel premium reach for stock video, parallax images, or canned Lottie loops. These read as "expensive template." Genuine 3D motion is rare because it's hard to do *well and fast*: sourcing usable models is a slog, models arrive in inconsistent scales/axes/styles, naive WebGL tanks performance, and accessibility/motion-sensitivity is usually an afterthought.

**Opportunity.** A repeatable system that (a) pulls free, license-clean 3D models from open-source repositories, (b) **normalizes and style-aligns** them so they look like they belong together, (c) shades them with a cohesive gradient/fresnel material language, and (d) animates them with a disciplined, reduced-motion-aware interaction model — all within a strict performance budget. Done once, this becomes a reusable engine for portfolios, product launches, agency sites, and client work.

---

## 3. Goals, non-goals & success metrics

### 3.1 Goals (in priority order)
1. **Signature motion** — cursor/scroll/hover-reactive 3D that feels physical and intentional, not decorative.
2. **Cohesion** — sourced models look unified (one art direction, one material language, one palette).
3. **Production performance** — 60 FPS interaction, fast load, no layout shift, graceful mobile + low-power fallbacks.
4. **Repeatable asset pipeline** — sourcing → license-check → normalize → align → optimize → manifest, scripted and auditable.
5. **Accessibility-first motion** — full experience honors `prefers-reduced-motion`, keyboard, and contrast.
6. **Buildable in Claude Code** — the entire thing is constructable and maintainable via Claude Code + skills.

### 3.2 Non-goals (v1)
- Not a CMS or blog engine (content can be MDX/flat files).
- Not multiplayer, real-time collaborative, or account-gated.
- Not WebXR/VR/AR (kept as a future track; see §22).
- Not a physics sandbox — motion is animated/tweened, not a full rigid-body sim (light spring physics only).
- Not an e-commerce checkout (can link out).
- Not "every page is 3D" — 3D is used where it earns attention; reading surfaces stay calm.

### 3.3 Success metrics
| Dimension | Metric | Target |
|---|---|---|
| Performance | Lighthouse Performance (mobile) | ≥ 90 |
| Performance | Interaction FPS (desktop, mid-tier GPU) | 60 (≥ 50 floor) |
| Web Vitals | LCP / INP / CLS | < 1.8s / < 120ms / < 0.05 |
| Engagement | Median scroll depth | ≥ 70% |
| Engagement | Hover/interaction rate on hero object | ≥ 40% of desktop sessions |
| Quality | Reduced-motion path fully usable | 100% of content reachable |
| Craft | Cross-browser parity (Chromium/WebKit/Gecko) | No visual regressions |

---

## 4. Audience & personas

| Persona | Context | What they need | Implication |
|---|---|---|---|
| **The decision-maker** (hiring manager / prospective client) | Desktop, 60–120s, evaluating craft | Instant "this is exceptional" + clear value, fast | Hero must land in < 2.5s; signature motion immediate |
| **The recruiter on mobile** | Phone, distracted, low bandwidth | Legible, fast, no jank; gets the gist | Mobile fallback is *first-class*, not degraded |
| **The fellow engineer** | Opens DevTools, inspects source | Clean DOM, sane network, no console errors, real craft | Code quality is part of the product |
| **The casual explorer** | Curious, will poke at things | Delight, discoverability, reward for interaction | Hover/scroll surprises; nothing breaks when prodded |
| **The accessibility user** | Reduced-motion / keyboard / screen reader | Full content, no motion sickness, focus order | A11y path is designed, not bolted on |

---

## 5. Experience principles

These are the tie-breakers. When two implementations are equally valid, the one that better serves these wins.

1. **Motion has meaning.** Every animation answers "why did that move?" Entrances orient, hovers confirm attention, scroll reveals structure. No motion for motion's sake.
2. **Physical, not floaty.** Easing, inertia, and damping mimic mass. Objects feel like they have weight and momentum (springs over linear tweens for interaction).
3. **The object notices you.** Cursor proximity and hover are the soul of the site — subtle parallax, lean-toward-cursor, rim-light bloom.
4. **Calm where it counts.** Reading surfaces are still and high-contrast. 3D never fights text.
5. **Performance is a feature, not a constraint.** A dropped frame is a design bug. Budget first, build second.
6. **Degrade with dignity.** Low power, reduced motion, no-WebGL, slow network — each has a *designed* fallback that still feels intentional.
7. **No AI slop.** Reject default purple-gradient-on-white, generic system fonts, and predictable hero-left/image-right layouts. Commit to one bold, specific art direction and execute it precisely.
8. **Earned attention.** Heavy moments (3D hero, signature transition) are rationed. Spending the budget everywhere spends it nowhere.

---

## 6. Design language

The design language is **token-driven**: everything below maps to CSS custom properties (and a parallel JS/TS token export consumed by the 3D layer), so the DOM and the WebGL scene share one source of truth.

### 6.1 Art direction (the default vision)

**Direction: "Lumen / cinematic dark studio."** A near-black, softly-graded studio void where objects sit in a pool of volumetric light. Think product photography meets planetarium. This is the default because dark backgrounds make fresnel rim-light, gradients, and bloom sing — and they sidestep the over-used "purple gradient on white" cliché.

> This is a *default*, not a mandate. The token system supports a light "gallery / paper" direction too (warm off-white, ink, single saturated accent). Pick one and commit — never blend two directions timidly.

### 6.2 Color & gradient system

Colors are defined in a perceptual space (OKLCH) for predictable lightness and smoother gradients, with sRGB hex fallbacks.

```css
:root {
  /* Base canvas (dark direction) */
  --bg-void:        oklch(0.16 0.012 265);   /* near-black, faint cool cast */
  --bg-raised:      oklch(0.21 0.016 265);   /* cards / panels */
  --bg-sunken:      oklch(0.12 0.010 265);

  /* Ink */
  --ink-hi:         oklch(0.97 0.01 250);    /* headings */
  --ink:            oklch(0.86 0.012 250);   /* body */
  --ink-mute:       oklch(0.66 0.014 255);   /* captions */

  /* Signature duotone accent — NOT generic purple.
     Default: molten ember -> glacier. Configurable. */
  --accent-warm:    oklch(0.78 0.17 55);     /* ember / amber */
  --accent-cool:    oklch(0.80 0.13 220);    /* glacier / cyan-slate */
  --accent-pop:     oklch(0.86 0.20 145);    /* rare electric pop (chartreuse) */

  /* Functional */
  --line:           oklch(1 0 0 / 0.08);
  --line-strong:    oklch(1 0 0 / 0.16);
  --shadow-rgb:     0 0 0;
}
```

**Gradient vocabulary** (used both in CSS backgrounds and as 3D material inputs):

| Gradient | Form | Use |
|---|---|---|
| **Aurora mesh** | Animated multi-stop radial/conic blobs, slow drift | Hero background atmosphere |
| **Duotone wash** | `--accent-warm` → `--accent-cool` linear | Section dividers, large type fill |
| **Fresnel rim** | View-angle gradient (shader, see §7.5) | The signature 3D look |
| **Vertical fade** | Canvas → transparent | Top/bottom legibility scrims over 3D |
| **Grain veil** | Tiled SVG/PNG noise at 3–6% opacity | Anti-banding + film texture over all gradients |

> **Anti-banding rule:** every large gradient ships with a dithered grain overlay (3–6% opacity). Smooth 8-bit gradients band on dark backgrounds; grain hides it and adds a premium film grade.

```css
/* Aurora mesh background (illustrative) */
.aurora {
  background:
    radial-gradient(60% 50% at 20% 25%, oklch(0.78 0.17 55 / 0.22), transparent 70%),
    radial-gradient(50% 45% at 80% 30%, oklch(0.80 0.13 220 / 0.20), transparent 70%),
    radial-gradient(70% 60% at 50% 90%, oklch(0.86 0.20 145 / 0.10), transparent 75%),
    var(--bg-void);
  background-blend-mode: screen, screen, screen, normal;
}
.grain::after {
  content: ""; position: absolute; inset: 0; pointer-events: none;
  background: url("/textures/grain.png"); opacity: 0.05; mix-blend-mode: overlay;
}
```

### 6.3 Typography

Per the anti-slop rule: **no Inter, Roboto, Arial, or system stack as the brand face, and no defaulting to Space Grotesk.** Pair a characterful display face with a clean, low-contrast body face.

| Role | Suggested direction | Notes |
|---|---|---|
| **Display** | A distinctive, high-personality serif or grotesk-with-quirks (e.g., an expressive variable serif, a wide neo-grotesk, or a refined editorial face) | Big, set tight (`-0.02em`), used sparingly and large |
| **Body** | A humanist sans or mono with good rhythm at 16–18px | Optimize for reading; `text-wrap: balance` on headings, `pretty` on body |
| **Mono / detail** | A characterful monospace | Labels, timestamps, technical captions, "engineer-facing" details |

**Type scale** (modular, ratio ≈ 1.25, fluid via `clamp`):

```css
:root {
  --step--1: clamp(0.83rem, 0.8rem + 0.15vw, 0.9rem);
  --step-0:  clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --step-1:  clamp(1.25rem, 1.1rem + 0.7vw, 1.5rem);
  --step-2:  clamp(1.6rem, 1.3rem + 1.4vw, 2.2rem);
  --step-3:  clamp(2.1rem, 1.5rem + 2.8vw, 3.4rem);
  --step-4:  clamp(2.8rem, 1.7rem + 5vw, 5.5rem);
  --step-5:  clamp(3.6rem, 1.6rem + 9vw, 9rem);     /* hero display */
}
```

> Load fonts with `font-display: swap`, subset to used glyphs, and `preload` the display face to avoid a FOUT during the hero reveal.

### 6.4 Spacing, grid & radius

```css
:root {
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem;
  --space-4: 1rem;    --space-6: 1.5rem; --space-8: 2rem;
  --space-12: 3rem;   --space-16: 4rem;  --space-24: 6rem;  --space-32: 8rem;
  --radius-sm: 8px; --radius: 14px; --radius-lg: 24px; --radius-pill: 999px;
  --content-max: 1200px; --measure: 68ch; /* line length for reading */
}
```

- **12-column fluid grid**, generous gutters, with deliberate **grid-breaking** elements (3D objects and oversized type bleed past columns and edges for tension — per the "unexpected layouts" principle).
- Vertical rhythm in multiples of `--space-8`.

### 6.5 Elevation, glass & shadow

Dark UI needs *soft, large, low-opacity* shadows plus subtle inner light, not hard drop shadows.

```css
:root {
  --shadow-sm:  0 1px 2px rgb(var(--shadow-rgb)/.4);
  --shadow-md:  0 8px 24px rgb(var(--shadow-rgb)/.45);
  --shadow-lg:  0 30px 80px rgb(var(--shadow-rgb)/.5);
  --glass:      blur(18px) saturate(140%);
}
.panel {
  background: linear-gradient(180deg, oklch(1 0 0 /0.06), oklch(1 0 0 /0.02));
  border: 1px solid var(--line);
  backdrop-filter: var(--glass);
  box-shadow: var(--shadow-md), inset 0 1px 0 oklch(1 0 0 /0.06);
}
```

### 6.6 Motion tokens

A small, shared set of durations and eases keeps motion coherent. The 3D layer reads the same numbers (as ms/spring configs) so DOM and WebGL feel like one system.

```css
:root {
  /* Durations */
  --dur-micro: 120ms; --dur-short: 240ms; --dur-mid: 480ms; --dur-long: 900ms;
  /* Eases */
  --ease-out-expo:    cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out-quint:cubic-bezier(0.83, 0, 0.17, 1);
  --ease-out-back:    cubic-bezier(0.34, 1.56, 0.64, 1); /* gentle overshoot */
}
```

**Spring defaults (interaction / 3D):** `stiffness 120, damping 18, mass 1` for cursor-follow; snappier `stiffness 260, damping 26` for hover state changes. Springs (not fixed-duration tweens) drive anything that tracks the pointer, so motion stays continuous and physical.

### 6.7 Custom cursor & micro-details

- **Custom cursor**: a small ring that scales/labels on interactive 3D ("drag / view") and snaps to magnetic buttons. Always falls back to native cursor on touch and for reduced-motion.
- **Magnetic buttons**: primary CTAs subtly attract the cursor within a radius (capped offset, spring return).
- **Focus rings**: visible, on-brand (not removed), using `:focus-visible`.
- **Selection color**: themed `::selection`.

---

## 7. The 3D & motion system (core differentiator)

This is the section that makes AETHER "AETHER." Everything here serves one feeling: *objects that have weight and notice you.*

### 7.1 Rendering stack

| Layer | Choice | Why |
|---|---|---|
| **Renderer (baseline)** | **Three.js (WebGL2)** | Universal support, mature, predictable. The production baseline. |
| **Renderer (progressive)** | **WebGPU / TSL** as opt-in enhancement | Better perf headroom where supported; **never** the required path. Feature-detect and fall back to WebGL2. |
| **Declarative layer** | **React Three Fiber (R3F)** | Component model for scenes; reconciler-driven, ergonomic. (Plain Three.js is acceptable for a no-framework build.) |
| **Helpers** | **@react-three/drei** | `useGLTF`, `Environment`, `Float`, `PresentationControls`, `MeshTransmissionMaterial`, `AdaptiveDpr`, `Preload`, `BakeShadows`. |
| **Post-processing** | **@react-three/postprocessing** (postprocessing lib) | Selective **Bloom**, subtle **Depth of Field**, **Chromatic Aberration**, **Vignette**, **Noise**. Use sparingly. |
| **DOM/timeline motion** | **GSAP** (+ ScrollTrigger) and/or **Motion** (Framer Motion) | Orchestrated reveals, scroll scenes, scrubbed timelines. |
| **Smooth scroll** | **Lenis** | Buttery, controllable scroll that ScrollTrigger and the 3D scroll-rig read from. |
| **Asset tooling** | **gltf-transform**, **gltfjsx** (R3F), **Draco/Meshopt**, **KTX2/Basis** | Pipeline (see §8). |

> **Decision rule:** ship the WebGL2 path first and tune it to budget. Treat WebGPU as a measured upgrade behind a capability flag, not a launch dependency.

### 7.2 Scene architecture

- **One persistent `<Canvas>`** that survives route changes (avoids re-init cost and context loss). Scenes/objects mount and unmount within it.
- **DOM ↔ 3D sync layer**: a small store (Zustand) holds shared state — pointer (normalized -1..1, smoothed), scroll progress (0..1 from Lenis), active section, reduced-motion flag, device tier. Both DOM and 3D subscribe.
- **HTML/3D co-location**: use drei `Html` or a measured "tracked element" approach so 3D objects can visually anchor to DOM layout (e.g., an object sitting beside a paragraph) without coupling the two render trees.
- **Render-on-demand** for static moments: use `frameloop="demand"` and `invalidate()` when nothing is animating to save battery; switch to continuous only during interaction/idle-rotation that is on-screen.

### 7.3 Camera & controls

- **Camera**: perspective, ~35–45° FOV for a product-photography feel; slight positive Z, gentle dolly on scroll.
- **No free OrbitControls in hero** (it lets users break the composition). Instead use **`PresentationControls`** (constrained, spring-damped, snaps back) so visitors can "nudge" objects within tasteful limits.
- **Cursor parallax camera**: the camera (or a parent group) lerps a tiny amount toward the pointer for depth — capped at a few degrees so it reads as life, not seasickness.

### 7.4 Lighting & environment

- **Image-Based Lighting** via a **CC0 HDRI** (Poly Haven / ambientCG) loaded as an `Environment` for realistic reflections — but **hidden as background** (we keep our graded void). HDRIs are tone-matched to the palette.
- **Key + rim setup**: one soft key light, one cool rim to carve silhouettes (reinforces the fresnel look), low-intensity fill from environment.
- **Contact shadows** (drei `ContactShadows` or baked) so objects feel grounded, not floating in null space.
- **Bake where possible**: `BakeShadows`, baked AO in textures — runtime shadow maps are expensive; bake the static ones.

### 7.5 Materials & shading — the gradient/fresnel signature

The unifying look across *all* sourced models is a **fresnel rim-gradient** layered over their PBR base. Fresnel = stronger color at glancing angles, which traces every silhouette with the brand duotone and ties mismatched models into one family.

**Fresnel gradient shader (GLSL, illustrative):**

```glsl
/* vertex */
varying vec3 vNormalW;
varying vec3 vViewDir;
void main() {
  vec4 worldPos = modelMatrix * vec4(position, 1.0);
  vNormalW = normalize(mat3(modelMatrix) * normal);
  vViewDir = normalize(cameraPosition - worldPos.xyz);
  gl_Position = projectionMatrix * viewMatrix * worldPos;
}
```
```glsl
/* fragment */
uniform vec3  uColorA;     // --accent-cool (core)
uniform vec3  uColorB;     // --accent-warm (rim)
uniform float uPower;      // fresnel falloff, ~2.5–4.0
uniform float uIntensity;  // rim strength, ~0.6–1.0
varying vec3  vNormalW;
varying vec3  vViewDir;
void main() {
  float f = pow(1.0 - clamp(dot(normalize(vNormalW), normalize(vViewDir)), 0.0, 1.0), uPower);
  vec3 col = mix(uColorA, uColorB, f * uIntensity);
  gl_FragColor = vec4(col, 1.0);
}
```

In practice this is applied as a **rim pass blended over** the model's real material (so textures/PBR detail survive) — via a custom `onBeforeCompile` patch on `MeshStandardMaterial`, a `MeshDistortMaterial`/custom shader for hero pieces, or TSL nodes on the WebGPU path. Drei's `MeshTransmissionMaterial` is reserved for glass/crystal hero objects.

**Material consistency policy** (enforced in the pipeline, §8.4): all approved models render with metallic-roughness PBR; spec-gloss is converted; emissive-heavy or stylized-unlit assets are either re-materialed to the house look or rejected. The point is *one coherent shading language*, not 12 different art styles in one scene.

### 7.6 Animation taxonomy

Every motion belongs to exactly one of these, each with a token-defined personality:

| Type | Trigger | Behavior | Notes |
|---|---|---|---|
| **Idle / turntable** | On-screen & not interacted | Slow constant Y-rotation (~6–12°/s) + faint float bob | Pauses off-screen (IntersectionObserver) and under reduced-motion |
| **Cursor parallax** | Pointer move (desktop) | Object/camera lean toward pointer, spring-damped, capped | The "it notices me" core |
| **Hover** | Pointer over object | Rotation speeds up, scale +4–8%, rim-light brightens (bloom), optional label | Confirms attention; reverts on out |
| **Scroll-linked** | Scroll progress | Object rotates/translates/morphs along a scrubbed timeline | Reveals structure; driven by Lenis→ScrollTrigger |
| **Entrance** | Enters viewport | Fade + scale-from-0.9 + slight rotate-in, staggered | One-shot; respects reduced-motion (fade-only) |
| **Transition** | Route / section change | Camera move or object hand-off between sections | Rationed — the "signature" moment |
| **State pulse** | Click / success | Brief spring overshoot, emissive flash | Micro-feedback only |

**Orchestration:** the page-load reveal is *one* well-staged sequence (staggered `animation-delay` / GSAP timeline) — per the principle that one orchestrated entrance beats scattered micro-animations.

### 7.7 Hover interaction — detailed spec

The hover behavior is the product's handshake. Spec it precisely:

- **Hit target**: raycast against a simplified proxy mesh (not the full hi-poly) for cheap, reliable picking.
- **On enter** (`onPointerOver`): set hovered=true; spring rotation speed `0.25 → 1.3`; spring scale `1.0 → 1.06`; raise fresnel `uIntensity` and bloom threshold so the rim blooms; fade in a mono label ("drag to view"); switch custom cursor to "view" state. Pause idle bob so motion reads as focused.
- **While hovered**: object leans a little *more* toward the pointer than the ambient parallax (it's "leaning in").
- **On leave** (`onPointerOut`): spring everything back; resume idle; cursor reverts. No abrupt snaps — all transitions are spring-damped over `--dur-short`.
- **Touch**: no hover; tap toggles a "focused" state (scale + label), and `PresentationControls` allows drag-rotate. Never strand interactivity behind hover on touch devices.
- **Latency**: hover feedback must begin within one frame; never wait on network or texture decode.

**R3F reference component:**

```jsx
import { useRef, useState } from 'react'
import { useFrame } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'
import { MathUtils } from 'three'

export function HoverObject({ url, reducedMotion }) {
  const ref = useRef()
  const [hovered, setHovered] = useState(false)
  const { scene } = useGLTF(url)               // Draco/KTX2-decoded GLB

  useFrame((state, dt) => {
    const g = ref.current
    if (!g) return

    // Idle turntable + hover acceleration (skip spin under reduced motion)
    const spin = reducedMotion ? 0 : (hovered ? 1.3 : 0.22)
    g.rotation.y += dt * spin

    // Cursor lean (spring-ish lerp), capped; disabled under reduced motion
    const k = reducedMotion ? 0 : 1
    const tx =  state.pointer.y * 0.22 * k + (hovered ? 0.06 : 0) * k
    const tz = -state.pointer.x * 0.16 * k
    g.rotation.x = MathUtils.lerp(g.rotation.x, tx, 0.08)
    g.rotation.z = MathUtils.lerp(g.rotation.z, tz, 0.08)

    // Hover scale
    const s = hovered ? 1.06 : 1.0
    const ns = MathUtils.lerp(g.scale.x, s, 0.12)
    g.scale.setScalar(ns)
  })

  return (
    <primitive
      ref={ref}
      object={scene}
      onPointerOver={(e) => { e.stopPropagation(); setHovered(true) }}
      onPointerOut={() => setHovered(false)}
    />
  )
}
useGLTF.preload && null
```

### 7.8 Rotation system

Rotation is layered, and the layers **compose** rather than fight:

1. **Base turntable** — constant slow Y-spin (idle), time-based (`dt`), so it's frame-rate independent.
2. **Cursor offset** — additive lean from pointer (spring/lerp), capped to ±~12°.
3. **Scroll drive** — a scroll-progress term can add controlled rotation through a section (e.g., a 90° reveal as the object scrolls into focus).
4. **User nudge** — `PresentationControls` lets the visitor push within limits; releases spring back to the composed baseline.
5. **Snap targets** (optional) — key "beauty angles" the object eases toward when idle, so it always rests photogenically.

All rotation is **quaternion-safe** (avoid gimbal issues on compound rotations), time-normalized, and clamped. Under reduced motion, rotation collapses to *optional, user-initiated drag only* (no autonomous spin).

---

## 8. 3D asset pipeline — sourcing, alignment, optimization

This is the second pillar: turning the messy reality of free 3D models into a clean, unified, license-clean, performance-budgeted asset set. The pipeline is **scripted and auditable** — every model that ships passes through it and lands in a manifest.

### 8.1 Sourcing from open-source repositories

Pull only from sources with clear, commercial-safe licenses. **Default to CC0** (no attribution burden); allow **CC-BY** with an attribution ledger. **Reject** NC (non-commercial) and ND (no-derivatives) for a production/commercial site, and reject anything with unclear provenance. (Full directory in **Appendix A**.)

Preferred-format priority: **glTF 2.0 / GLB** > FBX/OBJ (convert) > everything else. glTF is the web-native, PBR-correct, Y-up standard and minimizes conversion loss.

### 8.2 License compliance & attribution ledger

- Every asset records: source URL, author, license (SPDX-style id), attribution-required flag, and date pulled.
- CC-BY assets surface attribution in a `/credits` page and, where the license requires, near the asset.
- A CI check fails the build if any manifest entry has license `unknown` or a disallowed license.
- Keep the original downloaded file (immutable `raw/`) alongside the processed output for provenance.

### 8.3 Ingestion & normalization

Raw models arrive with inconsistent **scale, up-axis, pivot, and materials**. Normalize every asset to a canonical contract:

**Canonical contract**
- **Up-axis:** Y-up (rotate Z-up Blender/OBJ exports by -90° X).
- **Units:** meters; uniformly scale so the model fits a canonical bound (e.g., max dimension = 1.0 unit, or a per-role target).
- **Pivot/origin:** centered on geometry centroid (or footprint center for "standing" objects); origin at (0,0,0).
- **Forward:** -Z forward (document per asset if ambiguous).
- **Materials:** metallic-roughness PBR; convert spec-gloss; strip embedded cameras/lights; ensure correct normals (recompute/flip inverted faces).
- **Textures:** sRGB for base color/emissive, linear for normal/roughness/metalness; power-of-two; ≤ 2K (hero ≤ 4K).

**Normalization + optimization (gltf-transform, illustrative):**

```js
import { NodeIO } from '@gltf-transform/core'
import {
  dedup, prune, weld, quantize, draco, textureCompress, flatten, join
} from '@gltf-transform/functions'
import { Box3, Vector3 } from 'three' // or compute bounds via core API

const io = new NodeIO() /* .registerExtensions(...).registerDependencies(...) */
const doc = await io.read('raw/model.glb')

// 1. Clean graph
await doc.transform(
  dedup(),           // merge duplicate accessors/textures/materials
  prune(),           // drop unused nodes/meshes/materials
  flatten(),         // flatten node hierarchy
  weld(),            // weld vertices, index geometry
)

// 2. (custom) center pivot + scale to canonical bound
//    compute bounding box, translate by -center, scale by 1/maxDim
//    — apply as a transform on the root node, then bake.

// 3. Compress geometry + textures
await doc.transform(
  quantize(),                                   // pack vertex attributes
  draco(),                                      // or meshopt() — geometry compression
  textureCompress({ targetFormat: 'webp' }),    // + KTX2/Basis for GPU textures
  join(),                                        // merge compatible meshes -> fewer draw calls
)

await io.write('dist/model.draco.glb', doc)
```

> For R3F, also generate a typed component with **`gltfjsx`** so the scene graph is explicit, tree-shakeable, and easy to attach the fresnel material and hover logic to.

### 8.4 Alignment & QA — "do they align?"

"Alignment" has **two** meanings here, and both are gated before an asset is approved.

**(A) Technical alignment** — a hard checklist (automatable):
- [ ] Y-up, -Z forward, origin centered, fits canonical bound (±2%)
- [ ] Triangle count within per-role budget (see §11)
- [ ] Draw calls ≤ target after `join()`
- [ ] Metallic-roughness PBR; valid normals; no inverted faces
- [ ] Textures within size/format policy; no orphan textures
- [ ] No embedded lights/cameras; no NaN/degenerate geometry
- [ ] Compressed (Draco/Meshopt + KTX2) and decodes correctly

**(B) Stylistic alignment** — does it belong to the family?
- **Poly-density band:** all hero objects share a fidelity tier; don't mix photoscan realism with flat low-poly in the same scene.
- **Palette match:** sample dominant albedo colors and compare to the brand palette in a perceptual space (CIELAB ΔE); flag assets beyond a threshold (e.g., ΔE > 20) for re-texture or rejection. Output a **palette-match score** (0–1) into the manifest.
- **Material feel:** matte/metal/glass mix is intentional and limited; the fresnel rim pass unifies the rest.
- **Silhouette readability** at the size it'll appear (a busy model that's a blob at 240px fails).

**Automated turntable QA (the literal "see if they align"):**
1. For each candidate, render a **turntable contact sheet** — 8–16 frames at canonical angles under the house lighting (headless: Three.js + headless-gl/`gl`, Puppeteer screenshot of a hidden canvas, or a Blender CLI render).
2. Lay candidates side-by-side in a generated **alignment board** (HTML grid) so a human reviews cohesion at a glance.
3. Compute and overlay automated scores: palette ΔE, tri-count, bounding-box delta, draw calls.
4. **Approve / reject** in the manifest with reviewer + notes. Rejected assets stay in `raw/` for reference but never ship.

This turns "do these models look like they go together?" from a vibe into a reviewable artifact with both an automated first pass and a human final call.

### 8.5 Optimization & runtime loading

- **Geometry:** Draco or Meshopt (Meshopt decodes faster; Draco compresses smaller — pick per asset/CDN).
- **Textures:** **KTX2/Basis Universal** (GPU-native, stays compressed in VRAM) for anything non-trivial; WebP/AVIF for poster images.
- **LOD:** drei `<Detailed>` or manual LOD for hero objects (swap by distance/size).
- **Instancing:** `InstancedMesh` for any repeated geometry (particles, repeated decor).
- **Loading strategy:** `<Suspense>` + progressive reveal; **preload** only the hero model; lazy-load below-the-fold scenes on intersection; show a tasteful poster (rendered WebP of the model) until the GLB is ready (zero layout shift).
- **Decode off main thread:** Draco/KTX2 workers; cap device pixel ratio with drei `AdaptiveDpr` and `PerformanceMonitor` to auto-dial quality on weak GPUs.

### 8.6 Asset manifest (single source of truth)

Every shipped asset has a manifest entry; the app reads manifests, never hard-codes paths.

```jsonc
{
  "id": "artifact-001",
  "name": "Brass Astrolabe",
  "role": "hero",                       // hero | feature | decor | instanced
  "source": {
    "provider": "Poly Pizza",
    "url": "https://poly.pizza/m/EXAMPLE",
    "author": "Creator Name",
    "license": "CC-BY-4.0",
    "attributionRequired": true,
    "pulledOn": "2026-06-01"
  },
  "files": {
    "raw": "raw/astrolabe.glb",
    "optimized": "dist/astrolabe.meshopt.glb",
    "poster": "dist/astrolabe.webp"
  },
  "geometry": { "triangles": 18540, "drawCalls": 3,
                "bbox": { "min": [-0.5,-0.5,-0.5], "max": [0.5,0.5,0.5] } },
  "normalization": { "upAxis": "Y", "forward": "-Z", "unit": "meter",
                     "centeredPivot": true, "canonicalMaxDim": 1.0 },
  "style": { "shading": "PBR-metalRough", "fidelityTier": "mid",
             "paletteMatchDeltaE": 11.4, "paletteMatchScore": 0.93 },
  "qa": { "technicalPass": true, "stylisticPass": true,
          "reviewer": "Hadi", "approved": true, "notes": "Rim pass applied." },
  "performance": { "gpuMemoryMB": 6.4, "lodLevels": 3, "decode": "meshopt+ktx2" }
}
```

---

## 9. Information architecture & pages

Single persistent canvas, scroll-driven narrative, with a few sub-routes. 3D appears where it earns attention; reading sections stay calm.

| Route / section | Purpose | 3D role | Motion |
|---|---|---|---|
| **Hero** | The 5-second wow | Signature object, fresnel-lit, cursor-reactive | Orchestrated entrance, idle turntable, hover |
| **Manifesto / intro** | One bold statement | Minimal (object recedes, blurred behind scrim) | Scroll-fade, type reveal |
| **Showcase / work** | The substance (projects, products, cases) | Per-item objects that align to scroll position | Scroll-linked rotation, hover detail |
| **Process / how** | Build credibility | Diagrammatic light 3D or none | Staggered reveals |
| **Capabilities** | Skills/services grid | Decorative instanced 3D motifs | Hover micro-interactions |
| **CTA / contact** | Convert | Calm; magnetic button focus | Subtle |
| **/credits** | License attributions (CC-BY) | none | none |
| **/lab (optional)** | Experiments / 404 easter egg | Playground object | Free `PresentationControls` |

**Navigation:** minimal, sticky, transparent over hero then frosted on scroll; keyboard-reachable; a clearly labeled skip-link to main content.

---

## 10. Component & interaction library

Build a small, composable kit. Each component is responsive, themeable via tokens, keyboard-accessible, and reduced-motion aware.

**Primitives**
- `Canvas3D` (persistent stage), `Scene`, `HoverObject`, `ScrollObject`, `InstancedField`
- `MagneticButton`, `CursorRing`, `RevealText` (split-by-line/word stagger), `Marquee`
- `Panel` (glass), `Tag/Chip`, `Divider` (duotone), `Scrim`
- `LazyScene` (intersection-mounted 3D), `Poster` (placeholder before GLB), `LoaderBar`

**Patterns**
- **Sticky scroll scenes** (pin a section, scrub 3D + text through it).
- **Horizontal scroll gallery** (driven by vertical scroll via ScrollTrigger).
- **Reveal-on-enter** with `IntersectionObserver` + staggered children.
- **Magnetic CTA** + **custom cursor** states.
- **Theme toggle** (dark default ↔ optional light direction), persisted, no flash (set before paint).

**Component contract (every component):** documented props, sensible defaults, `prefers-reduced-motion` branch, focus states, no console warnings, and a Storybook/Ladle story (or a `/lab` demo) for visual QA.

---

## 11. Performance budget & strategy

Performance is a feature. The budget is a contract; CI enforces the hard caps.

### 11.1 Budget table

| Metric | Target | Hard cap |
|---|---|---|
| LCP (mobile, 4G) | < 1.8s | 2.5s |
| INP | < 120ms | 200ms |
| CLS | < 0.05 | 0.1 |
| TTI | < 3.0s | 4.0s |
| Interaction FPS (desktop mid-GPU) | 60 | ≥ 50 |
| Interaction FPS (mobile mid-tier) | 60 | ≥ 30 |
| Triangles / hero scene | ≤ 150k | 300k |
| Draw calls / scene | ≤ 80 | 150 |
| GPU memory | ≤ 256 MB | 512 MB |
| Initial JS (gzip, route) | ≤ 180 KB | 250 KB |
| Largest single model (compressed) | ≤ 1.5 MB | 3 MB |
| Total hero payload (incl. model+HDRI) | ≤ 3.5 MB | 6 MB |
| Time to first interactive model | < 2.5s | 4s |

### 11.2 Strategy
- **Device tiering:** detect GPU/CPU class (heuristics + `PerformanceMonitor`); set a quality tier (dpr cap, post-fx on/off, particle counts, shadow quality). Auto-downgrade on sustained frame drops.
- **Render-on-demand** when idle/off-screen; pause animation loops outside the viewport.
- **Code-split** per route; lazy-load 3D scenes and heavy libs (GSAP plugins) on demand.
- **Asset budget enforced in pipeline** (§8) — nothing ships over caps without explicit waiver.
- **Texture/geometry compression** mandatory (KTX2 + Draco/Meshopt).
- **Avoid layout thrash:** transforms/opacity only for animation; never animate layout-affecting properties; `content-visibility: auto` for long sections.
- **Fonts:** preload display face, `swap`, subset.
- **Measure in CI:** Lighthouse CI + a WebGL FPS smoke test on a throttled profile; fail PRs that regress budget.

---

## 12. Accessibility & inclusive motion

A11y is designed in, not retrofitted. The reduced-motion path is a **first-class experience**, not a broken one.

- **`prefers-reduced-motion: reduce`** → disable autonomous spin/parallax/scroll-scrub; keep content reachable; replace motion reveals with simple fades or instant show; 3D becomes a static, well-composed render (poster or single frame) with optional user-initiated drag only.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: .01ms !important;
    scroll-behavior: auto !important;
  }
}
```
```js
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
// gate idle spin, cursor parallax, scroll-scrub, and Lenis on !reduce
```

- **Keyboard:** full tab order, visible `:focus-visible` rings, skip-link, no keyboard traps; interactive 3D objects have a focusable DOM proxy with a label and key handlers (or a clearly labeled non-3D alternative).
- **Screen readers:** the canvas is `aria-hidden`; all *meaning* lives in real, semantic DOM (headings, alt text, landmarks). 3D is decorative/enhancing, never the sole carrier of information.
- **Contrast:** text meets WCAG AA (≥ 4.5:1 body) — verified *over* gradients/3D using scrims; don't let moving backgrounds drop contrast below threshold.
- **No motion traps:** nothing auto-plays faster than comfortable; no flashing > 3Hz (seizure safety).
- **Respect `prefers-reduced-transparency` / `prefers-contrast`** where supported (reduce glass blur, raise contrast).
- **Touch targets** ≥ 44px; hover-only affordances always have a tap/focus equivalent.

---

## 13. Responsive & adaptive strategy

Mobile is a **first-class** experience, not a stripped-down apology.

| Tier | Behavior |
|---|---|
| **Desktop (pointer, ≥ mid GPU)** | Full experience: cursor parallax, hover, post-fx, idle spin, scroll scenes |
| **Tablet / touch** | No hover/cursor parallax; tap-to-focus + drag-rotate; reduced post-fx; lighter scenes |
| **Mobile** | Simplified 3D (lower poly LOD, dpr cap, no/low post-fx) or high-quality **poster + light spin**; layout reflows to single column; type scale via `clamp`; touch-first nav |
| **Low-power / Save-Data** | Honor `Save-Data` + battery hints: serve posters instead of live 3D, kill ambient motion |
| **No WebGL2** | Graceful fallback: rendered hero stills (WebP/AVIF) with CSS parallax + gradients; site fully functional |

- **Breakpoints** are content-driven, not device-named; prefer fluid `clamp()` over hard breakpoints, with a few structural breakpoints for layout shifts.
- **Container queries** for components that appear in varied widths.
- **Test matrix:** real iOS Safari + Android Chrome, not just emulators (WebKit GPU quirks are real).

---

## 14. Tech stack & tooling

| Concern | Choice | Notes |
|---|---|---|
| **Framework** | React + Vite (or Next.js for SSR/SEO routes) | R3F lives in React; Astro is an option for content-heavy, islands-style builds |
| **3D** | Three.js (WebGL2) + R3F + drei + postprocessing | WebGPU/TSL as progressive enhancement |
| **Motion** | GSAP (+ ScrollTrigger) and/or Motion; Lenis smooth scroll | |
| **State** | Zustand | Shared pointer/scroll/tier store for DOM↔3D |
| **Styling** | CSS variables + (Tailwind *or* vanilla-extract / CSS Modules) | Tokens are the source of truth; avoid generic utility-only look |
| **Asset pipeline** | gltf-transform, gltfjsx, Draco/Meshopt, KTX2/Basis | Scripted, in CI |
| **Content** | MDX / flat files | No CMS in v1 |
| **Lang** | TypeScript (strict) | Types for tokens, manifest, store |
| **Lint/format** | ESLint + Prettier; Stylelint | |
| **Testing** | Vitest (unit), Playwright (e2e + visual), Lighthouse CI, axe (a11y) | Visual regression on key scenes |
| **Hosting** | Static/edge (Vercel / Netlify / Cloudflare Pages) + CDN | Immutable hashed assets, long cache |
| **Analytics** | Privacy-friendly, lightweight (e.g., Plausible-style) | No heavy 3rd-party bloat |

---

## 15. Building it in Claude Code (skills workflow)

This product is designed to be built and maintained inside **Claude Code**, leaning on installed **skills** so the agent produces production-grade output instead of generic scaffolding.

### 15.1 Skills to lean on
- **`frontend-design`** — the core skill for every component, page, and styling pass. It enforces distinctive, non-"AI-slop" aesthetics (no Inter/Roboto default, no purple-on-white cliché, no Space Grotesk convergence; commit to one bold direction). Invoke it whenever building/refining UI.
- **Document skills** (`docx`/`pptx`/`pdf`/`xlsx`) — for spinning the spec or a case study into a deliverable (e.g., a client-facing PDF or pitch deck of the site).
- **`skill-creator`** — to package the **asset pipeline** (§8) itself as a reusable custom skill (e.g., an `aether-asset-pipeline` skill: ingest → normalize → align-QA → optimize → manifest), so future projects get it for free.

### 15.2 Project memory & config
- Add a **`CLAUDE.md`** at repo root capturing: the art direction, tokens, performance budget, asset contract, and "definition of done." This keeps every Claude Code session on-spec.
- Keep this `Product.md` in the repo as the canonical brief; reference it from `CLAUDE.md`.
- Define conventions: file structure, naming, commit style, and "never animate layout properties / always honor reduced motion" guardrails.

### 15.3 Suggested build loop (with Claude Code)
1. **Scaffold** — Vite/Next + TS + R3F + drei + GSAP/Lenis + Zustand; lint/format; CI skeleton.
2. **Tokens first** — implement §6 as CSS variables + a typed TS token export consumed by the 3D layer. (frontend-design skill.)
3. **Persistent canvas + store** — `Canvas3D`, Zustand store (pointer/scroll/tier/reduced-motion), Lenis wired to scroll progress.
4. **Asset pipeline** — script §8 (gltf-transform + gltfjsx + Draco/KTX2), generate the alignment board, populate the manifest. (Package as a skill via skill-creator.)
5. **Signature object** — hero `HoverObject` with fresnel material, idle spin, cursor parallax, hover spec (§7.6–7.8). Tune until it *feels* physical.
6. **Pages & scroll scenes** — build IA (§9) with sticky/scroll-linked scenes; reading sections calm and high-contrast.
7. **Components** — the kit (§10), each with reduced-motion + a11y branches and a demo story.
8. **Performance pass** — device tiering, LOD, render-on-demand, code-split; wire Lighthouse CI + FPS smoke test to the budget (§11).
9. **A11y pass** — reduced-motion path, keyboard, contrast over gradients, axe in CI (§12).
10. **Polish** — custom cursor, magnetic CTAs, grain veils, entrance choreography, micro-feedback. Ration the heavy moments.
11. **Ship** — edge deploy, immutable assets, analytics, SEO, `/credits` for CC-BY.

### 15.4 Working style with the agent
- **Iterate visually:** have Claude Code screenshot key scenes and self-review against this spec each pass (the "recheck, add what's missing, recheck again" loop is the operating mode, not a one-off).
- **Parallelize** independent tracks (asset QA vs. component build) where the workflow allows.
- **Keep changes reviewable:** small commits, one concern each; never let a "polish" pass silently regress the performance budget.

---

## 16. Project phases & milestones

| Phase | Outcome | Exit criteria |
|---|---|---|
| **P0 — Foundations** | Repo, tokens, canvas, store, CI skeleton, `CLAUDE.md` | Tokens live; blank canvas renders; CI green |
| **P1 — Asset pipeline** | Scripted ingest→align→optimize→manifest + alignment board | ≥ 5 models pass technical+stylistic QA, in manifest |
| **P2 — Signature** | Hero object: fresnel + idle + cursor + hover | Feels physical; hits FPS; reduced-motion path works |
| **P3 — Structure** | All sections/IA, scroll scenes, reading surfaces | Content reachable; CLS < 0.05; nav a11y-complete |
| **P4 — Performance** | Tiering, LOD, code-split, budgets in CI | All §11 caps met on throttled profile |
| **P5 — A11y & responsive** | Reduced-motion, keyboard, mobile/touch first-class | axe clean; real-device pass; no-WebGL fallback works |
| **P6 — Polish & launch** | Cursor, magnetics, grain, choreography, SEO, credits | Lighthouse ≥ 90 mobile; cross-browser parity; ship |

---

## 17. Definition of done / acceptance criteria

A feature/page is "done" only when **all** hold:
- [ ] Meets the relevant performance budget (§11); no CI budget regression.
- [ ] Fully usable under `prefers-reduced-motion: reduce`.
- [ ] Keyboard-navigable with visible focus; passes axe; AA contrast (over any gradient/3D).
- [ ] No console errors/warnings; no WebGL context leaks across routes.
- [ ] Cross-browser parity (latest Chromium, WebKit/Safari, Gecko/Firefox).
- [ ] Real-device check on iOS Safari + Android Chrome.
- [ ] All 3D assets are license-clean and in the manifest; CC-BY credited.
- [ ] Graceful no-WebGL2 fallback present.
- [ ] Matches the committed art direction (no AI-slop defaults).
- [ ] Visual-regression snapshot reviewed for key scenes.

---

## 18. Testing & QA strategy

- **Unit (Vitest):** token math, store logic, manifest schema validation, normalization helpers.
- **E2E (Playwright):** nav, route transitions, hover/tap states, reduced-motion path, no-WebGL fallback.
- **Visual regression:** snapshot hero + key scenes at canonical angles/breakpoints; flag diffs.
- **Performance (Lighthouse CI + FPS smoke test):** throttled mobile profile; fail PRs over budget.
- **Accessibility (axe + manual):** automated scan + manual keyboard/screen-reader walkthrough.
- **Asset QA (pipeline, §8.4):** technical checklist + stylistic palette/alignment scoring + human approval, recorded in manifest.
- **Cross-browser/device matrix:** Chromium/WebKit/Gecko + real iOS/Android.

---

## 19. Deployment & infrastructure

- **Static/edge** hosting (Vercel/Netlify/Cloudflare Pages); SSR/SSG only where SEO routes need it.
- **CDN** for hashed, immutable assets (GLB/KTX2/fonts) with long-lived cache; HTML short cache.
- **Compression:** Brotli for text; assets pre-compressed.
- **CI/CD:** PR → lint/test/budget/axe → preview deploy → main → production. Budgets and a11y gates are blocking.
- **Headers:** sensible CSP, COOP/COEP if SharedArrayBuffer/threaded decoders are used, security headers.
- **Monitoring:** uptime + Web Vitals RUM (privacy-friendly), error logging.

---

## 20. Analytics, SEO & telemetry

- **Analytics:** lightweight, privacy-respecting; track scroll depth, hero interaction rate, route transitions — **without** harming performance budget.
- **SEO:** real semantic DOM (3D is decorative), per-route titles/meta, Open Graph/Twitter cards using **rendered 3D posters** as share images, JSON-LD where relevant, sitemap/robots, fast LCP.
- **Telemetry (perf):** sample real-user FPS/Web Vitals to validate the budget in the wild; auto-flag device tiers that fall below the FPS floor.

---

## 21. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Heavy 3D tanks mobile performance | High | High | Device tiering, posters/LOD, render-on-demand, hard budget in CI |
| Sourced models don't visually cohere | High | Med | Stylistic alignment QA (§8.4), fresnel-unify pass, fidelity-tier rule |
| License contamination (NC/ND/unknown) | Med | High | CC0-first, license ledger, CI fails on disallowed/unknown |
| Motion causes discomfort | Med | High | First-class reduced-motion path; capped parallax; no flashing |
| WebGL context loss on route change | Med | Med | One persistent canvas; handle `contextlost`/`contextrestored` |
| "Style over substance" — slow, empty wow | Med | High | Earned-attention principle; calm reading surfaces; perf-first |
| Bleeding-edge WebGPU instability | Med | Med | WebGL2 baseline; WebGPU behind capability flag only |
| Scope creep ("everything 3D") | High | Med | Non-goals (§3.2); 3D only where it earns attention |
| AI-slop aesthetics creep in | Med | High | frontend-design skill + explicit anti-slop guardrails in `CLAUDE.md` |

---

## 22. Open questions & future tracks

**Open questions**
- Exact brand palette/typeface (default is "Lumen" + ember/glacier duotone — confirm or replace).
- Light "gallery" direction as an alt theme, or dark-only?
- Content source: flat MDX now, headless CMS later?
- Which routes truly need SSR for SEO vs. static?
- Draco vs. Meshopt as the default (CDN/decoder trade-off)?

**Future tracks (post-v1)**
- WebGPU/TSL as the primary path once support is broadly safe.
- WebXR "view in your space" for hero objects.
- Generative/procedural objects (shader-driven) alongside sourced ones.
- Real-time configurator (swap materials/colors live).
- Audio-reactive motion (opt-in).
- Package the whole engine as a starter template + the asset pipeline as a published Claude Code skill.

---

## Appendix A — Open-source 3D & texture resource directory

Verify each asset's license individually; **default to CC0**, allow **CC-BY** (with attribution), and **reject NC/ND/unknown** for production. Prefer **glTF/GLB**.

| Source | Typical license | Best for | Notes |
|---|---|---|---|
| **Poly Pizza** (poly.pizza) | CC0 / CC-BY | Stylized low-poly models | Successor to Google Poly's spirit; GLB-ready |
| **Quaternius** (quaternius.com) | CC0 | Game-ready packs, consistent style | Great for cohesive sets |
| **Kenney** (kenney.nl) | CC0 | Kits, props, consistent low-poly | Huge, attribution-free |
| **Poly Haven** (polyhaven.com) | CC0 | **HDRIs**, textures, some models | Primary HDRI/IBL source |
| **ambientCG** (ambientcg.com) | CC0 | PBR textures, HDRIs | Great material library |
| **Khronos glTF Sample Assets** (github.com/KhronosGroup/glTF-Sample-Assets) | Mixed (per-model) | Reference/test models, validation | Check each model's license |
| **Smithsonian Open Access 3D** (3d.si.edu) | CC0 | Scanned real artifacts | Museum-quality, public domain |
| **NASA 3D Resources** (nasa.gov/3d-resources) | Public domain (mostly) | Spacecraft, science objects | Verify per asset |
| **Wikimedia Commons (3D)** | CC / PD | Misc, scanned objects | License varies per file |
| **Sketchfab** (sketchfab.com) | Per-model (filter CC) | Huge variety | Filter Downloadable + CC; verify each |
| **BlenderKit** (blenderkit.com) | Per-asset (free tier) | Models, materials, HDRIs | Check license flag |
| **Free3D / CGTrader / TurboSquid (free)** | Per-asset | Variety | Verify license carefully; many are restrictive |

> **Texture/HDRI go-to:** Poly Haven + ambientCG (both CC0). **Model go-to for cohesion:** Quaternius/Kenney (CC0, consistent style) + Poly Pizza. **Realism/artifacts:** Smithsonian Open Access (CC0).

---

## Appendix B — Library reference (quick map)

| Need | Library |
|---|---|
| WebGL/WebGPU renderer | three |
| Declarative 3D in React | @react-three/fiber |
| 3D helpers (loaders, controls, materials) | @react-three/drei |
| Post-processing (bloom, DOF, CA, vignette) | @react-three/postprocessing / postprocessing |
| Timeline + scroll animation | gsap (+ ScrollTrigger) |
| React-idiomatic motion | motion (Framer Motion) |
| Smooth scroll | lenis (@studio-freight/lenis) |
| Shared state | zustand |
| glTF optimization (Draco/Meshopt/KTX2) | @gltf-transform/core + /functions |
| glTF → R3F component | gltfjsx |
| Texture compression | KTX2 / Basis Universal (toktx, basisu) |
| Build | vite / next |
| Types | typescript |
| Tests | vitest, @playwright/test, @axe-core/playwright, lighthouse(-ci) |

---

## Appendix C — Glossary

- **glTF / GLB** — web-native 3D transmission format; GLB is the single-file binary form. Y-up, PBR.
- **PBR (metallic-roughness)** — physically based shading model glTF uses.
- **Fresnel** — view-angle-dependent reflectance; here, the rim-gradient that unifies all objects.
- **Draco / Meshopt** — geometry compression schemes (smaller files / faster decode respectively).
- **KTX2 / Basis Universal** — GPU-native compressed texture format (stays compressed in VRAM).
- **LOD** — Level of Detail; swap simpler meshes at distance/small size.
- **IBL / HDRI** — Image-Based Lighting from a high-dynamic-range environment image.
- **dpr** — device pixel ratio; capping it is a key perf lever.
- **Render-on-demand** — only render frames when something changed (`frameloop="demand"`).
- **TSL** — Three Shading Language (node-based shaders for the WebGPU path).
- **CC0 / CC-BY / NC / ND** — Creative Commons: public-domain / attribution / non-commercial / no-derivatives.
- **ΔE (Delta-E)** — perceptual color-difference metric (used for palette-match scoring).
- **INP / LCP / CLS** — Core Web Vitals: responsiveness / load / layout-stability.

---

## Appendix D — Reduced-motion fallback matrix

| Effect | Full | Reduced motion |
|---|---|---|
| Idle turntable spin | On (6–12°/s) | Off (static, photogenic angle) |
| Cursor parallax | On (capped) | Off |
| Hover acceleration | On | Scale/label only, no spin |
| Scroll-linked rotation | On (scrubbed) | Off; content shows on enter |
| Entrance reveal | Fade+scale+rotate, staggered | Instant or simple fade |
| Aurora mesh drift | Slow animated | Static gradient |
| Bloom/post-fx | On | Minimal/off |
| Smooth scroll (Lenis) | On | Native scroll |
| Custom cursor | On (desktop) | Native cursor |

---

## Appendix E — Review-pass log (the "refine 200×" discipline)

This document was hardened over successive passes; the discipline below is also the **ongoing operating mode** for the build (recheck → fill gaps → recheck → keep the best).

- **Pass — Skeleton:** vision, goals, audience, IA, stack.
- **Pass — Core depth:** full 3D/motion system (taxonomy, hover spec, rotation layering, fresnel shader) and the complete sourcing→alignment→optimize→manifest pipeline.
- **Pass — Production hardening:** performance budget with hard caps, device tiering, render-on-demand.
- **Pass — Inclusivity:** first-class reduced-motion path + fallback matrix, keyboard, contrast-over-gradient, no-WebGL fallback.
- **Pass — Fidelity/cohesion:** the *stylistic* alignment definition + automated turntable QA + palette ΔE scoring (the literal "do they align?").
- **Pass — Buildability:** Claude Code + skills workflow, `CLAUDE.md` memory, packaging the pipeline as a skill.
- **Pass — Delivery:** phases, definition-of-done, testing matrix, infra, SEO, analytics, risks, open questions.
- **Pass — Anti-slop:** explicit guardrails against generic AI aesthetics woven through principles, design language, and DoD.

**Standing rule:** every PR re-checks against §11 (budget), §12 (a11y), §17 (DoD), and the committed art direction before merge. Refinement is continuous, not a milestone.

---

*End of Product.md — Project AETHER.*
