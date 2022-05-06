import math
import random

from BlinnPhongMaterial import BlinnPhongMaterial
from Material import Material
from Vector3 import Vector3

class PathTracingMaterial(BlinnPhongMaterial):
	def __init__(self, color, scene, sampleCount):
		super().__init__(color, scene)
		self.sampleCount = sampleCount

	def getRandomHemisphereVector(self, normal):
		vector = Vector3(
			random.gauss(0, 1), random.gauss(0, 1), random.gauss(0, 1)
		).normalize()

		if (normal.dot(vector) < 0.0):
			return -vector

		return vector

	def getIndirectLighting(self, position, normal, light):
		indirectLighting = [0.0, 0.0, 0.0]

		for sampleIndex in range(self.sampleCount):
			direction = self.getRandomHemisphereVector(normal)
			dotProduct = direction.dot(normal)

			newIntersection = self.scene.getIntersection(position, direction)

			if (newIntersection != None):
				color = newIntersection.surface.material.getDirectLighting(
					newIntersection.getPosition(), newIntersection.getNormal(),
					light
				)

				indirectLighting[0] += color[0] * dotProduct
				indirectLighting[1] += color[1] * dotProduct
				indirectLighting[2] += color[2] * dotProduct

		indirectLighting[0] /= self.sampleCount
		indirectLighting[1] /= self.sampleCount
		indirectLighting[2] /= self.sampleCount

		return indirectLighting
