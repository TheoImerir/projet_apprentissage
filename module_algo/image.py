# coding: utf-8
import sys
import csv

class Image :
    
    def __init__(self, matrix, value):
        self.matrix = matrix
        self.value = value
    
    def sumLine(self, line):
        total = 0
        for i in range(6):
            if self.matrix[line][i] != -1:
                total += 1
        return total
        
    def sumColumn(self, column):
        total = 0
        for i in range(8):
            if self.matrix[i][column] != -1:
                total += 1
        return total
    
    def calculDiff(tab1, tab2):
        total = 0
        for i in range(len(tab1)):
            for j in range(len(tab1[0])):
                if tab1[i][j] != tab2[i][j] :
                    total += 1
        return total
        
    def distanceFrom(self, image):
        return Image.calculDiff(self.matrix, image.matrix)
    
    def shiftTab2(tab, gap):
        temp = []
        for i in range(len(tab)):
            index = (i-gap) % len(tab)
            temp.append(tab[index])
        return temp
    
    def shiftTab3(tab, gapI, gapJ):
        tab = Image.shiftTab2(tab, gapI)
        for i in range(len(tab)):
            tab[i] = Image.shiftTab2(tab[i], gapJ)
        return tab
    
    def alignWith(self, image):
        modelCol = []
        modelLine = []
        resizedCol = []
        resizedLine = []
        colGapIndex = 0
        lineGapIndex = 0
        difference = 50
        for i in range(6):
            modelCol.append(image.sumColumn(i))
            resizedCol.append(self.sumColumn(i))
        for i in range(8):
            modelLine.append(image.sumLine(i))
            resizedLine.append(self.sumLine(i))
        
        #On commence à calculer les différences et vérifier quel décalage est le meilleur
        for i in range(8):
            for j in range(6):
                tab = self.matrix
                tab = Image.shiftTab3(tab,i,j)
                temp = Image.calculDiff(tab,image.matrix)
                if(temp < difference):
                    difference = temp
                    lineGapIndex = i
                    colGapIndex = j
        
        self.matrix = Image.shiftTab3(self.matrix, lineGapIndex, colGapIndex)
        
    def drawMatrix(self):
        for i in range(8):
            for j in range(6):
                if(self.matrix[i][j] == 1):
                    sys.stdout.write("[#]")
                else:
                    sys.stdout.write("[ ]")
            print("")
