#!/usr/bin/python
import sys
import numpy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

'''
	This python script read from standard input and performs
	sentiment analysis. On EOF, it computes the average,median and
	std of neg,pos,neu,compound
'''
class Sentiment:
    
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.neg_list = []
        self.pos_list = []
        self.neu_list = []
        self.compound_list = []
        self.size = 0
        

    def reset(self):
        self.neg_list = []
        self.pos_list = []
        self.neu_list = []
        self.compound_list = []
        self.size = 0
        
    def score(self, lines):
        self.reset()
        for line in lines:
            vs = self.analyzer.polarity_scores(line)
            self.neg_list.append(vs['neg'])
            self.pos_list.append(vs['pos'])
            self.neu_list.append(vs['neu'])
            self.compound_list.append(vs['compound'])
        self.size = len(self.neg_list)
        self.average_neg = numpy.average(self.neg_list)
        self.median_neg = numpy.median(self.neg_list)
        self.std_neg = numpy.std(self.neg_list)
        
        self.average_pos = numpy.average(self.pos_list)
        self.median_pos = numpy.median(self.pos_list)
        self.std_pos = numpy.std(self.pos_list)
        
        self.average_neu = numpy.average(self.neu_list)
        self.median_neu = numpy.median(self.neu_list)
        self.std_neu = numpy.std(self.neu_list)
        
        self.average_compound = numpy.average(self.compound_list)
        self.median_compound = numpy.median(self.compound_list)
        self.std_compound = numpy.std(self.compound_list)
        #print ('average_neg={0:.7f}'.format(numpy.average(neg_list)))

    def get_avg_scores(self):
        return [self.average_neg, self.average_neu,
                self.average_pos, self.average_compound, self.size]
if __name__ == '__main__':
    sentiment = Sentiment()
    sentiment.score(["Hello ","bad"])
	

