#
# test.py
#
# Created by Mariano Arselan at 18-01-21
#

import math
import random
import sys
import getopt
import numbers


def rotation_matrix_axis_x(elevation=0.0):
    return Matrix3x3(1, 0, 0,
                     0, math.cos(elevation), -math.sin(elevation),
                     0, math.sin(elevation), math.cos(elevation))


def rotation_matrix_axis_y(azimuth=0.0):
    return Matrix3x3(math.cos(azimuth), 0, math.sin(azimuth),
                     0, 1, 0,
                     -math.sin(azimuth), 0, math.cos(azimuth))


def rotation_matrix_axis_z(angle=0.0):
    return Matrix3x3(math.cos(angle), -math.sin(angle), 0,
                     math.sin(angle), math.cos(angle), 0,
                     0, 0, 1)

class Line2D:
    def __init__(self, point, direction):
        self.point = point
        self.direction = direction

    def intersection_point(self, other_line):
        d1, d2 = self.direction.x, self.direction.y
        p1, p2 = self.point.x, self.point.y
        e1, e2 = other_line.direction.x, other_line.direction.y
        q1, q2 = other_line.point.x, other_line.point.y

        t = (d1 * (q2 - p2) + d2 * (p1 - q1)) / (d2 * e1 - d1 * e2)
        return other_line.point + (other_line.direction & t)

    def plot(self, plt, t0, t1, color='b', line_width=1):
        v0 = self.point + (self.direction & t0)
        v1 = self.point + (self.direction & t1)
        plt.plot([v0.x, v1.x], [v0.y, v1.y], color=color, linewidth=line_width)

class Segment2D:
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1

    def plot(self, plt, color='b', line_width=1):
        plt.plot([self.p0.x, self.p1.x], [self.p0.y, self.p1.y], color=color, linewidth=line_width)

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rotate(self, dir1, dir2):
        xp1 = self.dot_prod(dir1) / dir1.length()
        yp1 = self.dot_prod(dir2) / dir2.length()
        return Vector2D(xp1, yp1)

    def components(self):
        return (self.x, self.y)

    def __add__(self, vector):
        x1, y1 = self.components()
        x2, y2 = vector.components()
        return Vector2D(x1 + x2, y1 + y2)

    def __sub__(self, vector):
        x1, y1 = self.components()
        x2, y2 = vector.components()
        return Vector2D(x1 - x2, y1 - y2)

    def __neg__(self):
        x1, y1 = self.components()
        return Vector2D(-x1, -y1)

    def length(self):
        x, y = self.components()
        return math.sqrt(x ** 2 + y ** 2)

    def __and__(self, scalar):
        x, y = self.components()
        return Vector2D(x * scalar, y * scalar)

    # multiply this vector (assuming this is a column vector) with other vector (assuming as row vector)
    # the result is a 2x2 Matrix
    def __pow__(self, other):
        v1, v2 = self.components()
        w1, w2 = other.components()
        return Matrix2x2(v1 * w1, v1 * w2, v2 * w1, v2 * w2)

    # dot product. No matter if the operands are row or column vectors
    def dot_prod(self, vector):
        x1, y1 = self.components()
        x2, y2 = vector.components()
        return x1 * x2 + y1 * y2

    # row vector multiplied by a column vector.
    # the result is a scalar
    def __mul__(self, other):
        return self.dot_prod(other)

    def norm(self):
        x, y = self.components()
        length = self.length()
        return Vector2D(x / length, y / length)

    def plot(self, plt, color='b', line_width=1):
        plt.plot([0, self.x], [0, self.y], color=color, linewidth=line_width)

    def plot_as_point(self, plt, color='b'):
        plt.scatter([self.x], [self.y], color=color)

    @classmethod
    def sample(cls, from_x, to_x, from_y, to_y, count):
        arr_x = random.sample(range(from_x, to_x), count)
        arr_y = random.sample(range(from_y, to_y), count)
        return [Vector2D(x, y) for (x, y) in zip(arr_x, arr_y)]

    @classmethod
    def mean(cls, vectors):
        v = Vector2D(0, 0)
        for vector in vectors:
            v = v + vector
        return v & (1 / len(vectors))

    @classmethod
    def covariance_matrix(cls, vectors):
        cm = Matrix2x2(0, 0, 0, 0)
        m = Vector2D.mean(vectors)
        for vector in vectors:
            cm = cm + ((vector - m) ** (vector - m))
        return cm & (1 / len(vectors))

    @classmethod
    def fit_box(cls, eigenvector0, eigenvector1, sample, plt):
        l = [math.inf, -math.inf, math.inf, -math.inf]
        for vector in sample:
            dot_prod_0 = eigenvector0 * vector
            dot_prod_1 = eigenvector1 * vector
            l[0] = min(l[0], dot_prod_0)
            l[1] = max(l[1], dot_prod_0)
            l[2] = min(l[2], dot_prod_1)
            l[3] = max(l[3], dot_prod_1)

        a = (l[0] + l[1]) / 2
        b = (l[2] + l[3]) / 2

        ev0, ev1, ev2, ev3 = eigenvector0 & l[0], eigenvector0 & l[1], eigenvector1 & l[2], eigenvector1 & l[3]
        right_line = Line2D(ev1, ev3)
        left_line = Line2D(ev0, ev2)
        top_line = Line2D(ev2, ev0)
        bottom_line = Line2D(ev3, ev1)
        box_center = (eigenvector0 & a) + (eigenvector1 & b)

        ip0 = top_line.intersection_point(left_line)
        ip1 = top_line.intersection_point(right_line)
        ip2 = bottom_line.intersection_point(right_line)
        ip3 = bottom_line.intersection_point(left_line)

        return ip0, ip1, ip2, ip3, box_center


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        x, y = self.components()
        return f'({x}, {y})'


