import unittest

from ground_state_103 import GroundState103Model, TriadVector


class TestCoherencePenalties(unittest.TestCase):
    def test_ground_state_is_fully_coherent(self):
        self.assertEqual(GroundState103Model().informational_coherence(), 1.0)

    def test_displacement_lowers_coherence(self):
        model = GroundState103Model()
        model.apply_gradient(3.0, 0.0, 4.0)  # magnitude 5.0 -> 0.08 * 5.0
        self.assertEqual(model.informational_coherence(), 0.6)

    def test_heavy_visible_armor_costs_a_fixed_penalty(self):
        light = GroundState103Model(armor_weight=1.5)
        heavy = GroundState103Model(armor_weight=1.6)
        self.assertEqual(light.informational_coherence(), 1.0)
        self.assertEqual(heavy.informational_coherence(), 0.8)

    def test_hidden_seam_with_armor_costs_more_than_heavy_visible_armor(self):
        visible = GroundState103Model(armor_weight=2.0)
        hidden = GroundState103Model(seam_visible=False, armor_weight=2.0)
        self.assertEqual(visible.informational_coherence(), 0.8)
        self.assertEqual(hidden.informational_coherence(), 0.45)
        self.assertLess(hidden.informational_coherence(), visible.informational_coherence())

    def test_hidden_seam_without_armor_costs_nothing(self):
        self.assertEqual(
            GroundState103Model(seam_visible=False).informational_coherence(), 1.0
        )

    def test_penalty_is_capped_and_never_negative(self):
        model = GroundState103Model(seam_visible=False, armor_weight=50.0)
        model.apply_gradient(1000.0, 1000.0, 1000.0)
        self.assertEqual(model.informational_coherence(), 0.15)
        self.assertGreaterEqual(model.informational_coherence(), 0.0)


class TestSeamAndReset(unittest.TestCase):
    def test_toggle_seam_updates_flag_and_logs(self):
        model = GroundState103Model()
        model.toggle_seam(False)
        self.assertFalse(model.seam_visible)
        record = model.history[-1]
        self.assertEqual(record.action, "toggle_seam")
        self.assertEqual(record.note, "Seam set to obscured.")
        model.toggle_seam(True, note="looked again")
        self.assertTrue(model.seam_visible)
        self.assertEqual(model.history[-1].note, "looked again")

    def test_reset_returns_to_ground_and_restores_seam_by_default(self):
        model = GroundState103Model()
        model.apply_gradient(2.0, 2.0, 2.0, armor_delta=1.0)
        model.toggle_seam(False)
        model.reset_to_ground()
        self.assertEqual(model.state.as_tuple(), (0.0, 0.0, 0.0))
        self.assertEqual(model.armor_weight, 0.0)
        self.assertTrue(model.seam_visible)
        self.assertEqual(model.informational_coherence(), 1.0)

    def test_reset_can_leave_the_seam_alone(self):
        model = GroundState103Model()
        model.toggle_seam(False)
        model.reset_to_ground(restore_seam=False)
        self.assertFalse(model.seam_visible)


class TestHistoryAndSnapshot(unittest.TestCase):
    def test_steps_are_sequential_and_match_spiral_turn(self):
        model = GroundState103Model()
        model.apply_gradient(1.0)
        model.toggle_seam(False)
        model.step_spiral()
        model.reset_to_ground()
        self.assertEqual([r.step for r in model.history], [0, 1, 2, 3, 4])
        self.assertEqual(model.spiral_turn, 4)
        self.assertEqual(
            [r.action for r in model.history],
            ["init_ground_state", "apply_gradient", "toggle_seam", "spiral_turn", "reset_to_ground"],
        )

    def test_armor_never_goes_negative(self):
        model = GroundState103Model(armor_weight=1.0)
        model.apply_gradient(armor_delta=-5.0)
        self.assertEqual(model.armor_weight, 0.0)

    def test_step_spiral_returns_plus_synthesis_of_the_damped_state(self):
        model = GroundState103Model()
        model.apply_gradient(3.0, 0.0, 6.0)
        plus = model.step_spiral(damping=0.5)
        self.assertEqual(model.state.as_tuple(), (1.5, 0.0, 3.0))
        self.assertEqual(plus, 1.5)

    def test_snapshot_reports_current_state(self):
        model = GroundState103Model()
        model.apply_gradient(3.0, 0.0, 4.0, armor_delta=0.5)
        snap = model.snapshot()
        self.assertEqual(snap["ground_coords"], (0, 0, 0))
        self.assertEqual(snap["state"], (3.0, 0.0, 4.0))
        self.assertEqual(snap["gradient_norm"], 5.0)
        self.assertEqual(snap["armor_weight"], 0.5)
        self.assertEqual(snap["history_count"], 2)

    def test_triad_vector_helpers(self):
        vec = TriadVector(3.0, 0.0, 4.0)
        self.assertEqual(vec.gradient_magnitude(), 5.0)
        self.assertAlmostEqual(vec.plus_synthesis(), 7.0 / 3.0)


if __name__ == "__main__":
    unittest.main()