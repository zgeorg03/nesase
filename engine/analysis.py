# -*- coding: utf-8 -*-
import json
import numpy as np
import sys

class Analysis:
    
    def __init__(self,data_file=None,rangee=60*60*3):
        self.data_file = data_file
        self.parser()
        self.min_time = 0
        self.max_time = 0
        self.rangee = rangee
        self.stats()
        
    
    def parser(self):
        with open(self.data_file, 'r') as f:
            self.data = json.load(f)
 
    def stats(self):
        min_time = sys.maxsize
        max_time = -sys.maxsize - 1
        rangee = self.rangee
        
        for record in self.data:
            time = record['date']
            if time < 1519862400:
                continue
            if time < min_time:
                min_time = time
            if time > max_time:
                max_time = time
        self.min_time = min_time
        self.max_time = max_time
        buckets = int(np.ceil((max_time - min_time) / rangee))

        self.bucket_very_negative = np.zeros(buckets,dtype=np.int16)
        self.bucket_negative = np.zeros(buckets,dtype=np.int16)
        self.bucket_positive = np.zeros(buckets,dtype=np.int16)
        self.bucket_very_positive = np.zeros(buckets,dtype=np.int16) 
        
        for record in self.data:
            index = int( (record['date'] - self.min_time)/ rangee)
            
            if index < 0:
                continue
            if record['class_code'] == 4:
                self.bucket_very_negative[index] += 1
            if record['class_code'] == 3:
                self.bucket_negative[index] += 1
            if record['class_code'] == 2:
                self.bucket_positive[index] += 1
            if record['class_code'] == 1:
                self.bucket_very_positive[index] += 1       
                
    def get_buckets(self): 
        very_negative = []
        negative = []
        positive = []
        very_positive = []
        time = self.min_time * 1000
        for i in range(0,len(self.bucket_negative)):
         
            very_negative.append([time, int(self.bucket_very_negative[i])])            
            negative.append([time, int(self.bucket_negative[i])])            
            positive.append([time, int(self.bucket_positive[i])])            
            very_positive.append([time, int(self.bucket_very_positive[i])])   
            time += (self.rangee) * 1000
            
        return very_negative, negative, positive, very_positive        
if __name__ == '__main__':
    a = Analysis('data.json',rangee=60*60*24*7)
    a.stats()
    vneg, neg, pos, vpos = a.get_buckets()
    print(vneg)
