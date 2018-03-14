#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 17:42:27 2018

@author: zgeorg03
"""

import json # Used for converting json to dictionary
import datetime # Used for date conversions
file_name = "./log"
max_articles = 300

class NewsArticle:
    def __init__(self,hash,title,author,content,date,topics, feed):
        self.hash = hash
        self.title = title
        self.author = author
        self.content = content
        self.date = datetime.datetime.fromtimestamp(date/1000.0)
        self.topics = topics
        self.feed = feed
        
    def __repr__(self):
        return "hash={},title={},author={},date={},topics={}".format(
                self.hash, self.title, self.author,
                self.date, self.topics, self.feed)
    def __str__(self):
        return self.__repr__
        
def parse_news_article(line):
    data = json.loads(line)
    hash = data['hash']
    title = data['title']
    author = data['author']
    content = data['content']
    date = data['date']
    topics = data['topics']
    feed = data['feed']
    return NewsArticle(hash,title,author,content,date,topics,feed)


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
for arr in articles:
    print(arr.feed)

    
