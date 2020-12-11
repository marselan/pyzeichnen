#
# render.py
#
# Created by Mariano Arselan at 01-12-20
#

import matplotlib.pyplot as plt
import numbers
import math

class Polygon:
	def __init__(self, vectors):
		self.vectors = vectors.copy()

	def draw(self, close=True, color='b'):
		x, y = zip(*self.vectors)
		plt.plot(x, y, color=color)
		if (close):
			plt.plot((x[-1], x[0]), (y[-1], y[0]), color=color)

class Segment:
	def __init__(self, vector0, vector1):
		self.vectors = [vector0, vector1]
	def draw(self, color='b'):
		x, y = zip(*self.vectors)
		plt.plot(x, y, color=color)

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def draw(self, color='b'):
		plt.plot([self.x], [self.y], marker='.', color=color)

class Vector:
	def __init__(self, tip, tail=(0,0)):
		if isinstance(tip, numbers.Number):
			self.tip = (tip, tail)
			self.tail = (0,0)
		else:
			self.tail = tail
			self.tip = tip
	def draw(self, color='b'):
		plt.arrow(self.tail[0], self.tail[1],  self.tip[0] - self.tail[0], self.tip[1] - self.tail[1], head_width=.1, color=color)

	def add(self, vector):
		return Vector((self.tip[0] + vector.tip[0], self.tip[1] + vector.tip[1]))

	def sub(self, vector):
		return Vector((self.tip[0] - vector.tip[0], self.tip[1] - vector.tip[1]))

	def displacement(self, vector):
		return Vector(self.tip, vector.tip)

	def length(self):
		return math.sqrt(self.tip[0] ** 2 + self.tip[1] ** 2)

	def scalar_prod(self, scalar):
		return Vector(self.tip[0] * scalar, self.tip[1] * scalar)

	def dot_prod(self, vector):
		return self.tip[0] * vector.tip[0] + self.tip[1] * vector.tip[1]

class Function3D:
	def __init__(self, points):
		self.points = points.copy()

	def draw(self, ax, color='b'):
		x, y, z = zip(*self.points)
		ax.plot(x, y, z, color=color)


class Vector3D:
	def __init__(self, x, y, z):
		self.xyz = (x, y, z)

	def draw(self, ax, color='b'):
		x, y, z = self.xyz
		ax.plot([0, x], [0, y], [0, z], color=color)

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
		len = self.length()
		return Vector3D(x / len, y / len, z / len)

class Matrix3x3:
	def __init__(self, c00, c01, c02, c10, c11, c12, c20, c21, c22):
		self.v0 = Vector3D(c00, c01, c02)
		self.v1 = Vector3D(c10, c11, c12)
		self.v2 = Vector3D(c20, c21, c22)

	def prod(self, vector):
		return Vector3D(self.v0.dot_prod(vector), self.v1.dot_prod(vector), self.v2.dot_prod(vector))

def rotationMatrixAxisX(elevation=0.0):
	return Matrix3x3(1, 0, 0,
					 0, math.cos(elevation), -math.sin(elevation),
					 0, math.sin(elevation), math.cos(elevation))

def rotationMatrixAxisY(azimuth=0.0):
	return Matrix3x3(math.cos(azimuth), 0, math.sin(azimuth),
					 0, 1, 0,
					 -math.sin(azimuth), 0, math.cos(azimuth))

def rotationMatrixAxisZ(angle=0.0):
	return Matrix3x3(math.cos(angle), -math.sin(angle), 0,
					 math.sin(angle), math.cos(angle), 0,
					 0, 0, 1)

