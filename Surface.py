import abc

class Surface(abc.ABC):
	def __init__(self, material):
		self.material = material

	@abc.abstractmethod
	def getIntersection(self, origin, direction):
		pass

	@abc.abstractmethod
	def getNormal(self, position):
		pass

	@abc.abstractmethod
	def getSurfaceArea(self):
		pass

	@abc.abstractmethod
	def getRandomPoint(self):
		pass
