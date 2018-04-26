from Neurone import *
from random import *
from math import * 
from image import *
from func import *


layersTab = [] # All layers of neurones
nbNeurones = 10
nbLayers = 1
nbOutput = 10
nbInput = 14

def RN(correctionOrNot):
    ####################################### DECLARE VARIABLES ##############################
    learningRate = 0.1
    expertValue = 0

    # Stats
    totalTry = 0
    totalSuccess = 0
    totalFail = 0
    successRate = 0.0
    failRate = 0.0

    global layersTab
    global nbNeurones
    global nbLayers
    global nbOutput
    global nbInput 

    inputsTab = [] # all inputs
    layersTabCorrection = [] # Correction for all layers of neurones
    neuronesTab = [] # Tab containing all neurones for a layout
    neuronesTabCorrection = [] # Tab containing all correction for neurones

    # All of this is used to change weights of neurones
    layersErrorTab = [] # Tab containing errors calculated with the output neurones
    expectedResultTab = [] # Tab with value of 0 or 1. Value is 1 if index = expert value

    imageList  = Utils.getImageList()
    ######################################### INITIALISATION ###############################
    
    # Initialize expectedResultTab
    for i in range(nbOutput):
        expectedResultTab.append(0)     
    
    index = 0
    for img in imageList:
        index += 1
        if(index > 1):
            break
        # reset inputs for each images
        inputsTab = []
        sumCol = []
        sumLin = []
        
        expertValue = img.value
        for i in range(6):
            sumCol.append(img.sumColumn(i))
        for i in range(8):
            sumLin.append(img.sumLine(i))

        # Initialize input tab
        for i in range(6):
            inputsTab.append(sumCol[i])
        for i in range(8):
            inputsTab.append(sumLin[i])

        ######################################### CALCULATION START ##############################
        # Calculate output for first layer of neurones
        for neurone in layersTab[0]:
            neurone.calculateOutputFromValue(inputsTab)

        # Calculate output for each next layers
        for i in range(nbLayers - 1):
            for neurone in layersTab[i + 1]:
                neurone.calculateOutputFromNeurone(layersTab[i])
        
        # Calculate output for last layer of neurones (this last layers is called outputs)
        for neurone in layersTab[nbLayers]:
            neurone.calculateOutputFromNeurone(layersTab[nbLayers - 1])

        # Get the neuronne with the highest value
        bestNeuroneOutput = 0 # Value can be between 0 and 1, we set it to the minimum
        bestNeuroneIndex = 0
        for i in range(nbOutput):
            if(layersTab[nbLayers][i].output > bestNeuroneOutput):
                bestNeuroneOutput = layersTab[nbLayers][i].output
                bestNeuroneIndex = i

        # Print both expert and RN value        
        #print("Expert value: {0}".format(expertValue))
        #print("RN value: {0}".format(bestNeuroneIndex))
        if expertValue == bestNeuroneIndex:
            totalSuccess += 1
        else:
            totalFail += 1

        totalTry += 1

        # If we do not apply correction to the RN, we skip the correction of weights
        if(correctionOrNot == 0):
            continue
                    
        ##################################### CALCULATE CORRECTION OF WEIGHTS ##################################
        # This is always done this order: outputs -> central layers -> first layer
        ############### OUTPUT #############
        for i in range(nbOutput):
            if(i == expertValue):
                # Set to 1 if expert and result given by RN match
                expectedResultTab[i] = 1

        temp = []
        for i in range(nbOutput):
            temp.append(-(expectedResultTab[i] - layersTab[nbLayers][i].output) * layersTab[nbLayers][i].output * (1 - layersTab[nbLayers][i].output))
        layersErrorTab.append(temp)
            
        # Calculate the correction for each weight of the output neurones
        for i in range(nbOutput):
            neuronesTabCorrection.append(Neurone(nbNeurones))
            for j in range(nbNeurones):
                neuronesTabCorrection[i].weightTab[j] = layersTab[nbLayers][i].weightTab[j] - (layersTab[nbLayers-1][j].output * layersErrorTab[0][i] * learningRate)
       
        layersTabCorrection.append(neuronesTabCorrection)
        neuronesTabCorrection = []

        ############# CENTRAL LAYERS ################
        # For each "central layers", from the last (not counting the outputs one) to the first one
        for x in reversed(range(nbLayers)):
            # First layer is not calculated here
            if(x == 0):
                continue
            # Calculate a value that will be used to re-adjust weights for layers of neurones
            correction = []
            for i in range(nbNeurones):
                temp = []
                for j in range(len(layersTab[x+1])):
                    temp.append(layersTab[x+1][j].weightTab[i])
                correction.append(Neurone.calculateMatrixMultiplication(temp,Neurone.transposeMatrix(layersErrorTab[(nbLayers - x) - 1])))

            # Change the value that will be used to re-adjust weights for layers of neurones
            for i in range(nbNeurones):
                correction[i] = correction[i] * layersTab[x][i].output * (1 - layersTab[x][i].output)

            layersErrorTab.append(correction)

            # Calculate the correction for each weight of the "central" (first layer) neurones
            for i in range(nbNeurones):
                neuronesTabCorrection.append(Neurone(nbNeurones))
                for j in range(nbNeurones):
                    neuronesTabCorrection[i].weightTab[j] = layersTab[x][i].weightTab[j] - (layersTab[x-1][j].output * correction[i] * learningRate)
            
            layersTabCorrection.append(neuronesTabCorrection)
            neuronesTabCorrection = []

        ############# FIRST LAYER #################
        # Calculate a value that will be used to re-adjust weights for layers of neurones
        correction = []
        for i in range(nbNeurones):
            temp = []
            for j in range(nbNeurones):
                temp.append(layersTab[1][j].weightTab[i])
            correction.append(Neurone.calculateMatrixMultiplication(temp,Neurone.transposeMatrix(layersErrorTab[1])))

        # Change the value that will be used to re-adjust weights for layers of neurones
        for i in range(nbNeurones):
            correction[i] = correction[i] * layersTab[0][i].output * (1 - layersTab[0][i].output)

        # Calculate the correction for each weight of the "central" (first layer) neurones
        for i in range(nbNeurones):
            neuronesTabCorrection.append(Neurone(nbInput))
            for j in range(nbInput):
                neuronesTabCorrection[i].weightTab[j] = layersTab[0][i].weightTab[j] - (inputsTab[j] * correction[i] * learningRate)

        layersTabCorrection.append(neuronesTabCorrection)
        neuronesTabCorrection = []
        ##################################### APPLY CORRECTION OF WEIGHTS ##################################
    
        #print("==================")
        #for i in range(nbNeurones):
        #    print(layersTabCorrection[0][0].weightTab[i])
        
        for i in range(nbLayers + 1):
            layersTab[i] = layersTabCorrection[(nbLayers) - i]
            
        #print("==================")
        #for i in range(nbNeurones):
        #    print(layersTab[nbLayers][0].weightTab[i])
            
        layersTabCorrection = []

    successRate = (totalSuccess / totalTry) * 100
    failRate = (totalFail / totalTry) * 100
    print("===================")
    print("total try: ",totalTry)
    print("succes: ", totalSuccess)
    print("fail: ", totalFail)
    print("success rate: ", successRate)
    print("fail rate: ", failRate)
    print("===================")
            
def initRN():
    # Initialize all layers
    global layersTab
    global nbNeurones
    global nbLayers
    global nbOutput
    global nbInput
    neuronesTab = []
    
    for i in range(nbLayers):
        neuronesTab = []
        for j in range(nbNeurones):
            preced = 0
            if i == 0:
                preced = nbInput
            else :
                preced = nbNeurones
            neuronesTab.append(Neurone(preced))
        layersTab.append(neuronesTab)

    # Initialize all output
    neuronesTab = []
    for i in range(nbOutput):
        neuronesTab.append(Neurone(nbNeurones))
    layersTab.append(neuronesTab) 
           
def loadRNWeights():
    return 0

def startRN(iteration):
    initRN()
    for i in range(iteration):
        print("Iteration: ",i + 1)
        #for i in range(nbNeurones):
        #    print(layersTab[0][0].weightTab[i])
        print("=================================================")
        for i in range(nbNeurones):
            print(layersTab[nbLayers][0].weightTab[i])
        RN(1)
