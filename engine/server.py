# -*- coding: utf-8 -*-

from flask import Flask
from flask import request,redirect
from flask import render_template

app = Flask(__name__)


@app.route("/")
def index():
    
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    model = {}
    return render_template('dashboard.html',model=model)

if __name__ == '__main__':
    app.run(host="0.0.0.0")