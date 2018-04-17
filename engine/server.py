# -*- coding: utf-8 -*-
import sys
from flask import Flask,Response
from flask import request,redirect
from flask import render_template
from flask import jsonify
from analysis import Analysis
import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
from elasticsearch.helpers import bulk

import time
import threading


app = Flask(__name__)

client = None
collectionName="nesase"
host = "10.16.3.12"
port = 9200
connected = False
analysis = None
day = 60*60*24

def query(quer,days=None):


    if days and days != "-1":

        days = int(days)
        now = int(time.time())
        last = now - days * day

        s = Search(using=client, index=collectionName).filter('range', date={'gte': last, 'lte': now})
    else:
        s = Search(using=client, index=collectionName)

        
    
    q = Q('query_string',query=quer)
    s = s.query(q)

    if s.count() > 100:
        total = 100
    else:
        total = s.count()

    s = s[0:total]
    results = s.execute()

    return results
   


def queryTopic(topic):

    s = Search(using=client, index=collectionName)
    q = Q('query_string',query=topic, default_field="topics.keyword")
    s = s.query(q)

    if s.count() > 100:
        total = 100
    else:
        total = s.count()

    s = s[0:total]
    results = s.execute()

    return results
      
@app.route("/api/hotTopics")    
def hotTopics():
    d = request.args.get('d')
    
    body = { "size": 0, 
            "aggs": {
              "my_fields": {
                   "terms": {
                   "field": "topics.keyword",
                        "size": 10
                             }
                            }
                   }
           }
    if d and d != "-1":
        days = int(d)
        now = int(time.time())
        last = now - days * day
        body["query"]={'range':{
                                'date':{
                                        'gte': last, 'lte': now
                                        }
                            }
                        }
               


    print(body)
    res = client.search(index="nesase", doc_type="document", body=body)
    result = []
    for term in res["aggregations"]["my_fields"]["buckets"]:
        result.append({"name":term['key'], "count":term['doc_count']})
   
    return jsonify(result)
    
def graphdata():
 
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
    hotTopics()
    count =     client.count(index="nesase")['count']
    model={"count":count}

    return render_template('index.html',model=model)
    #return redirect("/dashboard")


@app.route("/api/query")
def api_query():
    q = request.args.get('q')
    d = request.args.get('d')
    if(q):
        results = query(q,d)
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
                 "retrieved": str(len(results)),
                 "records":records
                } 
        return jsonify(model)
    
    return jsonify({"error":"Text needed"})
   
 
@app.route("/api/queryTopic")
def api_query_topic():
    q = request.args.get('q')
    if(q):
        results = queryTopic(q)
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
                 "retrieved": str(len(results)),
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


####################################### Index Manager

@app.route('/createindex')
def createIndex():
    collectionName="nesase"

    if client.indices.exists(collectionName):
        return jsonify({"msg":"index exists"})
    else:
        client.indices.create(index=collectionName, ignore=400)
        return jsonify({"msg":"index created"})
    

@app.route('/deleteindex')
def deleteIndex():
    collectionName="nesase"
    if client.indices.exists(collectionName):
        client.indices.delete(collectionName)
        return jsonify({"msg":"index deleted"})
    else:
        return jsonify({"msg":"index doesn't exist"})
    
@app.route('/addDocs', methods = ['POST'])
def add_documents():
    print (request.is_json)
    content = request.get_json()
    ldocs = []
    for article in content:
        
        ldocs.append({
                '_op_type': 'index',
                '_index':   'nesase',
                '_type':    'document',
                '_id':      article['id'],
                'author':   article['author'],
                'class':     article['class'],
                'class_code':     article['class_code'],
                'content':     article['content'],
                'date':     article['date'],
                'feed':     article['feed'],
                'neg_content':     article['neg_content'],
                'neg_title':     article['neg_title'],
                'neu_content':     article['neu_content'],
                'neu_title':     article['neu_title'],
                'overall_score':     article['overall_score'],
                'pos_content':     article['pos_content'],
                'pos_title':     article['pos_title'],
                'score_content':     article['score_content'],
                'score_title':     article['score_title'],
                'title':     article['title'],
                'url':     article['url'],
#                'topics':     (', '.join(article['topics']))    
                'topics':   article['topics']
                })
    bulk(client, ldocs)

    return jsonify({"msg":"Documents added"})

def add_ram_documents(content):

    ldocs = []
    for article in content:
        ldocs.append({
                '_op_type': 'index',
                '_index':   'nesase',
                '_type':    'document',
                '_id':      article['id'],
                'author':   article['author'],
                'class':     article['class'],
                'class_code':     article['class_code'],
                'content':     article['content'],
                'date':     article['date'],
                'feed':     article['feed'],
                'neg_content':     article['neg_content'],
                'neg_title':     article['neg_title'],
                'neu_content':     article['neu_content'],
                'neu_title':     article['neu_title'],
                'overall_score':     article['overall_score'],
                'pos_content':     article['pos_content'],
                'pos_title':     article['pos_title'],
                'score_content':     article['score_content'],
                'score_title':     article['score_title'],
                'title':     article['title'],
                'url':     article['url'],
                'topics':   article['topics']
                })
    bulk(client, ldocs)


    return {"msg":"Documents added"}
def worker(data_file=None,start=0,end=-1):
    while True:
        if connected:
            break
        time.sleep(1)
            
    print('Loading...'+data_file)
    data = None
    with open(data_file, 'r') as f:
        data = json.load(f)  
    size = len(data)

    if end == -1:
        end = size
        
    add = []
    print("Total size: {} ".format(size))
    for i,r in enumerate(data):
        if i >= start and i<end:
            add.append(r)
            
    add_ram_documents(add);
    print("Added")
    return

if __name__ == '__main__':
    
    configs = {
            'data_file':"./data2.json",
            'start':0,
            'end':0
            }
    
#    analysis = Analysis('data.json',rangee=60*60*24)
    client = Elasticsearch([{'host': host, 'port': port}])

    try:
        status = client.cat.health()
        connected = True
    except Exception as e:
        print(e)
        print("[Info] - Couldn't connect to elastic-search")
        sys.exit(1)



    t = threading.Thread(target=worker,kwargs=configs)
    t.setDaemon(True)
    t.start()
        
    print("[Info] - Connected to elastic-search succesfully")
  

    app.run(host="0.0.0.0")
    
    

