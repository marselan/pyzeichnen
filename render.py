#
# render.py
#
# Created by Mariano Arselan at 01-12-20
#
import pywavefront
import math


class Frustum:
    def __init__(self, width, height, front, rear, azimuth=0.0, elevation=0.0, angle=0.0):
        self.width = width
        self.height = height
        self.front = front
        self.rear = rear
        self.azimuth = azimuth
        self.elevation = elevation
        self.angle = angle
        self.width = width


class Matrix3x3:
    def __init__(self, c00, c01, c02, c10, c11, c12, c20, c21, c22):
        self.v0 = Vector3D(c00, c01, c02)
        self.v1 = Vector3D(c10, c11, c12)
        self.v2 = Vector3D(c20, c21, c22)

    def prod(self, vector):
        return Vector3D(self.v0.dot_prod(vector), self.v1.dot_prod(vector), self.v2.dot_prod(vector))


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


class Function3D:
    def __init__(self, points):
        self.points = points.copy()

    def draw(self, ax, color='b'):
        x, y, z = zip(*self.points)
        ax.plot(x, y, z, color=color)


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

    def draw(self, ax, color='b', camera_az=0.0, camera_elev=0.0, camera_ang=0.0):
        x, y, z = self.xyz
        x_rotation_matrix = rotation_matrix_axis_x(elevation=camera_elev)
        y_rotation_matrix = rotation_matrix_axis_y(azimuth=camera_az)
        z_rotation_matrix = rotation_matrix_axis_z(angle=camera_ang)
        v = z_rotation_matrix.prod(y_rotation_matrix.prod(x_rotation_matrix.prod(self)))
        vx, vy, vz = v.xyz
        ax.plot([0, vx], [0, vy], [0, vz], color=color)

    def project(self, ax, color='b', camera_az=0.0, camera_elev=0.0, camera_ang=0.0):
        x, y, z = self.xyz
        x_rotation_matrix = rotation_matrix_axis_x(elevation=camera_elev)
        y_rotation_matrix = rotation_matrix_axis_y(azimuth=camera_az)
        z_rotation_matrix = rotation_matrix_axis_z(angle=camera_ang)
        dir1 = z_rotation_matrix.prod(y_rotation_matrix.prod(x_rotation_matrix.prod(Vector3D(1, 0, 0))))
        dir2 = z_rotation_matrix.prod(y_rotation_matrix.prod(x_rotation_matrix.prod(Vector3D(0, 1, 0))))
        dir3 = z_rotation_matrix.prod(y_rotation_matrix.prod(x_rotation_matrix.prod(Vector3D(0, 0, 1))))
        ax.plot([0, dir1.dot_prod(Vector3D(x, 0, 0))], [0, dir2.dot_prod(Vector3D(0, y, 0))],
                [0, dir3.dot_prod(Vector3D(0, 0, z))], color=color)

    def components(self):
        return self.xyz

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


class Segment3D:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, ax, color='b', flat=False, camera_az=0.0, camera_elev=0.0):

        dir1 = Vector3D(math.cos(camera_az), math.sin(camera_az), 0)
        dir2 = Vector3D(-math.sin(camera_az), math.cos(camera_az), 0)
        dir3 = Vector3D(0, 0, 1)

        xp1 = self.p1.dot_prod(dir1) / dir1.length()
        yp1 = self.p1.dot_prod(dir2) / dir2.length()
        if flat:
            zp1 = 0
        else:
            zp1 = self.p1.dot_prod(dir3) / dir3.length()

        xp2 = self.p2.dot_prod(dir1) / dir1.length()
        yp2 = self.p2.dot_prod(dir2) / dir2.length()
        if flat:
            zp2 = 0
        else:
            zp2 = self.p2.dot_prod(dir3) / dir3.length()

        ax.plot([xp1, xp2], [yp1, yp2], [zp1, zp2], color=color)

    def project(self, plt, color='b', camera_az=0.0, camera_elev=0.0, camera_ang=0.0, camera_dist=1.0):
        x_rotation_matrix = rotation_matrix_axis_x(elevation=camera_elev)
        y_rotation_matrix = rotation_matrix_axis_y(azimuth=camera_az)
        z_rotation_matrix = rotation_matrix_axis_z(angle=camera_ang)
        dir1 = z_rotation_matrix.prod(y_rotation_matrix.prod(x_rotation_matrix.prod(Vector3D(1, 0, 0))))
        dir2 = z_rotation_matrix.prod(y_rotation_matrix.prod(x_rotation_matrix.prod(Vector3D(0, 1, 0))))
        dir3 = z_rotation_matrix.prod(y_rotation_matrix.prod(x_rotation_matrix.prod(Vector3D(0, 0, 1))))

        dot_prod = dir3.dot_prod(Vector3D(*self.p1.normal))
        if dot_prod <= 0:
            return

        xp1 = self.p1.dot_prod(dir1) / (dir1.length() * camera_dist)
        yp1 = self.p1.dot_prod(dir2) / (dir2.length() * camera_dist)
        xp2 = self.p2.dot_prod(dir1) / (dir1.length() * camera_dist)
        yp2 = self.p2.dot_prod(dir2) / (dir2.length() * camera_dist)
        plt.plot([xp1, xp2], [yp1, yp2], color=color)


