import locale
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
import os
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

latex = "G:\\My Drive\\Doutorado\\Modelos_Latex_INPE\\docs\\Proposal\\Figures\\"
def path_tex(folder):
    
    return os.path.join(latex, folder)

fontsize = 35

lw = 1
major = 8
minor = 4
plt.rcParams.update({'font.size': fontsize, 
                     'axes.linewidth' : lw,
                     'grid.linewidth' : lw,
                     'lines.linewidth' : lw,
                     'legend.frameon' : False,
                     'savefig.bbox' : 'tight',
                     'savefig.pad_inches' : 0.05,
                     'mathtext.fontset': 'dejavuserif', 
                     'font.family': 'serif', 
                     'ytick.direction': 'in',
                     'ytick.minor.visible' : True,
                     'ytick.right' : True,
                     'ytick.major.size' : lw + major,
                     'ytick.major.width' : lw,
                     'ytick.minor.size' : lw + minor,
                     'ytick.minor.width' : lw,
                     'xtick.direction' : 'in',
                     'xtick.major.size' : lw + major,
                     'xtick.major.width': lw,
                     'xtick.minor.size' : lw + minor,
                     'xtick.minor.width' :lw,
                     'xtick.minor.visible' : True,
                     'xtick.top' : True,
                     'axes.prop_cycle' : 
                    plt.cycler('color', ['#0C5DA5', '#00B945', 'k','#FF9500', 
                                                              '#FF2C00', '#845B97', '#474747', '#9e9e9e'])
                         }) 

    
def change_axes_color(ax, p,
                      axis = "y", 
                      position = "right"
                      ):
    """Change color from the other side"""
    ax.yaxis.label.set_color(p.get_color())
    
    ax.yaxis.label.set_color(p.get_color())
    
    ax.tick_params(axis='y', colors = p.get_color())
    
    ax.spines['right'].set_color(p.get_color())

def text_painels(axs, x = 0.01, y = 0.85, 
                 fontsize = fontsize):
    """Plot text for enumerate painels by letter"""
    chars = list(map(chr, range(97, 123)))
    
    if isinstance(axs, np.ndarray):
        list_plots = axs.flat
    if isinstance(axs, list):
        list_plots = axs
    
    for num, ax in enumerate(list_plots):
        char = chars[num]
        ax.text(x, y, f"({char})", 
                transform = ax.transAxes, 
                fontsize = fontsize)
        
        
def dateFormating(ax):
    
    ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))
    
