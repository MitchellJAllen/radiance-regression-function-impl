# radiance-regression-function-impl
My implementation of Radiance Regression Functions (Ren et al. 2013) for CS 6190

# Usage
This project requires the Python libraries PyTorch, Numpy, PIL, and "blitz-bayesian-pytorch".
To render the scene using path tracing, run the command `python renderPathTracing.py`
Rendering the scene using neural networks first requires generating data and training neural networks:
* To generate training data, run the command `python generateData.py`. This will create a file of 100,000 data points in the directory "data". This command can be run as many times as desired.
* To train the neural networks with the above data, run the command `python trainNeuralNetworks.py`. This will load all data generated from the previous step and train neural networks, which will be saved to the "models" directory.
* Finally, the command `python renderNeuralNetworks.py` can be run. It should produce a result similar to path tracing.

The scene can be reconfigured in the file "SceneConstructor.py". Specifically, lights can be added, deleted, moved, or re-colored without having to regenerate the above neural networks.