class Segment3D:
	def __init__(self, p1, p2):
		self.p1 = Vector3D(*p1.components())
		self.p2 = Vector3D(*p2.components())

	def draw(self, ax, color='b', flat=False, camera_az=0.0, camera_elev=0.0):

		dir1 = Vector3D(math.cos(camera_az), math.sin(camera_az), 0)
		dir2 = Vector3D(-math.sin(camera_az), math.cos(camera_az), 0)
		dir3 = Vector3D(0, 0, 1)

		xp1 = self.p1.dot_prod(dir1) / dir1.length()
		yp1 = self.p1.dot_prod(dir2) / dir2.length()
		if (flat):
			zp1 = 0
		else:
			zp1 = self.p1.dot_prod(dir3) / dir3.length()

		xp2 = self.p2.dot_prod(dir1) / dir1.length()
		yp2 = self.p2.dot_prod(dir2) / dir2.length()
		if (flat):
			zp2 = 0
		else:
			zp2 = self.p2.dot_prod(dir3) / dir3.length()

		ax.plot([xp1, xp2], [yp1, yp2], [zp1, zp2], color=color)

	def project(self, plt, color='b', camera_az=0.0, camera_elev=0.0, camera_ang=0.0, camera_dist=1.0):
		xRotationMatrix = rotationMatrixAxisX(elevation=camera_elev)
		yRotationMatrix = rotationMatrixAxisY(azimuth=camera_az)
		zRotationMatrix = rotationMatrixAxisZ(angle=camera_ang)
		dir1 = zRotationMatrix.prod(yRotationMatrix.prod(xRotationMatrix.prod(Vector3D(1, 0, 0))))
		dir2 = zRotationMatrix.prod(yRotationMatrix.prod(xRotationMatrix.prod(Vector3D(0, 1, 0))))

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

	def project(self, plt, color='b', camera_az=0.0, camera_elev=0.0, camera_ang=0.0):
		s1 = Segment3D(self.p1, self.p2)
		s2 = Segment3D(self.p1, self.p3)
		s3 = Segment3D(self.p2, self.p3)
		s1.project(plt, color=color, camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang)
		s2.project(plt, color=color, camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang)
		s3.project(plt, color=color, camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang)

class Square3D:
	def __init__(self, p1, p2, p3, p4):
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.p4 = p4

	def draw(self, ax, color='b', flat=False, camera_az=0.0):
		s1 = Segment3D(self.p1, self.p2)
		s2 = Segment3D(self.p2, self.p3)
		s3 = Segment3D(self.p3, self.p4)
		s4 = Segment3D(self.p4, self.p1)
		s1.draw(ax, color=color, flat=flat, camera_az=camera_az)
		s2.draw(ax, color=color, flat=flat, camera_az=camera_az)
		s3.draw(ax, color=color, flat=flat, camera_az=camera_az)
		s4.draw(ax, color=color, flat=flat, camera_az=camera_az)

	def project(self, plt, color='b', camera_az=0.0, camera_elev=0.0, camera_ang=0.0):
		s1 = Segment3D(self.p1, self.p2)
		s2 = Segment3D(self.p2, self.p3)
		s3 = Segment3D(self.p3, self.p4)
		s4 = Segment3D(self.p4, self.p1)
		s1.project(plt, color=color, camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang)
		s2.project(plt, color=color, camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang)
		s3.project(plt, color=color, camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang)
		s4.project(plt, color=color, camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang)

class Polygon3D:
	def __init__(self, vectors):
		self.vectors = vectors

	def draw(self, ax, color='b', flat=False, camera_az=0.0):
		print()

	def project(self, plt, color='k', camera_az=0.0, camera_elev=0.0, camera_ang=0.0, camera_dist=1.0):
		for vi, ve in zip(self.vectors[0:], self.vectors[1:]):
			Segment3D(vi, ve).project(plt, color=color, camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang, camera_dist=camera_dist)
		Segment3D(self.vectors[-1], self.vectors[0]).project(plt, color=color, camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang, camera_dist=camera_dist)


class Object3D:
	def __init__(self, polygons):
		self.polygons = polygons

	def project(self, plt, camera_az=0.0, camera_elev=0.0, camera_ang=0.0, camera_dist=1.0):
		for polygon in self.polygons:
			polygon.project(plt, color='k', camera_az=camera_az, camera_elev=camera_elev, camera_ang=camera_ang, camera_dist=camera_dist)

class Scene3D:
	def __init__(self, objects, camera_az=0.0, camera_elev=0.0, camera_ang=0.0, camera_dist=1.0):
		self.objects = objects
		self.camera_azimuth = camera_az
		self.camera_elevation = camera_elev
		self.camera_angle = camera_ang
		self.camera_distance = camera_dist

	def project(self, plt):
		for object in self.objects:
			object.project(plt,
						   camera_az=self.camera_azimuth,
						   camera_elev=self.camera_elevation,
						   camera_ang=self.camera_angle,
						   camera_dist=self.camera_distance)
