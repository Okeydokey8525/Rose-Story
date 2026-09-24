import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from vector3 import Vector3
from garden import Garden
from soil import SoilGrid, SoilPlot, SoilState, SoilTransitionError

class TestSoilGrid(unittest.TestCase):
    def setUp(self):
        # 2x2 grid
        self.garden = Garden(cols=2, rows=2, cell_size=2.0, origin=Vector3(0,0,0))
        self.soil_grid = SoilGrid(self.garden)

    def test_grid_initialization(self):
        self.assertEqual(len(self.soil_grid.plots), 4)

        # New plots start as Empty
        for plot in self.soil_grid.plots:
            self.assertEqual(plot.state, SoilState.EMPTY)

    def test_plot_ordering_and_position(self):
        # Index 0 (r=0, c=0)
        p0 = self.soil_grid.get_plot_by_index(0)
        self.assertEqual(p0.position, self.garden.cell_positions[0])

        # Index 3 (r=1, c=1)
        p3 = self.soil_grid.get_plot(row=1, col=1)
        self.assertEqual(p3.position, self.garden.cell_positions[3])
        self.assertEqual(p3.index, 3)

    def test_valid_state_transitions(self):
        plot = self.soil_grid.get_plot_by_index(0)

        # Empty -> Planted Dry
        plot.transition_to(SoilState.PLANTED_DRY)
        self.assertEqual(plot.state, SoilState.PLANTED_DRY)

        # Planted Dry -> Planted Watered
        plot.transition_to(SoilState.PLANTED_WATERED)
        self.assertEqual(plot.state, SoilState.PLANTED_WATERED)

        # Planted Watered -> Harvestable
        plot.transition_to(SoilState.HARVESTABLE)
        self.assertEqual(plot.state, SoilState.HARVESTABLE)

        # Harvestable -> Empty
        plot.transition_to(SoilState.EMPTY)
        self.assertEqual(plot.state, SoilState.EMPTY)

    def test_invalid_state_transitions(self):
        plot = self.soil_grid.get_plot_by_index(0)
        self.assertEqual(plot.state, SoilState.EMPTY)

        # Cannot jump from Empty to Watered or Harvestable
        with self.assertRaises(SoilTransitionError):
            plot.transition_to(SoilState.PLANTED_WATERED)

        with self.assertRaises(SoilTransitionError):
            plot.transition_to(SoilState.HARVESTABLE)

        # Ensure state remained unchanged
        self.assertEqual(plot.state, SoilState.EMPTY)

    def test_plot_independence(self):
        plot_a = self.soil_grid.get_plot_by_index(0)
        plot_b = self.soil_grid.get_plot_by_index(1)

        plot_a.transition_to(SoilState.PLANTED_DRY)

        self.assertEqual(plot_a.state, SoilState.PLANTED_DRY)
        self.assertEqual(plot_b.state, SoilState.EMPTY) # B should remain unchanged

    def test_out_of_bounds_retrieval(self):
        with self.assertRaises(IndexError):
            self.soil_grid.get_plot_by_index(5)

        with self.assertRaises(IndexError):
            self.soil_grid.get_plot(row=5, col=0)

if __name__ == '__main__':
    unittest.main()
