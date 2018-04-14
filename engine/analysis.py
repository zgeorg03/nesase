# -*- coding: utf-8 -*-
import json
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from datetime import datetime as dt

week = ('M', 'T', 'W', 'T', 'F','S','S')
 
 
class Analysis:
    
    def __init__(self,data_file=None,plots_path='./plots'):
        self.plots_size = (16,9)
        self.plots_path = plots_path
        try:
            os.mkdir(self.plots_path)
        except FileExistsError as e :
            pass
        self.data_file = data_file
        self.day_seconds = 60*60*24
        self.skip = 1520294400
        self.min_time = 0
        self.max_time = 0
        self.parser()
        print("Total Articles Parsed:{}".format(len(self.data)))
 
  
    def parser(self):
        with open(self.data_file, 'r') as f:
            self.data = json.load(f)
 
    def daily_stats(self):
        buckets = {}
        for record in self.data:
            
            time = record['date']
            
            if time < self.skip:
                continue
            date = dt.fromtimestamp(time).date()
            if date in buckets:
                buckets[date].append(record)
            else:
                buckets[date] = [record]
        res = []
        
        for i,key in enumerate(buckets):
            val = buckets[key]
            vn,n,p,vp = 0,0,0,0
            for record in val:
            
                if record['class_code'] == 4:
                    vn+= 1
                if record['class_code'] == 3:
                    n+= 1
                if record['class_code'] == 2:
                    p+= 1
                if record['class_code'] == 1:
                    vp+= 1  
        
            
            res.append([key,vn,n,p,vp])   
        
        self.daily_labels = []
        res.sort(key=lambda x: x[0])
        res = np.array(res)
        
        for i,d in enumerate(res[:,0]):
            index = d.weekday()
            self.daily_labels.append(week[index])
        return np.array(res)
    
    def hourly_stats(self):
        buckets = {}
        for record in self.data:
            
            time = record['date']
            
            if time < self.skip:
                continue
            date = dt.fromtimestamp(time).hour
            if date in buckets:
                buckets[date].append(record)
            else:
                buckets[date] = [record]
        res = []
        
        for i,key in enumerate(buckets):
            val = buckets[key]
            vn,n,p,vp = 0,0,0,0
            for record in val:
            
                if record['class_code'] == 4:
                    vn+= 1
                if record['class_code'] == 3:
                    n+= 1
                if record['class_code'] == 2:
                    p+= 1
                if record['class_code'] == 1:
                    vp+= 1  
                    
            
            
            res.append([key,vn,n,p,vp])   
        
        self.hourly_labels = []
        res.sort(key=lambda x: x[0])
        
        res = np.array(res)
    
        for i,d in enumerate(res[:,0]):
            index = d
            self.hourly_labels.append(str(index).zfill(2))
        return np.array(res)
    
    
    def hourly_plots(self):
             
        self.hourly_stats = self.hourly_stats()
        self.hourly_counts_plot()
        self.hourly_perc_plot()
    
    def hourly_counts_plot(self):
        data = self.hourly_stats
        labels = self.hourly_labels

        fig,ax = plt.subplots(figsize=self.plots_size)
        ind = np.arange(len(labels))
        ax.bar(ind,data[:,1],color='#e6194b',label='Very Negative')
        ax.bar(ind,data[:,2],color='#fabebe',bottom=data[:,1],label='Negative')
        ax.bar(ind,data[:,3],color='#aaffc3',bottom=data[:,2]+data[:,1],label='Positive')
        ax.bar(ind,data[:,4],color='#3cb44b',bottom=data[:,3]+data[:,2]+data[:,1],label='Very Positive')
        ax.set_xlabel('Hour')
        ax.set_ylabel('Count')
        ax.set_xticks(ind,labels)
        plt.title('Hourly counts of each sentiment class')
        plt.xticks(ind,labels)
        ax.legend()
        
        path = os.path.join(self.plots_path,'hourly_counts.svg')
        print('Plot saved in '+path)
        plt.savefig(path,format='svg') 
   
    def hourly_perc_plot(self):
        labels = self.hourly_labels

        data = []
        for r in self.hourly_stats:
            d,vn,n,p,vp = r
            print(d,vn,n)
            t = vn+n+p+vp
            vn,n,p,vp = vn/t*100, n/t*100, p/t*100, vp/t*100
            data.append([d,vn,n,p,vp])
        data = np.array(data)
            
          # Percentage Plot
        fig,ax = plt.subplots(figsize=self.plots_size)
        ind = np.arange(len(labels))

        ax.bar(ind,data[:,1],color='#e6194b',label='Very Negative')
        ax.bar(ind,data[:,2],color='#fabebe',bottom=data[:,1],label='Negative')
        ax.bar(ind,data[:,3],color='#aaffc3',bottom=data[:,2]+data[:,1],label='Positive')
        ax.bar(ind,data[:,4],color='#3cb44b',bottom=data[:,3]+data[:,2]+data[:,1],label='Very Positive')
        ax.set_ylim([0,100])
        ax.set_xlabel('Hour') 
        ax.set_ylabel('Percentage')
        plt.title('Hourly percentage of each sentiment class')   
        plt.xticks(ind,labels)
        ax.legend()
  
        path = os.path.join(self.plots_path,'hourly_perc_counts.svg')
        print('Plot saved in '+path)
        plt.savefig(path,format='svg')
            
    def daily_plots(self):
        self.daily_stats = self.daily_stats()     
        self.daily_counts_plot();
        self.daily_perc_plot();  
        
    def daily_counts_plot(self):
        data = self.daily_stats
        labels = self.daily_labels
        
        fig,ax = plt.subplots(figsize=self.plots_size)
        ind = np.arange(len(labels))
        ax.bar(ind,data[:,1],color='#e6194b',label='Very Negative')
        ax.bar(ind,data[:,2],color='#fabebe',bottom=data[:,1],label='Negative')
        ax.bar(ind,data[:,3],color='#aaffc3',bottom=data[:,2]+data[:,1],label='Positive')
        ax.bar(ind,data[:,4],color='#3cb44b',bottom=data[:,3]+data[:,2]+data[:,1],label='Very Positive')
        ax.set_xlabel('Day') 
        ax.set_ylabel('Count')
        ax.set_xticks(ind,labels)
        plt.title('Daily counts of each sentiment class')
        plt.xticks(ind,labels)
        ax.legend()
        
        path = os.path.join(self.plots_path,'daily_counts.svg')
        print('Plot saved in '+path)
        plt.savefig(path,format='svg')
        
    def daily_perc_plot(self):
        labels = self.daily_labels

        data = []
        for r in self.daily_stats:
            d,vn,n,p,vp = r
            print(d,vn,n)
            t = vn+n+p+vp
            vn,n,p,vp = vn/t*100, n/t*100, p/t*100, vp/t*100
            data.append([d,vn,n,p,vp])
        data = np.array(data)
            
          # Percentage Plot
        fig,ax = plt.subplots(figsize=self.plots_size)
        ind = np.arange(len(labels))

        ax.bar(ind,data[:,1],color='#e6194b',label='Very Negative')
        ax.bar(ind,data[:,2],color='#fabebe',bottom=data[:,1],label='Negative')
        ax.bar(ind,data[:,3],color='#aaffc3',bottom=data[:,2]+data[:,1],label='Positive')
        ax.bar(ind,data[:,4],color='#3cb44b',bottom=data[:,3]+data[:,2]+data[:,1],label='Very Positive')
        ax.set_ylim([0,100])
        ax.set_xlabel('Day') 
        ax.set_ylabel('Percentage')
        plt.title('Daily percentage of each sentiment class')   
        plt.xticks(ind,labels)
        ax.legend()
  
        path = os.path.join(self.plots_path,'daily_perc_counts.svg')
        print('Plot saved in '+path)
        plt.savefig(path,format='svg')
        
         
if __name__ == '__main__':
   
    a = Analysis('data.json')
    a.hourly_plots()
    a.daily_plots()
  
  
