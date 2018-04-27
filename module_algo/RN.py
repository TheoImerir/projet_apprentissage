from Neurone import *
from random import *
from math import * 
from image import *
from func import *


layersTab = [] # All layers of neurones
nbNeurones = 20
nbLayers = 1
nbOutput = 10
nbInput = 14 + 1

def RN(correctionOrNot,imageLimit,debugLevel):
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

    # Pour choper dans la base de donnée
    #imageList  = Utils.getImageList()
    
    # Pour choper dans un fichier CSV
    imageList = Utils.getTestList('test.csv')
    ######################################### INITIALISATION ###############################
    
    # Initialize expectedResultTab
    for i in range(nbOutput):
        expectedResultTab.append(0)     
    
    index = 0
    for img in imageList:
        index += 1
        if((index > imageLimit) & (imageLimit > 0)):
            break

        if(debugLevel > 0):
            print("###############################################################################")
            print("Image N*:", index)
            print("###############################################################################")


        # reset inputs for each images
        inputsTab = []
        sumCol = []
        sumLin = []
        
        expertValue = img.value
        
        #for i in range(8):
        #    for j in range(6):
        #        inputsTab.append(img.matrix[i][j])

        for i in range(6):
            sumCol.append(img.sumColumn(i))
        for i in range(8):
            sumLin.append(img.sumLine(i))

        # Initialize input tab
        for i in range(6):
            inputsTab.append(sumCol[i])
        for i in range(8):
            inputsTab.append(sumLin[i])

        # Biais
        inputsTab.append(1)

        ######################################### CALCULATION START ##############################
        # Calculate output for first layer of neurones, EXCEPT for biais
        for i in range(nbNeurones):
            layersTab[0][i].calculateOutputFromValue(inputsTab)
            
        # Calculate output for each next layers except for output layer
        for i in range(nbLayers - 1):
            # Do not calculate biais
            for j in range(nbNeurones):
                # This will calculate output for each neurones EXCEPT biais
                layersTab[i + 1][j].calculateOutputFromNeurone(layersTab[i])
        
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

        if(debugLevel > 0):
            print("=====================================")
            print("outputs:")
            for i in range(nbOutput):
                print(layersTab[nbLayers][i].output)

        # Print both expert and RN value        
        if(debugLevel > 0):
            print("Expert value: {0}".format(expertValue))
            print("RN value: {0}".format(bestNeuroneIndex))
        
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
        if(debugLevel > 0):
            print("==================================")
            print("output layer:")

        for i in range(nbOutput):
            if(i == expertValue):
                # Set to 1 if expert and result given by RN match
                expectedResultTab[i] = 1

        temp = []
        for i in range(nbOutput):
            temp.append(-(expectedResultTab[i] - layersTab[nbLayers][i].output) * layersTab[nbLayers][i].output * (1 - layersTab[nbLayers][i].output))
        layersErrorTab.append(temp)
        
        # Calculate the correction for each weight of the output neurones EXCEPT BIAIS
        for i in range(nbOutput):
            neuronesTabCorrection.append(Neurone(nbNeurones + 1,0))
            for j in range(nbNeurones + 1):
                if(j == nbNeurones):
                    neuronesTabCorrection[i].weightTab[j] = layersTab[nbLayers][i].weightTab[j] - (0 * layersErrorTab[0][i] * learningRate)
                else:
                    neuronesTabCorrection[i].weightTab[j] = layersTab[nbLayers][i].weightTab[j] - (layersTab[nbLayers-1][j].output * layersErrorTab[0][i] * learningRate)

        layersTabCorrection.append(neuronesTabCorrection)
        neuronesTabCorrection = []

        if(debugLevel > 0):
            print("=====================================")
            print("Actual weights of output neurones:")
            for i in range(nbOutput):
                print(layersTab[nbLayers][i].weightTab)
            print("=====================================")
            print("Correction for outputs neurones:")
            for i in range(nbOutput):
                print(layersTabCorrection[0][i].weightTab)

        ############# CENTRAL LAYERS ################
        # For each "central layers", from the last (not counting the outputs one) to the first one
        if(debugLevel > 0):
            print("============================")
            print("Central layers")
        
        for x in reversed(range(nbLayers)):
            # First layer is not calculated here
            if(x == 0):
                continue

            if(debugLevel > 0):
                print("============================")
                print("layer: ", x)
            
            # Calculate a value that will be used to re-adjust weights for layers of neurones
            correction = []
            for i in range(nbNeurones):
                temp = []
                for j in range(len(layersTab[x+1]) - 1):
                    temp.append(layersTab[x+1][j].weightTab[i])
                correction.append(Neurone.calculateMatrixMultiplication(temp,Neurone.transposeMatrix(layersErrorTab[(nbLayers - x) - 1])))

            # Change the value that will be used to re-adjust weights for layers of neurones
            for i in range(nbNeurones):
                correction[i] = correction[i] * layersTab[x][i].output * (1 - layersTab[x][i].output)

            layersErrorTab.append(correction)
            
            # Calculate the correction for each weight of the "central" (first layer) neurones
            for i in range(nbNeurones):
                neuronesTabCorrection.append(Neurone(nbNeurones + 1,0))
                for j in range(nbNeurones + 1):
                    if(j == nbNeurones):
                        neuronesTabCorrection[i].weightTab[j] = layersTab[x][i].weightTab[j] - (1 * correction[i] * learningRate)
                    else:
                        neuronesTabCorrection[i].weightTab[j] = layersTab[x][i].weightTab[j] - (layersTab[x-1][j].output * correction[i] * learningRate)    

            layersTabCorrection.append(neuronesTabCorrection)
            neuronesTabCorrection = []

            if(debugLevel > 0):
                print("=====================================")
                print("Actual weights of central layer:")
                # Do not display for firstLayer ! This is why continue if i == 0
                for i in range(nbLayers):
                    if(i == 0):
                        continue
                    for j in range(nbNeurones):
                        print(layersTab[i][j].weightTab)
                print("=====================================")
                print("Correction for central layer :")
                for i in range(nbLayers):
                    if(i == 0):
                        continue    
                    for j in range(nbNeurones):
                        print(layersTabCorrection[nbLayers - i][j].weightTab)

        ############# FIRST LAYER #################
        # Calculate a value that will be used to re-adjust weights for layers of neurones
        if(debugLevel > 0):
            print("================================")
            print("First layer:")
        
        correction = []
        for i in range(nbNeurones):
            temp = []
            for j in range(len(layersTab[1]) - 1):
                temp.append(layersTab[1][j].weightTab[i])
            correction.append(Neurone.calculateMatrixMultiplication(temp,Neurone.transposeMatrix(layersErrorTab[nbLayers - 1])))

        if(debugLevel > 0):
            print("=========================")
            print("Correction tab (before):")
            print(correction)

        # Change the value that will be used to re-adjust weights for layers of neurones
        for i in range(nbNeurones):
            correction[i] = correction[i] * layersTab[0][i].output * (1 - layersTab[0][i].output)

        if(debugLevel > 0):
            print("=========================")
            print("Correction tab:")
            print(correction)

        # Calculate the correction for each weight of the first layer of neurones
        for i in range(nbNeurones):
            if(i == nbNeurones): # If this is biais
                    neuronesTabCorrection.append(Neurone(nbInput,1))
            else: # This is not the biais but a normal neurone
                    neuronesTabCorrection.append(Neurone(nbInput,0))
            for j in range(nbInput):
                neuronesTabCorrection[i].weightTab[j] = layersTab[0][i].weightTab[j] - (inputsTab[j] * correction[i] * learningRate)

        neuronesTabCorrection.append(Neurone(nbInput,1))
        layersTabCorrection.append(neuronesTabCorrection)
        neuronesTabCorrection = []

        if(debugLevel > 0):
            print("=====================================")
            print("ouputs of first layer:")
            for i in range(nbNeurones):
                print(layersTab[0][i].output)
            print("=====================================")
            print("Actual weights of first layer:")
            for i in range(nbNeurones):
                print(layersTab[0][i].weightTab)
            print("=====================================")
            print("Correction for first layer :")
            for j in range(nbNeurones):
                print(layersTabCorrection[nbLayers][j].weightTab) 

        ##################################### APPLY CORRECTION OF WEIGHTS #################################
        for i in range(nbLayers + 1):
            layersTab[i] = layersTabCorrection[(nbLayers) - i]

        layersTabCorrection = []
        layersErrorTab = [] # Tab containing errors calculated with the output neurones

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
            else:
                preced = nbNeurones + 1

            neuronesTab.append(Neurone(preced,0))
        neuronesTab.append(Neurone(preced,1))
        print(len(neuronesTab))
        layersTab.append(neuronesTab)

    # Initialize all output
    neuronesTab = []
    for i in range(nbOutput):
        neuronesTab.append(Neurone(nbNeurones + 1,0))
    layersTab.append(neuronesTab) 
           
def loadRNWeights():
    return 0

def startRN(iteration,imageLimit,debugLevel):
    initRN()
    for i in range(iteration):
        print("Iteration: ",i + 1)
        RN(1,imageLimit,debugLevel)