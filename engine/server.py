# -*- coding: utf-8 -*-

from flask import Flask,Response
from flask import request,redirect
from flask import render_template
from flask import jsonify
from analysis import Analysis
import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q



app = Flask(__name__)

analysis = None


def query(quer):
    client = Elasticsearch(hosts=["10.16.3.12"])
    collectionName="nesase"
    s = Search(using=client, index=collectionName)
    q = Q('query_string',query=quer)
    s = s.query(q)
    total = s.count()
    s = s[0:total]
    results = s.execute()
    return results
   
    
def graphdata():
    client = Elasticsearch()
#    client = Elasticsearch([{'host': '10.16.3.12', 'port': 9200}])
    collectionName="nesase"
    doc = {
            'size' : 10000,
            'query': {
                'match_all' : {}
           }
       }
    res = client.search(index=collectionName, doc_type='document', body=doc,scroll='1m')
    very_negative = []
    negative = []
    positive = []
    very_positive = []
#    for doc in res['hits']['hits']:
#       id => doc['_id'] , date => doc['_source']['date'] 
        
    


@app.route("/")
def index():
    model={}
    q = request.args.get('q')
    if(q):
        results=query(q)
#        for hit in results:
#            print(hit.meta.score, hit.title)
            
        model = {"count":"Total results: "+ str(results.hits.total),
                 "results":results
                     }
    
    return render_template('index.html',model=model)
    #return redirect("/dashboard")


@app.route("/api/query")
def api_query():
    q = request.args.get('q')
    if(q):
        results=query(q)
        records = []
        for hit in results:
            record = {}
            record['title'] = hit['title'],
            record['content'] = hit['content']
            record['sentiment_score'] = hit['overall_score']
            record['class_code'] = hit['class_code']
            record['from']= hit['author']
            record['link']= hit['url']
            record['date']= hit['date']
            records.append(record)
            
       
        model = {
                 "total": str(results.hits.total),
                 "records":records
                } 
        return jsonify(model)
    return jsonify({"error":"Text needed"})
   
    

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
#    analysis = Analysis('data.json',rangee=60*60*24)
    app.run(host="0.0.0.0")
    
    
    

