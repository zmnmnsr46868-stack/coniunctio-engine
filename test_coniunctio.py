import os
import json
import unittest
from coniunctio_engine import ConiunctioEngine, GroundState, MagneticDyad, Witness
from analyzer import load_trajectory


class TestConiunctioEngine(unittest.TestCase):

    def test_ground_state_initialization(self):
        gs = GroundState()
        self.assertEqual(gs.coords, [0.0, 0.0, 0.0])

    def test_magnetic_dyad_tension(self):
        dyad = MagneticDyad([0.0, 0.0, 0.0])
        tension = dyad.calculate_tension([3.0, 4.0, 0.0])
        self.assertAlmostEqual(tension, 5.0)

    def test_witness_coherence(self):
        witness = Witness()
        coherence = witness.evaluate(0.0)
        self.assertEqual(coherence, 1.0)
        
        coherence_high = witness.evaluate(1.0)
        self.assertAlmostEqual(coherence_high, 1.0 / 2.0)

    def test_engine_step_and_spiral(self):
        engine = ConiunctioEngine()
        rec = engine.step(0.2, 0.25, 0.15)
        
        self.assertEqual(rec["cycle"], 1)
        self.assertEqual(rec["state"], "SPIRAL")
        self.assertGreater(rec["coherence"], 0.618)

    def test_engine_ground_reset(self):
        engine = ConiunctioEngine()
        # High input values create massive tension, dropping coherence below 0.618
        rec = engine.step(2.0, 2.0, 2.0)
        
        self.assertEqual(rec["state"], "GROUND_RESET")
        self.assertEqual(rec["spiral_depth"], 0)

    def test_analyzer_integration(self):
        """Verify that analyzer can load and parse exported session history."""
        engine = ConiunctioEngine()
        engine.step(0.2, 0.25, 0.15)
        engine.step(0.25, 0.3, 0.2)

        temp_filename = "trajectory_test_ci.json"
        with open(temp_filename, "w", encoding="utf-8") as f:
            json.dump(engine.history, f)

        try:
            path, history = load_trajectory(temp_filename)
            self.assertEqual(path, temp_filename)
            self.assertEqual(len(history), 2)
            self.assertEqual(history[0]["cycle"], 1)
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)


if __name__ == "__main__":
    unittest.main()
