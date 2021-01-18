#
# test.py
#
# Created by Mariano Arselan at 18-01-21
#

from unittest import TestCase


class TestVector2D(TestCase):
    def test_length(self):
        from linalg import Vector2D
        v0 = Vector2D(0, 0)
        v1 = Vector2D(1, 1)
        v2 = Vector2D(2, 2)
        self.assertEqual(v0.components(), (0, 0))
        self.assertEqual(v1.components(), (1, 1))
        self.assertEqual(v2.components(), (2, 2))
        self.assertEqual(v0, v0)
        self.assertEqual(v1, v1)
        self.assertNotEqual(v0, v1)
        self.assertEqual(v0.length(), 0)
        self.assertAlmostEqual(v1.length(), 1.41, delta=0.01)

    def test_dot_prod(self):
        from linalg import Vector2D
        v0 = Vector2D(0, 0)
        v1 = Vector2D(1, 1)
        v2 = Vector2D(2, 2)
        self.assertEqual(v0.components(), (0, 0))
        self.assertEqual(v1.components(), (1, 1))
        self.assertEqual(v2.components(), (2, 2))

        self.assertEqual(v0.dot_prod(v0), 0)
        self.assertEqual(v0.dot_prod(v1), 0)
        self.assertEqual(v1.dot_prod(v1), 2.0)

    def test_add(self):
        from linalg import Vector2D
        v0 = Vector2D(0, 0)
        v1 = Vector2D(1, 1)
        v2 = Vector2D(2, 2)
        v3 = Vector2D(2, 4)
        v4 = Vector2D(3, 5)
        self.assertEqual(v0.components(), (0, 0))
        self.assertEqual(v1.components(), (1, 1))
        self.assertEqual(v2.components(), (2, 2))
        self.assertEqual(v3.components(), (2, 4))
        self.assertEqual(v4.components(), (3, 5))

        self.assertEqual(v0.add(v0), v0)
        self.assertEqual(v0.add(v1), v1)
        self.assertEqual(v1.add(v1), v2)
        self.assertEqual(v1.add(v3), v4)
        self.assertEqual(v1.add(v3).add(v0), v4)