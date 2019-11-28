# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 17:11:11 2019

@author: Yue
"""
import pandas as pd
import numpy as np

#scatter plot
table = pd.read_csv("data.csv", index_col=None)
ax = table.plot.scatter(x='1', y='index_label',title='Accumulative Melbourne StackOverFlow users')
ax.set_xlabel("Page Number")
ax.set_ylabel("Users count")

#curve-fitting to find Melbourne users count in remaining unsearched pages
x = np.array(table['1'])
y = np.array(table['index_label'])
f1 = np.polyfit(x, y,3)
p1 = np.poly1d(f1)
yvals = p1(304877)  #fitted accumulative Melbourne users in the last page
print('Estimated Total Melbourne Users',yvals)