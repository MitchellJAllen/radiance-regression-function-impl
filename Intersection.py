class Intersection():
	def __init__(self, origin, direction, surface, depth):
		self.origin = origin
		self.direction = direction
		self.surface = surface
		self.depth = depth

		self.cachedPosition = None
		self.cachedNormal = None

	def getPosition(self):
		if (self.cachedPosition == None):
			self.cachedPosition = (self.origin + self.depth * self.direction)

		return self.cachedPosition

	def getNormal(self):
		if (self.cachedNormal == None):
			self.cachedNormal = self.surface.getNormal(self.getPosition())

		return self.cachedNormal
