from kVoisins import *
from baye import *
from image import *

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
    tab = getTestList()
    
    confusion = []
    for i in range(10):
        tempConfusion = []
        for j in range(10):
            tempConfusion.append(0)
        confusion.append(tempConfusion)
        
#    tab.append(Image([[-1,-1,-1,-1,-1,-1],[-1,-1,1,-1,-1,-1],[-1,-1,1,-1,-1,-1],[-1,-1,1,-1,-1,-1],[-1,-1,1,1,1,-1],[-1,-1,-1,1,-1,-1],[-1,-1,-1,1,-1,-1],[-1,-1,-1,1,-1,-1]], 4))
#    tab.append(Image([[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,1,-1],[-1,-1,-1,-1,1,-1],[-1,-1,-1,-1,1,-1],[-1,-1,-1,-1,1,-1],[-1,-1,-1,-1,1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1]], 1))
#    tab.append(Image([[-1,-1,-1,-1,-1,-1],[-1,1,1,1,1,-1],[-1,-1,-1,-1,1,-1],[-1,-1,-1,-1,1,-1],[-1,1,1,1,-1,-1],[-1,-1,-1,-1,1,-1],[-1,-1,-1,-1,1,-1],[-1,1,1,1,-1,-1]], 3))
#    tab.append(Image([[1,1,1,1,-1,-1],[1,-1,-1,-1,-1,-1],[1,-1,-1,-1,-1,-1],[1,1,1,1,-1,-1],[1,-1,-1,1,-1,-1],[1,-1,-1,1,-1,-1],[1,1,1,1,-1,-1],[-1,-1,-1,-1,-1,-1]], 6))
#    tab.append(Image([[-1,1,1,-1,-1,-1],[-1,1,-1,1,-1,-1],[-1,1,-1,-1,1,-1],[1,1,1,1,1,-1],[-1,1,-1,-1,-1,-1],[-1,1,-1,-1,-1,-1],[-1,1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1]], 4))
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
    neighbours = 13
    print("Nb neighbours: {0}".format(neighbours))
    successTab = []
    failTab = []
    for i in range(10):
        successTab.append(0)
        failTab.append(0)
    success = 0
    fail = 0
    tab = []
    tab = getTestList()
    
    confusion = []
    for i in range(10):
        tempConfusion = []
        for j in range(10):
            tempConfusion.append(0)
        confusion.append(tempConfusion)
    
#    tab.append(Image([[-1,-1,-1,-1,-1,-1],[-1,-1,1,-1,-1,-1],[-1,-1,1,-1,-1,-1],[-1,-1,1,-1,-1,-1],[-1,-1,1,1,1,-1],[-1,-1,-1,1,-1,-1],[-1,-1,-1,1,-1,-1],[-1,-1,-1,1,-1,-1]], 4))
#    tab.append(Image([[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,1,-1],[-1,-1,-1,-1,1,-1],[-1,-1,-1,-1,1,-1],[-1,-1,-1,-1,1,-1],[-1,-1,-1,-1,1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1]], 1))
#    tab.append(Image([[-1,-1,-1,-1,-1,-1],[-1,1,1,1,1,-1],[-1,-1,-1,-1,1,-1],[-1,-1,-1,-1,1,-1],[-1,1,1,1,-1,-1],[-1,-1,-1,-1,1,-1],[-1,-1,-1,-1,1,-1],[-1,1,1,1,-1,-1]], 3))
#    tab.append(Image([[1,1,1,1,-1,-1],[1,-1,-1,-1,-1,-1],[1,-1,-1,-1,-1,-1],[1,1,1,1,-1,-1],[1,-1,-1,1,-1,-1],[1,-1,-1,1,-1,-1],[1,1,1,1,-1,-1],[-1,-1,-1,-1,-1,-1]], 6))
#    tab.append(Image([[-1,1,1,-1,-1,-1],[-1,1,-1,1,-1,-1],[-1,1,-1,-1,1,-1],[1,1,1,1,1,-1],[-1,1,-1,-1,-1,-1],[-1,1,-1,-1,-1,-1],[-1,1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1]], 4))
    for x in tab:
        ret = kVoisins(x,neighbours)
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
    imageList = getImageList()
    for image in imageList:
        image.drawMatrix()
        print()
        
#printList()
testBayes()
testKVoisins()
