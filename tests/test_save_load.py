import unittest
import sys
import os
import tempfile
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from vector3 import Vector3
from garden import Garden
from soil import SoilGrid, SoilState
from rose import Rose, RoseStage, STAGE_DURATION
from save_load import save_game, load_game, SaveLoadError

class TestSaveLoad(unittest.TestCase):

    def setUp(self):
        self.garden = Garden(cols=2, rows=2, cell_size=2.0)
        self.grid = SoilGrid(self.garden)

        # We will use a temp directory to avoid polluting the repo
        self.temp_dir = tempfile.TemporaryDirectory()
        self.save_path = os.path.join(self.temp_dir.name, "test_save.json")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_empty_grid_save_load(self):
        save_game(self.save_path, self.grid, [])
        self.assertTrue(os.path.exists(self.save_path))

        loaded_grid, loaded_roses = load_game(self.save_path, self.garden)
        self.assertEqual(len(loaded_grid.plots), 4)
        self.assertEqual(len(loaded_roses), 0)
        for plot in loaded_grid.plots:
            self.assertEqual(plot.state, SoilState.EMPTY)

    def test_complex_state_save_load(self):
        # Set up a complex state
        # Plot 0: Planted Watered, Sprout
        p0 = self.grid.get_plot_by_index(0)
        p0.transition_to(SoilState.PLANTED_DRY)
        p0.transition_to(SoilState.PLANTED_WATERED)
        r0 = Rose(p0)
        r0.update(STAGE_DURATION + 3.5) # Promotes to SPROUT, leaves 3.5 progress

        # Plot 2: Harvestable, Bloom
        p2 = self.grid.get_plot_by_index(2)
        p2.transition_to(SoilState.PLANTED_DRY)
        p2.transition_to(SoilState.PLANTED_WATERED)
        r2 = Rose(p2)
        r2.update(STAGE_DURATION * 10) # Promotes to BLOOM
        p2.transition_to(SoilState.HARVESTABLE) # mark harvestable

        roses = [r0, r2]

        # Capture original state to verify non-mutation
        orig_p0_state = p0.state
        orig_r0_stage = r0.stage

        # Save
        save_game(self.save_path, self.grid, roses)

        # Ensure original state was completely untouched
        self.assertEqual(p0.state, orig_p0_state)
        self.assertEqual(r0.stage, orig_r0_stage)

        # Load
        loaded_grid, loaded_roses = load_game(self.save_path, self.garden)

        # Verify Plots
        lp0 = loaded_grid.get_plot_by_index(0)
        lp2 = loaded_grid.get_plot_by_index(2)
        self.assertEqual(lp0.state, SoilState.PLANTED_WATERED)
        self.assertEqual(lp2.state, SoilState.HARVESTABLE)

        # Verify Roses
        self.assertEqual(len(loaded_roses), 2)

        lr0 = next(r for r in loaded_roses if r.plot.index == 0)
        lr2 = next(r for r in loaded_roses if r.plot.index == 2)

        self.assertEqual(lr0.stage, RoseStage.SPROUT)
        self.assertAlmostEqual(lr0.growth_progress, 3.5)
        self.assertEqual(lr0.plot, lp0) # Ensures association points to the correct new grid plot

        self.assertEqual(lr2.stage, RoseStage.BLOOM)
        self.assertEqual(lr2.growth_progress, 0.0)
        self.assertEqual(lr2.plot, lp2)

    def test_error_missing_file(self):
        with self.assertRaises(SaveLoadError):
            load_game("does_not_exist.json", self.garden)

    def test_error_malformed_json(self):
        with open(self.save_path, 'w') as f:
            f.write("{invalid_json: 123")

        with self.assertRaises(SaveLoadError):
            load_game(self.save_path, self.garden)

    def test_error_unsupported_version(self):
        with open(self.save_path, 'w') as f:
            json.dump({"version": 9999}, f)

        with self.assertRaises(SaveLoadError):
            load_game(self.save_path, self.garden)

    def test_error_invalid_soil_state(self):
        data = {
            "version": 1,
            "plots": [{"index": 0, "state": "INVALID_STATE"}],
            "roses": []
        }
        with open(self.save_path, 'w') as f:
            json.dump(data, f)

        # We also need length to match the garden to pass the geometry check
        # Let's adjust the data to pass length check but fail the enum parse
        data["plots"] = [{"index": i, "state": "EMPTY"} for i in range(4)]
        data["plots"][0]["state"] = "INVALID_STATE"

        with open(self.save_path, 'w') as f:
            json.dump(data, f)

        with self.assertRaises(SaveLoadError):
            load_game(self.save_path, self.garden)

    def test_error_invalid_rose_stage(self):
        data = {
            "version": 1,
            "plots": [{"index": i, "state": "EMPTY"} for i in range(4)],
            "roses": [{"plot_index": 0, "stage": "SUPER_BLOOM", "growth_progress": 0.0}]
        }
        with open(self.save_path, 'w') as f:
            json.dump(data, f)

        with self.assertRaises(SaveLoadError):
            load_game(self.save_path, self.garden)

    def test_error_invalid_plot_association(self):
        data = {
            "version": 1,
            "plots": [{"index": i, "state": "EMPTY"} for i in range(4)],
            "roses": [{"plot_index": 999, "stage": "SEED", "growth_progress": 0.0}]
        }
        with open(self.save_path, 'w') as f:
            json.dump(data, f)

        with self.assertRaises(SaveLoadError):
            load_game(self.save_path, self.garden)

if __name__ == '__main__':
    unittest.main()
