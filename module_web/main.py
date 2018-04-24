from flask import Flask, request
from flask_cors import CORS
from pymongo import MongoClient
from functions.func import Utils

app = Flask(__name__)
app.debug = True
CORS(app)

#Utils.createBase('50samples.csv')
data = Utils.recupDonnees()

for document in data:
   print(Utils.transformBddToImage(document['value'], document['data']))
