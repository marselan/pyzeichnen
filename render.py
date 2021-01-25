#
# render.py
#
# Created by Mariano Arselan at 01-12-20
#
import pywavefront
import random
from matplotlib import pyplot
from matplotlib.patches import Polygon
from util import quick_sort
from linalg import rotation_matrix_axis_x
from linalg import rotation_matrix_axis_y
from linalg import rotation_matrix_axis_z
from linalg import Vector3D
from linalg import Triangle3D
from linalg import Line3D

class Frustum:
    def __init__(self, width, height, front, rear, x_res, y_res, plt, light, azimuth=0.0, elevation=0.0, angle=0.0):
        self.width = width
        self.height = height
        self.front = front
        self.rear = rear
        self.x_res = x_res
        self.y_res = y_res
        self.plt = plt
        self.light = light
        self.azimuth = azimuth
        self.elevation = elevation
        self.angle = angle
        self.width = width
        self.dir1 = Vector3D(1, 0, 0)
        self.dir2 = Vector3D(0, 1, 0)
        self.dir3 = Vector3D(0, 0, 1)
        self.pixel_size_x = width / x_res
        self.pixel_size_y = height / y_res
        self.half_pixel_x = self.pixel_size_x / 2
        self.half_pixel_y = self.pixel_size_y / 2
        self.half_width = width / 2
        self.half_height = height / 2

        self.update_base()

    def get_point_at(self, pixel_x, pixel_y):
        return self.pixel_size_x * pixel_x - self.half_width + self.half_pixel_x, -self.pixel_size_y * pixel_y + self.half_height - self.half_pixel_y

    def update_base(self):
        x_rotation_matrix = rotation_matrix_axis_x(elevation=self.elevation)
        y_rotation_matrix = rotation_matrix_axis_y(azimuth=self.azimuth)
        z_rotation_matrix = rotation_matrix_axis_z(angle=self.angle)
        self.dir1 = z_rotation_matrix * (y_rotation_matrix * (x_rotation_matrix * Vector3D(1, 0, 0)))
        self.dir2 = z_rotation_matrix * (y_rotation_matrix * (x_rotation_matrix * Vector3D(0, 1, 0)))
        self.dir3 = z_rotation_matrix * (y_rotation_matrix * (x_rotation_matrix * Vector3D(0, 0, 1)))

    def set_azimuth(self, azimuth):
        self.azimuth = azimuth
        self.update_base()

    def set_elevation(self, elevation):
        self.elevation = elevation
        self.update_base()

    def set_angle(self, angle):
        self.angle = angle
        self.update_base()

    def set_distance(self, distance):
        self.front = distance
        self.update_base()

    def transform(self, triangle):
        dir1 = self.dir1
        dir2 = self.dir2
        dir3 = self.dir3

        p1 = triangle.p1
        p2 = triangle.p2
        p3 = triangle.p3

        triangle_norm = triangle.normal.norm()
        dot_prod = dir3.dot_prod(triangle_norm)
        if dot_prod <= 0:
            return None

        # project Z coords onto current base
        zp1 = p1.dot_prod(dir3) / dir3.length()
        zp2 = p2.dot_prod(dir3) / dir3.length()
        zp3 = p3.dot_prod(dir3) / dir3.length()

        # check if Z coords of the three points are inside the frustum
        if self.front <= zp1 or self.front <= zp2 or self.front <= zp3:
            return None
        if zp1 <= self.rear or zp2 <= self.rear or zp2 <= self.rear:
            return None

        # project X coords onto current base
        xp1 = p1.dot_prod(dir1) / dir1.length()
        xp2 = p2.dot_prod(dir1) / dir1.length()
        xp3 = p3.dot_prod(dir1) / dir1.length()

        # project Y coords onto current base
        yp1 = p1.dot_prod(dir2) / dir2.length()
        yp2 = p2.dot_prod(dir2) / dir2.length()
        yp3 = p3.dot_prod(dir2) / dir2.length()

        # create a triangle with the new coords
        tp1 = Vector3D(xp1, yp1, zp1)
        tp2 = Vector3D(xp2, yp2, zp2)
        tp3 = Vector3D(xp3, yp3, zp3)
        return Triangle3D(tp1, tp2, tp3)

    def project_triangle(self, triangle):
        dir1 = self.dir1
        dir2 = self.dir2
        dir3 = self.dir3

        p1 = triangle.p1
        p2 = triangle.p2
        p3 = triangle.p3

        # calculate light for the projected triangle
        triangle_norm = triangle.normal.norm()
        transformed_light = self.light.rotate(dir1, dir2, dir3)
        light_norm = transformed_light.norm()
        shadow = triangle_norm.dot_prod(light_norm)
        color = (0, 0, max(shadow, 0))

        vc_distance = 10.0
        vanishing_point = self.front + vc_distance

        # project the new triangle onto the front plane of the frustum
        vp1_dist = abs(vanishing_point - p1.z)
        xp1 = p1.x * vc_distance / vp1_dist
        yp1 = p1.y * vc_distance / vp1_dist

        vp2_dist = abs(vanishing_point - p2.z)
        xp2 = p2.x * vc_distance / vp2_dist
        yp2 = p2.y * vc_distance / vp2_dist

        vp3_dist = abs(vanishing_point - p3.z)
        xp3 = p3.x * vc_distance / vp3_dist
        yp3 = p3.y * vc_distance / vp3_dist

        self.plt.fill([xp1, xp2, xp3], [yp1, yp2, yp3], color=color)

    def project(self, triangle, x, y):
        # calculate light for the projected triangle
        triangle_norm = triangle.normal.norm()
        light_norm = self.light.norm()
        shadow = triangle_norm.dot_prod(light_norm)
        color = (0, 0, max(shadow, 0))
        self.plt.scatter([x], [y], color=color)



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
        self.triangles = []
        self.objects = []
        self.plt = plt
        self.frustum = frustum
        self.light = light

    def set_azimuth(self, azimuth):
        self.frustum.set_azimuth(azimuth)
        self.project_fast()

    def set_elevation(self, elevation):
        self.frustum.set_elevation(elevation)
        self.project_fast()

    def set_angle(self, angle):
        self.frustum.set_angle(angle)
        self.project_fast()

    def set_camera_distance(self, camera_distance):
        self.frustum.set_distance(camera_distance)
        self.project_fast()

    def project_fast(self):
        transformed_triangles = []
        for triangle in self.triangles:
            transformed_triangle = self.frustum.transform(triangle)
            if transformed_triangle is None:
                continue
            transformed_triangles.append(transformed_triangle)
        quick_sort(transformed_triangles)
        for triangle in transformed_triangles:
            self.frustum.project_triangle(triangle)

    def project(self):
        camera_distance = self.frustum.front
        vanishing_point = camera_distance + 10.0
        for pixel_y in range(0, self.frustum.y_res):
            for pixel_x in range(0, self.frustum.x_res):
                nearest_point = None
                nearest_triangle = None
                nearest_original_triangle = None
                point_x, point_y = self.frustum.get_point_at(pixel_x, pixel_y)
                print(f'({point_x},{point_y})')
                # self.plt.plot([point_x], [point_y], ".r")
                for triangle in self.triangles:
                    transformed_triangle = self.frustum.transform(triangle)
                    if transformed_triangle is None:
                        continue
                    line = Line3D(Vector3D(point_x, point_y, self.frustum.front), Vector3D(0, 0, vanishing_point))
                    i_point = transformed_triangle.intersection_point(line)
                    # print(i_point)
                    if i_point is None:
                        continue
                    if nearest_point is None or nearest_point.z() < i_point.z():
                        nearest_point = i_point
                        nearest_triangle = transformed_triangle
                        nearest_original_triangle = triangle

                if nearest_triangle is not None:
                    self.frustum.project(nearest_original_triangle, point_x, point_y)

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
            self.triangles = []
            for index in range(0, len(vectors), 3):
                triangle = Triangle3D(*vectors[index:index + 3])
                self.triangles.append(triangle)

            index = 0
            for mesh in scene.mesh_list:
                face = Face3D()
                for _ in mesh.faces:
                    triangle = self.triangles[index]
                    index += 1
                    face.add(triangle)
                self.objects.append(face)

if __name__ == '__main__':
    p1 = Vector3D(1, 1, 0)
    p2 = Vector3D(0, 0, 0)
    p3 = Vector3D(2, 1, 0)

    triang = ((1, 1), (0, 0), (2, 1))
    count_points = 1000
    figure = pyplot.figure()
    axes = figure.add_subplot(111, aspect='equal')
    axes.set_xlim(0, 2)
    axes.set_ylim(0, 2)
    axes.add_patch(Polygon(triang, linewidth=1, edgecolor='k', facecolor='none'))

    t = Triangle3D(p1, p2, p3)

    for i in range(count_points):
        x = random.uniform(0, 2)
        y = random.uniform(0, 2)
        l = Line3D(Vector3D(x, y, 1), Vector3D(x, y, 0))
        if t.intersection_point(l) is None:
            pyplot.plot(x, y, '.g')
        else:
            pyplot.plot(x, y, '.b')

    pyplot.show()
