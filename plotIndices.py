# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 11:45:16 2022

@author: Luiz
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from main import *

def postdamPlot(ax):
    ax.plot(df, lw = 1, color = "gray")
    
    ax.set(ylabel = "Ap index", xlabel = "Months")
    
    ax.axhline(22, color = "k", 
               linestyle = "--", label = "Ap = 22 (kp = 4)")
    
    ax.legend(loc = "upper right")
    



infile = "Database/"
filename = "OMNI2.txt"

df = OMNI2Data(infile, 
          filename,
          year = 2014, 
          parameter = None)


fig, ax = plt.subplots(figsize = (8, 10), 
                       nrows = 4, sharex = True)


plt.subplots_adjust(hspace = 0.0)


kwargs = dict(lw = 0.8, 
             color = "k")


df["dst"].plot(ax = ax[0], **kwargs)

ax[0].set(ylabel = "Dst (nT)")
df["kp"].plot(ax = ax[1], **kwargs)


ax[1].set(ylabel = "Kp index", 
          ylim = [0, 9])


df[['ae', 'al']].plot(ax = ax[2], 
                      legend = False)


ax[2].set(xlabel = "Months", )
for ax in ax.flat:
    ax.axhline(0, lw = 1, 
               linestyle = "--", 
               color = "k")
print(df)