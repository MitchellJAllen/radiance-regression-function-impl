import math
import PIL.Image
import PIL.ImageTk
import threading
import tkinter

from Vector3 import Vector3

class MultiThreadedRenderer:
	def __init__(
		self, imageWidth, imageHeight, fieldOfView, scene, threadCount,
		updateDelay, backgroundColor
	):
		self.imageWidth = imageWidth
		self.imageHeight = imageHeight
		self.image = PIL.Image.new(mode="RGB", size=(imageWidth, imageHeight))

		self.fieldOfView = fieldOfView * (math.pi / 180.0)
		self.gamma = 1.0 / 2.2

		self.scene = scene
		self.threadCount = threadCount
		self.updateDelay = updateDelay
		self.backgroundColor = backgroundColor

		self.root = tkinter.Tk()
		self.label = tkinter.Label(self.root)
		self.label.pack()

	def updateImage(self):
		imageWrap = PIL.ImageTk.PhotoImage(self.image)

		self.label.configure(image = imageWrap)
		self.label.image = imageWrap

		self.root.after(self.updateDelay, self.updateImage)

	def processColor(self, colorComponent):
		return int(255.0 * pow(max(0.0, min(1.0, colorComponent)), self.gamma))

	def threadFunction(self, threadId):
		offsetZ = math.tan((math.pi - self.fieldOfView) / 2.0)
		scaleY = -self.imageHeight / self.imageWidth

		pixelCount = self.imageWidth * self.imageHeight

		for index in range(threadId, pixelCount, self.threadCount):
			xIndex = index % self.imageWidth
			yIndex = index // self.imageWidth

			x = (2.0 * xIndex + 1.0) / self.imageWidth - 1.0
			y = (2.0 * yIndex + 1.0) / self.imageHeight - 1.0

			origin = Vector3(0, 0, -offsetZ)
			direction = Vector3(x, scaleY * y, offsetZ)

			intersection = self.scene.getIntersection(origin, direction)
			color = self.backgroundColor

			if intersection != None:
				color = intersection.surface.material.getCombinedLighting(
					intersection.getPosition(), intersection.getNormal()
				)

			finalRed = self.processColor(color[0])
			finalGreen = self.processColor(color[1])
			finalBlue = self.processColor(color[2])

			self.image.putpixel(
				(xIndex, yIndex), (finalRed, finalGreen, finalBlue)
			)

	def start(self):
		threads = [None] * self.threadCount

		for threadId in range(0, self.threadCount):
			threads[threadId] = threading.Thread(
				target = self.threadFunction, args = (threadId,)
			)
			threads[threadId].start()

		self.updateImage()
		self.root.mainloop()

		for thread in threads:
			thread.join()
