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
    model = {"name":"asdas"}
    return render_template('index.html',model=model)
    #return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    model = {"name":"asdas"}
    return render_template('dashboard.html',model=model)


@app.route("/api/graph1")    
def graph1():
    data = {}
    data['vneg'], data['neg'],data['pos'],data['vpos'] = analysis.get_buckets()


    resp = Response(response=json.dumps(data),
                    status=200,
                    mimetype="application/json")
    return resp

if __name__ == '__main__':
    analysis = Analysis('data.json',rangee=60*60*24)
    app.run(host="0.0.0.0")
    