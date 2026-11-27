# ground_state_103.py
"""Calibration model for THE 103 — THE GROUND STATE in coniunctio-engine.

Models unexcited potential [0, 0, 0], gradient-driven flow (89 / V_mem),
global informational coordination (+ operator), and a resettable Seam so that
acquired state (armor/mask) remains distinguishable from baseline and open
to revision.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class TriadVector:
    """Represents the three lenses/channels (e.g., Sun/Moon/Earth or Thought/Memory/Instinct)."""

    thought: float = 0.0
    memory: float = 0.0
    instinct: float = 0.0

    def as_tuple(self) -> Tuple[float, float, float]:
        return (self.thought, self.memory, self.instinct)

    def gradient_magnitude(self) -> float:
        """Measures departure from the [0, 0, 0] ground state."""
        return (self.thought**2 + self.memory**2 + self.instinct**2) ** 0.5

    def plus_synthesis(self) -> float:
        """Relational integration (+) holding channels in tension without collapsing them."""
        return (self.thought + self.memory + self.instinct) / 3.0


@dataclass
class RevisionRecord:
    """Tracks revisions across the Seam without sealing the baseline as dogma."""

    step: int
    action: str
    gradient_norm: float
    coherence_index: float
    note: str = ""


@dataclass
class GroundState103Model:
    """Calibrated, unsealed baseline model for THE 103."""

    ground_coords: Tuple[int, int, int] = (0, 0, 0)
    seam_visible: bool = True
    armor_weight: float = 0.0
    state: TriadVector = field(default_factory=TriadVector)
    spiral_turn: int = 0
    history: List[RevisionRecord] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.history:
            self.history.append(
                RevisionRecord(
                    step=0,
                    action="init_ground_state",
                    gradient_norm=self.state.gradient_magnitude(),
                    coherence_index=1.0,
                    note="Calibrated at [0, 0, 0]; seam visible and open to revision.",
                )
            )

    def apply_gradient(
        self,
        d_thought: float = 0.0,
        d_memory: float = 0.0,
        d_instinct: float = 0.0,
        armor_delta: float = 0.0,
        note: str = "",
    ) -> None:
        """Introduces difference/potential gradient (89 / bioelectric V_mem) and optional armor."""
        self.state = TriadVector(
            thought=round(self.state.thought + d_thought, 6),
            memory=round(self.state.memory + d_memory, 6),
            instinct=round(self.state.instinct + d_instinct, 6),
        )
        self.armor_weight = round(max(0.0, self.armor_weight + armor_delta), 6)
        self.spiral_turn += 1
        self.history.append(
            RevisionRecord(
                step=self.spiral_turn,
                action="apply_gradient",
                gradient_norm=round(self.state.gradient_magnitude(), 6),
                coherence_index=round(self.informational_coherence(), 6),
                note=note or "Gradient shifted; swamp/form condensing.",
            )
        )

    def toggle_seam(self, visible: bool, note: str = "") -> None:
        """Explicitly reveals or obscures the seam and logs the transition."""
        self.seam_visible = visible
        self.spiral_turn += 1
        self.history.append(
            RevisionRecord(
                step=self.spiral_turn,
                action="toggle_seam",
                gradient_norm=round(self.state.gradient_magnitude(), 6),
                coherence_index=round(self.informational_coherence(), 6),
                note=note or f"Seam set to {'visible' if visible else 'obscured'}.",
            )
        )

    def informational_coherence(self) -> float:
        """Models top-down informational coordination (+): penalizes unacknowledged/heavy armor."""
        visible_heavy_armor_penalty = 0.20 if (self.seam_visible and self.armor_weight > 1.5) else 0.0
        hidden_seam_penalty = (
            min(0.55, 0.25 + 0.15 * self.armor_weight)
            if (not self.seam_visible and self.armor_weight > 0.0)
            else 0.0
        )
        raw_score = (
            1.0
            - min(
                0.85,
                0.08 * self.state.gradient_magnitude()
                + visible_heavy_armor_penalty
                + hidden_seam_penalty,
            )
        )
        return round(max(0.0, raw_score), 6)

    def step_spiral(self, damping: float = 0.85, note: str = "") -> float:
        """Advances one spiral turn (100 -> 103), dampening excess friction toward a new octave."""
        if not (0.0 <= damping <= 1.0):
            raise ValueError("damping must be between 0.0 and 1.0")

        self.state = TriadVector(
            thought=round(self.state.thought * damping, 6),
            memory=round(self.state.memory * damping, 6),
            instinct=round(self.state.instinct * damping, 6),
        )
        self.armor_weight = round(self.armor_weight * damping, 6)
        self.spiral_turn += 1
        plus_val = round(self.state.plus_synthesis(), 6)

        self.history.append(
            RevisionRecord(
                step=self.spiral_turn,
                action="spiral_turn",
                gradient_norm=round(self.state.gradient_magnitude(), 6),
                coherence_index=round(self.informational_coherence(), 6),
                note=note or f"Spiral turn {self.spiral_turn}; plus_synthesis={plus_val}.",
            )
        )
        return plus_val

    def reset_to_ground(self, restore_seam: bool = True, note: str = "") -> None:
        """Resets state and armor back to [0, 0, 0] (like bioelectric depolarization / seam check)."""
        self.state = TriadVector()
        self.armor_weight = 0.0
        if restore_seam:
            self.seam_visible = True
        self.spiral_turn += 1
        self.history.append(
            RevisionRecord(
                step=self.spiral_turn,
                action="reset_to_ground",
                gradient_norm=0.0,
                coherence_index=round(self.informational_coherence(), 6),
                note=note or "Returned to [0, 0, 0] ground state; model remains unsealed.",
            )
        )

    def snapshot(self) -> Dict[str, object]:
        """Exports current calibration state for inspection or logging."""
        return {
            "ground_coords": self.ground_coords,
            "spiral_turn": self.spiral_turn,
            "seam_visible": self.seam_visible,
            "armor_weight": self.armor_weight,
            "state": self.state.as_tuple(),
            "gradient_norm": round(self.state.gradient_magnitude(), 6),
            "plus_synthesis": round(self.state.plus_synthesis(), 6),
            "coherence_index": round(self.informational_coherence(), 6),
            "history_count": len(self.history),
        }
