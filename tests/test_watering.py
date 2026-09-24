import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from vector3 import Vector3
from garden import Garden
from soil import SoilGrid, SoilPlot, SoilState, SoilTransitionError
from rose import Rose, RoseStage
from actions import water_plot, water_plot_by_index, water_plot_by_coord

class TestWatering(unittest.TestCase):

    def setUp(self):
        # 2x2 spatial grid + logical soil grid
        self.garden = Garden(cols=2, rows=2, cell_size=2.0)
        self.grid = SoilGrid(self.garden)

    def test_basic_watering(self):
        plot = self.grid.get_plot_by_index(0)
        # Setup: Must be planted to be valid for watering
        plot.transition_to(SoilState.PLANTED_DRY)

        water_plot(plot)
        self.assertEqual(plot.state, SoilState.PLANTED_WATERED)

    def test_invalid_watering_empty(self):
        plot = self.grid.get_plot_by_index(0)
        self.assertEqual(plot.state, SoilState.EMPTY)

        with self.assertRaises(SoilTransitionError):
            water_plot(plot)
        # Ensure state remained unchanged
        self.assertEqual(plot.state, SoilState.EMPTY)

    def test_invalid_watering_already_watered(self):
        plot = self.grid.get_plot_by_index(0)
        plot.transition_to(SoilState.PLANTED_DRY)
        plot.transition_to(SoilState.PLANTED_WATERED)

        with self.assertRaises(SoilTransitionError):
            water_plot(plot) # Cannot water again
        self.assertEqual(plot.state, SoilState.PLANTED_WATERED)

    def test_invalid_watering_harvestable(self):
        plot = self.grid.get_plot_by_index(0)
        plot.transition_to(SoilState.PLANTED_DRY)
        plot.transition_to(SoilState.PLANTED_WATERED)
        plot.transition_to(SoilState.HARVESTABLE)

        with self.assertRaises(SoilTransitionError):
            water_plot(plot)
        self.assertEqual(plot.state, SoilState.HARVESTABLE)

    def _test_rose_stage_independence(self, stage: RoseStage):
        plot = self.grid.get_plot_by_index(0)
        plot.transition_to(SoilState.PLANTED_DRY)

        rose = Rose(plot)
        # Advance rose manually to the target stage without triggering soil state
        while rose.stage != stage:
            rose.grow()

        # Water the plot
        water_plot(plot)

        # Verify the soil state changed, but the rose stage did NOT
        self.assertEqual(plot.state, SoilState.PLANTED_WATERED)
        self.assertEqual(rose.stage, stage)

    def test_rose_independence(self):
        # Explicitly verify for all possible Rose stages
        for stage in RoseStage:
            self.setUp() # Reset grid
            self._test_rose_stage_independence(stage)

    def test_plot_independence(self):
        plot0 = self.grid.get_plot_by_index(0)
        plot1 = self.grid.get_plot_by_index(1)

        plot0.transition_to(SoilState.PLANTED_DRY)
        plot1.transition_to(SoilState.PLANTED_DRY)

        water_plot(plot0)

        # Plot 0 should be watered, Plot 1 should remain dry
        self.assertEqual(plot0.state, SoilState.PLANTED_WATERED)
        self.assertEqual(plot1.state, SoilState.PLANTED_DRY)

    def test_grid_integration(self):
        # Setup plots
        plot_index = self.grid.get_plot_by_index(2)
        plot_coord = self.grid.get_plot(1, 1) # index 3

        plot_index.transition_to(SoilState.PLANTED_DRY)
        plot_coord.transition_to(SoilState.PLANTED_DRY)

        # Test helper functions
        water_plot_by_index(self.grid, 2)
        water_plot_by_coord(self.grid, 1, 1)

        self.assertEqual(plot_index.state, SoilState.PLANTED_WATERED)
        self.assertEqual(plot_coord.state, SoilState.PLANTED_WATERED)

if __name__ == '__main__':
    unittest.main()
