import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from base import postdamData, OMNI2Data
import plotConfig 
from datetime import datetime, timedelta


def change_axes_color(ax, p,
                      axis = "y", 
                      position = "right"
                      ):
    
    ax.yaxis.label.set_color(p.get_color())
    
    ax.yaxis.label.set_color(p.get_color())
    
    ax.tick_params(axis='y', colors = p.get_color())
    
    ax.spines['right'].set_color(p.get_color())
    



def plotSolarflux(ax, 
                  ystart = 1990, yend = 2019, 
                  yshade = 2014):
    sflux = postdamData(infile= "database/postdam.txt")
    
    sflux = sflux.loc[(sflux.index.year > ystart) & 
                      (sflux.index.year < yend) & 
                      (sflux["F10.7obs"] > 10) & 
                      (sflux["F10.7obs"] < 500)]
    
    
    ax.plot(sflux["F10.7obs"], lw = 0.8, color = "k")
    
    ax.set(ylabel = "$_{F10,7} $ cm", 
           yticks = np.arange(100, 450, 100), 
           xlabel = "Anos")
    if yshade:
        date = datetime(yshade, 1, 1)
        ax.axvspan(date, 
                   date + timedelta(days = 366),
                   alpha = 0.5, color = "gray")
    
def dateFormating(ax):
    import matplotlib.dates as dates
    ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))
    
def plotDisturbanceIndex(ax, df, 
                         col = "dst", 
                         label = "Dst (nT)", 
                         ylim = [-100, 50], 
                         yticks = np.arange(-150, 50, 50)):
        
    if col == "dst":
        ax.plot(df[col], lw = 1.5, color = "k")
        ax.axhline(0, linestyle = "--", color = "k")
    else:
        y = df[col].values
        x = df.index.values 
        ax.bar(x, y, width = 1, color = "k")
        
    ax.set(ylabel = label, 
           ylim = ylim, 
           yticks = yticks)
    
    dateFormating(ax)
    
def plotAuroralIndex(ax, df, 
                     ylim = [-500, 500], 
                     step = 200):
    
    kwargs = dict(lw = 2)
    
    ax.plot(df['ae'], lw = 2, color = "k")
    
    ax1 = ax.twinx()
    
    p1, = ax1.plot(df["al"], **kwargs)
    
    change_axes_color(ax1, p1)
    
    ax.axhline(0, **kwargs, linestyle = "--", color = "k")
    yticks =  np.arange(ylim[0], ylim[-1] + step, step)
                        
    ax1.set(ylabel = "AL (nT)", 
            ylim = ylim, 
            yticks = yticks)
    
    ax.set(ylabel = "AE (nT)", 
            ylim = ylim, 
            yticks = yticks)
    
    dateFormating(ax)
    
def plotIndices(save = False):
    
    
    fig = plt.figure(figsize = (20, 18))
    
    
    
    df = OMNI2Data(infile = "database/omni.txt",
              year = 2014, 
              parameter = None)
    
    
    
    gs = fig.add_gridspec(1, bottom = 0.98, top = 1.2)
    ax1 =  gs.subplots()
    plotSolarflux(ax1)


    gs = fig.add_gridspec(3, hspace=0, wspace=0)
    (ax2, ax3, ax4) = gs.subplots(sharex='col')
    
    
    
    plotDisturbanceIndex(ax2, df)
    
    plotDisturbanceIndex( ax3, df, 
                         col = "kp", 
                         label = "Índice Kp", 
                         ylim = [0, 9], 
                         yticks = np.arange(0, 10, 2))
     
    plotAuroralIndex( ax4, df)
    
    
    ax4.set(xlabel = "Meses")

    plt.show()
    
    return fig
    
plotIndices(save = False)
    