# coding: utf-8
from image import * 
from func import Utils
from math import *

def kVoisins(image, k):
    bestValue = -1
    bestValueScore = -1
    distMap = []
    score = [0,0,0,0,0,0,0,0,0,0]
    imageList = Utils.getImageList()
    if(k > len(imageList)):
        return -1
    
    for i in imageList:
        image.alignWith(i)
        dist = image.distanceFrom(i)
        if(dist == 0):
            return i.value
        distMap.append({'distance':dist, 'value':i.value})
    
    distMap.sort(key = lambda k: k['distance'])
    #print(distMap)
    #print(image.value)
    for i in range(k):
        score[distMap[i]['value']] += 1
    #print(score)
    for i in range(10):
        if(score[i] > bestValueScore):
            bestValueScore = score[i]
            bestValue = i
    return bestValue
