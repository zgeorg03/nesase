# -*- coding: utf-8 -*-

from flask import Flask,Response
from flask import request,redirect
from flask import render_template
from flask import jsonify
from analysis import Analysis
import json

app = Flask(__name__)

analysis = None

@app.route("/")
def index():
    
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    model = {}
    return render_template('dashboard.html',model=model)

@app.route("/data/graph1")    
def graph1():
    data = {}
    vneg, neg,data['pos'],data['neg'] = analysis.get_buckets()

    data['vneg'] = vneg
    data['neg'] = neg

    resp = Response(response=json.dumps(data),
                    status=200,
                    mimetype="application/json")
    return resp

if __name__ == '__main__':
    analysis = Analysis('data.json',rangee=60*60)
    app.run(host="0.0.0.0")
    