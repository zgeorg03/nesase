# NeSASE: A News Sentiment &amp; Analytics Search Engine

This frameworks allows the user to query news articles based on their sentiment.Sentiment Analysis is a technique used for determining the overall emotional reaction to a document, interaction or an event. In our case with news articles, by analysing the sentiment of the article's text, we can tell whether it expresses a positive, negative or neutral feeling to the reader.

The are two main modules in this framework. The engine and the crawler.

## Engine
A RESTfull service for querying through the Elasticsearch engine implemented in  python: **server.py**

After receiving a news article from the crawler, it performs the sentiment analysis and then indexes the analyzed article using the functionality of the ElasticSearch engine. 

The Sentiment analysis is performed via the **sentiment_analysis.py** python file. It uses [VADER](https://github.com/cjhutto/vaderSentiment) a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media, and works well on texts from other domains. 


### How to run?

```bash
python server.py
```

The server starts on port 5000. It makes a connection to elasticsearch engine on 10.16.3.12. Note that this is a private IP, so you must first setup elastic search and change the IP accordingly.


## BBC Crawler
A java program that retrieves headlines from BBC RSS feed and produces a log file containing the following information for each article:
* Title
* Content
* Date
* Author
* List of topics that the article belongs to


