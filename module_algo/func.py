from image import *
from pymongo import MongoClient
import csv, json

class Utils:

    global db
    #client = MongoClient('172.30.1.212:27017')
    client = MongoClient('localhost:27017')
    # Creation de la base connaissance si elle n'existe pas
    db = client.connaissance

    def insertData(data):
        dataJson = json.dumps(data)
        db.images.insert(dataJson);

    def createBase(fichierCsv):
        datas = []
        with open(fichierCsv) as csvfile:
       	    reader = csv.reader(csvfile, delimiter=',')
            for line in reader:
                datas.append({'value':line[0], 'data':line[1:]})
        db.images.insert(datas)

    def recupDonnees():
        return db.images.find({})
    
    def insertData(json_data):
        db.images.insert(json_data)

    def transformBddToImage(valeur, tab48):
        matrice = []
        tabTmp = []
        for i in range(8):
            for j in range(6):
                   tabTmp.append(int(tab48[i*6+j]))
            matrice.append(tabTmp) 
            tabTmp = []
        return Image(matrice, int(valeur))

    def sauvBaseToCsv(csvFile):
        data = Utils.recupDonnees()
        with open(csvFile, 'w') as csvfile:
            #writer = csv.writer(csvfile, delimiter=',')
            for document in data:
                #writer.writerow([document['value'],document['data'][0]])
                csvfile.write(str(document['value'])+",")
                for i in range(48):
                    if (i == 47):
                        csvfile.write(str(document['data'][i])+"\n")
                    else:
                        csvfile.write(str(document['data'][i])+",")
            
    def from49To6x8Matrix(tab):
        matrix = []
        for i in range(8):
            tempMatrix = []
            for j in range(6):
                tempMatrix.append(int(tab[i*6 + j + 1]))
            matrix.append(tempMatrix)
        return matrix

    def from48To6x8Matrix(tab):
        matrix = []
        for i in range(8):
            tempMatrix = []
            for j in range(6):
                tempMatrix.append(int(tab[i*6 + j]))
            matrix.append(tempMatrix)
        return matrix

    def getTestList(csvFile):
        imageList = []
        with open(csvFile) as csvfile:
            tempMatrix = []
            data = csv.reader(csvfile, delimiter=',')
            for line in data:
                tempMatrix = Utils.from48To6x8Matrix(line[1:])
                imageList.append(Image(tempMatrix,int(line[0])))
        return imageList

    def getImageList() :
        imageList = []
        data = Utils.recupDonnees()
        for document in data:
            imageList.append(Utils.transformBddToImage(document['value'], document['data']))
        return imageList
