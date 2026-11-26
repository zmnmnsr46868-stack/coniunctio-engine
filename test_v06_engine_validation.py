import math
import unittest

from coniunctio_v06 import AdaptiveConiunctioEngine


class TestEngineParameterValidation(unittest.TestCase):
    def test_non_positive_or_non_finite_threshold_rejected(self):
        for bad in (0.0, -1.0, float("nan"), float("inf"), float("-inf")):
            with self.subTest(threshold=bad):
                with self.assertRaises(ValueError):
                    AdaptiveConiunctioEngine(threshold=bad)

    def test_non_finite_parameters_rejected(self):
        for name in ("adapt_rate", "alpha", "beta", "homeostatic_drift"):
            for bad in (float("nan"), float("inf")):
                with self.subTest(param=name, value=bad):
                    with self.assertRaises(ValueError):
                        AdaptiveConiunctioEngine(**{name: bad})

    def test_existing_sign_rules_still_enforced(self):
        with self.assertRaises(ValueError):
            AdaptiveConiunctioEngine(adapt_rate=0.0)
        with self.assertRaises(ValueError):
            AdaptiveConiunctioEngine(alpha=-0.1)
        with self.assertRaises(ValueError):
            AdaptiveConiunctioEngine(homeostatic_drift=-0.1)

    def test_small_positive_threshold_survives_sustained_friction(self):
        engine = AdaptiveConiunctioEngine(threshold=0.01)
        engine.dyad.set_tension(3.0, -3.0)
        for _ in range(8):
            engine.step()
        self.assertTrue(math.isfinite(engine.ground.threshold))
        self.assertGreater(engine.ground.threshold, 0.01)

    def test_threshold_breathes_out_and_back(self):
        engine = AdaptiveConiunctioEngine(threshold=0.5)
        engine.dyad.set_tension(5.0, -5.0)
        for _ in range(6):
            engine.step()
        expanded = engine.ground.threshold
        self.assertGreater(expanded, 0.5)
        engine.dyad.set_tension(0.0, 0.0)
        for _ in range(int(expanded / engine.homeostatic_drift) + 5):
            engine.step()
        self.assertAlmostEqual(engine.ground.threshold, 0.5)
        self.assertEqual(engine.current_phase, "INTEGRATION")


if __name__ == "__main__":
    unittest.main()