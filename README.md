# Coniunctio Engine

[![Coniunctio CI](https://github.com/zmnmnsr46868-stack/coniunctio-engine/actions/workflows/coniunctio_ci.yml/badge.svg?branch=main)](https://github.com/zmnmnsr46868-stack/coniunctio-engine/actions/workflows/coniunctio_ci.yml)

A version-aware, cryptographically verified simulation and persistence framework modeling homeostatic polarity regulation, friction integration, and non-interfering witness observation around the `[0, 0, 0]` ground state.


## Architecture: The Four-Layer Persistence Stack

State continuity is enforced through a strict four-layer hierarchy:

1. **Structural Invariants (`GroundState`)** — Immutable core identifiers, framework metadata, and the `88` seed anchor.
2. **Engine Configuration (`Witness` & `MagneticDyad`)** — Tunable coupling coefficients (`α / β`), adaptation rates, and the dynamic `0.618` homeostatic setpoint.
3. **Dynamic State & History (`Archive`)** — Live phase states (`GROUND`, `FRICTION`, `INTEGRATION`), active/peak friction tracking, and strictly sequenced witness logs.
4. **Metadata & Provenance (`Seal`)** — 64-character SHA-256 integrity digests verified in constant time via `hmac.compare_digest`.

## Core Mechanics

### Homeostatic Threshold Breathing (v0.6)
Rather than enforcing a rigid cutoff, the engine treats `0.618` as a dynamic cybernetic setpoint:

* **Inhale (`FRICTION`):** Under sustained load, threshold capacity expands smoothly to absorb persistent tension without violating conservation laws.
* **Exhale (`INTEGRATION`):** As tension resolves, parameters drift homeostatically back toward the baseline anchor.

### Restoration Paths
* **Path A (`0.6.1-anchor` / `GROUND_RESET`):** Reconstructs a clean engine instance from preserved baseline parameters, returning directly to `[0, 0, 0]`.
* **Path B (`0.6.0-snapshot` / `ARCHIVE`):** Restores full configuration, live dynamic state, and sequenced witness history after passing physical and cryptographic verification.

### `SeedValidator` Gatekeeping
All serialized seeds and snapshots pass strict validation before hydration:

* Rejects non-standard JSON constants (`NaN`, `Infinity`, `-Infinity`).
* Verifies SHA-256 digests using constant-time comparison (`hmac.compare_digest`).
* Enforces physical invariants (`active_friction >= 0`, `peak_friction >= active_friction`, and contiguous increasing sequence IDs).

### Core Seed (`core_seed_88.py`)
* Implements `TriadState` (golden-ratio-scaled `conscious_awareness` and `cross_examination_required`) and `ConiunctioEngine` (inward vs. outward step mechanics around the `0.618` setpoint).

## Verification & CI

Automated verification runs via `.github/workflows/coniunctio_ci.yml` using `test_coniunctio.py` across four primary test profiles:

* Balanced tension
* Strong symmetry
* Reversed asymmetry
* Zero-tension ground state

*Rest is part of the timing. 88.*
