import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from vector3 import Vector3
from soil import SoilPlot, SoilState, SoilTransitionError
from rose import Rose, RoseStage, STAGE_DURATION
from actions import water_plot, mark_harvestable, harvest_plot, HarvestEligibilityError

class TestHarvest(unittest.TestCase):

    def setUp(self):
        self.plot = SoilPlot(index=0, position=Vector3(0,0,0))
        self.plot.transition_to(SoilState.PLANTED_DRY)
        self.rose = Rose(self.plot)
        water_plot(self.plot)

    def _grow_rose_to(self, target_stage: RoseStage):
        while self.rose.stage != target_stage:
            self.rose.update(STAGE_DURATION)

    def test_harvest_eligibility_valid(self):
        self._grow_rose_to(RoseStage.BLOOM)
        mark_harvestable(self.rose)
        self.assertEqual(self.plot.state, SoilState.HARVESTABLE)

    def test_harvest_eligibility_invalid_stages(self):
        for stage in [RoseStage.SEED, RoseStage.SPROUT, RoseStage.YOUNG_PLANT, RoseStage.BUD]:
            self.setUp() # reset
            self._grow_rose_to(stage)

            with self.assertRaises(HarvestEligibilityError):
                mark_harvestable(self.rose)

            self.assertNotEqual(self.plot.state, SoilState.HARVESTABLE)

    def test_harvest_action_valid(self):
        self._grow_rose_to(RoseStage.BLOOM)
        mark_harvestable(self.rose)

        harvest_plot(self.plot)
        self.assertEqual(self.plot.state, SoilState.EMPTY)
        # Rose state is not arbitrarily destroyed or modified into an undefined state
        self.assertEqual(self.rose.stage, RoseStage.BLOOM)

    def test_harvest_action_invalid_states(self):
        # Cannot harvest a DRY plot
        plot_dry = SoilPlot(index=1, position=Vector3(0,0,0))
        plot_dry.transition_to(SoilState.PLANTED_DRY)
        with self.assertRaises(SoilTransitionError):
            harvest_plot(plot_dry)

        # Cannot harvest a WATERED plot
        with self.assertRaises(SoilTransitionError):
            harvest_plot(self.plot)

        # Cannot harvest an EMPTY plot
        plot_empty = SoilPlot(index=2, position=Vector3(0,0,0))
        with self.assertRaises(SoilTransitionError):
            harvest_plot(plot_empty)

    def test_harvest_independence(self):
        # Set up a second plot that is watered but not blooming
        plot2 = SoilPlot(index=1, position=Vector3(1,0,0))
        plot2.transition_to(SoilState.PLANTED_DRY)
        rose2 = Rose(plot2)
        water_plot(plot2)

        # Grow first rose to BLOOM and harvest
        self._grow_rose_to(RoseStage.BLOOM)
        mark_harvestable(self.rose)
        harvest_plot(self.plot)

        # Verify first plot is empty
        self.assertEqual(self.plot.state, SoilState.EMPTY)

        # Verify second plot and rose are completely untouched
        self.assertEqual(plot2.state, SoilState.PLANTED_WATERED)
        self.assertEqual(rose2.stage, RoseStage.SEED)

if __name__ == '__main__':
    unittest.main()
