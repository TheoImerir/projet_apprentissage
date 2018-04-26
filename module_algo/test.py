from kVoisins import *
from baye import *
from image import *
from RN import * 

def testRN():
    startRN(2) 

def printConfusion(confusion):
    for i in confusion:
        print(i)

def testBayes():
    print("===========================")
    print("Test fonction Bayes")
    successTab = []
    failTab = []
    for i in range(10):
        successTab.append(0)
        failTab.append(0)
    success = 0
    fail = 0
    tab = []
    tab = Utils.getTestList('test.csv')
    
    confusion = []
    for i in range(10):
        tempConfusion = []
        for j in range(10):
            tempConfusion.append(0)
        confusion.append(tempConfusion)
    for x in tab:
        ret = bayes(x)
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
    
def testKVoisins():
    print("===========================")
    print("Test fonction K voisins")
    neighbours = 20
    print("Nb neighbours: {0}".format(neighbours))
    successTab = []
    failTab = []
    for i in range(10):
        successTab.append(0)
        failTab.append(0)
    success = 0
    fail = 0
    tab = []
    imageList = Utils.getTestList('test.csv')
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
#testBayes()
testKVoisins()
#testRN()
