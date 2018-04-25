from Neurone import *
from random import *
from math import * 
from image import *
from func import *
def RN():

	####################################### DECLARE VARIABLES ##############################
	nbNeurones = 10
	nbLayers = 1
	nbOutput = 10
	nbInput = 14
	learningRate = 0.1
	expertValue = image.value

	inputsTab = [] # all inputs
	neuronesTab = [] # Tab containing all neurones for all layout
	neuronesTabCorrection = [] # Tab containing all correction for neurones
	outputsTab = [] # Tab containing all 10 neurones, representing the outputs
	outputsTabCorrection = [] # Tab containing correction for all neurones 

	# All of this is used to change weights of neurones
	errorTab = [] # Tab containing errors calculated with the output neurones
	expectResultTab = [] # Tab with value of 0 or 1. Value is 1 if index = expert value

	imageList  = Utils.getImageList()
	######################################### INITIALISATION ################################

	for image in imageList:
		for i in range(6):
			sumCol.append(image.sumColumn(i))
		for i in range(8):
			sumLin.append(image.sumLine(i))

		# Initialize input tab
		for i in range(6):
			inputsTab.append(sumLin[i])
		for i in range(8):
			inputsTab.append(sumCol[i])

		# This will be used later when using multiple layers
		#for i in range(nbLayers):
		#	layerTab = []
		#	for j in range(nbNeurones):
		#		layerTab.append(Neurone(0))
		#	neuronesTab.append(layerTab)

		# initialize FIRST layer
		for i in range(nbNeurones):
			neuronesTab.append(Neurone(nbInput))
			neuronesTabCorrection.append(nbInput)

		# Initialize all output
		for i in range(nbOutput):
			outputsTab.append(Neurone(nbNeurones))
			outputsTabCorrection.append(nbNeurones)

		# Initialize both errorTab and expectedResultTab, there size is equal to outputsTab (nbOutput)
		for i in range(nbOutput):
			errorTab.append(0)
			expectResultTab.append(0)

		######################################### CALCULATION START ##############################
		# For each neurones we calculate it's output
		for neurone in nbNeurones:
			neurone.calculateOutputFromValue(inputsTab)

		# For each output we calculate it's weight and apply sigmoide
		for o in outputsTab:
			o.calculateOutputFromNeurone(neuronesTab)

		# Get the neuronne with the highest value
		bestNeuroneOutput = 0 # Value can be between 0 and 1, we set it to the minimum
		bestNeuroneIndex = 0
		for i in range(len(outputsTab)):
			if(outputsTab[i].output > bestNeuroneOutput):
				bestNeuroneOutput = outputsTab[i].output
				bestNeuroneIndex = i

		# Print both expert and RN value		
		print("Expert value: {0}".format(expertValue))
		print("RN value: {0}".format(bestNeuroneIndex))

		for i in range(nbOutput):
			if(i == expertValue):
				# Set to 1 if expert and result given by RN match
				expectedResultTab[i] = 1

		for i in range(nbOutput):
			errorTab[i] = -(expectedResultTab[i] - outputsTab[i].output) * outputsTab[i].output * (1 - outputsTab[i].output)

		##################################### CALCULATE CORRECTION OF WEIGHTS ##################################
		# Calculate the correction for each weight of the output neurones
		for i in range(nbOutput):
			for j in range(nbNeurones):
				outputsTabCorrection[i].weightTab[j] = outputsTab[i].weightTab[j] - (neuronesTab[j].output * errorTab[i] * learningRate)

		# Calculate a value that will be used to re-adjust weights for layers of neurones
		correction = []
		for i in range(nbNeurones):
			temp = []
			for j in range(nbOutput):
				temp.append(outputsTab[j].weightTab[i])
			correction.append(calculateMatrixMultiplication(temp,transposeMatrix(outputsTab)))

		# Change the value that will be used to re-adjust weights for layers of neurones
		for i in range(nbNeurones):
			correction[i] = correction[i] * neuronesTab[i].output * (1 - neuronesTab[i].output)

		# Calculate the correction for each weight of the "central" (first layer) neurones
		for i in range(nbNeurones):
			for j in range(nbInput):
				neuronesTabCorrection[i].weightTab[j] = neuronesTab[i].weightTab[j] - (inputsTab[j] * correction[i] * learningRate)

		##################################### APPLY CORRECTION OF WEIGHTS ##################################
		for i in range(nbNeurones):
			for j in range(nbInput):
				neuronesTab[i].weightTab[j] = neuronesTabCorrection[i].weightTab[j]
		for i in range(nbOutput):
			for j in range(nbNeurones):
				outputsTab[i].weightTab[j] = outputsTabCorrection[i].weightTab[j]

		################################# RESET EXPECTED VALUE TAB AND ERRORS TAB ########################
		neuronesTabCorrection = []
		outputsTabCorrection = []
		expectedResultTab = []
		errorTab = []