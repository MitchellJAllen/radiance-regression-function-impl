import datetime
import numpy
import pickle
import random

from Light import Light
from SceneConstructor import SceneConstructor
from Vector3 import Vector3

usePathTracing = True

sceneConstructor = SceneConstructor(usePathTracing)
scene = sceneConstructor.scene

dataCount = 100000

data = numpy.zeros((dataCount, 12))

for dataIndex in range(dataCount):
	position, normal, surface = scene.getRandomPoint()
	light = Light(Vector3(0.0, 0.0, 0.0), [1.0, 1.0, 1.0])

	selector = 35.0 * random.random()

	if selector < 27.0:
		light.position.x = random.random() * 6.0 - 3.0
		light.position.y = random.random() * 6.0 - 3.0
		light.position.z = random.random() * 5.9 - 3.0
	else:
		light.position.x = random.random() * 3.8 - 1.9
		light.position.y = random.random() * 3.8 - 1.9
		light.position.z = random.random() * 1.9 + 3.0

	indirectLighting = surface.material.getIndirectLighting(
		position, normal, light
	)

	data[dataIndex, 0] = position.x
	data[dataIndex, 1] = position.y
	data[dataIndex, 2] = position.z

	data[dataIndex, 3] = normal.x
	data[dataIndex, 4] = normal.y
	data[dataIndex, 5] = normal.z

	data[dataIndex, 6] = light.position.x
	data[dataIndex, 7] = light.position.y
	data[dataIndex, 8] = light.position.z

	data[dataIndex, 9] = indirectLighting[0]
	data[dataIndex, 10] = indirectLighting[1]
	data[dataIndex, 11] = indirectLighting[2]

timeSuffix = datetime.datetime.now().strftime("_%Y%m%d%H%M%S")
fileName = "data/data" + timeSuffix + ".pkl"

with open(fileName, "wb") as dataFile:
    pickle.dump(data, dataFile)
