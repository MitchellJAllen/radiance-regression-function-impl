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

def loadData(filePath):
	data = None

	with open(filePath, "rb") as dataFile:
		data = pickle.load(dataFile)

	return data

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

	leftWallIndices = []
	rightWallIndices = []
	centerWallIndices = []
	floorIndices = []
	ceilingIndices = []
	sphereIndices = []
	unclassifiedIndices = []

	for rowIndex in range(rowCount):
		rowData = data[rowIndex : rowIndex + 1, :]

		if isLeftWallPosition(rowData[0, :]):
			leftWallIndices.append(rowIndex)
		elif isRightWallPosition(rowData[0, :]):
			rightWallIndices.append(rowIndex)
		elif isCenterWallPosition(rowData[0, :]):
			centerWallIndices.append(rowIndex)
		elif isFloorPosition(rowData[0, :]):
			floorIndices.append(rowIndex)
		elif isCeilingPosition(rowData[0, :]):
			ceilingIndices.append(rowIndex)
		elif isSpherePosition(rowData[0, :]):
			sphereIndices.append(rowIndex)
		else:
			unclassifiedIndices.append(rowIndex)

	leftWallData = data[leftWallIndices, :]
	rightWallData = data[rightWallIndices, :]
	centerWallData = data[centerWallIndices, :]
	floorData = data[floorIndices, :]
	ceilingData = data[ceilingIndices, :]
	sphereData = data[sphereIndices, :]

	print("classifications:")
	print("left wall:", len(leftWallIndices)) # 131729 / 1M
	print("right wall:", len(rightWallIndices)) # 132127 / 1M
	print("center wall:", len(centerWallIndices)) # 264325 / 1M
	print("floor:", len(floorIndices)) # 132433 / 1M
	print("ceiling:", len(ceilingIndices)) # 132280 / 1M
	print("sphere:", len(sphereIndices)) # 207106 / 1M
	print("unclassified:", len(unclassifiedIndices)) # 0 / 1M

	return [
		leftWallData, rightWallData, centerWallData,
		floorData, ceilingData, sphereData
	]

def trainAndSaveNetwork(
	data, testCount, batchSize, hiddenNodes, epochCount, filePath
):
	trainCount = data.shape[0] - testCount
	batchCount = math.ceil(trainCount / batchSize)

	featureCount = 9

	x_train = torch.tensor(data[:trainCount, :featureCount]).float()
	y_train = torch.tensor(data[:trainCount, featureCount:]).float()

	x_test = torch.tensor(data[trainCount:, :featureCount]).float()
	y_test = torch.tensor(data[trainCount:, featureCount:]).float()

	model = torch.nn.Sequential(
		blitz.modules.BayesianLinear(9, hiddenNodes),
		torch.nn.ReLU(),
		blitz.modules.BayesianLinear(hiddenNodes, hiddenNodes),
		torch.nn.ReLU(),
		blitz.modules.BayesianLinear(hiddenNodes, 3)
	)

	optimizer = torch.optim.Adam(model.parameters(), lr = 0.01)
	criterion = torch.nn.MSELoss()

	for epoch in range(epochCount):
		for batch in range(trainCount // batchSize):
			x_batch = x_train[batch * batchSize : (batch + 1) * batchSize, :]
			y_batch = y_train[batch * batchSize : (batch + 1) * batchSize, :]

			optimizer.zero_grad()
			loss = criterion(model(x_batch), y_batch)

			loss.backward()
			optimizer.step()

	p = model(x_test)

	print("MSE loss for", filePath, ":", criterion(y_test, p).item())

	with open(filePath, "wb") as dataFile:
		pickle.dump(model, dataFile)

dataPath = "data/"
dataFileNames = os.listdir(dataPath)

data = numpy.empty((0, 12))

for dataFileName in dataFileNames:
	if dataFileName == "README.md":
		continue

	dataFilePath = dataPath + dataFileName
	loadedData = loadData(dataFilePath)

	data = numpy.append(data, loadedData, axis = 0)

filteredData = filterData(data)

leftWallData = filteredData[0]
rightWallData = filteredData[1]
centerWallData = filteredData[2]
floorData = filteredData[3]
ceilingData = filteredData[4]
sphereData = filteredData[5]

testCount = 1000
batchSize = 250
hiddenNodes = 20
epochCount = 32

print("networks:")

trainAndSaveNetwork(
	leftWallData, testCount, batchSize, hiddenNodes, epochCount,
	"models/leftWall.pkl"
)
trainAndSaveNetwork(
	rightWallData, testCount, batchSize, hiddenNodes, epochCount,
	"models/rightWall.pkl"
)
trainAndSaveNetwork(
	centerWallData, testCount, batchSize, hiddenNodes, epochCount,
	"models/centerWall.pkl"
)
trainAndSaveNetwork(
	floorData, testCount, batchSize, hiddenNodes, epochCount,
	"models/floor.pkl"
)
trainAndSaveNetwork(
	ceilingData, testCount, batchSize, hiddenNodes, epochCount,
	"models/ceiling.pkl"
)
trainAndSaveNetwork(
	sphereData, testCount, batchSize, hiddenNodes, epochCount,
	"models/sphere.pkl"
)
