# coding: utf-8
from func import Utils
from image import * 
from math import *
from statistics import *
from random import *

class Bayes:
    def __init__(self):
        self.averageLine = []
        self.averageColumn = []
        self.stdevLine = []
        self.stdevColumn = []
        self.coefsLines = []
        self.coefsColumn = []
        self.powLines = []
        self.powColumn = []
        for i in range(8):
            self.coefsLines.append(0)
        for i in range(6):
            self.coefsColumn.append(0)
        for i in range(8):
            self.powLines.append(1)
        for i in range(6):
            self.powColumn.append(1)
    
    def setAverageAndStdev(self,avLine,avColumn,stLine,stColumn):
        self.averageLine = avLine.copy()
        self.averageColumn = avColumn.copy()
        self.stdevLine = stLine.copy()
        self.stdevColumn = stColumn.copy()
    
    def learn(self):
        img = 0
        actual = 0
        imageList = Utils.getImageList()
        imageList.sort(key=lambda x: x.value)
        while actual < 10:
            tabSumCol = []
            tabSumLin = []
            # Pour toutes les images de même valeurs (que les 1 ou les 2 ...) on fait la somme des lignes des colonne
            if img >= len(imageList):
                actual += 1
                continue
            img = Bayes.getTabsSums(imageList,img,actual,tabSumCol,tabSumLin)
            # Une fois que l'on a les sommes des lignes et colonnes on calcul la moyenne et l'écart type pour la somme des lignes et des colonnes pour chaque chiffre 
            if len(tabSumCol) > 0:
                self.averageLine.append(Bayes.getAverage(tabSumLin,8))
                self.averageColumn.append(Bayes.getAverage(tabSumCol,6))
                self.stdevLine.append(Bayes.getStdev(tabSumLin,8))
                self.stdevColumn.append(Bayes.getStdev(tabSumCol,6))
            actual += 1

    def loiNormale(x, moyenne, ecartType):
        var = pow(ecartType,2);
        if var == 0:
            var = 1
        denom = pow((2*pi*var),0.5);
        num = exp(-(pow(x-moyenne,2))/(2*var));
        return num/denom;

    def getTabsSums(imageList, index, actual, tabSumCol, tabSumLin):
        while imageList[index].value == actual:
            # On recentre toutes les images de la BD par rapport à celle passé en argument
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

    def bayes(self, image):
        actual = 0
        proba = []
        bestValue = -1
        bestValueProba = -1
        while actual < 10:
            # Une fois que l'on a les sommes des lignes et colonnes on calcul la moyenne et l'écart type pour la somme des lignes et des colonnes pour chaque chiffre 
            i = 0
            p = 1
            while i < 8:
                #print(self.averageLine[actual][i], self.stdevLine[actual][i])
                p *= pow(Bayes.loiNormale(image.sumLine(i), self.averageLine[actual][i], self.stdevLine[actual][i]) + self.coefsLines[i], self.powLines[i])
                i+=1
            i = 0
            while i < 6:
            #print(self.averageColumn[actual][i], self.stdevColumn[actual][i])
                p *= pow(Bayes.loiNormale(image.sumColumn(i), self.averageColumn[actual][i], self.stdevColumn[actual][i]) + self.coefsColumn[i], self.powColumn[i])
                i+=1
            proba.append(p)
            actual += 1
        totalProba = 0
        for i in range(len(proba)):
            totalProba += proba[i]
            if(proba[i] > bestValueProba):
                bestValueProba = proba[i]
                bestValue = i
        return bestValue

    def setParams(self,coefsLin,coefsCol,powLin,powCol):
        self.coefsLines = coefsLin.copy()
        self.coefsColumn = coefsCol.copy()
        self.powLines = powLin.copy()
        self.powColumn = powCol.copy()

    def setRandomParameters(self):
        for i in range(len(self.coefsLines)):
            self.coefsLines[i] = randrange(-2,2)
        for i in range(len(self.coefsColumn)):
            self.coefsLines[i] = randrange(-2,2)
        for i in range(len(self.coefsLines)):
            self.powLines[i] = randrange(-5,5)
        for i in range(len(self.coefsColumn)):
            self.powLines[i] = randrange(-5,5)

    def getNeighbour(self):
        coefsLin = []
        coefsCol = []
        powLin = []
        powCol = []
        for c in self.coefsLines:
            coefsLin.append(c + randrange(-1,1))
        for c in self.coefsColumn:
            coefsCol.append(c + randrange(-1,1))
        for c in self.powLines:
            powLin.append(c + randrange(-2,2))
        for c in self.powColumn:
            powCol.append(c + randrange(-2,2))
        n = Bayes()
        n.setAverageAndStdev(self.averageLine,self.averageColumn,self.stdevLine,self.stdevColumn)
        n.setParams(coefsLin, coefsCol, powLin, powCol)
#        n.setParams(self.coefsLines, self.coefsColumn, powLin, powCol)
        return n

    def evaluate(self, imageList): 
        success = 0
        for i in imageList:
            if self.bayes(i) == i.value :
                success += 1
        return success

    def descente(self):
        seed()
        imageList = []
        imageList = Utils.getImageList()
        b = Bayes()
        b.setAverageAndStdev(self.averageLine,self.averageColumn,self.stdevLine,self.stdevColumn)
        b.setRandomParameters()
        noImprovement = 0
        success = 0
        successPrevious = 0
        successPrevious = b.evaluate(imageList)
        while noImprovement < 100:
            b2 = b.getNeighbour()
            success = b2.evaluate(imageList)
            print(success, " > ", successPrevious)
            print(b2.coefsLines)
            print(b2.coefsColumn)
            print(b2.powColumn)
            if success > successPrevious:
                b = b2
                successPrevious = success
                noImprovement = 0
                print(b2.powLines)
            else:
                noImprovement += 1
        if b.evaluate(imageList) > self.evaluate(imageList):
            self.setParams(b.coefsLines,b.coefsColumn,b.powLines,b.powColumn)
        print(self.coefsLines)
        print(self.powLines)
        print(self.coefsColumn)
        print(self.powColumn)
        print("\n\n")
