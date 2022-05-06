from Light import Light
from NeuralNetworkMaterial import NeuralNetworkMaterial
from PathTracingMaterial import PathTracingMaterial
from Scene import Scene
from SphereSurface import SphereSurface
from TriangleSurface import TriangleSurface
from Vector3 import Vector3

class SceneConstructor:
	def __init__(self, usePathTracing):
		self.scene = Scene()

		self.scene.addLight(Light(Vector3(0, 1.5, 2), [1.0, 1.0, 1.0]))
		#self.scene.addLight(Light(Vector3(3, 3, 2.9), [1.0, 1.0, 1.0]))

		if usePathTracing:
			sampleCount = 64

			leftMaterial = PathTracingMaterial(
				[1.0, 0.0, 0.0], self.scene, sampleCount
			)
			rightMaterial = PathTracingMaterial(
				[0.0, 1.0, 0.0], self.scene, sampleCount
			)
			centerMaterial = PathTracingMaterial(
				[0.75, 0.75, 0.75], self.scene, sampleCount
			)
			floorMaterial = PathTracingMaterial(
				[0.75, 0.75, 0.75], self.scene, sampleCount
			)
			ceilingMaterial = PathTracingMaterial(
				[0.75, 0.75, 0.75], self.scene, sampleCount
			)
			sphereMaterial = PathTracingMaterial(
				[0.75, 0.75, 0.75], self.scene, sampleCount
			)
		else:
			leftMaterial = NeuralNetworkMaterial(
				[1.0, 0.0, 0.0], self.scene, "models/leftWall.pkl"
			)
			rightMaterial = NeuralNetworkMaterial(
				[0.0, 1.0, 0.0], self.scene, "models/rightWall.pkl"
			)
			centerMaterial = NeuralNetworkMaterial(
				[0.75, 0.75, 0.75], self.scene, "models/centerWall.pkl"
			)
			floorMaterial = NeuralNetworkMaterial(
				[0.75, 0.75, 0.75], self.scene, "models/floor.pkl"
			)
			ceilingMaterial = NeuralNetworkMaterial(
				[0.75, 0.75, 0.75], self.scene, "models/ceiling.pkl"
			)
			sphereMaterial = NeuralNetworkMaterial(
				[0.75, 0.75, 0.75], self.scene, "models/sphere.pkl"
			)

		self.scene.addSurface(
			SphereSurface(sphereMaterial, Vector3(0, -1, 4), 1.0)
		)

		# left wall
		self.scene.addSurface(TriangleSurface(
			leftMaterial, Vector3(-2, 2, 3), Vector3(-2, -2, 3),
			Vector3(-2, -2, 5)
		))
		self.scene.addSurface(TriangleSurface(
			leftMaterial, Vector3(-2, 2, 3), Vector3(-2, -2, 5),
			Vector3(-2, 2, 5)
		))

		# right wall
		self.scene.addSurface(TriangleSurface(
			rightMaterial, Vector3(2, 2, 5), Vector3(2, -2, 5),
			Vector3(2, -2, 3)
		))
		self.scene.addSurface(TriangleSurface(
			rightMaterial, Vector3(2, 2, 5), Vector3(2, -2, 3),
			Vector3(2, 2, 3)
		))

		# center wall
		self.scene.addSurface(TriangleSurface(
			centerMaterial, Vector3(-2, 2, 5), Vector3(-2, -2, 5),
			Vector3(2, -2, 5)
		))
		self.scene.addSurface(TriangleSurface(
			centerMaterial, Vector3(-2, 2, 5), Vector3(2, -2, 5),
			Vector3(2, 2, 5)
		))

		# floor
		self.scene.addSurface(TriangleSurface(
			floorMaterial, Vector3(-2, -2, 5), Vector3(-2, -2, 3),
			Vector3(2, -2, 3)
		))
		self.scene.addSurface(TriangleSurface(
			floorMaterial, Vector3(-2, -2, 5), Vector3(2, -2, 3),
			Vector3(2, -2, 5)
		))

		# ceiling
		self.scene.addSurface(TriangleSurface(
			ceilingMaterial, Vector3(-2, 2, 3), Vector3(-2, 2, 5),
			Vector3(2, 2, 5)
		))
		self.scene.addSurface(TriangleSurface(
			ceilingMaterial, Vector3(-2, 2, 3), Vector3(2, 2, 5),
			Vector3(2, 2, 3)
		))
