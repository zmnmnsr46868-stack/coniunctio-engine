# coniunctio-engine

An executable dialectical state-integration framework bridging Jungian psychology, predictive coding, and phase dynamics.

## Overview

**Coniunctio Engine** models psychological state transitions by mapping internal tension against a stable observer baseline. When internal tension drops below the critical golden ratio threshold ($\phi \approx 0.618$), the system transitions from reactive loop dynamics to intentional evolutionary spirals.

## Architecture & Core Components

| Component | Role in Model | Mathematical Basis |
| :--- | :--- | :--- |
| **`GroundState`** | The unconditioned, unperturbed baseline | $[0, 0, 0]$ coordinate anchor |
| **`MagneticDyad`** | Models active psychological polarities (Thought, Feeling, Instinct) | Vector magnitude calculation |
| **`Witness`** | The central observer that introduces the pause | Bounded coherence function: $1 / (1 + \text{tension})$ |
| **`ConiunctioEngine`** | The master integration loop | Evaluates phase-lock threshold across cycles |

## Phase-Lock Dynamics

1. **Tension Calculation:** Incoming cognitive/emotional inputs form a vector via `MagneticDyad`.
2. **Coherence Mapping:** The `Witness` observes the tension and calculates a coherence score.
3. **Golden Ratio Threshold ($\phi \approx 0.618$):**
   * **$C > 0.618$ (Phase Lock Achieved):** Signals a successful transition from loop to spiral.
   * **$C \le 0.618$ (Noise Detected):** Reverts focus back to the baseline at $[0, 0, 0]$.

## Quick Start

### Prerequisites
* Python 3.8+ (uses only standard library modules like `math` and `time`).

### Run a Single Step
```python
from coniunctio_engine import ConiunctioEngine

engine = ConiunctioEngine()
coherence = engine.step(thought=0.2, feeling=0.3, instinct=0.1)