class Vector3D:
    def __init__(self, x, y, z, n_x=None, n_y=None, n_z=None):
        self.xyz = (x, y, z)
        if n_x is None:
            n_x = x
        if n_y is None:
            n_y = y
        if n_z is None:
            n_z = z
        self.normal = (n_x, n_y, n_z)

    def rotate(self, dir1, dir2, dir3):
        xp1 = self.dot_prod(dir1) / dir1.length()
        yp1 = self.dot_prod(dir2) / dir2.length()
        zp1 = self.dot_prod(dir3) / dir3.length()

        return Vector3D(xp1, yp1, zp1)

    def components(self):
        return self.xyz

    def x(self):
        x, _, _ = self.components()
        return x

    def y(self):
        _, y, _ = self.components()
        return y

    def z(self):
        _, _, z = self.components()
        return z

    def add(self, vector):
        x1, y1, z1 = self.xyz
        x2, y2, z2 = vector.components()
        return Vector3D(x1 + x2, y1 + y2, z1 + z2)

    def sub(self, vector):
        x1, y1, z1 = self.xyz
        x2, y2, z2 = vector.components()
        return Vector3D(x1 - x2, y1 - y2, z1 - z2)

    def length(self):
        x, y, z = self.xyz
        return math.sqrt(x ** 2 + y ** 2 + z ** 2)

    def scalar_prod(self, scalar):
        x, y, z = self.xyz
        return Vector3D(x * scalar, y * scalar, z * scalar)

    def dot_prod(self, vector):
        x1, y1, z1 = self.xyz
        x2, y2, z2 = vector.components()
        return x1 * x2 + y1 * y2 + z1 * z2

    def cross_prod(self, vector):
        x1, y1, z1 = self.xyz
        x2, y2, z2 = vector.components()
        return Vector3D(y1 * z2 - z1 * y2, z1 * x2 - x1 * z2, x1 * y2 - y1 * x2)

    def norm(self):
        x, y, z = self.xyz
        length = self.length()
        return Vector3D(x / length, y / length, z / length)

    def __repr__(self):
        x, y, z = self.xyz
        return f'({x}, {y}, {z})'


class Line3D:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.direction = p2.sub(p1)

    def get_coord_for_param(self, t):
        return self.direction.scalar_prod(t).add(self.p1)


