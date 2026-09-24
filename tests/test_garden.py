import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from vector3 import Vector3
from garden import Garden

class TestGarden(unittest.TestCase):

    def setUp(self):
        # 2x2 grid, each cell size 2.0, starting at (0, 0, 0)
        self.garden = Garden(cols=2, rows=2, cell_size=2.0, origin=Vector3(0, 0, 0))

    def test_garden_construction(self):
        self.assertEqual(self.garden.cols, 2)
        self.assertEqual(self.garden.rows, 2)
        self.assertEqual(self.garden.cell_size, 2.0)
        self.assertEqual(self.garden.origin, Vector3(0, 0, 0))

    def test_cell_count(self):
        self.assertEqual(len(self.garden.cell_positions), 4)

    def test_deterministic_cell_positions(self):
        # Cell 0 (r=0, c=0): Center should be at x=1, y=0, z=1
        pos_0 = self.garden.cell_positions[0]
        self.assertEqual(pos_0, Vector3(1, 0, 1))

        # Cell 1 (r=0, c=1): Center should be at x=3, y=0, z=1
        pos_1 = self.garden.cell_positions[1]
        self.assertEqual(pos_1, Vector3(3, 0, 1))

        # Cell 2 (r=1, c=0): Center should be at x=1, y=0, z=3
        pos_2 = self.garden.cell_positions[2]
        self.assertEqual(pos_2, Vector3(1, 0, 3))

        # Cell 3 (r=1, c=1): Center should be at x=3, y=0, z=3
        pos_3 = self.garden.cell_positions[3]
        self.assertEqual(pos_3, Vector3(3, 0, 3))

    def test_mesh_generation(self):
        # The base mesh is now a continuous 4-vertex quad covering the whole garden
        mesh = self.garden.mesh
        self.assertIsNotNone(mesh)
        self.assertEqual(len(mesh.vertices), 4)
        self.assertEqual(len(mesh.faces), 2)

        # Check first face bounds
        f0 = mesh.faces[0]
        self.assertEqual(len(f0), 3) # Must be a triangle

        # Verify deterministic geometry bounds for the base ground
        self.assertEqual(mesh.vertices[0], Vector3(0, 0, 0))
        self.assertEqual(mesh.vertices[1], Vector3(4, 0, 0))
        self.assertEqual(mesh.vertices[2], Vector3(0, 0, 4))
        self.assertEqual(mesh.vertices[3], Vector3(4, 0, 4))

    def test_plot_mesh_generation(self):
        # Specific plots now generate slightly padded meshes
        plot_mesh = self.garden.get_plot_mesh(0)
        self.assertEqual(len(plot_mesh.vertices), 4)
        self.assertEqual(len(plot_mesh.faces), 2)

        # Should be padded slightly inward from (0,0) and (2,2)
        v = plot_mesh.vertices[0]
        self.assertAlmostEqual(v.x, 0.1) # 2.0 * 0.05
        self.assertAlmostEqual(v.z, 0.1)

if __name__ == '__main__':
    unittest.main()
