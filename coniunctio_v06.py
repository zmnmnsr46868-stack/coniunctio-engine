"""
coniunctio_v06.py - Coniunctio Engine v0.6 ("Adaptive Capacity")
Extends core dynamics with homeostatic threshold breathing, dynamic adaptation
rates, sign-agnostic damping, and energy-conserving integration.
"""

import math


class Witness:
    def __init__(self):
        self.observation_count = 0
        self.log = []

    def record(self, state_snapshot: dict):
        self.observation_count += 1
        self.log.append((self.observation_count, state_snapshot))


class MagneticDyad:
    def __init__(self, tension_a: float = 0.0, tension_b: float = 0.0):
        self.tension_a = 0.0
        self.tension_b = 0.0
        self.set_tension(tension_a, tension_b)

    def set_tension(self, a: float, b: float):
        if not (math.isfinite(a) and math.isfinite(b)):
            raise ValueError("tensions must be finite numbers")
        self.tension_a = float(a)
        self.tension_b = float(b)

    def get_net_force(self) -> float:
        return self.tension_a + self.tension_b

    def get_total_tension(self) -> float:
        return abs(self.tension_a) + abs(self.tension_b)

    def is_balanced(self) -> bool:
        return math.isclose(self.get_net_force(), 0.0, abs_tol=1e-9)


class GroundState:
    def __init__(self, threshold: float = 2.0):
        if not math.isfinite(threshold) or threshold < 0:
            raise ValueError("threshold must be a finite non-negative number")
        self.base_threshold = float(threshold)
        self.threshold = float(threshold)
        self.friction = 0.0
        self.peak_friction = 0.0

    def compute_friction(
        self, net_force: float, total_tension: float, alpha: float, beta: float
    ) -> float:
        self.friction = (alpha * abs(net_force)) + (beta * total_tension)
        if self.friction > self.peak_friction:
            self.peak_friction = self.friction
        return self.friction

    def is_stable(self) -> bool:
        return self.friction <= self.threshold


class AdaptiveConiunctioEngine:
    def __init__(
        self,
        threshold: float = 2.0,
        adapt_rate: float = 1.0,
        alpha: float = 1.0,
        beta: float = 0.1,
        homeostatic_drift: float = 0.05,
    ):
        if adapt_rate <= 0:
            raise ValueError("adapt_rate must be positive")
        if alpha < 0 or beta < 0:
            raise ValueError("friction weights must be non-negative")
        if homeostatic_drift < 0:
            raise ValueError("homeostatic_drift must be non-negative")

        self.base_threshold = float(threshold)
        self.threshold = float(threshold)
        self.adapt_rate = float(adapt_rate)
        self.alpha = float(alpha)
        self.beta = float(beta)
        self.homeostatic_drift = float(homeostatic_drift)

        self.dyad = MagneticDyad(0.0, 0.0)
        self.ground = GroundState(threshold=threshold)
        self.witness = Witness()

        self.current_phase = "GROUND"
        self.last_conservation_error = 0.0
        self.friction_step_streak = 0

    def _rebalance_conserving_energy(self, target_total: float):
        if target_total <= 0.0:
            self.last_conservation_error = 0.0
            return

        is_opposing = (self.dyad.tension_a * self.dyad.tension_b) < 0
        if is_opposing:
            if abs(self.dyad.tension_a) >= abs(self.dyad.tension_b):
                new_a = self.dyad.tension_a * 0.95
                new_b = self.dyad.tension_b * 1.05
            else:
                new_a = self.dyad.tension_a * 1.05
                new_b = self.dyad.tension_b * 0.95
        else:
            sign_a = 1.0 if self.dyad.tension_a >= 0 else -1.0
            sign_b = 1.0 if self.dyad.tension_b >= 0 else -1.0
            new_a = sign_a * (target_total * 0.5)
            new_b = sign_b * (target_total * 0.5)

        raw_sum = abs(new_a) + abs(new_b)
        if raw_sum > 0.0:
            scale = target_total / raw_sum
            self.dyad.set_tension(new_a * scale, new_b * scale)

        post_energy = self.dyad.get_total_tension()
        self.last_conservation_error = abs(target_total - post_energy)

    def _damp_pole(self, value: float, half_reduction: float) -> float:
        if value > 0.0:
            return max(0.0, value - half_reduction)
        if value < 0.0:
            return min(0.0, value + half_reduction)
        return 0.0

    def step(self):
        net_force = self.dyad.get_net_force()
        total_tension = self.dyad.get_total_tension()

        friction = self.ground.compute_friction(
            net_force, total_tension, self.alpha, self.beta
        )

        if self.ground.is_stable():
            self.current_phase = "INTEGRATION"
            self.friction_step_streak = 0

            # Homeostatic recovery: drift threshold back toward base configuration
            if self.ground.threshold > self.base_threshold:
                self.ground.threshold = max(
                    self.base_threshold,
                    self.ground.threshold - self.homeostatic_drift,
                )
                self.threshold = self.ground.threshold

            # Energy-conserving polarity rebalancing
            self._rebalance_conserving_energy(total_tension)
        else:
            self.current_phase = "FRICTION"
            self.friction_step_streak += 1
            self.last_conservation_error = 0.0

            # Adaptive Capacity: expand threshold dynamically under sustained load
            if self.friction_step_streak > 2:
                expansion = self.homeostatic_drift * (
                    friction / self.ground.threshold
                )
                self.ground.threshold += expansion
                self.threshold = self.ground.threshold

            # Sign-agnostic progressive damping (allows multi-step streaks to register)
            reduction = self.adapt_rate * (1.0 + 0.1 * self.friction_step_streak)
            half_red = reduction / 2.0
            self.dyad.set_tension(
                self._damp_pole(self.dyad.tension_a, half_red),
                self._damp_pole(self.dyad.tension_b, half_red),
            )

        self.witness.record(
            {
                "phase": self.current_phase,
                "friction": friction,
                "threshold": self.ground.threshold,
                "streak": self.friction_step_streak,
                "t_a": self.dyad.tension_a,
                "t_b": self.dyad.tension_b,
                "conservation_error": self.last_conservation_error,
            }
        )
