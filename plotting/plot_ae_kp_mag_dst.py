import numpy as np
import matplotlib.pyplot as plt
import settings as s
import datetime as dt
import pandas as pd
from common import plot_terminators
from PlanetaryIndices import plot_disturbance_index
from common import load


ae = load("database/PlanetaryIndices/kyoto2013_03.txt")


s.config_labels()

fig, ax = plt.subplots(
    dpi = 300,
    figsize = (10, 10),
    sharex = True,
    nrows = 4
    )

plt.subplots_adjust(hspace = 0.1)
ax[0].plot(ae[["AE", "AL"]], label = ['AE', 'AL'])

kp = load("database/PlanetaryIndices/Kp_hourly.txt")

x = kp.index
y = kp["Kp"].values

ax[1].bar(x, y, width = 0.1, color = "gray")

ax[0].set(ylabel = 'AE/AL (nT)', 
          ylim = [-3000, 3000])

ax[1].set(ylabel = 'Kp', 
          ylim = [0, 9], 
          xlim = [kp.index[0], kp.index[-1]],
          yticks = np.arange(0, 9, 2))

mag = load("database/magnetometers/mag.txt").sort_index()



ax[2].plot(mag['F'])

ax1 = ax[2].twinx()

line, = ax1.plot(mag['Z'], color = '#0C5DA5')

ax[2].set(ylim = [26100, 26400], ylabel = "$B_F$ (nT)")
ax1.set(ylim = [-3300, -3500], ylabel = "$B_z$ (nT)")

s.change_axes_color(ax1, line)

ax[3].axhline(0, linestyle = "--")
ax[0].axhline(0, linestyle = "--")


dst = load("database/PlanetaryIndices/kyoto2000.txt")

ax[3].plot(dst['dst'])

ax[3].set(ylim = [-150, 50], ylabel = "Dst (nT)")
s.format_time_axes(ax[3])



for i, ax in enumerate(ax.flat):
    letter = s.chars()[i]
    ax.text(0.015, 0.85, f"({letter})", 
            transform = ax.transAxes)
    plot_terminators(ax, dst)
    
    
fig.savefig("PlanetaryIndices/figures/dst_ae_index.png", 
            dpi = 300, 
            pad_inches = 0, 
            bbox_inches = "tight")


