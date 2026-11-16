# coniunctio-engine [![Coniunctio CI](https://github.com/zmnmnsr46868-stack/coniunctio-engine/actions/workflows/test.yml/badge.svg)](https://github.com/zmnmnsr46868-stack/coniunctio-engine/actions/workflows/test.yml)

An executable dialectical state-integration framework bridging Jungian psychology, predictive coding, and phase dynamics.

## Overview

**Coniunctio Engine (v0.2)** models psychological state transitions by mapping incoming prediction error (tension) against an adaptive observer prior anchored to an unconditioned baseline. When internal tension drops below the critical golden ratio conjugate threshold (`φ⁻¹ ≈ 0.618`), coherence rises above `0.618`, shifting the system from reactive loop dynamics into stateful evolutionary spirals.

## Architecture & Core Components

| Component | Role in Model | Mathematical Basis |
| :--- | :--- | :--- |
| **`GroundState`** | The unconditioned, unperturbed observer baseline | `[0, 0, 0]` coordinate anchor |
| **`MagneticDyad`** | Models active polarities (Thought, Feeling, Instinct) against priors | Prediction error magnitude: `√((t - pₜ)² + (f - p_f)² + (i - pᵢ)²)` |
| **`Witness`** | The central observer that introduces the pause | Bounded coherence function: `1 / (1 + tension)` |
| **`ConiunctioEngine`** | Stateful integration engine with trajectory memory | Updates priors at rate `1 - φ⁻¹ ≈ 0.382` during phase lock |

## Phase-Lock & Spiral Dynamics

1. **Prediction Error Calculation:** `MagneticDyad` measures the Euclidean distance between incoming inputs and the current predictive `prior`.
2. **Coherence Mapping:** The `Witness` observes the resulting tension and computes a bounded coherence score `C`.
3. **Golden Ratio Conjugate Threshold (`φ⁻¹ ≈ 0.618`):**
   * **`C > 0.618` (`SPIRAL`):** Phase lock achieved. `spiral_depth` increments and the predictive `prior` adapts toward the integrated state.
   * **`C ≤ 0.618` (`GROUND_RESET`):** High surprise/noise detected. `spiral_depth` resets to `0` and the system returns to `[0, 0, 0]`.

## Quick Start

### Prerequisites
* Python 3.8+ (uses only standard library modules `math` and `time`).

### Run a Stateful Trajectory
```python
from coniunctio_engine import ConiunctioEngine

engine = ConiunctioEngine()
print(engine.step(thought=0.2, feeling=0.25, instinct=0.15))
print(engine.step(thought=0.25, feeling=0.30, instinct=0.20))
