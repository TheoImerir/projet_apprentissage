from functions.image import *
from pymongo import MongoClient
import csv, json

class Utils:

    global db
    client = MongoClient('172.30.1.212:27017')
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

    def transformBddToImage(valeur, tab48):
        matrice = []
        tabTmp = []
        for i in range(8):
            for j in range(6):
                   tabTmp.append(int(tab48[j*i]))
            matrice.append(tabTmp) 
            tabTmp = []
        return Image(matrice, int(valeur))

