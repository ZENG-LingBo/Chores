# Chores

## RainBorrow calculator

Interactive EBITDA calculator for the RainBorrow umbrella-sharing business model (TEMG3950, Group 1).

- Live page: https://zeng-lingbo.github.io/Chores/
- Source: [`docs/index.html`](docs/index.html), a single self-contained HTML file (no build step needed to serve it).

The page is published with GitHub Pages via [`.github/workflows/pages.yml`](.github/workflows/pages.yml), which deploys the `docs/` folder on every push to `main`.

## RainBorrow Umbrella Studio

Interactive product viewer for the RainBorrow showcase umbrella, with the bold, stacked canopy artwork from the design PDF.

- Page: `/umbrella/`; direct free-camera view: `/umbrella/?view=free`.
- Outside, inside, top and hardware-detail camera presets; daylight and evening lighting; optional slow rotation; PNG export.
- Free cam hides the surrounding page. Drag to orbit, right-drag or Shift-drag to pan, scroll to zoom. Touch supports one-finger orbit and two-finger pan/pinch. Focus the canvas to use WASD movement, Q/E vertical movement, arrow-key orbit, +/- zoom, R reset, and Escape to leave free cam.
- `docs/umbrella/studio.js` builds the curved eight-panel canopy, lining, fibreglass ribs, stretchers, telescopic shaft and grip. The panel textures in `assets/` are exported from the print artwork; the current PDF is linked from the viewer.
- Static HTML/CSS/JS with a vendored Three.js module and local assets; no build step or external CDN dependency. Nunito is distributed under the included OFL license. Fonts in the canopy artwork are outlined/rasterized.
- Serve `docs/` with any static HTTP server for local preview. `index.html`, `studio.css` and `studio.js` are the entry points.

## Umbrella Visibility Lab

3D simulation of what the holder of an advertising umbrella sees, and what share of their visual field is ad.

- Page: `/umbrella/simulator.html` (the original simulator, retained with its `app.js`)
- 3D rendering uses [three.js](https://threejs.org) (MIT), vendored and minified in `docs/umbrella/vendor/`, so there is still no build step.
- The percentages come from tracing ~90,000 evenly spaced rays across the human visual field (about 200° × 135°) against the exact canopy geometry, with the ad artwork as the source of truth for which rays hit an ad.

## RainBorrow Logo Studio

Mix-and-match tool for the RainBorrow logo, with twelve app-icon symbols built around sharing one umbrella in both rain and sun.

- Page: `/logo/` (source in [`docs/logo/index.html`](docs/logo/index.html), one self-contained file)
- Every symbol is drawn as SVG in code, with flat, depth and glass finishes, and app-icon, round or bare frames.
- Exports a 1024 px symbol PNG, symbol SVG and a transparent logo PNG. The share link stores the full combination in the URL hash.
