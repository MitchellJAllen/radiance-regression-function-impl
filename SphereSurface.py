import math
import random

from Intersection import Intersection
from Surface import Surface
from Vector3 import Vector3

class SphereSurface(Surface):
	def __init__(self, material, center, radius):
		super().__init__(material)
		self.center = center
		self.radius = radius

	def getIntersection(self, origin, direction):
		epsilon = 1e-7

		u = direction.normalize()
		co = origin - self.center

		a = u.dot(co)
		b = co.dot(co)

		delta = a * a - b + self.radius * self.radius

		if (delta < 0):
			return None

		sqrtDelta = math.sqrt(delta)
		frontDepth = -a - sqrtDelta
		backDepth = -a + sqrtDelta

		if (backDepth < epsilon):
			return None

		depth = frontDepth

		if (frontDepth < epsilon):
			depth = backDepth

		return Intersection(origin, u, self, depth)

	def getNormal(self, position):
		return (position - self.center).normalize()

	def getSurfaceArea(self):
		return 4.0 * math.pi * self.radius * self.radius

	def getRandomUnitVector(self):
		vector = Vector3(
			random.gauss(0, 1), random.gauss(0, 1), random.gauss(0, 1)
		).normalize()

		return vector

	def getRandomPoint(self):
		normal = self.getRandomUnitVector()
		position = self.radius * normal + self.center

		return (position, normal, self)
