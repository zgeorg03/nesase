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

file_name = "./log"
max_articles = 10

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
        return self.__repr__

    
    def produce_title_scores(self, sentiment):
        lines = self.sep.split(self.title)
        sentiment.score(lines)
        title_avg_scores = sentiment.get_avg_scores()
        return title_avg_scores
    
    def produce_content_scores(self, sentiment):
        lines = self.sep.split(self.content)
        sentiment.score(lines)
        content_avg_scores = sentiment.get_avg_scores()
        return content_avg_scores

        
def parse_news_article(line):
    data = json.loads(line)
    hash = data['hash']
    title = data['title']
    author = data['author']
    content = data['content']
    date = data['date']
    topics = data['topics']
    feed = data['feed']
    url = data['link']
    return NewsArticle(hash,title,author,url,content,date,topics,feed)


articles = []
count = 0
with open(file_name,"r",encoding="UTF-8") as file:
    for line in file:
        if line.startswith(','):
            continue
        articles.append(parse_news_article(line))
        count += 1
        if count >= max_articles:
            break
        
sentiment = Sentiment()


x = []
for i in range(0,max_articles):
    x.append(articles[i].produce_title_scores(sentiment))
x = np.array(x)
print(x[:,0])


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










