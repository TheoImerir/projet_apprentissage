from kVoisins import *
from baye import *
from RN import * 
from func import Utils

def testRN():
    startRN(2) 

def printConfusion(confusion):
    for i in confusion:
        print(i)

def testBayes():
    print("===========================")
    print("Test fonction Bayes")
    b = Bayes()
    # Utilisé pour s'en appuyer comme BDD
    imageList = Utils.getTestList('test.csv')
    b.learn(imageList)
    # Utilisé pour tester par rapport à la base de donnée précédente. Pourquoi je fais ça : Parce que les données
    # dans echantillonToTest ne se retrouvent pas dans test.csv -> encore plus significatif
    imageList = Utils.getTestList('echantillonToTest.csv')
    b.descente(imageList)
    successTab = []
    failTab = []
    for i in range(10):
        successTab.append(0)
        failTab.append(0)
    success = 0
    fail = 0
    tab = []
    tab = Utils.getTestList('echantillonToTest.csv')
    
    confusion = []
    for i in range(10):
        tempConfusion = []
        for j in range(10):
            tempConfusion.append(0)
        confusion.append(tempConfusion)
    for x in tab:
        ret = b.bayes(x)
        confusion[x.value][ret] += 1
        if ret == x.value:
            success += 1
            successTab[x.value] += 1
        else:
            fail += 1
            failTab[x.value] += 1
    printConfusion(confusion)
    print("nb Success: {0} \nSuccess:{1}".format(success,successTab))
    print("nb fail: {0} \nfail:{1}".format(fail,failTab))
    print("success rate: {0} %".format(success / len(tab) * 100))
    print("===========================")
    
def descenteVoisin(min, max):
   bestScore = 0.0
   result = 0.0
   meilleurVoisin = 0
   for i in range(min,max): 
        result = testKVoisins(i)
        if result > bestScore:
            bestScore = result
            meilleurVoisin = i
       
   print("Meilleur voisin : ", meilleurVoisin)
   print("Avec score de :", bestScore)

def testKVoisins(neighbours):
    print("===========================")
    print("Test fonction K voisins")
    print("Nb neighbours: {0}".format(neighbours))
    successTab = []
    failTab = []
    for i in range(10):
        successTab.append(0)
        failTab.append(0)
    success = 0
    fail = 0
    tab = []
    imageList = Utils.getTestList("test.csv")
    tab = Utils.getTestList('echantillonToTest.csv')
    
    confusion = []
    for i in range(10):
        tempConfusion = []
        for j in range(10):
            tempConfusion.append(0)
        confusion.append(tempConfusion)
    for x in tab:
        ret = kVoisins(x,neighbours,imageList)
        confusion[x.value][ret] += 1
        if ret == x.value:
            success += 1
            successTab[x.value] += 1
        else:
            fail += 1
            failTab[x.value] += 1
    printConfusion(confusion)
    print("nb Success: {0} \nSuccess:{1}".format(success,successTab))
    print("nb fail: {0} \nfail:{1}".format(fail,failTab))
    print("success rate: {0} %".format(success / len(tab) * 100))
    print("===========================")
    return ((success / len(tab)) * 100)

def printList():
    imageList = Utils.getTestList('test.csv')
    for image in imageList:
        image.drawMatrix()
        print()
    print("------------------------------")
    imageList = Utils.getImageList()
    for image in imageList:
        image.drawMatrix()
        print()
        
#printList()
testBayes()
#testKVoisins(10)
#descenteVoisin(1,20)
#testRN()
#descente()
