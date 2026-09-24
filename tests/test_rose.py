import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from vector3 import Vector3
from soil import SoilPlot, SoilState
from rose import Rose, RoseStage, RoseTransitionError

class TestRose(unittest.TestCase):

    def setUp(self):
        # Create a mock plot for testing
        self.plot = SoilPlot(index=42, position=Vector3(10, 0, -10))
        # Ensure plot has some valid game state independent of the Rose
        self.plot.transition_to(SoilState.PLANTED_DRY)

        self.rose = Rose(self.plot)

    def test_rose_creation(self):
        self.assertEqual(self.rose.plot, self.plot)
        self.assertEqual(self.rose.plot.index, 42)

        # Position must match exactly
        self.assertEqual(self.rose.position, Vector3(10, 0, -10))

        # Initial stage must be Seed
        self.assertEqual(self.rose.stage, RoseStage.SEED)

    def test_lifecycle_progression(self):
        # Seed -> Sprout
        self.rose.grow()
        self.assertEqual(self.rose.stage, RoseStage.SPROUT)

        # Sprout -> Young Plant
        self.rose.grow()
        self.assertEqual(self.rose.stage, RoseStage.YOUNG_PLANT)

        # Young Plant -> Bud
        self.rose.grow()
        self.assertEqual(self.rose.stage, RoseStage.BUD)

        # Bud -> Bloom
        self.rose.grow()
        self.assertEqual(self.rose.stage, RoseStage.BLOOM)

    def test_invalid_transitions(self):
        # The grow() method strictly enforces step-by-step.
        # But we also verify it doesn't allow growing past Bloom.
        self.rose.stage = RoseStage.BLOOM
        with self.assertRaises(RoseTransitionError):
            self.rose.grow()

        # Reversing stages is structurally impossible via the standard grow() API
        # but if we manually forced it, ensure grow() wouldn't somehow loop.
        self.assertEqual(self.rose.stage, RoseStage.BLOOM)

    def test_independence(self):
        plot1 = SoilPlot(index=1, position=Vector3(0,0,0))
        plot2 = SoilPlot(index=2, position=Vector3(2,0,0))
        # Strictly follow the Soil state machine for testing setup
        plot1.transition_to(SoilState.PLANTED_DRY)
        plot2.transition_to(SoilState.PLANTED_DRY)
        plot2.transition_to(SoilState.PLANTED_WATERED)

        rose1 = Rose(plot1)
        rose2 = Rose(plot2)

        rose1.grow() # Sprout
        rose1.grow() # Young Plant

        # Advancing rose1 doesn't affect rose2
        self.assertEqual(rose1.stage, RoseStage.YOUNG_PLANT)
        self.assertEqual(rose2.stage, RoseStage.SEED)

        # Advancing rose1 doesn't modify its SoilPlot state (independence verification)
        self.assertEqual(rose1.plot.state, SoilState.PLANTED_DRY)
        self.assertEqual(rose2.plot.state, SoilState.PLANTED_WATERED)

if __name__ == '__main__':
    unittest.main()
