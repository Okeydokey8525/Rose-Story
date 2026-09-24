import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from vector3 import Vector3
from camera import Camera

class TestCamera(unittest.TestCase):

    def setUp(self):
        # Default 800x600 camera looking at +Z
        self.camera = Camera(
            position=Vector3(0, 0, 0),
            fov=90.0,
            screen_width=800,
            screen_height=600,
            near=0.1
        )

    def test_construction(self):
        cam = Camera()
        self.assertEqual(cam.position, Vector3(0, 0, 0))
        self.assertEqual(cam.fov, 90.0)
        self.assertEqual(cam.screen_width, 800)
        self.assertEqual(cam.screen_height, 600)

    def test_center_projection(self):
        # A point directly in front of the camera (0, 0, 10)
        point = Vector3(0, 0, 10)
        proj = self.camera.project(point)
        self.assertIsNotNone(proj)

        # Should project exactly to the center of the screen
        self.assertAlmostEqual(proj[0], 400.0)
        self.assertAlmostEqual(proj[1], 300.0)

    def test_directional_projection(self):
        # Point to the right (positive X)
        pt_right = Vector3(5, 0, 10)
        proj_right = self.camera.project(pt_right)
        self.assertIsNotNone(proj_right)
        self.assertGreater(proj_right[0], 400.0) # Should be to the right of center
        self.assertAlmostEqual(proj_right[1], 300.0) # Still vertically centered

        # Point to the left (negative X)
        pt_left = Vector3(-5, 0, 10)
        proj_left = self.camera.project(pt_left)
        self.assertIsNotNone(proj_left)
        self.assertLess(proj_left[0], 400.0) # Should be to the left of center

        # Point down (positive Y in screen space)
        pt_down = Vector3(0, 5, 10)
        proj_down = self.camera.project(pt_down)
        self.assertIsNotNone(proj_down)
        self.assertGreater(proj_down[1], 300.0) # Should be below center

        # Point up (negative Y in screen space)
        pt_up = Vector3(0, -5, 10)
        proj_up = self.camera.project(pt_up)
        self.assertIsNotNone(proj_up)
        self.assertLess(proj_up[1], 300.0) # Should be above center

    def test_perspective_distance(self):
        # Point at z=10
        pt_close = Vector3(5, 0, 10)
        proj_close = self.camera.project(pt_close)

        # Same point but further away at z=20
        pt_far = Vector3(5, 0, 20)
        proj_far = self.camera.project(pt_far)

        self.assertIsNotNone(proj_close)
        self.assertIsNotNone(proj_far)

        # The further point should project closer to the center (400)
        dist_close = abs(proj_close[0] - 400.0)
        dist_far = abs(proj_far[0] - 400.0)

        self.assertLess(dist_far, dist_close)

    def test_behind_camera(self):
        # Point behind the camera
        pt_behind = Vector3(0, 0, -5)
        proj_behind = self.camera.project(pt_behind)

        # Should return None (culled)
        self.assertIsNone(proj_behind)

    def test_zero_depth(self):
        # Point exactly on the camera origin or inside the near clipping plane
        pt_zero = Vector3(0, 0, 0)
        pt_near = Vector3(0, 0, 0.05) # less than default near=0.1

        self.assertIsNone(self.camera.project(pt_zero))
        self.assertIsNone(self.camera.project(pt_near))

    def test_camera_translation(self):
        # Move camera to the right by 5
        self.camera.position = Vector3(5, 0, 0)

        # Projecting a point that is also at x=5 should result in center screen X
        pt = Vector3(5, 0, 10)
        proj = self.camera.project(pt)

        self.assertIsNotNone(proj)
        self.assertAlmostEqual(proj[0], 400.0)

if __name__ == '__main__':
    unittest.main()
