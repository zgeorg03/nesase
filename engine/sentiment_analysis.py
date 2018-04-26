#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 17:42:27 2018

@author: zgeorg03
"""
import re
import json # Used for converting json to dictionary
import datetime # Used for date conversions

import matplotlib.pyplot as plt
import numpy as np

from sentiment import Sentiment
import json



class NewsArticle:
    def __init__(self,hash,title,author,url,content,date,topics, feed):
        self.hash = hash
        self.title = title
        self.author = author
        self.url = url
        self.content = content
        self.date = datetime.datetime.fromtimestamp(date/1000.0)
        self.topics = topics
        self.feed = feed
        self.sep = re.compile("[.!?]")
        
    def __repr__(self):
        return "hash={},title={},author={},date={},topics={}".format(
                self.hash, self.title, self.author,
                self.date, self.topics, self.feed)
        
    def __str__(self):
        return self.__repr__()

    
    def produce_title_scores(self, sentiment):
        lines = self.sep.split(self.title)
        sentiment.score(lines)
        neg,neu,pos,com,count = sentiment.get_avg_scores()
        return (float("{0:.2f}".format(neg*100)), float("{0:.2f}".format(neu*100))
        , float("{0:.2f}".format(pos*100)), float("{0:.2f}".format(com*100)),count
        )

    
    def produce_content_scores(self, sentiment):
        lines = self.sep.split(self.content)
        sentiment.score(lines)
        neg,neu,pos,com,count = sentiment.get_avg_scores()
        return (float("{0:.2f}".format(neg*100)), float("{0:.2f}".format(neu*100))
        , float("{0:.2f}".format(pos*100)), float("{0:.2f}".format(com*100)),count
        )

class Parser:
    def __init__(self,file_in,max_articles=None,file_out=None):
        self.file_name = file_name
        self.max_articles = max_articles
        self.articles = []
        self.sentiment = Sentiment()
        self.results = []
        self.file_out = file_out
    
    def parse(self):
        count = 0
        with open(self.file_name,"r",encoding="UTF-8") as file:
            for line in file:
                if line.startswith(','):
                    continue
                self.articles.append(self.parse_news_article(line))
                count += 1
              
                if self.max_articles:
                    if count >= self.max_articles:
                        break
        
        
    def write(self):
        for i,article in enumerate(self.articles):
            if i % 100 == 0:
                print('Finished: {} docs'.format(i))
            self.write_article(article)
     
        if self.file_out:
            with open(self.file_out, 'w') as outfile:
                json.dump(self.results, outfile,sort_keys=True,indent=4)
        else:
            print(json.dumps(self.results,sort_keys=True,indent=4))

    def write_article(self,article):
        res = {}
        res['neg_title'],res['neu_title'],res['pos_title'],res['score_title'], _ = article.produce_title_scores(self.sentiment)
        res['neg_content'],res['neu_content'],res['pos_content'],res['score_content'], _ = article.produce_content_scores(self.sentiment)
        res['id'] = article.hash
        res['title'] = article.title
        res['date'] = int(article.date.timestamp())
        res['content'] = article.content
        res['topics'] =  article.topics
        res['feed'] = article.feed
        res['url'] = article.url
        res['author'] = article.author
        
        res['overall_score']= float(res['score_title'])*0.75 + float(res['score_content'])*0.25
        overall_score =  res['overall_score']
        if overall_score <= -50:
            res['class']= 'Very Negative'
            res['class_code'] = 4
        elif overall_score <= 0:
            res['class']= 'Negative'
            res['class_code'] = 3
        elif overall_score <= 50:
            res['class']= 'Positive'
            res['class_code'] = 2
        elif overall_score <= 100:
            res['class']= 'Very Positive'
            res['class_code'] = 1
        
        self.results.append(res)
        
       
  
    def parse_news_article(self, line):
        data = json.loads(line)
        hash = data['hash']
        title = data['title']
        author = data['author']
        content = data['content']
        date = data['date']
        topics = list(set(data['topics']))
        feed = data['feed']
        url = data['link']
        return NewsArticle(hash,title,author,url,content,date,topics,feed)

if __name__ == '__main__':
    
    file_name = "./log"
    #max_articles = 1000
    p = Parser(file_name,file_out='data-26-04.json')
    
    p.parse()
    p.write()
    print('Finished')
 

    
def test():
 
    
    plt.figure(figsize=(12,9))
    plt.title('Articles: {}'.format(max_articles))
    plt.plot(x[:,0],'x',label="Negative {0:.2f}".format(np.average(x[:,0])))
    plt.plot(x[:,2],'+',label="Positive {0:.2f}".format(np.average(x[:,2])))
    plt.plot(x[:,1],'.',label="Neutral {0:.2f}".format(np.average(x[:,1])))
    plt.plot(x[:,3],'.',label="Compound {0:.2f}".format(np.average(x[:,3])))
    plt.legend()
    
    x = []
    for i in range(0,max_articles):
        x.append(articles[i].produce_content_scores(sentiment))
    x = np.array(x)
    print(x[:,0])
    
    
    plt.figure(figsize=(12,9))
    plt.title('Articles: {}'.format(max_articles))
    plt.plot(x[:,0],'x',label="Negative {0:.2f}".format(np.average(x[:,0])))
    plt.plot(x[:,2],'+',label="Positive {0:.2f}".format(np.average(x[:,2])))
    plt.plot(x[:,1],'.',label="Neutral {0:.2f}".format(np.average(x[:,1])))
    plt.plot(x[:,3],'.',label="Compound {0:.2f}".format(np.average(x[:,3])))
    plt.legend()
    
    
    
    






