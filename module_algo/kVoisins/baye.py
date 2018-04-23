# coding: utf-8
from image import * 
from math import *
from statistics import *

def loiNormale(x, moyenne, ecartType):
    var = pow(ecartType,2);
    if var == 0:
        if x == moyenne:
            return 1
        else:
            return 0
    denom = pow((2*pi*var),0.5);
    num = exp(-(pow(x-moyenne,2))/(2*var));
    return num/denom;

def getTabsSums(imageList, index, actual, tabSumCol, tabSumLin):
    while imageList[index].value == actual:
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

def bayes(image):
    imageList = getImageList()
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
        img = getTabsSums(imageList,img,actual,tabSumCol,tabSumLin)
        # Une fois que l'on a les sommes des lignes et colonnes on calcul la moyenne et l'écart type pour la somme des lignes et des colonnes pour chaque chiffre 
        if len(tabSumCol) > 0:
            moyenneLin = getAverage(tabSumLin,8)
            moyenneCol = getAverage(tabSumCol,6)
            ecartTypeLin = getStdev(tabSumLin,8)
            ecartTypeCol = getStdev(tabSumCol,6)
            i = 0
            p = 1
            while i < 8:
                p *= loiNormale(image.sumLine(i), moyenneLin[i], ecartTypeLin[i])
                i+=1
            i = 0
            while i < 6:
                p *= loiNormale(image.sumColumn(i), moyenneCol[i], ecartTypeCol[i])
                i+=1
            proba.append(p)
        else:
            proba.append(0)
        actual += 1
    for i in range(len(proba)):
        if(proba[i] > bestValueProba):
            bestValueProba = proba[i]
            bestValue = i
    return bestValue
    
y = Image([[-1,-1,-1,-1,-1,-1],[-1,1,1,1,1,-1],[-1,-1,-1,-1,1,-1],[-1,-1,-1,-1,1,-1],[-1,1,1,1,-1,-1],[-1,-1,-1,-1,1,-1],[-1,-1,-1,-1,1,-1],[-1,1,1,1,-1,-1]], -1)
y.drawMatrix()
print(bayes(y))
