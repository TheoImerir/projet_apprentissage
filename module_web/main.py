from flask import Flask, request, render_template
from flask_cors import CORS
import json
import sys
sys.path.append('../module_algo')
from baye import *
from kVoisins import *
from func import *

app = Flask(__name__)
app.debug = True
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/benchmark', methods=['POST'])
def benchmark():
    data = request.get_json()
    image = Image(Utils.from48To6x8Matrix(data),-1)
    image.drawMatrix()
    print("Lancement kVoisins")
    resultkVoisin = kVoisins(image,20)
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

    return json.dumps(data), 200, {'Content-Type': 'application/json'}

@app.route('/correction', methods=['POST'])
def correction():
    Utils.insertData(request.get_json())
    return "Ok, j'ai bien appris"

if __name__ == "main":
    app.run(host='0.0.0.0',port=5000)
