from Neurone import *
from random import *
def RN:
	nbNeurones = 10
	nbLayers = 1
	inputTab = [] # Do not forget the "biais"
	neuronesTab = [] # Tab containing all neurones for all layout
	outputTab = [] # tab of size 10, from 0 to 9
	biais = 1;

	# This will be used later when using multiple layers
	#for i in range(nbLayers):
	#	layerTab = []
	#	for j in range(nbNeurones):
	#		layerTab.append(Neurone(0))
	#	neuronesTab.append(layerTab)

	# Initialize all output
	for i in range(10):
		outputTab.append(0)

	# initialize all neurones
	for i in range(nbNeurones):
		neuronesTab.append(Neurone(0))

	# Initialize input tab
	for i in range(6 + 8)
		inputTab.append(random())
		#TODO: Get value from DB or calculate them from a matrix

	# For each neurones we calculate it's output
	for neurone in nbNeurones:
		neurone.calculateOutput(inputTab)

	# For each output we calculate it's weight and apply sigmoide
	for o in outputTab:
		total = 0
		for n in neurones:

		sigmoide(x)