class Triangle3D:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        v1 = p2.sub(p1)
        v2 = p3.sub(p1)
        self.normal = v1.cross_prod(v2)

    def intersection_point(self, line):
        xp, yp, zp = self.p1.components()
        a, b, c = self.normal.components()
        d = -a * xp - b * yp - c * zp
        x1, y1, z1 = line.p1.components()
        v1, v2, v3 = line.direction.components()
        denominator = a * v1 + b * v2 + c * v3
        if denominator == 0:
            return None
        # alpha is the parameter in the parametric equation of the line at the point of intersection
        alpha = -(a * x1 + b * y1 + c * z1 + d) / denominator

        # intersection point = (x, y, z)
        x = x1 + alpha * v1
        y = y1 + alpha * v2
        z = z1 + alpha * v3

        p1 = self.p1
        p2 = self.p2
        p3 = self.p3

        # check if the intersection point is inside the triangle
        side_1 = (x - p2.x()) * (p1.y() - p2.y()) - (p1.x() - p2.x()) * (y - p2.y())
        side_2 = (x - p3.x()) * (p2.y() - p3.y()) - (p2.x() - p3.x()) * (y - p3.y())
        side_3 = (x - p1.x()) * (p3.y() - p1.y()) - (p3.x() - p1.x()) * (y - p1.y())
        if (side_1 < 0.0) == (side_2 < 0.0) == (side_3 < 0.0):
            return Vector3D(x, y, z)

        return None

    def project(self, plt, frustum, light=Vector3D(0, 0, 1)):
        dir1 = frustum.dir1
        dir2 = frustum.dir2
        dir3 = frustum.dir3

        triangle_norm = self.normal.norm()
        dot_prod = dir3.dot_prod(triangle_norm)
        if dot_prod <= 0:
            return None

        # frustum.front is the camera distance
        vc_distance = 10.0
        vanishing_point = frustum.front + vc_distance

        # project Z coords onto current base
        zp1 = self.p1.dot_prod(dir3) / dir3.length()
        zp2 = self.p2.dot_prod(dir3) / dir3.length()
        zp3 = self.p3.dot_prod(dir3) / dir3.length()

        # check if Z coords of the three points are inside the frustum
        if frustum.front <= zp1 or frustum.front <= zp2 or frustum.front <= zp3:
            return None
        if zp1 <= frustum.rear or zp2 <= frustum.rear or zp2 <= frustum.rear:
            return None

        # project X coords onto current base
        xp1 = self.p1.dot_prod(dir1) / dir1.length()
        xp2 = self.p2.dot_prod(dir1) / dir1.length()
        xp3 = self.p3.dot_prod(dir1) / dir1.length()

        # project Y coords onto current base
        yp1 = self.p1.dot_prod(dir2) / dir2.length()
        yp2 = self.p2.dot_prod(dir2) / dir2.length()
        yp3 = self.p3.dot_prod(dir2) / dir2.length()

        # create a triangle with the new coords
        tp1 = Vector3D(xp1, yp1, zp1)
        tp2 = Vector3D(xp2, yp2, zp2)
        tp3 = Vector3D(xp3, yp3, zp3)
        projected_triangle = Triangle3D(tp1, tp2, tp3)

        # calculate light for the projected triangle
        triangle_norm = projected_triangle.normal.norm()
        transformed_light = light.rotate(frustum.dir1, frustum.dir2, frustum.dir3)
        light_norm = transformed_light.norm()
        shadow = triangle_norm.dot_prod(light_norm)
        color = (0, 0, max(shadow, 0))

        # project the new triangle onto the front plane of the frustum
        vp1_dist = abs(vanishing_point - zp1)
        xp1 = xp1 * vc_distance / vp1_dist
        yp1 = yp1 * vc_distance / vp1_dist

        vp2_dist = abs(vanishing_point - zp2)
        xp2 = xp2 * vc_distance / vp2_dist
        yp2 = yp2 * vc_distance / vp2_dist

        vp3_dist = abs(vanishing_point - zp3)
        xp3 = xp3 * vc_distance / vp3_dist
        yp3 = yp3 * vc_distance / vp3_dist

        plt.fill([xp1, xp2, xp3], [yp1, yp2, yp3], color=color)

    def __le__(self, other):
        # in * THIS PARTICULAR CASE * I define that a triangle is less or equal to other by comparing the Z orders
        # of their points
        max_z1 = max(max(self.p1.z(), self.p2.z()), self.p3.z())
        max_z2 = max(max(other.p1.z(), other.p2.z()), other.p3.z())
        return max_z1 <= max_z2

    def __repr__(self):
        return f'Triangle [ {self.p1}, {self.p2}, {self.p3} ] '


