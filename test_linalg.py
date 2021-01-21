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

        self.assertEqual(v0 + v0, v0)
        self.assertEqual(v0 + v1, v1)
        self.assertEqual(v1 + v1, v2)
        self.assertEqual(v1 + v3, v4)
        self.assertEqual(v1 + v3 + v0, v4)

    def test_multiply_row_by_col_vectors(self):
        from linalg import Vector2D
        v0 = Vector2D(0, 0)
        v1 = Vector2D(1, 1)
        v2 = Vector2D(2, 4)
        v3 = Vector2D(3, 5)
        self.assertEqual(v0.components(), (0, 0))
        self.assertEqual(v1.components(), (1, 1))
        self.assertEqual(v2.components(), (2, 4))
        self.assertEqual(v3.components(), (3, 5))

        self.assertEqual(v0 * v0, 0)
        self.assertEqual(v0 * v1, 0)
        self.assertEqual(v1 * v1, 2)
        self.assertEqual(v2 * v3, 26)

    def test_multiply_col_by_row_vectors(self):
        from linalg import Vector2D
        from linalg import Matrix2x2
        v0 = Vector2D(0, 0)
        v1 = Vector2D(1, 1)
        v2 = Vector2D(2, 4)
        v3 = Vector2D(3, 5)
        self.assertEqual(v0.components(), (0, 0))
        self.assertEqual(v1.components(), (1, 1))
        self.assertEqual(v2.components(), (2, 4))
        self.assertEqual(v3.components(), (3, 5))

        self.assertEqual(v0 ** v0, Matrix2x2(0, 0, 0, 0))
        self.assertEqual(v0 ** v1, Matrix2x2(0, 0, 0, 0))
        self.assertEqual(v1 ** v1, Matrix2x2(1, 1, 1, 1))
        self.assertEqual(v1 ** v2, Matrix2x2(2, 4, 2, 4))
        self.assertEqual(v2 ** v3, Matrix2x2(6, 10, 12, 20))

    def test_scalar_prod(self):
        from linalg import Vector2D
        v0 = Vector2D(0, 0)
        v1 = Vector2D(1, 1)
        v2 = Vector2D(2, 4)
        self.assertEqual(v0.components(), (0, 0))
        self.assertEqual(v1.components(), (1, 1))
        self.assertEqual(v2.components(), (2, 4))

        self.assertEqual(v0 & 0, Vector2D(0, 0))
        self.assertEqual(v0 & 1, Vector2D(0, 0))
        self.assertEqual(v1 & 0, Vector2D(0, 0))
        self.assertEqual(v1 & 2, Vector2D(2, 2))
        self.assertEqual(v2 & 3, Vector2D(6, 12))

    def test_covariance_matrix(self):
        from linalg import Vector2D
        from linalg import Matrix2x2
        v0 = Vector2D(5, 2)
        v1 = Vector2D(12, 8)
        v2 = Vector2D(18, 18)
        v3 = Vector2D(23, 20)
        v4 = Vector2D(45, 1)

        sample = [v0, v1, v2, v3, v4]
        mean = Vector2D.mean(sample)
        self.assertEqual(mean, Vector2D(20.6, 9.8))
        cov_mat = Vector2D.covariance_matrix(sample)
        self.assertAlmostEqual(cov_mat.r0.x, 185.04)
        self.assertAlmostEqual(cov_mat.r0.y, -14.88)
        self.assertAlmostEqual(cov_mat.r1.x, -14.88)
        self.assertAlmostEqual(cov_mat.r1.y, 62.56)



