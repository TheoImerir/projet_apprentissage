from math import *
from random import *

class Neurone:
	def __init__(self, nbPreced):
        self.output = 0
        self.weightTab = []
        for i in range(nbPreced):
			# Generate random value between -1 and 1
        	self.weightTab[].append((random()*2) - 1)

	def calculateOutputFromValue(self,inputTab):
		total = 0
		for i in range(len(inputTab)):
			total += self.weight[i] * inputTab[i]
		result = sigmoide(total)
		self.output = result

	def calculateOutputFromNeurone(self,neuronesTab):
		total = 0
		for i in range(len(neuronesTab)):
			total += self.weight[i] * neuronesTab[i].output 
		result = sigmoide(total)
		self.output = result

	def correctWeight(self,correction):
		weight -= correction

	def calculateCorrection(self,correctRate,value):
		# TODO: calculate the correction to apply depending on correctRate and previous values
		return 0
	
	def sigmoide(input):
	temp = 1/(1+exp(-input))
	return temp