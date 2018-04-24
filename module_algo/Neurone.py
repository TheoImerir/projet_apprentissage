from math import *
from random import *

class Neurone:
	def __init__(self, output):
		# Generate random value between -1 and 1
        self.weight = (random()*2) - 1
        self.output = output

	def calculateOutput(self,inputTab):
		total = 0
		for i in inputTab:
			total += self.weight * i
		result = sigmoide(total)
		return result

	def correctWeight(self,correction):
		weight -= correction

	def calculateCorrection(self,correctRate,value):
		# TODO: calculate the correction to apply depending on correctRate and previous values
		return 0
	
	def sigmoide(input):
	temp = 1/(1+exp(-input))
	return temp