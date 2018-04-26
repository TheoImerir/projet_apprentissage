from flask import Flask, request, render_template
from flask_cors import CORS
import json
import sys
sys.path.append('../module_algo')
from baye import *
from kVoisins import *
from func import *
from benchmark import Benchmark

app = Flask(__name__)
app.debug = True
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/benchmark', methods=['POST'])
def benchmark():
    data = request.get_json()
    print(data)
    return Benchmark.startSearch(data), 200, {'Content-Type': 'application/json'}

@app.route('/correction', methods=['POST'])
def correction():
    Utils.insertData(request.get_json())
    return "Ok, j'ai bien appris"

if __name__ == "main":
    app.run(host='0.0.0.0',port=5000)
