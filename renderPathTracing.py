from MultiThreadedRenderer import MultiThreadedRenderer
from SceneConstructor import SceneConstructor

imageWidth = 640
imageHeight = 360

fieldOfView = 90

threadCount = 12
updateDelay = 1000

usePathTracing = True

sceneConstructor = SceneConstructor(usePathTracing)
testScene = sceneConstructor.scene

backgroundColor = [0.0, 0.0, 0.5]

renderer = MultiThreadedRenderer(
	imageWidth, imageHeight, fieldOfView, testScene, threadCount, updateDelay,
	backgroundColor
)

renderer.start()
