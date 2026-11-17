"""
coniunctio_engine.py - Core architecture for the Coniunctio Engine (v0.5.1)
Adds polarity-aware integration, input validation safeguards, and conservation tracking.
"""

import math
import time


class GroundState:
    def __init__(self, threshold: float = 2.0):
        if threshold < 0:
            raise ValueError("threshold must be non-negative")
        self.threshold = threshold
        self.friction = 0.0
        self.peak_friction = 0.0

    def is_stable(self) -> bool:
        return self.friction <= self.threshold

    def apply_friction(self, amount: float):
        if not math.isfinite(amount):
            raise ValueError("friction amount must be finite")
        self.friction += abs(amount)
        if self.friction > self.peak_friction:
            self.peak_friction = self.friction

    def adapt(self, amount: float):
        if amount <= 0:
            raise ValueError("adapt_rate must be positive")
        self.friction = max(0.0, self.friction - amount)


class MagneticDyad:
    def __init__(self):
        self.tension_a = 0.0
        self.tension_b = 0.0

    def set_tension(self, a: float, b: float):
        if not (math.isfinite(a) and math.isfinite(b)):
            raise ValueError("tensions must be finite numbers")
        self.tension_a = a
        self.tension_b = b

    def net_force(self) -> float:
        return self.tension_a + self.tension_b

    def total_tension(self) -> float:
        return abs(self.tension_a) + abs(self.tension_b)

    def is_balanced(self) -> bool:
        return math.isclose(self.net_force(), 0.0, abs_tol=1e-9)


class Witness:
    def __init__(self):
        self.observation_count = 0
        self.ledger = []

    def observe(
        self,
        pre_state: dict,
        current_phase: str,
        ground: GroundState,
        dyad: MagneticDyad,
        conservation_error: float = 0.0
    ) -> dict:
        self.observation_count += 1
        post_snapshot = {
            "step": self.observation_count,
            "phase": current_phase,
            "stable": ground.is_stable(),
            "active_friction": round(ground.friction, 4),
            "peak_friction": round(ground.peak_friction, 4),
            "tension_a": round(dyad.tension_a, 4),
            "tension_b": round(dyad.tension_b, 4),
            "net_force": round(dyad.net_force(), 4),
            "total_tension": round(dyad.total_tension(), 4),
            "conservation_error": round(conservation_error, 8),
            "unperturbed": True,
            "timestamp": time.time(),
        }

        transition_record = {
            "step": self.observation_count,
            "from_phase": pre_state["phase"],
            "to_phase": current_phase,
            "delta_friction": round(post_snapshot["active_friction"] - pre_state["active_friction"], 4),
            "delta_tension": round(post_snapshot["total_tension"] - pre_state["total_tension"], 4),
            "snapshot": post_snapshot,
        }

        self.ledger.append(transition_record)
        return post_snapshot


class ConiunctioEngine:
    def __init__(
        self,
        threshold: float = 2.0,
        adapt_rate: float = 0.5,
        alpha: float = 1.0,
        beta: float = 0.1,
    ):
        if adapt_rate <= 0:
            raise ValueError("adapt_rate must be positive")
        if alpha < 0 or beta < 0:
            raise ValueError("friction weights must be non-negative")
            
        self.ground = GroundState(threshold=threshold)
        self.dyad = MagneticDyad()
        self.witness = Witness()
        self.current_phase = "GROUND"
        self.adapt_rate = adapt_rate
        self.alpha = alpha
        self.beta = beta
        self.last_conservation_error = 0.0

    def _capture_pre_state(self) -> dict:
        return {
            "phase": self.current_phase,
            "active_friction": self.ground.friction,
            "total_tension": self.dyad.total_tension(),
            "net_force": self.dyad.net_force(),
        }

    def step(self) -> dict:
        pre_state = self._capture_pre_state()
        self.last_conservation_error = 0.0

        if self.current_phase == "GROUND":
            if self.dyad.total_tension() > 0.0:
                self.current_phase = "SPIRAL"

        elif self.current_phase == "SPIRAL":
            generated_friction = (
                self.alpha * abs(self.dyad.net_force())
                + self.beta * self.dyad.total_tension()
            )
            self.ground.apply_friction(generated_friction)
            self.current_phase = (
                "FRICTION" if not self.ground.is_stable() else "INTEGRATION"
            )

        elif self.current_phase == "FRICTION":
            self.ground.adapt(self.adapt_rate)
            if self.ground.is_stable():
                self.current_phase = "INTEGRATION"

        elif self.current_phase == "INTEGRATION":
            target_total = self.dyad.total_tension()
            if target_total > 0.0:
                # Check polarity: opposite signs oppose, same signs reinforce
                is_opposing = (self.dyad.tension_a * self.dyad.tension_b) < 0
                
                if is_opposing:
                    # Opposing poles: shift magnitudes toward equilibrium
                    if abs(self.dyad.tension_a) >= abs(self.dyad.tension_b):
                        new_a = self.dyad.tension_a * 0.95
                        new_b = self.dyad.tension_b * 1.05
                    else:
                        new_a = self.dyad.tension_a * 1.05
                        new_b = self.dyad.tension_b * 0.95
                else:
                    # Reinforcing poles: distribute load symmetrically based on sign
                    sign_a = 1.0 if self.dyad.tension_a >= 0 else -1.0
                    sign_b = 1.0 if self.dyad.tension_b >= 0 else -1.0
                    new_a = sign_a * (target_total * 0.5)
                    new_b = sign_b * (target_total * 0.5)

                raw_sum = abs(new_a) + abs(new_b)
                if raw_sum > 0.0:
                    scale = target_total / raw_sum
                    self.dyad.set_tension(new_a * scale, new_b * scale)
                
                # Calculate conservation error epsilon_T = |T_before - T_after|
                post_total = self.dyad.total_tension()
                self.last_conservation_error = abs(target_total - post_total)
                
            self.current_phase = "GROUND"

        return self.witness.observe(
            pre_state, self.current_phase, self.ground, self.dyad, self.last_conservation_error
        )
