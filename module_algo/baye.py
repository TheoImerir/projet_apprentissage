# coding: utf-8
from func import Utils
from image import * 
from math import *
from statistics import *
from random import *

class Parameters:
    def __init__(self):
        self.coefsLines[]
        self.coefsColumn[]
        for i in range(8):
            self.coefsLines.append(1)
        for i in range(6):
            self.coefsColumn.append(1)

    def __init__(self,coefsLin,coefsCol):
        self.coefsLines = coefsLin.copy()
        self.coefsColumn = coefsCol.copy()

def setRandomParameters(p):
    for c in range(len(p.coefsLines)):
        p.coefsLines[i] = random.range(0.5,2,0.1)
    for c in range(len(p.coefsColumn)):
        p.coefsLines[i] = random.range(0.5,2,0.1)

def getNeighbour(p):
    coefsLin = []
    coefsCol = []
    for c in p.coefsLines:
        coefsLin.append(c * random.range(0.8,1.2,0.1))
    for c in p.coefsColumn:
        coefsCol.append(c * random.range(0.8,1.2,0.1))
    return Parameters(coefsLin, coefsCol)

def evaluate(p, imageList): 
    success = 0
    for i in imageList:
        if bayes(i,p) == i.value :
            successPrevious += 1
    return success

def descente():
    random.seed()
    imageList = getImageList()
    p = Parameters()
    setRandomParameters(p)
    noImprovement = 0
    success = 0
    successPrevious = 0
    successPrevious = evaluate(p,imageList)
    while noImprovement < 100:
        p2 = getNeighbour(p)
        success = evaluate(p2,imageList)
        if success > successPrevious:
            p = p2
            successPrevious = success
            noImprovement = 0
        else:
            noImprovement += 1
    print(p.coefsLines)
    print(p.coefsColumn)

def loiNormale(x, moyenne, ecartType):
    var = pow(ecartType,2);
    if var == 0:
        var = 1
    denom = pow((2*pi*var),0.5);
    num = exp(-(pow(x-moyenne,2))/(2*var));
    return num/denom;

def getTabsSums(imageList, index, actual, tabSumCol, tabSumLin, targetImage):
    while imageList[index].value == actual:
        # On recentre toutes les images de la BD par rapport à celle passé en argument
        imageList[index].alignWith(targetImage)
        sumCol = []
        sumLin = []
        for i in range(6):
            sumCol.append(imageList[index].sumColumn(i))
        for i in range(8):
            sumLin.append(imageList[index].sumLine(i))
        tabSumCol.append(sumCol)
        tabSumLin.append(sumLin)
        index += 1
        if index >= len(imageList):
            break
    return index

def getAverage(tab, size) : 
    moyenne = []
    for i in range(size):
        total = 0
        for j in range(len(tab)):
            total += tab[j][i]
        moyenne.append(total / len(tab))
    return moyenne

def getStdev(tab, size) :
    ecartType = []
    for i in range(size):
        temp = []
        for j in range(len(tab)):
            temp.append(tab[j][i])
        if len(temp) > 1 :
            ecartType.append(stdev(temp))
        else :
            ecartType.append(1)
    return ecartType

def bayes(image, param):
    imageList = Utils.getImageList()
    img = 0
    actual = 0
    imageList.sort(key=lambda x: x.value)
    proba = []
    bestValue = -1
    bestValueProba = -1
    while actual < 10:
        tabSumCol = []
        tabSumLin = []
        # Pour toutes les images de même valeurs (que les 1 ou les 2 ...) on fait la somme des lignes des colonne
        if img >= len(imageList):
            proba.append(0)
            actual += 1
            continue
        img = getTabsSums(imageList,img,actual,tabSumCol,tabSumLin,image)
        # Une fois que l'on a les sommes des lignes et colonnes on calcul la moyenne et l'écart type pour la somme des lignes et des colonnes pour chaque chiffre 
        if len(tabSumCol) > 0:
            moyenneLin = getAverage(tabSumLin,8)
            moyenneCol = getAverage(tabSumCol,6)
            ecartTypeLin = getStdev(tabSumLin,8)
            ecartTypeCol = getStdev(tabSumCol,6)
            i = 0
            p = 1
            while i < 8:
                p *= pow(loiNormale(image.sumLine(i), moyenneLin[i], ecartTypeLin[i]),param.coefsLines[i])
                i+=1
            i = 0
            while i < 6:
                p *= pow(loiNormale(image.sumColumn(i), moyenneCol[i], ecartTypeCol[i]),param.coefsColumn[i])
                i+=1
            proba.append(p)
        else:
            proba.append(0)
        actual += 1
    totalProba = 0
    for i in range(len(proba)):
        totalProba += proba[i]
        if(proba[i] > bestValueProba):
            bestValueProba = proba[i]
            bestValue = i
    return bestValue
