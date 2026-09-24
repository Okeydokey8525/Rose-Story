import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pygame
from vector3 import Vector3
from camera import Camera
from mesh import Mesh
from renderer import Renderer

class TestRenderer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize pygame for headless surface creation
        pygame.init()
        # Ensure we just use a software surface for tests
        pygame.display.set_mode((800, 600), pygame.HIDDEN)

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.surface = pygame.Surface((800, 600))
        self.camera = Camera(screen_width=800, screen_height=600)
        self.renderer = Renderer(self.camera, self.surface)

    def test_mesh_construction(self):
        v = [Vector3(0, 0, 1), Vector3(1, 0, 1), Vector3(0, 1, 1)]
        f = [(0, 1, 2)]
        m = Mesh(vertices=v, faces=f)

        self.assertEqual(len(m.vertices), 3)
        self.assertEqual(len(m.faces), 1)
        self.assertEqual(m.faces[0], (0, 1, 2))

    def test_renderer_valid_triangle(self):
        # Triangle in front of camera
        mesh = Mesh(
            vertices=[Vector3(0, -1, 5), Vector3(-1, 1, 5), Vector3(1, 1, 5)],
            faces=[(0, 1, 2)]
        )

        # Draw on black surface
        self.surface.fill((0, 0, 0))
        self.renderer.render_mesh(mesh, color=(255, 0, 0))

        # Check if the surface is no longer completely black.
        # The center point of the triangle (0, 0, 5) projects exactly to the center of the screen (400, 300)
        # Because we draw a red triangle, the center pixel should be red.
        pixel_color = self.surface.get_at((400, 300))
        self.assertEqual(pixel_color.r, 255)
        self.assertEqual(pixel_color.g, 0)
        self.assertEqual(pixel_color.b, 0)

    def test_renderer_clipped_triangle(self):
        # Triangle where one vertex is behind the camera (Z = -5)
        mesh = Mesh(
            vertices=[Vector3(0, 0, -5), Vector3(-1, 1, 5), Vector3(1, 1, 5)],
            faces=[(0, 1, 2)]
        )

        # Draw on black surface
        self.surface.fill((0, 0, 0))
        # This shouldn't crash
        self.renderer.render_mesh(mesh, color=(255, 0, 0))

        # Because it's clipped, the surface should remain black (assuming our simple culling drops the whole face)
        pixel_color = self.surface.get_at((400, 300))
        self.assertEqual(pixel_color.r, 0)

    def test_renderer_invalid_face_indices(self):
        # Face asks for index 5, but there are only 3 vertices
        mesh = Mesh(
            vertices=[Vector3(0, -1, 5), Vector3(-1, 1, 5), Vector3(1, 1, 5)],
            faces=[(0, 1, 5)]
        )

        # Should not crash
        self.renderer.render_mesh(mesh)

if __name__ == '__main__':
    unittest.main()
