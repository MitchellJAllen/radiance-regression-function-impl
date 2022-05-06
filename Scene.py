import math
import random

class Scene:
	def __init__(self):
		self.surfaces = []
		self.surfaceAreas = [0.0]
		self.lights = []

	def addSurface(self, surface):
		self.surfaces.append(surface)

		surfaceArea = surface.getSurfaceArea()
		cumulativeArea = self.surfaceAreas[len(self.surfaceAreas) - 1]

		self.surfaceAreas.append(surfaceArea + cumulativeArea)

	def addLight(self, light):
		self.lights.append(light)

	def getIntersection(self, origin, direction):
		minimumIntersection = None
		minimumDepth = math.inf

		for surface in self.surfaces:
			intersection = surface.getIntersection(origin, direction)

			if (intersection != None and intersection.depth < minimumDepth):
				minimumIntersection = intersection
				minimumDepth = intersection.depth

		return minimumIntersection

	def getRandomPoint(self):
		totalArea = self.surfaceAreas[len(self.surfaceAreas) - 1]

		selector = random.random() * totalArea

		for surfaceIndex in range(len(self.surfaces)):
			cumulativeArea = self.surfaceAreas[surfaceIndex + 1]

			if selector <= cumulativeArea:
				return self.surfaces[surfaceIndex].getRandomPoint()

		return None
