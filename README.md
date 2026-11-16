# Coniunctio Engine (v0.2)

A zero-dependency Python diagnostic framework modeling dynamic psychological states, predictive coding, and spiral coherence around the golden ratio conjugate ($\phi^{-1} \approx 0.618$).

Built exclusively with the Python standard library (`math`, `time`, `json`, `glob`, `os`, `sys`, `unittest`).

---

## Core Architecture

* **`coniunctio_engine.py`**: The core state-transition engine (`GroundState`, `MagneticDyad`, `Witness`, and `ConiunctioEngine`) tracking cycle coherence, relational tension, and adaptive priors.
* **`sandbox.py`**: Interactive command-line REPL for testing live trajectories, running built-in presets (`spiral` and `shock`), and exporting session histories to JSON.
* **`analyzer.py`**: Diagnostic post-processor that parses exported `trajectory_*.json` runs, computes session metrics, and plots an ASCII coherence timeline against the `0.618` phase-lock threshold.
* **`test_coniunctio.py`**: Automated unit and integration test suite verified on every push via GitHub Actions.

---

## Quick Start

### 1. Run the Interactive Sandbox
Launch the REPL to feed `(thought, feeling, instinct)` vectors or run preset trajectories:

```bash
python sandbox.py
