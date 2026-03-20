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
from math import log10, floor

# %%
def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x
# %%
def setStyle():
    #Plot Style
    plt.style.use(['science', 'muted' ]) #,'muted' ,'high-vis''ieee',
    
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
    plt.rc('figure', titlesize=SMALL_SIZE)  # fontsize of the figure title\n",
    plt.rcParams['text.usetex'] = True
    plt.rcParams['figure.figsize'] = fig_size
    plt.rcParams['figure.dpi'] = 200 #Default dpi, useful so that plots are a decent size in jupyter
    
    
    colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    print(plt.rcParams['axes.prop_cycle'].by_key()['color'][1])
    
    x=np.linspace(0,1000,1000)
    R = [0,1,2,3,5,6,7,8,9,10] # [str(r) for r in R]
    labels =  [str(r) for r in R] #['\u03C3 = 2.5 nm, $c$ = 2 nm','\u03C3 = 0.5 nm, $c$ = 2 nm','\u03C3 = 2.5 nm, $c$ = 10 nm','\u03C3 = 0.5 nm, $c$ = 10 nm']
    for i, r in enumerate(R):
        plt.plot(x/(r+1), label=labels[i])
        # plt.plot(x,x/(i+1),label=i)
    plt.legend()
    # plt.savefig('/home/jerome/Documents/MASTERS/Figures/surfacePlotLegend.pdf')
    # plt.savefig('/home/jerome/Documents/MASTERS/Figures/surfacePlotLegend.png', dpi=2000)
    plt.show()

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
    print(np.shape(peaks))
    heighty = peaks[1]['peak_heights'] #list of the heights of the peaks
    print(heighty)
    peak_pos = x[int(peaks[0])] #list of the peaks positions

    
    ax.plot(x*xunit_modifier, y, label=str(name),color = color)
    ax.scatter(peak_pos*xunit_modifier,heighty,color = color, s = 15, marker = 'D')
    
def plotStokes1D(S0,S1,S2,S3, r, sF=1, axis = 1):
    
    tickAx = [round_sig(-r*sF/2),
          round_sig(-r*sF/4),
          0,
          round_sig(r*sF/4),
          round_sig(r*sF/2)
          ]
    
    # nx = len(S0)
    # print("HERE")
    # print(np.shape(nx))
    
    if axis == 1:
        nx = len(S0)
        print(nx)
        fig, axs = plt.subplots(2, 2)
        im = axs[0, 0].plot(S0, label="S0")
        axs[0, 0].set(ylabel="Normalised Amplitude")
        axs[0, 1].plot(S1, label="S1")
        axs[1, 0].plot(S2, label="S2")
        axs[1, 0].set(xlabel="position [m]", ylabel="Normalised Amplitude")
        axs[1, 1].plot(S3, label="S3")
        axs[1, 1].set(xlabel="position [m]")
    
        for ax in axs.flat:
            ax.legend()
            ax.set_xticks(np.arange(0,nx+1,nx/4))
            ax.set_xticklabels(tickAx)
        # print("Saving Stokes Cuts Plots to: {}".format(dirPath + 'plots/stokesPlotsXcut' + pk[0:len(str(pk))-4] + '.png'))
        # plt.savefig(dirPath + 'plots/stokesPlotsXcut' + pk[0:len(str(pk))-4] + '.png')
        plt.show()
        plt.clf()    
    
    elif axis == 2:
        nx = len(S0[0])
        fig, axs = plt.subplots(2, 2)
        axs[0, 0].plot(S0[0], label="S0: x-cut")
        axs[0, 0].plot(S0[1], label="S0: y-cut")
        axs[0, 0].set(ylabel="Normalised Amplitude")
        axs[0, 1].plot(S1[0], label="S1: x-cut")
        axs[0, 1].plot(S1[1], label="S1: y-cut")
        axs[1, 0].plot(S2[0], label="S2: x-cut")
        axs[1, 0].plot(S2[1], label="S2: y-cut")
        axs[1, 0].set(xlabel="position [m]", ylabel="Normalised Amplitude")
        axs[1, 1].plot(S3[0], label="S3: x-cut")
        axs[1, 1].plot(S3[1], label="S3: y-cut")
        axs[1, 1].set(xlabel="position [m]")
    
        for ax in axs.flat:
            ax.legend()
            ax.set_xticks([0,nx/4,nx/2,3*nx/4,nx])
            ax.set_xticklabels(tickAx)
            
        # print("Saving Stokes Cuts Plots to: {}".format(dirPath + 'plots/stokesPlotsXcut' + pk[0:len(str(pk))-4] + '.png'))
        # plt.savefig(dirPath + 'plots/stokesPlotsXcut' + pk[0:len(str(pk))-4] + '.png')
        plt.show()
        plt.clf()            

if __name__ == '__main__':
    setStyle()