class Triangle3D:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def draw(self, ax, color='b', flat=False, camera_az=0.0):
        s1 = Segment3D(self.p1, self.p2)
        s2 = Segment3D(self.p1, self.p3)
        s3 = Segment3D(self.p2, self.p3)
        s1.draw(ax, color=color, flat=flat, camera_az=camera_az)
        s2.draw(ax, color=color, flat=flat, camera_az=camera_az)
        s3.draw(ax, color=color, flat=flat, camera_az=camera_az)

    def project_orthographic(self, plt, light=Vector3D(0, 0, 1), camera_az=0.0, camera_elev=0.0, camera_ang=0.0,
                             camera_dist=1.0):
        x_rotation_matrix = rotation_matrix_axis_x(elevation=camera_elev)
        y_rotation_matrix = rotation_matrix_axis_y(azimuth=camera_az)
        z_rotation_matrix = rotation_matrix_axis_z(angle=camera_ang)
        dir1 = z_rotation_matrix.prod(y_rotation_matrix.prod(x_rotation_matrix.prod(Vector3D(1, 0, 0))))
        dir2 = z_rotation_matrix.prod(y_rotation_matrix.prod(x_rotation_matrix.prod(Vector3D(0, 1, 0))))
        dir3 = z_rotation_matrix.prod(y_rotation_matrix.prod(x_rotation_matrix.prod(Vector3D(0, 0, 1))))

        triangle_norm = Vector3D(*self.p1.normal).norm()
        dot_prod = dir3.dot_prod(triangle_norm)
        if dot_prod <= 0:
            return

        xp1 = self.p1.dot_prod(dir1) / (dir1.length() * camera_dist)
        yp1 = self.p1.dot_prod(dir2) / (dir2.length() * camera_dist)
        xp2 = self.p2.dot_prod(dir1) / (dir1.length() * camera_dist)
        yp2 = self.p2.dot_prod(dir2) / (dir2.length() * camera_dist)
        xp3 = self.p3.dot_prod(dir1) / (dir1.length() * camera_dist)
        yp3 = self.p3.dot_prod(dir2) / (dir2.length() * camera_dist)

        light_norm = light.norm()
        shadow = triangle_norm.dot_prod(light_norm)
        color = (0, 0, max(shadow, 0))

        plt.fill([xp1, xp2, xp3], [yp1, yp2, yp3], color=color)

    def project(self, plt, frustum, light=Vector3D(0, 0, 1)):
        x_rotation_matrix = rotation_matrix_axis_x(elevation=frustum.elevation)
        y_rotation_matrix = rotation_matrix_axis_y(azimuth=frustum.azimuth)
        z_rotation_matrix = rotation_matrix_axis_z(angle=frustum.angle)
        dir1 = z_rotation_matrix.prod(y_rotation_matrix.prod(x_rotation_matrix.prod(Vector3D(1, 0, 0))))
        dir2 = z_rotation_matrix.prod(y_rotation_matrix.prod(x_rotation_matrix.prod(Vector3D(0, 1, 0))))
        dir3 = z_rotation_matrix.prod(y_rotation_matrix.prod(x_rotation_matrix.prod(Vector3D(0, 0, 1))))

        triangle_norm = Vector3D(*self.p1.normal).norm()
        dot_prod = dir3.dot_prod(triangle_norm)
        if dot_prod <= 0:
            return

        # frustum.front is the camera distance
        camera_dist = frustum.front
        vanishing_point = frustum.front + 10.0
        vc_distance = abs(vanishing_point - frustum.front)

        zp1 = self.p1.dot_prod(dir3) / dir3.length()
        zp2 = self.p2.dot_prod(dir3) / dir3.length()
        zp3 = self.p3.dot_prod(dir3) / dir3.length()

        # check if z coords of the three points are inside the frustum
        if camera_dist <= zp1 or camera_dist <= zp2 or camera_dist <= zp3:
            return
        if zp1 <= frustum.rear or zp2 <= frustum.rear or zp2 <= frustum.rear:
            return

        vp1_dist = abs(vanishing_point - zp1)
        xp1 = self.p1.dot_prod(dir1) / dir1.length()
        xp1 = xp1 * vc_distance / vp1_dist
        yp1 = self.p1.dot_prod(dir2) / dir2.length()
        yp1 = yp1 * vc_distance / vp1_dist

        vp2_dist = abs(vanishing_point - zp2)
        xp2 = self.p2.dot_prod(dir1) / dir1.length()
        xp2 = xp2 * vc_distance / vp2_dist
        yp2 = self.p2.dot_prod(dir2) / dir2.length()
        yp2 = yp2 * vc_distance / vp2_dist

        vp3_dist = abs(vanishing_point - zp3)
        xp3 = self.p3.dot_prod(dir1) / dir1.length()
        xp3 = xp3 * vc_distance / vp3_dist
        yp3 = self.p3.dot_prod(dir2) / dir2.length()
        yp3 = yp3 * vc_distance / vp3_dist

        light_norm = light.norm()
        shadow = triangle_norm.dot_prod(light_norm)
        color = (0, 0, max(shadow, 0))

        plt.fill([xp1, xp2, xp3], [yp1, yp2, yp3], color=color)

    def __repr__(self):
        return f'Triangle [ {self.p1}, {self.p2}, {self.p3} ] '


