import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from vector3 import Vector3
from soil import SoilPlot, SoilState
from rose import Rose, RoseStage, STAGE_DURATION
from actions import water_plot

class TestGrowth(unittest.TestCase):

    def setUp(self):
        self.plot = SoilPlot(index=0, position=Vector3(0,0,0))
        self.plot.transition_to(SoilState.PLANTED_DRY)
        self.rose = Rose(self.plot)

    def test_initial_state(self):
        self.assertEqual(self.rose.stage, RoseStage.SEED)
        self.assertEqual(self.rose.growth_progress, 0.0)

    def test_dry_soil_prevents_growth(self):
        self.assertEqual(self.plot.state, SoilState.PLANTED_DRY)
        self.rose.update(STAGE_DURATION * 5)

        self.assertEqual(self.rose.stage, RoseStage.SEED)
        self.assertEqual(self.rose.growth_progress, 0.0)

    def test_watered_soil_allows_growth(self):
        water_plot(self.plot)

        self.rose.update(STAGE_DURATION)
        self.assertEqual(self.rose.stage, RoseStage.SPROUT)

        # Verify it does not modify the soil state
        self.assertEqual(self.plot.state, SoilState.PLANTED_WATERED)

    def test_insufficient_time(self):
        water_plot(self.plot)

        self.rose.update(STAGE_DURATION - 0.1)
        self.assertEqual(self.rose.stage, RoseStage.SEED)
        self.assertAlmostEqual(self.rose.growth_progress, STAGE_DURATION - 0.1)

    def test_zero_delta(self):
        water_plot(self.plot)
        self.rose.update(0)
        self.assertEqual(self.rose.stage, RoseStage.SEED)

    def test_threshold_crossing_preserves_remainder(self):
        water_plot(self.plot)

        # Cross the threshold by 2.5 units
        self.rose.update(STAGE_DURATION + 2.5)

        self.assertEqual(self.rose.stage, RoseStage.SPROUT)
        self.assertAlmostEqual(self.rose.growth_progress, 2.5)

    def test_large_delta_multi_stage_progression(self):
        water_plot(self.plot)

        # Provide exactly enough time for 3 full stages
        self.rose.update(STAGE_DURATION * 3)

        # SEED -> SPROUT -> YOUNG_PLANT -> BUD
        self.assertEqual(self.rose.stage, RoseStage.BUD)
        self.assertEqual(self.rose.growth_progress, 0.0)

    def test_bloom_behavior(self):
        water_plot(self.plot)

        # Provide enough time to blast past BLOOM
        self.rose.update(STAGE_DURATION * 10)

        self.assertEqual(self.rose.stage, RoseStage.BLOOM)
        self.assertEqual(self.rose.growth_progress, 0.0)

        # Providing even more time remains safe and unchanged
        self.rose.update(STAGE_DURATION)
        self.assertEqual(self.rose.stage, RoseStage.BLOOM)

    def test_independence(self):
        plot2 = SoilPlot(index=1, position=Vector3(1,0,0))
        plot2.transition_to(SoilState.PLANTED_DRY)
        rose2 = Rose(plot2)

        water_plot(self.plot) # plot 1 is watered, plot 2 is dry

        self.rose.update(STAGE_DURATION)
        rose2.update(STAGE_DURATION)

        self.assertEqual(self.rose.stage, RoseStage.SPROUT)
        self.assertEqual(rose2.stage, RoseStage.SEED) # Rose 2 was dry, no growth

if __name__ == '__main__':
    unittest.main()
