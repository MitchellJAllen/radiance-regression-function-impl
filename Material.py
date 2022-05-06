import abc

class Material(abc.ABC):
	def __init__(self, color, scene):
		self.color = color
		self.scene = scene

	@abc.abstractmethod
	def getDirectLighting(self, position, normal, light):
		pass

	@abc.abstractmethod
	def getIndirectLighting(self, position, normal, light):
		pass

	def getCombinedLighting(self, position, normal):
		combinedLighting = [0.0, 0.0, 0.0]

		for light in self.scene.lights:
			directLighting = self.getDirectLighting(position, normal, light)
			indirectLighting = self.getIndirectLighting(position, normal, light)

			indirectLighting[0] *= self.color[0]
			indirectLighting[1] *= self.color[1]
			indirectLighting[2] *= self.color[2]

			combinedLighting[0] += directLighting[0] + indirectLighting[0]
			combinedLighting[1] += directLighting[1] + indirectLighting[1]
			combinedLighting[2] += directLighting[2] + indirectLighting[2]

		return combinedLighting