class Face3D:
    def __init__(self, triangles=None):
        if triangles is None:
            triangles = []
        self.triangles = triangles

    def add(self, triangle):
        self.triangles.append(triangle)

    def __repr__(self):
        representation = "Face <"
        for triangle in self.triangles:
            representation += f'{triangle}'
        representation += " >"
        return representation

    def project(self, plt, frustum, light=Vector3D(0, 0, 1)):
        for triangle in self.triangles:
            triangle.project(plt, frustum=frustum, light=light)


class Scene3D:
    def __init__(self, file_name, plt, frustum, light):
        self.file_name = file_name
        self.objects = []
        self.plt = plt
        self.frustum = frustum
        self.light = light

    def set_azimuth(self, azimuth):
        self.frustum.azimuth = azimuth
        self.project()

    def set_elevation(self, elevation):
        self.frustum.elevation = elevation
        self.project()

    def set_angle(self, angle):
        self.frustum.angle = angle
        self.project()

    def set_camera_distance(self, camera_distance):
        self.frustum.front = camera_distance
        self.project()

    def project(self):
        for obj in self.objects:
            obj.project(self.plt,
                        frustum=self.frustum,
                        light=self.light)

    def parse_file(self):
        scene = pywavefront.Wavefront(self.file_name, strict=True, encoding="utf-8", collect_faces=True, parse=True,
                                      create_materials=True, cache=False)
        for name, material in scene.materials.items():
            print(material.vertex_format)

            v = material.vertices
            vectors = []
            if material.vertex_format == 'N3F_V3F':
                for index in range(0, len(v), 6):
                    vector = Vector3D(*v[index + 3:index + 6], *v[index:index + 3])
                    vectors.append(vector)
            else:
                for index in range(0, len(v), 3):
                    vector = Vector3D(*v[index:index + 3])
                    vectors.append(vector)
            triangles = []
            for index in range(0, len(vectors), 3):
                triangle = Triangle3D(*vectors[index:index + 3])
                triangles.append(triangle)

            index = 0
            for mesh in scene.mesh_list:
                face = Face3D()
                for _ in mesh.faces:
                    triangle = triangles[index]
                    index += 1
                    face.add(triangle)
                self.objects.append(face)
