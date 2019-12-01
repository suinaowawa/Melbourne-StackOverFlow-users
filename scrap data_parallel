# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 21:45:21 2019

@author: Yue
"""
import requests
from bs4 import BeautifulSoup
import datetime
import time
import multiprocessing
import csv

class crawl:
    
    def __init__(self,users_count):
        self.users_count = users_count
    
    def getHTMLText(self,url):        
        try:
            r = requests.get(url,headers={'User-Agent': 'Mozilla/4.0'})
            r.raise_for_status()
            return r.text
        except:
            print("Failed!") 
    
    def getData(self,html):
        
        soup = BeautifulSoup(html, "html.parser")
        usersList = soup.find('div',attrs={'class':'grid-layout'}) # find the all users in one page
        
        for user in usersList.find_all('div',attrs={'class':'grid-layout--cell'}): # for each user       
            
            user_detail=user.find('div',attrs={'class':'user-details'})
            user_location=user_detail.find('span',attrs={'class':'user-location'}).getText()
            
            if 'Melbourne' in user_location:
                time.sleep(0.00001)
                self.users_count.value += 1
                reputationString=user_detail.find('div',attrs={'class':'-flair'}).find('span',attrs={'class':'reputation-score'}).getText()
    #           if reputation with K in string, get exact number from 'title'
                if 'k' in reputationString:
                    reputationScore=user_detail.find('div',attrs={'class':'-flair'}).find('span',attrs={'class':'reputation-score'}).attrs['title']
                    a=reputationScore[17:-1].replace(',','')
                    reputationScore = int(a)
                else:
                    reputationScore = int(reputationString.replace(',',''))
                    
                with open("data2.csv", "a",newline='',encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow((self.users_count.value,reputationScore,user_location))#写入表头信息
                    csvfile.close()
    
            else:
                pass
        
    def format_time(self,seconds):
        if seconds < 400:
            s = float(seconds)
            return "%.1f seconds" % (s,)
        elif seconds < 4000:
            m = seconds / 60.0
            return "%.2f minutes" % (m,)
        else:
            h = seconds / 3600.0
            return "%.2f hours" % (h,)
    
    def main_func(self,url):
        html = self.getHTMLText(url)
        self.getData(html)

if __name__ == '__main__':
    start_page = 1
    end_page = 100
    
    fp =open('data2.csv','w',newline='',encoding='utf-8')
    writer = csv.writer(fp)
    writer.writerow(('Users count','reputation','location'))#write header
    fp.close()
    
    users_count = multiprocessing.Manager().Value('d',0)
    crawler = crawl(users_count)
    
    start_time = datetime.datetime.now()
    urls = []
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    
    for i in range(start_page, end_page+1):
        url = 'https://stackoverflow.com/users' + '?page=' + str(i) + '&tab=reputation&filter=all'
        urls.append(url)
    print("processing Page%s---Page%s"%(start_page,end_page))
    
    pool.map(crawler.main_func,urls)
    pool.close()
    pool.join()
    
    end_time = datetime.datetime.now()
    dt = end_time - start_time
    seconds = dt.total_seconds()
    t = crawler.format_time(seconds)
    print('total_time',t)
    
