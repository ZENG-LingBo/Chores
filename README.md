# Chores

## RainBorrow calculator

Interactive EBITDA calculator for the RainBorrow umbrella-sharing business model (TEMG3950, Group 1).

- Live page: https://zeng-lingbo.github.io/Chores/
- Source: [`docs/index.html`](docs/index.html), a single self-contained HTML file (no build step needed to serve it).

The page is published with GitHub Pages via [`.github/workflows/pages.yml`](.github/workflows/pages.yml), which deploys the `docs/` folder on every push to `main`.

## Umbrella View Simulator

3D simulation of what the holder of an advertising umbrella sees, and what share of their visual field is ad.

- Page: `/umbrella/` (source in [`docs/umbrella/`](docs/umbrella/))
- 3D rendering uses [three.js](https://threejs.org) (MIT), vendored and minified in `docs/umbrella/vendor/`, so there is still no build step.
- The percentages come from tracing ~90,000 evenly spaced rays across the human visual field (about 200° × 135°) against the exact canopy geometry, with the ad artwork as the source of truth for which rays hit an ad.
