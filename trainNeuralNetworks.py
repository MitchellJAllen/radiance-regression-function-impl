import math
import numpy
import os
import pickle

import torch
import torch.nn
import torch.nn.functional
import torch.optim

import blitz.modules
import blitz.utils

epsilon = 1e-7

def isLeftWallPosition(rowData):
	return (
		abs(rowData[0] - -2.0) < epsilon and
		rowData[1] > (-2.0 - epsilon) and rowData[1] < (+2.0 + epsilon) and
		rowData[2] > (+3.0 - epsilon) and rowData[2] < (+5.0 + epsilon)
	)

def isRightWallPosition(rowData):
	return (
		abs(rowData[0] - +2.0) < epsilon and
		rowData[1] > (-2.0 - epsilon) and rowData[1] < (+2.0 + epsilon) and
		rowData[2] > (+3.0 - epsilon) and rowData[2] < (+5.0 + epsilon)
	)

def isCenterWallPosition(rowData):
	return (
		rowData[0] > (-2.0 - epsilon) and rowData[0] < (+2.0 + epsilon) and
		rowData[1] > (-2.0 - epsilon) and rowData[1] < (+2.0 + epsilon) and
		abs(rowData[2] - +5.0) < epsilon
	)

def isFloorPosition(rowData):
	return (
		rowData[0] > (-2.0 - epsilon) and rowData[0] < (+2.0 + epsilon) and
		abs(rowData[1] - -2.0) < epsilon and
		rowData[2] > (+3.0 - epsilon) and rowData[2] < (+5.0 + epsilon)
	)

def isCeilingPosition(rowData):
	return (
		rowData[0] > (-2.0 - epsilon) and rowData[0] < (+2.0 + epsilon) and
		abs(rowData[1] - +2.0) < epsilon and
		rowData[2] > (+3.0 - epsilon) and rowData[2] < (+5.0 + epsilon)
	)

def isSpherePosition(rowData):
	xDiff = rowData[0] - 0.0
	yDiff = rowData[1] - -1.0
	zDiff = rowData[2] - +4.0

	return (xDiff * xDiff + yDiff * yDiff + zDiff * zDiff) < (1.0 + epsilon)

def filterData(data):
	rowCount = data.shape[0]

	leftWallCount = 0
	rightWallCount = 0
	centerWallCount = 0
	floorCount = 0
	ceilingCount = 0
	sphereCount = 0
	unclassifiedCount = 0

	leftWallData = numpy.empty((0, 12))
	rightWallData = numpy.empty((0, 12))
	centerWallData = numpy.empty((0, 12))
	floorData = numpy.empty((0, 12))
	ceilingData = numpy.empty((0, 12))
	sphereData = numpy.empty((0, 12))

	for rowIndex in range(rowCount):
		rowData = data[rowIndex : rowIndex + 1, :]

		if isLeftWallPosition(rowData[0, :]):
			leftWallCount += 1
			leftWallData = numpy.append(leftWallData, rowData, axis = 0)
		elif isRightWallPosition(rowData[0, :]):
			rightWallCount += 1
			rightWallData = numpy.append(rightWallData, rowData, axis = 0)
		elif isCenterWallPosition(rowData[0, :]):
			centerWallCount += 1
			centerWallData = numpy.append(centerWallData, rowData, axis = 0)
		elif isFloorPosition(rowData[0, :]):
			floorCount += 1
			floorData = numpy.append(floorData, rowData, axis = 0)
		elif isCeilingPosition(rowData[0, :]):
			ceilingCount += 1
			ceilingData = numpy.append(ceilingData, rowData, axis = 0)
		elif isSpherePosition(rowData[0, :]):
			sphereCount += 1
			sphereData = numpy.append(sphereData, rowData, axis = 0)
		else:
			unclassifiedCount += 1

	print("left:", leftWallCount, leftWallData.shape) # 26114 / 200K
	print("right:", rightWallCount, rightWallData.shape) # 26622 / 200K
	print("center:", centerWallCount, centerWallData.shape) # 52850 / 200K
	print("floor:", floorCount, floorData.shape) # 26342 / 200K
	print("ceiling:", ceilingCount, ceilingData.shape) # 26300 / 200K
	print("sphere:", sphereCount, sphereData.shape) # 41772 / 200K
	print("unclassified:", unclassifiedCount) # 0 / 200K

def loadData(filePath):
	data = None

	with open(filePath, "rb") as dataFile:
		data = pickle.load(dataFile)

	return data

dataPath = "data/"
dataFileNames = os.listdir(dataPath)

data = numpy.empty((0, 12))

for dataFileName in dataFileNames:
	if dataFileName == "README.md":
		continue

	dataFilePath = dataPath + dataFileName
	loadedData = loadData(dataFilePath)

	data = numpy.append(data, loadedData, axis = 0)

print(data.shape)

filterData(data)

testCount = 1000
trainCount = data.shape[0] - testCount

batchSize = 250
batchCount = math.ceil(trainCount / batchSize)

featureCount = 9

x_train = torch.tensor(data[:trainCount, :featureCount]).float()
y_train = torch.tensor(data[:trainCount, featureCount:]).float()

x_test = torch.tensor(data[trainCount:, :featureCount]).float()
y_test = torch.tensor(data[trainCount:, featureCount:]).float()

print(x_train.size())
print(y_train.size())

print(x_test.size())
print(y_test.size())

hiddenNodes = 20

model = torch.nn.Sequential(
	blitz.modules.BayesianLinear(9, hiddenNodes),
	torch.nn.ReLU(),
	blitz.modules.BayesianLinear(hiddenNodes, hiddenNodes),
	torch.nn.ReLU(),
	blitz.modules.BayesianLinear(hiddenNodes, 3)
)

optimizer = torch.optim.Adam(model.parameters(), lr = 0.01)
criterion = torch.nn.MSELoss()

for epoch in range(32):
	for batch in range(trainCount // batchSize):
		x_batch = x_train[batch * batchSize : (batch + 1) * batchSize, :]
		y_batch = y_train[batch * batchSize : (batch + 1) * batchSize, :]

		optimizer.zero_grad()
		loss = criterion(model(x_batch), y_batch)

		loss.backward()
		optimizer.step()

p = model(x_test)

print(p.size())
print(criterion(y_test, p))

with open("models/test.pkl", "wb") as dataFile:
	pickle.dump(model, dataFile)
