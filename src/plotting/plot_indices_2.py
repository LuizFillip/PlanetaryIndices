import numpy as np
import matplotlib.pyplot as plt
import settings as s
from common import plot_terminators, load
from PlanetaryIndices import repeat_values_in_data

def plot_mag_electron(ax, infile):
    
    df = load(infile + 'omni_2012_2015.lst')

    df = df.loc[~((df['BZ'] > 990) | 
                  (df['Ey'] > 990))]

    ax.plot(df['BZ'])
    
    ax.set(ylim = [-25, 25], ylabel = "$B_z$ (nT)")
    
    ax1 = ax.twinx()
    
    line, = ax1.plot(df['Ey'], color = '#0C5DA5')
    
    ax1.set(ylim = [-25, 25], ylabel = "$E_y$ (mV/m)")
    
    s.change_axes_color(ax1, line)
    
def plot_kp(ax, infile):
    
    kp = load(infile + "Kp_hourly.txt")
    x = kp.index
    y = kp["Kp"].values
    
    ax.bar(x, y, width = 0.1, color = "gray")
    
    ax.set(
        ylabel = 'Kp', 
        ylim = [0, 9], 
        yticks = np.arange(0, 9, 2)
        )
    
    
    f = repeat_values_in_data(
        load(infile + 'solar_flux.txt')
        )
    ax1 = ax.twinx()
    
    line, = ax1.plot(f['F10.7a'], color = 'red')
    ax1.set(ylabel = '$F_{10.7}$')
    s.change_axes_color(ax1, line)
    
def plot_aroural(ax, infile):

    ae = load(infile + "kyoto2013_03.txt")
    
    ax.plot(ae[["AE", "AL"]], 
               label = ['AE', 'AL'])
    
    ax.set(ylabel = 'AE/AL (nT)', 
              ylim = [-3000, 3000])
    
    ax.legend(ncol = 2, loc = 'upper right')
    
def plot_dst(ax, infile):
    dst = load(infile + "kyoto2000.txt")
    
    ax.plot(dst['dst'])
    
    ax.set(
        xlim = [dst.index[0], dst.index[-1]], 
        ylim = [-150, 70],
        ylabel = "Dst (nT)"
        )
    
    ax1 = ax.twinx()
    df = load(infile + 'omni_2012_2015.lst')
    line, = ax1.plot(df['SymH'], color = '#0C5DA5')
    
    ax1.set(ylabel = 'SYM-H', ylim = [-200, 100])
    s.change_axes_color(ax1, line)
    
    
    return dst
    
def plot_solar_wind(ax, infile):
    df = load(infile + 'omni_2012_2015.lst')
    df = df.loc[~(df['Speed'] > 9990)]
    ax.plot(df['Speed'])
    
    ax.set(ylabel = '$V_{sw}$ (km/s)', ylim = [200, 900])
    
    
    
def plot_indices_2():
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (14, 14),
        sharex = True,
        nrows = 5
        )
    
    plt.subplots_adjust(hspace = 0)
    
    infile = 'database/PlanetaryIndices/'
    
    plot_solar_wind(ax[0], infile)
    plot_aroural(ax[1], infile)
    plot_mag_electron(ax[2], infile)
    plot_kp(ax[3], infile)
    df = plot_dst(ax[4], infile)
    
    s.format_time_axes(ax[4], pad = 60)
    
    for i, ax in enumerate(ax.flat):
        letter = s.chars()[i]
        ax.axhline(0, linestyle = '--')
        ax.text(
            0.02, 0.83, f"({letter})", 
            transform = ax.transAxes
            )
        plot_terminators(ax, df)
    return fig 

f = plot_indices_2()

# f.savefig('PlanetaryIndices/figures/IMF_index.png', dpi = 300)