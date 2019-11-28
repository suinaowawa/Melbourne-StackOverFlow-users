# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 21:07:55 2019

@author: Yue

input: https://stackoverflow.com/users/696257/dkulkarni

"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns
from tkinter import *

# Function for get HTML text from input url
def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("Failed!")

# Function for getting user's reputation score
def getData(html):
    soup = BeautifulSoup(html, "html.parser")
    a=soup.find('div',attrs={'class':'grid--cell fs-title fc-dark'}).getText().replace(',','')
    if a == '':
        reputationScore = 0
    else:
        reputationScore = int(a)
    return reputationScore

# The app interface using tkinter
root = Tk()
root.title('test_APP')
frame = Frame(root)

f = Figure(figsize=(8,6), dpi=100) 
canvas = FigureCanvasTkAgg(f, master=frame) 
canvas.get_tk_widget().grid(row=1, column=3, rowspan=6) 

p = f.gca() 
frame.pack(padx=10, pady=10)
v1 = StringVar()
v2 = StringVar()
v3 = StringVar()
v4 = StringVar()

Label(frame, text='Please input your StackOverFlow URL:').grid(row=0, column=0)
e1 = Entry(frame, width=80, textvariable=v1).grid(row=1,column=0)
e2 = Entry(frame, width=80, textvariable=v2, state='readonly',).grid(row=3, column=0)
e3 = Entry(frame, width=80, textvariable=v3, state='readonly').grid(row=4, column=0)
e4 = Entry(frame, width=80, textvariable=v4, state='readonly').grid(row=5, column=0)

def main_func():
    url = v1.get()
    html=getHTMLText(url)
    score = getData(html)
    table = pd.read_csv("data.csv", index_col=None)
    table = table.append(
                pd.Series(
                    [table.shape[0]+1,score,1],
                    index=table.columns,
                    name=table.shape[0]+1,
                )
            )
    
    table=table.sort_values(by=["0"] , ascending=False)
    table.index = range(len(table))
    rank = table[table['0'].isin([score])].index+1
    rank = rank[0] 
    
    v2.set("Your reputation score is %d."%score)
    v3.set("Your rank in Melbourne is %d out of 151,601."%rank)
    percentage=100*rank/151601
    v4.set("You are in the top %.4f%s of Melbourne Stackoverflow users based on reputation."%(percentage,'%'))

    sns.set()
    sns.set_context("talk")
    n, bins, patches=p.hist(table['0'], 25) 

    close_bin=min(bins, key=lambda x:abs(x-score))
    bin_num=list(bins).index(close_bin)
    patches[bin_num].set_color('r')

    p.set_xlabel('Reputation', fontsize = 15) 
    p.set_ylabel('Users count', fontsize = 15)
    p.set_title('Histogram of Melbourne StackOverFlow users\' reputation')
    canvas.draw()

Button(frame, text='See your ranking in Melbourne', command=main_func).grid(row=2, column=0, pady=5)
mainloop()


