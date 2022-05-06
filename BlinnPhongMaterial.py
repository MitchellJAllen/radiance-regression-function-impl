from Material import Material

class BlinnPhongMaterial(Material):
	def __init__(self, color, scene):
		super().__init__(color, scene)

	def getDirectLighting(self, position, normal, light):
		lightVector = light.position - position

		lightDistance = lightVector.length()
		lightVector /= lightDistance

		shadowIntersection = self.scene.getIntersection(position, lightVector)

		if (
			shadowIntersection != None and
			shadowIntersection.depth < lightDistance
		):
			return [0, 0, 0]

		diffuse = max(0.0, normal.dot(lightVector))

		return [
			light.color[0] * self.color[0] * diffuse,
			light.color[1] * self.color[1] * diffuse,
			light.color[2] * self.color[2] * diffuse
		]

	def getIndirectLighting(self, position, normal, light):
		return [0.0, 0.0, 0.0]
