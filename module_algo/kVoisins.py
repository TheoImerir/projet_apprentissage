# coding: utf-8
from image import * 
from func import Utils
from math import *

#k = 1

#def reglageK():
#    bestValue = 0
#    bestValueScore = 0
#    testList = Utils.getTestList('../module_algo/test.csv')
#    for i in range(25):
#        k = i+1
#        tempScore = 0
#        for image in testList:
#            if kVoisins(image) == image.value:
#                tempScore += 1
#        if(tempScore > bestValueScore):
#            bestValue = k
#            bestValueScore = tempScore
#    k = bestValue
#    print(k)

def kVoisins(image,k,imageList):
    bestValue = -1
    bestValueScore = -1
    distMap = []
    score = [0,0,0,0,0,0,0,0,0,0]
    if(k > len(imageList)):
        return -1
    
    for i in imageList:
        image.alignWith(i)
        dist = image.distanceFrom(i)
        #if(dist == 0):
        #    print("already exist : {0}".format(dist))
        #    return i.value
        distMap.append({'distance':dist, 'value':i.value})
    
    distMap.sort(key = lambda k: k['distance'])
    for i in range(k):
        score[distMap[i]['value']] += 1
    for i in range(10):
        if(score[i] > bestValueScore):
            bestValueScore = score[i]
            bestValue = i
    return bestValue

#reglageK()
