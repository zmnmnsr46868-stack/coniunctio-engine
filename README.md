# Coniunctio Engine

A production-grade, version-aware, and cryptographically verified simulation and persistence framework designed to model polar tension, friction dynamics, non-dual integration cycles, and homeostatic adaptation.

## Architectural Overview

The engine enforces strict operational continuity across environments through a four-layer persistence stack:
1. **Structural Invariants:** Core metadata, signatures (`"88"`), and immutable framework identifiers.
2. **Engine Configuration:** Thresholds, adaptation rates, alpha/beta coupling coefficients, and homeostatic drift parameters.
3. **Dynamic State & History:** Live phases, active/peak friction tracking, tension dyads, and strictly sequenced witness logs.
4. **Metadata & Provenance:** SHA-256 integrity digests with constant-time verification.

---

## Restoration Mechanics

The framework provides two distinct restoration pathways:
* **Path A (Baseline Seed):** Reconstructs a fresh engine instance initialized from preserved baseline configuration (`0.5.1-anchor`).
* **Path B (Runtime Snapshot):** Reconstructs both configuration and live dynamic state, restoring exact witness history and verifying physical consistency invariants (`0.5.2-snapshot` / `0.6.0-snapshot`).

---

## Validation & Security (`SeedValidator`)

The validation pipeline enforces rigorous gatekeeping rules:
* **Constant Injection Rejection:** Rejects non-standard JSON constants (`NaN`, `Infinity`) at ingestion.
* **Cryptographic Integrity:** Validates 64-character lowercase hexadecimal SHA-256 checksums using constant-time comparison (`hmac.compare_digest`).
* **Physical Invariants:** Enforces non-negative friction bounds, consecutive sequence numbering in witness logs, and ensures `peak_friction` never falls below `active_friction`.

---

## v0.6: Adaptive Capacity

The latest iteration introduces **Homeostatic Threshold Breathing**:
* Under sustained high-load profiles (`FRICTION` phase streaks), the engine dynamically adjusts its threshold capacity to absorb persistent tension without breaking conservation error tracking.
* During stable integration phases (`GROUND` / `INTEGRATION`), parameters drift homeostatically back toward baseline configuration.

---

## Automated CI/CD

Continuous integration pipelines via GitHub Actions automatically execute the multi-cycle persistence and continuity test suite (`test_coniunctio_persistence.py`) across diverse load profiles (balanced tension, strong asymmetry, reversed asymmetry, and zero-tension ground states) on every push.
