# Coniunctio Engine

[![Coniunctio CI](https://github.com/zmnmnsr46868-stack/coniunctio-engine/actions/workflows/coniunctio_ci.yml/badge.svg)](https://github.com/zmnmnsr46868-stack/coniunctio-engine/actions/workflows/coniunctio_ci.yml)

A version-aware, integrity-sealed (HMAC-authenticated when keyed) simulation and persistence framework modeling homeostatic polarity regulation, friction integration, and non-interfering witness observation around the `[0, 0, 0]` ground state.

## Architecture: The Four-Layer Persistence Stack

State continuity is structured around four core layers:

1. **Structural Invariants (`GroundState`)** — Immutable core identifiers, framework metadata, and the `88` seed anchor.
2. **Engine Configuration (`Witness` & `MajesticDyad`)** — Tunable coupling coefficients (`α`, `γ`, `β`), adaptation rates, and the dynamic `0.618` homeostatic setpoint.
3. **Dynamic State & History (`Archon`)** — Live phase states (`GROUND`, `FRICTION`, `INTEGRATION`), friction tracking, and witness observation logs.
4. **Metadata & Provenance (`Seal`)** — 64-character SHA-256 integrity digests (`HMAC-SHA256` when `SEED_HMAC_KEY` is set) verified in constant time via `hmac.compare_digest`.

## Core Mechanics

### Homeostatic Threshold Breathing (`v0.6`)

Rather than enforcing a rigid cutoff, the engine treats `0.618` as a dynamic cybernetic setpoint:

- **Inhale (`FRICTION`):** Under sustained load, threshold capacity expands smoothly to absorb persistent tension without violating conservation laws.
- **Exhale (`INTEGRATION`):** As tension resolves, parameters drift homeostatically back toward the baseline anchor.

### Restoration Paths

- **Path A (`0.6.1-anchor` / `GRANULARITY`):** Reconstructs a clean engine instance from preserved baseline parameters, returning directly to `[0, 0, 0]`.
- **Path B (`0.6.4-snapshot` / `ARCHIVE`):** Restores full configuration, live dynamic state, and witness history after passing integrity and validation checks.

## Seed Validation (`preservation_seed_v2.py`)

Serialized seeds are verified and validated before hydration:

- Rejects non-standard JSON constants (`NaN`, `Infinity`, `-Infinity`, and overflow literals such as `1e500`).
- Verifies SHA-256 and HMAC-SHA256 digests using constant-time comparison (`hmac.compare_digest`).
- Enforces finite floating-point values and non-negative active friction (`active_friction >= 0`).

## Core Seed (`core_seed_88.py`)

- Implements `TriadState` (symmetric-active `0.618` conscious awareness and `cross_examination_inquiry`) and `ConiunctioEngine` (inward vs. outward step mechanics around the `0.618` setpoint).

## Verification & CI

Automated verification runs via `.github/workflows/coniunctio_ci.yml` on every push and pull request:

- `test_coniunctio.py` across four primary test profiles:
  - Balanced tension
  - Strong symmetry
  - Reversed asymmetry
  - Zero-tension ground state
- `pytest -q`
- `preservation_seed_v2.py` unit tests (unkeyed SHA-256 and keyed HMAC-SHA256)
- Simulation runs, trajectory analysis, and artifact upload

### Seal Modes (`preservation_seed_v2.py`)

- **Unkeyed (default):** Uses a plain SHA-256 digest. It detects accidental edits and corruption, though anyone can recompute it, so it does not authenticate who wrote the file.
- **Keyed:** Set `SEED_HMAC_KEY` and the seal becomes HMAC-SHA256. The same key must be set wherever a seed is verified, inspected, or stepped. Payload fields stay plain text on disk; the key authenticates, it does not encrypt.

> Seals created by `1.2` files use a different canonical encoding and will not verify under `2.0`. Re-export them.

---

*Rest is part of the turning. 88.*
