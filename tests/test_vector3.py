import unittest
import math

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from vector3 import Vector3

class TestVector3(unittest.TestCase):

    def test_construction(self):
        v = Vector3(1.0, 2.5, -3.0)
        self.assertEqual(v.x, 1.0)
        self.assertEqual(v.y, 2.5)
        self.assertEqual(v.z, -3.0)

        # Default construction
        v0 = Vector3()
        self.assertEqual(v0.x, 0.0)
        self.assertEqual(v0.y, 0.0)
        self.assertEqual(v0.z, 0.0)

    def test_addition(self):
        v1 = Vector3(1, 2, 3)
        v2 = Vector3(-1, 0, 5)
        v3 = v1 + v2
        self.assertEqual(v3, Vector3(0, 2, 8))

    def test_subtraction(self):
        v1 = Vector3(1, 2, 3)
        v2 = Vector3(3, 1, -1)
        v3 = v1 - v2
        self.assertEqual(v3, Vector3(-2, 1, 4))

    def test_scalar_multiplication(self):
        v = Vector3(2, -3, 4)
        v_scaled1 = v * 2.5
        self.assertEqual(v_scaled1, Vector3(5.0, -7.5, 10.0))

        # Test right multiplication
        v_scaled2 = 3 * v
        self.assertEqual(v_scaled2, Vector3(6, -9, 12))

    def test_scalar_division(self):
        v = Vector3(4, -6, 8)
        v_div = v / 2
        self.assertEqual(v_div, Vector3(2, -3, 4))

        with self.assertRaises(ZeroDivisionError):
            _ = v / 0

    def test_equality(self):
        v1 = Vector3(1.0000000001, 2, 3)
        v2 = Vector3(1.0, 2.0, 3.0)
        self.assertTrue(v1 == v2) # Should pass within floating point tolerance

        v3 = Vector3(1.0, 2.0, 3.1)
        self.assertFalse(v2 == v3)

    def test_dot_product(self):
        v1 = Vector3(1, 2, 3)
        v2 = Vector3(4, -5, 6)
        self.assertEqual(v1.dot(v2), 1*4 + 2*(-5) + 3*6)

    def test_cross_product(self):
        # Standard right-handed coordinate system test
        x_axis = Vector3(1, 0, 0)
        y_axis = Vector3(0, 1, 0)
        z_axis = Vector3(0, 0, 1)

        self.assertEqual(x_axis.cross(y_axis), z_axis)
        self.assertEqual(y_axis.cross(x_axis), z_axis * -1)

    def test_length(self):
        v = Vector3(3, 4, 0)
        self.assertEqual(v.length(), 5.0)

    def test_normalization(self):
        v = Vector3(0, 3, 4)
        v_norm = v.normalized()
        self.assertEqual(v_norm, Vector3(0, 0.6, 0.8))
        self.assertAlmostEqual(v_norm.length(), 1.0)

    def test_zero_vector_normalization(self):
        v = Vector3(0, 0, 0)
        v_norm = v.normalized()
        self.assertEqual(v_norm, Vector3(0, 0, 0)) # Should handle gracefully without zero division

if __name__ == '__main__':
    unittest.main()
