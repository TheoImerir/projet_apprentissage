# coding: utf-8
import sys

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
            total += abs(tab1[i] - tab2[i])
        return total
        
    def distanceFrom(self, image):
        modelCol = []
        modelLine = []
        resizedCol = []
        resizedLine = []
        for i in range(6):
            modelCol.append(image.sumColumn(i))
            resizedCol.append(self.sumColumn(i))
        for i in range(8):
            modelLine.append(image.sumLine(i))
            resizedLine.append(self.sumLine(i))
            
        colGapScore = Image.calculDiff(modelCol,resizedCol)
        lineGapScore = Image.calculDiff(modelLine,resizedLine)
        return colGapScore + lineGapScore
    
    def shiftTab(tab, gap):
        temp = []
        for i in range(len(tab)):
            index = (i-gap) % len(tab)
            temp.append(tab[index])
        return temp
    
    def alignWith(self, image):
        modelCol = []
        modelLine = []
        resizedCol = []
        resizedLine = []
        colGapScore = 9999
        colGapIndex = 0
        lineGapScore = 9999
        lineGapIndex = 0
        for i in range(6):
            modelCol.append(image.sumColumn(i))
            resizedCol.append(self.sumColumn(i))
        for i in range(8):
            modelLine.append(image.sumLine(i))
            resizedLine.append(self.sumLine(i))
        
        colGapScore = Image.calculDiff(modelCol,resizedCol)
        colGapIndex = 0
        lineGapScore = Image.calculDiff(modelLine,resizedLine)
        lineGapIndex = 0
        
        #On commence à calculer les différences et vérifier quel décalage est le meilleur
        i = 1
        while i < 6:
            resizedCol = Image.shiftTab(resizedCol,1)
            temp = Image.calculDiff(modelCol,resizedCol)
            if(temp < colGapScore):
                colGapScore = temp
                colGapIndex = i
            i += 1
        
        i = 1
        while i < 8:
            resizedLine = Image.shiftTab(resizedLine,1)
            temp = Image.calculDiff(modelLine,resizedLine)
            if(temp < lineGapScore):
                lineGapScore = temp
                lineGapIndex = i
            i += 1
        
        tab = Image.shiftTab(self.matrix, lineGapIndex)
        for i in range(len(tab)):
            tab[i] = Image.shiftTab(tab[i], colGapIndex)
        
        self.matrix = tab
        
    def drawMatrix(self):
        for i in range(8):
            for j in range(6):
                if(self.matrix[i][j] == 1):
                    sys.stdout.write("[#]")
                else:
                    sys.stdout.write("[ ]")
            print("")
