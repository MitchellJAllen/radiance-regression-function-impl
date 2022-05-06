import random

from Intersection import Intersection
from Surface import Surface

class TriangleSurface(Surface):
	def __init__(self, material, vertex0, vertex1, vertex2):
		super().__init__(material)
		self.vertex0 = vertex0
		self.vertex1 = vertex1
		self.vertex2 = vertex2

	def getIntersection(self, origin, direction):
		epsilon = 1e-7

		edge1 = self.vertex1 - self.vertex0
		edge2 = self.vertex2 - self.vertex0

		d = direction.normalize()

		dCrossE2 = d.cross(edge2)
		e1DotDCrossE2 = edge1.dot(dCrossE2)

		if (abs(e1DotDCrossE2) < epsilon):
			return None

		invE1DotDCrossE2 = 1 / e1DotDCrossE2
		v0Origin = origin - self.vertex0

		u = invE1DotDCrossE2 * v0Origin.dot(dCrossE2)

		if (u < -epsilon or u > 1 + epsilon):
			return None

		v0OriginCrossE1 = v0Origin.cross(edge1)

		v = invE1DotDCrossE2 * d.dot(v0OriginCrossE1)

		if (v < -epsilon or u + v > 1 + epsilon):
			return None

		t = invE1DotDCrossE2 * edge2.dot(v0OriginCrossE1)

		if (t < epsilon):
			return None

		return Intersection(origin, d, self, t)

	def getNormal(self, position):
		edge02 = self.vertex2 - self.vertex0
		edge01 = self.vertex1 - self.vertex0

		return edge02.cross(edge01).normalize()

	def getSurfaceArea(self):
		edge02 = self.vertex2 - self.vertex0
		edge01 = self.vertex1 - self.vertex0

		return 0.5 * edge02.cross(edge01).length()

	def getRandomPoint(self):
		edge02 = self.vertex2 - self.vertex0
		edge01 = self.vertex1 - self.vertex0

		u = random.random()
		v = random.random()

		if u + v > 1.0:
			u = 1.0 - u
			v = 1.0 - v

		position = self.vertex0 + u * edge01 + v * edge02
		normal = self.getNormal(position)

		return (position, normal, self)
