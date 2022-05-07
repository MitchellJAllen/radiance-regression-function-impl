import numpy
import pickle
import torch

from BlinnPhongMaterial import BlinnPhongMaterial
from Material import Material
from Vector3 import Vector3

class NeuralNetworkMaterial(BlinnPhongMaterial):
	def __init__(self, color, scene, networkFilePath):
		super().__init__(color, scene)
		self.network = None

		with open(networkFilePath, "rb") as dataFile:
			self.network = pickle.load(dataFile)

	def getIndirectLighting(self, position, normal, light):
		networkInput = numpy.array([[
			position.x, position.y, position.z,
			normal.x, normal.y, normal.z,
			light.position.x, light.position.y, light.position.z
		]])

		networkInput = torch.tensor(networkInput).float()

		with torch.no_grad():
			networkOutput = self.network(networkInput)[0, :]

		indirectLighting = [
			networkOutput[0] * light.color[0],
			networkOutput[1] * light.color[1],
			networkOutput[2] * light.color[2]
		]

		return indirectLighting