class Matrix2x2:
    def __init__(self, c00, c01, c10, c11):
        self.r0 = Vector2D(c00, c01)
        self.r1 = Vector2D(c10, c11)

    def __add__(self, other):
        return Matrix2x2(*(self.r0 + other.r0).components(), *(self.r1 + other.r1).components())

    def __and__(self, scalar):
        return Matrix2x2(*(self.r0 & scalar).components(), *(self.r1 & scalar).components())

    def __mul__(self, vector):
        return Vector2D(self.r0 * vector, self.r1 * vector)

    def __pow__(self, other):
        return Matrix2x2(self.r0 * other.c0, self.r0 * other.c1, self.r1 * other.c0, self.r1 * other.c1)

    def __eq__(self, other):
        return self.r0 == other.r0 and self.r1 == other.r1

    def eigenvalues(self):
        c00, c01 = self.r0.components()
        c10, c11 = self.r1.components()
        b = c00 + c11
        c = c00 * c11 - c10 * c01
        square_root = math.sqrt( b * b - 4 * c )
        lambda_1 = (-b + square_root) / 2
        lambda_2 = (-b - square_root) / 2
        return (lambda_1, lambda_2)

    def eigenvectors(self):
        import numpy as np
        from numpy import linalg
        np_mat = np.array([[*self.r0.components()], [*self.r1.components()]])
        w, v = linalg.eig(np_mat)
        ev0 = Vector2D(*v[0])
        ev1 = Vector2D(*v[1])
        return (w[0], w[1]), ev0, ev1

    def __repr__(self):
        return f"|{self.r0.x} {self.r0.y}|\n|{self.r1.x} {self.r1.y}|"

def draw_vector_2d(vector, plt, color):
    plt.plot([0, vector.x], [0, vector.y], color=color)

class Matrix3x3:
    def __init__(self, c00, c01, c02, c10, c11, c12, c20, c21, c22):
        self.v0 = Vector3D(c00, c01, c02)
        self.v1 = Vector3D(c10, c11, c12)
        self.v2 = Vector3D(c20, c21, c22)

    def prod(self, vector):
        return Vector3D(self.v0.dot_prod(vector), self.v1.dot_prod(vector), self.v2.dot_prod(vector))


def render_2d_vector_sample():
    from matplotlib import pyplot as plt
    plt.axes().set_aspect('equal')
    sample = Vector2D.sample(0, 1000, -1000, 0, 100)
    mean = Vector2D.mean(sample)
    cov_mat = Vector2D.covariance_matrix(sample)

    eigenvalues, eigenvector0, eigenvector1 = cov_mat.eigenvectors()

    ip0, ip1, ip2, ip3, center = Vector2D.fit_box(eigenvector0, eigenvector1, sample, plt)

    s0 = Segment2D(ip0, ip1)
    s1 = Segment2D(ip1, ip2)
    s2 = Segment2D(ip2, ip3)
    s3 = Segment2D(ip3, ip0)

    plt.scatter([v.x for v in sample], [v.y for v in sample])
    plt.scatter(mean.x, mean.y)
    s0.plot(plt, 'orange')
    s1.plot(plt, 'orange')
    s2.plot(plt, 'orange')
    s3.plot(plt, 'orange')

    plt.show()


def main(argv):
    use_case = ""
    try:
        opts, args = getopt.getopt(argv, "hu:", ["help=", "use-case="])
    except getopt.GetoptError:
        print('linalg -h or lingalg --help for list of options')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("-u, --use-case:")
            print("linalg -u [use case name]")
            print("List of use case names:")
            print(" * render-2d-vector-sample")
            print(" * render-2d-vector-sample-best-fit")
        elif opt in ("-u", "--use-case"):
            use_case = arg

    if use_case == 'render-2d-vector-sample':
        render_2d_vector_sample()


if __name__ == '__main__':
    main(sys.argv[1:])
