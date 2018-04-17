from flask import Flask
from flask import request
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk



app = Flask(__name__)
# =============================================================================
# post with Body, raw, application/json at 127.0.0.1:8090/addDoc
# =============================================================================
@app.route('/addDoc', methods = ['POST'])
def postJsonHandler():
    print (request.is_json)
    content = request.get_json()
    client = Elasticsearch([{'host': '10.16.3.12', 'port': 9200}])
#    client = Elasticsearch()

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

    return 'JSON posted'

@app.route('/')
def welcome():
    return 'Welcome'

@app.route('/createindex')
def createIndex():
    collectionName="nesase"
    
    client = Elasticsearch([{'host': '10.16.3.12', 'port': 9200}])
#    client = Elasticsearch()

    if client.indices.exists(collectionName):
        return "index exist"
    else:
        client.indices.create(index=collectionName, ignore=400)
        return "index created"

    
@app.route('/deleteindex')
def deleteIndex():
    collectionName="nesase"
#    client = Elasticsearch()
    client = Elasticsearch([{'host': '10.16.3.12', 'port': 9200}])

    if client.indices.exists(collectionName):
        client.indices.delete(collectionName)
        return "index deleted"
    else:
        return "index does not exist"
    
 
app.run(host='0.0.0.0', port= 8090)







































