import unittest

from ground_state_103 import GroundState103Model, TriadVector

NAN, INF = float("nan"), float("inf")


class TestNonFiniteRejection(unittest.TestCase):
    def test_triad_vector_rejects_non_finite(self):
        for field in ("thought", "memory", "instinct"):
            for bad in (NAN, INF, -INF):
                with self.subTest(field=field, value=bad):
                    with self.assertRaises(ValueError):
                        TriadVector(**{field: bad})

    def test_apply_gradient_rejects_non_finite_and_changes_nothing(self):
        for name in ("d_thought", "d_memory", "d_instinct", "armor_delta"):
            for bad in (NAN, INF, -INF):
                with self.subTest(param=name, value=bad):
                    model = GroundState103Model()
                    model.apply_gradient(1.0, 2.0, 3.0, armor_delta=0.5)
                    before = (model.snapshot(), len(model.history))
                    with self.assertRaises(ValueError):
                        model.apply_gradient(**{name: bad})
                    self.assertEqual((model.snapshot(), len(model.history)), before)

    def test_model_rejects_bad_armor_at_construction(self):
        for bad in (NAN, INF, -INF, -0.1):
            with self.subTest(armor_weight=bad):
                with self.assertRaises(ValueError):
                    GroundState103Model(armor_weight=bad)

    def test_model_still_usable_after_a_rejected_call(self):
        model = GroundState103Model()
        with self.assertRaises(ValueError):
            model.apply_gradient(d_thought=NAN)
        model.apply_gradient(3.0, 0.0, 4.0)
        self.assertEqual(model.snapshot()["gradient_norm"], 5.0)
        model.reset_to_ground()
        self.assertEqual(model.snapshot()["gradient_norm"], 0.0)


class TestInitialRecord(unittest.TestCase):
    def test_default_start_is_unchanged(self):
        model = GroundState103Model()
        record = model.history[0]
        self.assertEqual(record.coherence_index, 1.0)
        self.assertEqual(
            record.note, "Calibrated at [0, 0, 0]; seam visible and open to revision."
        )

    def test_initial_record_matches_real_coherence_when_not_at_ground(self):
        model = GroundState103Model(
            seam_visible=False, armor_weight=2.0, state=TriadVector(3.0, 0.0, 0.0)
        )
        record = model.history[0]
        self.assertEqual(record.coherence_index, model.informational_coherence())
        self.assertLess(record.coherence_index, 1.0)
        self.assertIn("away from [0, 0, 0]", record.note)


class TestValidBehaviourUnchanged(unittest.TestCase):
    def test_gradient_then_spiral_back_toward_ground(self):
        model = GroundState103Model()
        model.apply_gradient(3.0, 0.0, 4.0, armor_delta=2.0)
        self.assertEqual(model.snapshot()["gradient_norm"], 5.0)
        self.assertEqual(model.snapshot()["coherence_index"], 0.4)
        for _ in range(10):
            model.step_spiral()
        snap = model.snapshot()
        self.assertEqual(snap["gradient_norm"], 0.984372)
        self.assertEqual(snap["coherence_index"], 0.92125)
        self.assertEqual(snap["history_count"], 12)

    def test_damping_bounds_still_enforced(self):
        model = GroundState103Model()
        for bad in (-0.1, 1.1, NAN):
            with self.subTest(damping=bad):
                with self.assertRaises(ValueError):
                    model.step_spiral(damping=bad)


if __name__ == "__main__":
    unittest.main()
