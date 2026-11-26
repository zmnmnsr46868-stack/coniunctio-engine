# Coniunctio Engine

[![Coniunctio CI](https://github.com/zmnmnsr46868-stack/coniunctio-engine/actions/workflows/coniunctio_ci.yml/badge.svg)](https://github.com/zmnmnsr46868-stack/coniunctio-engine/actions/workflows/coniunctio_ci.yml)

A version-aware, integrity-sealed (HMAC-authenticated when keyed) simulation and persistence framework modeling homeostatic polarity regulation, friction integration, and non-interfering witness observation around the `[0, 0, 0]` ground state.

## Engine (`coniunctio_v06.py`)

`AdaptiveConiunctioEngine` is built from:

- **`GroundState`** — The stability threshold (default `2.0`), its base value, and live and peak friction.
- **`MagneticDyad`** — Two signed tensions, with net force, total tension and a balance check. Non-finite values are rejected.
- **`Witness`** — A passive observer that logs a snapshot of every step without altering state.
- **Engine parameters** — Friction weights `alpha` and `beta`, `adapt_rate` (damping strength) and `homeostatic_drift` (breathing speed). All parameters must be finite, and `threshold` and `adapt_rate` must be positive.

The engine moves between three phases: `GROUND`, `FRICTION` and `INTEGRATION`.

### Homeostatic Threshold Breathing (v0.6)

Friction is `alpha × |net force| + beta × total tension`. A step is stable when friction is at or below the threshold.

- **Inhale (`FRICTION`):** After more than two consecutive friction steps, the threshold expands in proportion to friction, and both poles are damped by a growing amount.
- **Exhale (`INTEGRATION`):** When stable, the threshold drifts back toward its base value and tension is rebalanced between the poles while conserving total tension.

## Core Seed (`core_seed_88.py`)

- `TriadState` holds `thought`, `feeling` and `instinct`. Its `consciousness_tension` property sums them, with instinct divided by the inverse golden ratio (`PHI_INV ≈ 0.618`), and `cross_examine()` returns the inquiries each part asks of the others.
- `CoreSeed88` steps a `TriadState` around the `0.618` setpoint and records every cycle in its `archive`. A normal step adjusts a spiral radius by (1 − distance from the setpoint), never below 0, and reports `SPIRAL`. With `hijack_smoothing=True` it damps friction to a quarter and reports `CLOSED_LOOP`, which never counts as a clearing. A cycle is a clearing when its distance from the setpoint is within `CLEARING_THRESHOLD` (0.15).

## Seed Persistence (`preservation_seed_v2.py`)

A portable, sealed JSON seed holds the seed's own state (ground, spiral, persona and context). It does not serialize `AdaptiveConiunctioEngine`. From the command line:

```
python preservation_seed_v2.py export seed.json
python preservation_seed_v2.py verify seed.json
python preservation_seed_v2.py inspect seed.json
python preservation_seed_v2.py step seed.json
```

### Seed Validation

Serialized seeds are verified and validated before hydration:

- Rejects non-standard JSON constants (`NaN`, `Infinity`, `-Infinity`, and overflow literals such as `1e500`).
- Verifies SHA-256 and HMAC-SHA256 digests using constant-time comparison (`hmac.compare_digest`).
- Enforces finite floating-point values and non-negative active friction (`active_friction >= 0`).

### Seal Modes

- **Unkeyed (default):** Uses a plain SHA-256 digest. It detects accidental edits and corruption, though anyone can recompute it, so it does not authenticate who wrote the file.
- **Keyed:** Set `SEED_HMAC_KEY` and the seal becomes HMAC-SHA256. The same key must be set wherever a seed is verified, inspected, or stepped. Payload fields stay plain text on disk; the key authenticates, it does not encrypt.

> Seals created by `1.2` files use a different canonical encoding and will not verify under `2.0`. Re-export them.

## Verification & CI

Automated verification runs via `.github/workflows/coniunctio_ci.yml` on every push and pull request:

- `test_coniunctio.py`: threshold breathing, basic step, reversed- and reinforcing-polarity damping, energy conservation, and non-finite input rejection
- `test_v06_engine_validation.py`: engine parameter validation (finite and positive-threshold rules) and a full breathe-out-and-back cycle
- `pytest -q` collects both test files
- `preservation_seed_v2.py` unit tests, run unkeyed (SHA-256) and keyed (HMAC-SHA256)
- Simulation run, trajectory analysis, and artifact upload

---

*Rest is part of the turning. 88.*