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
    

def change_axes_color(ax, p,
                      axis = "y", 
                      position = "right"
                      ):
    
    ax.yaxis.label.set_color(p.get_color())
    
    ax.yaxis.label.set_color(p.get_color())
    
    ax.tick_params(axis='y', colors = p.get_color())
    
    ax.spines['right'].set_color(p.get_color())
    
def read_sym_asy(year = 2014):
    
    df = pd.read_csv("Database/asy_sym.txt", 
                     delim_whitespace= True)
    
    
    df.index = pd.to_datetime(df.index)
    
    return df.loc[df.index.year == year, :]   





def plotIndices(save = False):
    
    fig, ax = plt.subplots(figsize = (8, 10), 
                           nrows = 4, 
                           sharex = True)
    
    
    plt.subplots_adjust(hspace = 0.0)
    
    
    df = OMNI2Data(infile = "Database/", 
              filename = "OMNI2.txt",
              year = 2014, 
              parameter = None)
    
    # =============================================================================
    # Dst index
    # =============================================================================
    
    kwargs = dict(lw = 0.8, 
                 color = "k")
    
    
    df["dst"].plot(ax = ax[0], **kwargs)
    
    ax[0].set(ylabel = "Dst (nT)", ylim = [-100, 50])
    
    
    # =============================================================================
    # Kp index
    # =============================================================================
    df["kp"].plot(ax = ax[1], **kwargs)
    
    
    ax[1].set(ylabel = "Kp index", 
              ylim = [0, 9])
    
    
    df['ae'].plot(ax = ax[2], color = "k",
                          legend = False)
    
    ax1 = ax[2].twinx()
    
    p1, = ax1.plot(df["al"], color = '#0C5DA5')
    
    # =============================================================================
    #     Auroral Electrijet Activity
    # =============================================================================
        
    change_axes_color(ax1, p1)
    
    ax1.set(ylabel = "AL (nT)", ylim = [-400, 700])
    
    ax[2].set(ylim = [-400, 700], ylabel = "AE (nT)")
    
    
    # =============================================================================
    #     Symmetric and Assymmetric H
    # =============================================================================
        
    df = read_sym_asy(year = 2014)
    
    
    df["SYM-D"].plot(ax = ax[3], color = "k")
    
    
    ax2 = ax[3].twinx()
    p2, = ax2.plot(df["SYM-H"], color = '#0C5DA5')
    
    
    change_axes_color(ax2, p2)
    
    
    ax2.set(ylim = [-70, 70], ylabel = "SYM-H", 
            xlabel = "Months")
    ax[3].set(ylim = [-70, 70], ylabel = "SYM-D", 
              xlabel = "Months")
    
    # =============================================================================
    #     Reference lines
    # =============================================================================
    
    for ax in [ax1, ax2, ax[0]]:
        ax.axhline(0, linestyle = "--", color = "k")
        
    if save:
        plt.savefig(f"img/all_indices.png", 
                    dpi = 100, bbox_inches="tight")
        
    plt.show()
    
plotIndices(save = True)
    