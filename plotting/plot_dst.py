import numpy as np
import matplotlib.pyplot as plt
from PlanetaryIndices import OMNI2
import settings as s
import datetime as dt


def plot_disturbance_index(
        ax, 
        df, 
        col = "dst"
        ):
    
    """Plotting Disturbance Storm and Kp indexes"""
    
    args = dict(linestyle = "--", color = "k", lw = 1)
    
    if col == "dst":
        ax.plot(df[col], lw = 1, color = "k")
        ax.axhline(0, **args)
        
        # vmin, vmax, step = compute_ticks(df[col])
        
        ax.set(ylabel = "Dst (nT)", 
               # ylim = [vmin - step, vmax], 
               # yticks = np.arange(
               #     vmin, 
               #     vmax + step, 
               #     step
               #     )
               )
    else:
        y = df[col]
        x = df.index
        ax.axhline(4, **args)
        ax.bar(x, y, width = 2, color = "k")
    
        ax.set(ylabel = "Índice Kp", 
               ylim = [0, 9],
               yticks = np.arange(0, 10, 2)
                       )
    
    s.format_axes_date(ax)
    
import pandas as pd
infile = "database/PlanetaryIndices/kyoto2000.txt"
# 


# df = df[(df.index > dt.datetime(2013, 3, 13)) &
#         (df.index < dt.datetime(2013, 3, 23))]


df = pd.read_csv(infile, index_col=0)
df.index = pd.to_datetime(df.index)

df