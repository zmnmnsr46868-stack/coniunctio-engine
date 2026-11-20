# Coniunctio Engine

A version-aware, cryptographically verified simulation and persistence framework modeling homeostatic polarity regulation, friction integration, and non-interfering witness observation around the `[0, 0, 0]` ground state[span_0](start_span)[span_0](end_span).

## Architecture: The Four-Layer Persistence Stack[span_1](start_span)[span_1](end_span)

State continuity is enforced through a strict four-layer hierarchy[span_2](start_span)[span_2](end_span):

1. **Structural Invariants (`GroundState`)** — Immutable core identifiers, framework metadata, and the `88` seed anchor[span_3](start_span)[span_3](end_span).
2. **Engine Configuration (`Witness` & `MagneticDyad`)** — Tunable coupling coefficients ($\alpha / \beta$), adaptation rates, and the dynamic `0.618` homeostatic setpoint[span_4](start_span)[span_4](end_span).
3. **Dynamic State & History (`Archive`)** — Live phase states (`GROUND`, `FRICTION`, `INTEGRATION`), active/peak friction tracking, and strictly sequenced witness logs[span_5](start_span)[span_5](end_span).
4. **Metadata & Provenance (`Seal`)** — 64-character SHA-256 integrity digests verified in constant time via `hmac.compare_digest`[span_6](start_span)[span_6](end_span).

---

## Core Mechanics[span_7](start_span)[span_7](end_span)

### Homeostatic Threshold Breathing (`v0.6`)[span_8](start_span)[span_8](end_span)
Rather than enforcing a rigid cutoff, the engine treats **0.618** as a dynamic cybernetic setpoint[span_9](start_span)[span_9](end_span):
- **Inhale (`FRICTION`):** Under sustained load, threshold capacity expands smoothly to absorb persistent tension without violating conservation bounds[span_10](start_span)[span_10](end_span).
- **Exhale (`GROUND / INTEGRATION`):** As tension resolves, parameters drift homeostatically back toward the baseline anchor[span_11](start_span)[span_11](end_span).

### Restoration Paths[span_12](start_span)[span_12](end_span)
- **Path A (`0.5.1-anchor` / `GROUND_RESET`):** Reconstructs a clean engine instance from preserved baseline parameters, returning directly to `[0, 0, 0]`[span_13](start_span)[span_13](end_span).
- **Path B (`0.6.0-snapshot` / `Spiral`):** Restores full configuration, live dynamic state, and sequenced witness history after passing physical and cryptographic verification[span_14](start_span)[span_14](end_span).

### `SeedValidator` Gatekeeping[span_15](start_span)[span_15](end_span)
All serialized seeds and snapshots pass strict validation before hydration[span_16](start_span)[span_16](end_span):
- Rejects non-standard JSON constants (`NaN`, `Infinity`, `-Infinity`)[span_17](start_span)[span_17](end_span).
- Verifies SHA-256 digests using constant-time comparison (`hmac.compare_digest`)[span_18](start_span)[span_18](end_span).
- Enforces physical invariants (`active_friction >= 0`, `peak_friction >= active_friction`, and contiguous witness log sequence IDs)[span_19](start_span)[span_19](end_span).

### Core Seed (`core_seed_88.py`)[span_20](start_span)[span_20](end_span)[span_21](start_span)[span_21](end_span)[span_22](start_span)[span_22](end_span)
- Implements `TriadState` (golden-ratio-scaled `consciousness_tension` and cross-examination inquiries) and `CoreSeed88` (spiral vs. hijack-loop step mechanics around the `0.618` setpoint)[span_23](start_span)[span_23](end_span).

---

## Verification & CI[span_24](start_span)[span_24](end_span)

Automated verification runs via `.github/workflows/coniunctio_ci.yml` using `test_coniunctio.py` across four primary load profiles[span_25](start_span)[span_25](end_span):
- Balanced tension[span_26](start_span)[span_26](end_span)
- Strong asymmetry[span_27](start_span)[span_27](end_span)
- Reversed asymmetry[span_28](start_span)[span_28](end_span)
- Zero-tension ground state[span_29](start_span)[span_29](end_span)

---

*Rest is part of the turning. 88.*[span_30](start_span)[span_30](end_span)
