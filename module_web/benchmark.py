import sys
sys.path.append('../module_algo') 
from kVoisins import *
from baye import *
from func import *
from image import Image


class Benchmark:
    def startSearch(data):
        image = Image(Utils.from48To6x8Matrix(data),-1)
        image.drawMatrix()
        print("Lancement kVoisins")
        imageList = Utils.getImageList()
        resultkVoisin = kVoisins(image,20,imageList)
        print(resultkVoisin)
        print("Lancement Bayes")
        resultBaye = bayes(image)
        print(resultBaye)
        #print("Lancement RN")
        #resultRN = RN(image)
        resultRN = 0
        #print(resultRN)

        data = {} 
        data['kVoisin'] = resultkVoisin
        data['bayes'] = resultBaye
        data['RN'] = resultRN 
        
        return json.dumps(data)
