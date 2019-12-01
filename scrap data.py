# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 20:44:53 2019

@author: Yue
"""

import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import numpy as np
users_count = 0  #variable to count Melbourne users
flag = 0   #indicator for stop scraping
# use pandas dataframe to store all data
table = pd.DataFrame(columns=list(range(2)), dtype=np.float64)
#table = pd.DataFrame(pd.read_csv("table_new3.csv",index_col=0))

# This is a small utility for printing readable time strings:
def format_time(seconds):
    if seconds < 400:
        s = float(seconds)
        return "%.1f seconds" % (s,)
    elif seconds < 4000:
        m = seconds / 60.0
        return "%.2f minutes" % (m,)
    else:
        h = seconds / 3600.0
        return "%.2f hours" % (h,)

# Function to get the HTML text
def getHTMLText(url,k):
    try:
        kw={'page':k,'tab':'Reputation','filter':'all'}
        r = requests.get(url,params=kw,headers={'User-Agent': 'Mozilla/4.0'})
        r.raise_for_status()
        return r.text
    except:
        print("Failed!")

# scrap wanted data (reputation of Melbourne user) from HTML
def getData(html,k):
    soup = BeautifulSoup(html, "html.parser")
    usersList = soup.find('div',attrs={'class':'grid-layout'}) # find the all users in one page
    count = 1
    for user in usersList.find_all('div',attrs={'class':'grid-layout--cell'}): # for each user       
        data = []
        user_detail=user.find('div',attrs={'class':'user-details'})
        user_location=user_detail.find('span',attrs={'class':'user-location'}).getText()
        if 'Melbourne' in user_location:
            global users_count
            users_count += 1
            print(user_location)
            
            reputationString=user_detail.find('div',attrs={'class':'-flair'}).find('span',attrs={'class':'reputation-score'}).getText()
#           if reputation with K in string, get exact number from 'title'
            if 'k' in reputationString:
                reputationScore=user_detail.find('div',attrs={'class':'-flair'}).find('span',attrs={'class':'reputation-score'}).attrs['title']
                a=reputationScore[17:-1].replace(',','')
                reputationScore = int(a)
            else:
                reputationScore = int(reputationString.replace(',',''))
                                    
            data.append(users_count)
            data.append(reputationScore)
            print(reputationScore)
            data.append(k)
            count += 1
            global table
            table = table.append(
                pd.Series(
                    data[1:len(data)],
                    index=table.columns,
                    name=data[0],

                )
            )
        else:
            pass
    
    return data



# main

start_time = datetime.datetime.now()
basic_url = 'https://stackoverflow.com/users'
k = 0 # start page
while k<=304877:    
    if flag == 1:
        #break loop when found user with reputation 1
        break
    k+=1
    html=getHTMLText(basic_url,k)
    getData(html,k)
    end_time = datetime.datetime.now()
    dt = end_time - start_time
    seconds = dt.total_seconds()
    t = format_time(seconds)
    print("Page %s Done| time spent %s | found count %d" %(k,t,users_count))
    table.to_csv("data.csv", index_label="index_label")

end_time = datetime.datetime.now()
dt = end_time - start_time
seconds = dt.total_seconds()
t = format_time(seconds)
print("total_time",t)
table.to_csv("data.csv", index_label="index_label")
