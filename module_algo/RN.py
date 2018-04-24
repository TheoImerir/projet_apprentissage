from Neurone import *
from random import *
from math import * 

def RN:

	####################################### DECLARE VARIABLES ##############################
	nbNeurones = 10
	nbLayers = 1
	nbOutput = 10
	nbInput = 14
	learningRate = 0.1
	expertValue = 0 # TODO
	
	inputTab = [] # all inputs
	neuronesTab = [] # Tab containing all neurones for all layout
	outputTab = [] # Tab containing all 10 neurones, representing the outputs

	# All of this is used to change weights of neurones
	errorTab = [] # Tab containing errors calculated with the output neurones
	expectResultTab = [] # Tab with value of 0 or 1. Value is 1 if index = expert value

	######################################### INITIALISATION ################################
	# This will be used later when using multiple layers
	#for i in range(nbLayers):
	#	layerTab = []
	#	for j in range(nbNeurones):
	#		layerTab.append(Neurone(0))
	#	neuronesTab.append(layerTab)

	# Initialize input tab
	for i in range(nbInput):
		inputTab.append(i)
		#TODO: Get value from DB or calculate them from a matrix

	# initialize FIRST layer
	for i in range(nbNeurones):
		neuronesTab.append(Neurone(nbInput))

	# Initialize all output
	for i in range(nbOutput):
		outputTab.append(Neurone(nbNeurones))

	# Initialize both errorTab and expectedResultTab, there size is equal to outputTab (nbOutput)
	for i in range(nbOutput):
		errorTab.append(0)
		expectResultTab.append(0)

	######################################### CALCULATION START ##############################
	# For each neurones we calculate it's output
	for neurone in nbNeurones:
		neurone.calculateOutputFromValue(inputTab)

	# For each output we calculate it's weight and apply sigmoide
	for o in outputTab:
		o.calculateOutputFromNeurone(neuronesTab)

	# Get the neuronne with the highest value
	bestNeuroneOutput = 0 # Value can be between 0 and 1, we set it to the minimum
	bestNeuroneIndex = 0
	for i in range(len(outputTab)):
		if(outputTab[i].output > bestNeuroneOutput):
			bestNeuroneOutput = outputTab[i].output
			bestNeuroneIndex = i
	print("Result of RN: {0}".format(i))

	for i in range(nbOutput):
		if(i == expertValue):
			# Set to 1 if expert and result given by RN match
			expectedResultTab[i] = 1

	for i in range(nbOutput):
		errorTab[i] = 0.5 * pow(expectedResultTab[i] - outputTab[i].output,2)

	##################################### CORRECTION OF WEIGHTS ##################################


	####################################### RESET EXPECTED VALUE TAB AND ERRORS TAB ################