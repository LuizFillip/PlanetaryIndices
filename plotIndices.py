import numpy as np
import matplotlib.pyplot as plt
from base import postdamData, OMNI2Data
import setup as s
from datetime import datetime, timedelta
import matplotlib.dates as dates


def dateFormating(ax):
    
    ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))
    


def plotSolarflux(ax, 
                  years = [1996, 2020], 
                  yshade = 2014):
    
    """Plotting Solar flux F10.7 cm"""
    
    sflux = postdamData(infile = "database/postdam.txt")
    
    sflux = sflux.loc[(sflux.index.year > years[0]) & 
                      (sflux.index.year < years[-1]) & 
                      (sflux["F10.7obs"] > 10) & 
                      (sflux["F10.7obs"] < 500)]
    
    
    ax.plot(sflux["F10.7obs"], lw = 0.8, color = "k")
    
    ax.set(ylabel = "$_{F10,7} $ cm", 
           yticks = np.arange(100, 450, 100), 
           xlabel = "Anos")
    
    if yshade:
        date = datetime(yshade, 1, 1)
        end = date + timedelta(days = 366)
        ax.axvspan(date, 
                   end,
                   alpha = 0.5, color = "gray")
        
        ax.text(end, 350, yshade, 
                transform = ax.transData)
    

    
def plotDisturbanceIndex(ax, df, 
                         col = "dst", 
                         label = "Dst (nT)", 
                         ylim = [-100, 50], 
                         step = 30):
    
    """Plotting Disturbance Storm and Kp indexes"""
    
    args = dict(linestyle = "--", color = "k", lw = 1)
    
    if col == "dst":
        ax.plot(df[col], lw = 1, color = "k")
        ax.axhline(0, **args)
    else:
        y = df[col].values
        x = df.index.values 
        ax.axhline(3, **args)
        ax.bar(x, y, width = 1, color = "k")
    
    yticks = np.arange(ylim[0], ylim[-1] + step, step)
        
    ax.set(ylabel = label, 
           ylim = ylim, 
           yticks = yticks)
    
    dateFormating(ax)
    
def plotAuroralIndex(ax, df, 
                     ylim = [-500, 500], 
                     step = 200):
    
    """Plotting auroral indexes"""
    
    args = dict(lw = 1)
    
    ax.plot(df['ae'], color = "k", **args)
    
    ax1 = ax.twinx()
    
    p1, = ax1.plot(df["al"], **args)
    
    s.change_axes_color(ax1, p1)
    
    ax.axhline(0, linestyle = "--", 
               color = "k", **args)
    
    
    yticks =  np.arange(ylim[0], 
                        ylim[-1] + step, step)
                        
    ax1.set(ylabel = "AL (nT)", 
            ylim = ylim, 
            yticks = yticks)
    
    ax.set(ylabel = "AE (nT)", 
            ylim = ylim, 
            yticks = yticks)
    
    dateFormating(ax)
    
def plotIndices():
    
    
    fig = plt.figure(figsize = (8, 6))
    
    s.config_labels()
    
    gs = fig.add_gridspec(1, bottom = 0.98, top = 1.2)
    ax1 =  gs.subplots()
    plotSolarflux(ax1)


    gs = fig.add_gridspec(3, hspace = 0.1)
    (ax2, ax3, ax4) = gs.subplots(sharex = 'col')
    
    df = OMNI2Data(infile = "database/omni.txt",
                   year = 2014, parameter = None)
    
    plotDisturbanceIndex(ax2, df)
    
    plotDisturbanceIndex(ax3, df, 
                         col = "kp", 
                         label = "Índice Kp", 
                         ylim = [0, 9], 
                         step = 2)
     
    plotAuroralIndex(ax4, df)
    
    ax4.set(xlabel = "Meses")
    
    s.text_painels([ax1, ax2, ax3, ax4], 
                   x = 0.01, y = 0.85)

    plt.show()
    
    return fig
    
fig = plotIndices()
    
fig.savefig("img/PlanetaryIndices.png")