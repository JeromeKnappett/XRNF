'''
Custom plot style for the latex template ltu-thesis using the SciencePlots colour scheme 'muted' and batlow colourmap

Requires
https://github.com/garrettj403/SciencePlots ## for plot style
https://pypi.org/project/cmcrameri/         ## for batlow colour map

To use:

    from plt_style import *

'''

import matplotlib.pyplot as plt
import numpy as np

#Plot Style
#plt.style.use(['science','muted','no-latex'])

#Plot Parameters
fig_width_pt = 426.79134  # Get this from LaTeX using \\showthe\\columnwidth\n",
inches_per_pt = 1.0/72.27               # Convert pt to inches\n",
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio\n",
fig_width = fig_width_pt*inches_per_pt  # width in inches\n",
fig_height =fig_width*golden_mean       # height in inches\n",
fig_size = [fig_width,fig_height]

SMALL_SIZE = 4
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

#plt.rcParams["image.cmap"]  = cm.batlow
plt.rc('font', size=10)          # controls default text sizes\n",
plt.rc('axes', titlesize=10)     # fontsize of the axes title\n",
plt.rc('axes', labelsize=10)    # fontsize of the x and y labels\n",
plt.rc('xtick', labelsize=8)    # fontsize of the tick labels\n",
plt.rc('ytick', labelsize=8)    # fontsize of the tick labels\n",
plt.rc('legend', fontsize=8)    # legend fontsize\n",
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title\n",
plt.rcParams['text.usetex'] = False
plt.rcParams['figure.figsize'] = fig_size
plt.rcParams['figure.dpi'] = 150 #Default dpi, useful so that plots are a decent size in jupyter


print(plt.rcParams['axes.prop_cycle'].by_key()['color'][1])

def findpeaks(x,y,name,ax, color,xunit_modifier=1):
    '''
    Variables:
    x : x-axis data
    y : y-axis data
    name : Name for legend as a string
    ax : passes ax from matplotlib
    xunit_modifier : My calculations use microns so I set this at 1000 to convert to nm
    color : gets next color from axis plot cycle
    ------------------------------------------------------------------
    EXAMPLE:
    import matplotlib.pyplot as plt
    from plt_style import *

    wl = 0.0067 #wavelength in microns
    fig,ax = plt.subplots() #Initiates plots
    color = next(ax._get_lines.prop_cycler)['color'] #gets colour so line and peak are the same colour

    findpeaks(x,y,str(name),ax,color)

    ax.set_xlabel('Thickness (nm)')
    ax.set_ylabel(r'$\mathcal{D}_1$')
    ax.set_xlim(0,250)
    ax.legend()
    plt.savefig('diff_eff_Ni3Al_vs_others_at{}nm.pdf'.format(wl*1000))
    plt.savefig('diff_eff_Ni3Al_vs_others_at{}nm.png'.format(wl*1000),dpi=2000)

        

    '''
    from scipy.signal import find_peaks
    peaks = find_peaks(y, height=(max(y)))
    heighty = peaks[1]['peak_heights'] #list of the heights of the peaks
    peak_pos = x[peaks[0]] #list of the peaks positions

    
    ax.plot(x*xunit_modifier, y, label=str(name),color = color)
    ax.scatter(peak_pos*xunit_modifier,heighty,color = color, s = 15, marker = 'D')
