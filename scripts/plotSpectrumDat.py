#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 11:30:07 2023

@author: jerome
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 10:11:24 2023

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
import xraydb
import pylab
from math import log10, floor


colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]


# %%
def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig - int(floor(log10(abs(x)))) - 1)
    else:
        return x


def plotSpectrumME(datfile, E, n=1, names=None,colours=colours,linestyles='-',Elim=None, fsize=10,savePath=None):
    Isums = []
    hMax = []
    for i in range(0, n):
        T = np.loadtxt(datfile[i], dtype=str, comments=None, skiprows=10, usecols=(0))
        iE = str(
            np.loadtxt(
                datfile[i],
                dtype=str,
                comments=None,
                skiprows=1,
                usecols=(0),
                max_rows=1,
            )
        )[1:]
        fE = str(
            np.loadtxt(
                datfile[i],
                dtype=str,
                comments=None,
                skiprows=2,
                usecols=(0),
                max_rows=1,
            )
        )[1:]
        N = str(
            np.loadtxt(
                datfile[i],
                dtype=str,
                comments=None,
                skiprows=3,
                usecols=(0),
                max_rows=1,
            )
        )[1:]
        iX = str(
            np.loadtxt(
                datfile[i],
                dtype=str,
                comments=None,
                skiprows=4,
                usecols=(0),
                max_rows=1,
            )
        )[1:]
        fX = str(
            np.loadtxt(
                datfile[i],
                dtype=str,
                comments=None,
                skiprows=5,
                usecols=(0),
                max_rows=1,
            )
        )[1:]
        apSize = float(fX) - float(iX)  # [f-i for f,i in zip(fX,iX)]
        dE = (float(fE) - float(iE)) / float(N)  # [(f-i)/n for f,i,n in zip(fE,iE,N)]
        print("Aperture Size [m]:      ", apSize)
        print("Energy Resolution [eV]: ", dE)

        # Converting to float for plotting
        newT = [float(t) for t in T]
        ex = np.linspace(0,10000,10000)
#        np.linspace()
        plt.plot(newT, label=names[i], color=colours[i], linestyle=linestyles[i],lw=1.2)  #'Multi Electron')

        # finding FWHM
        numpeaks = int((float(fE)) / E[i])
        print("Number of peaks: ", numpeaks)
        for n in range(0, numpeaks):
            # print(int(n*(E[i]//dE)))
            # print(int((n+1)*(E[i]//dE)))
            # print(np.shape(np.array(newT)))

            start = 100 + int(n * (E[i] // dE))
            stop = 100 + int((n + 1) * (E[i] // dE))
            # print(start,stop)
            h = np.array(newT[start:stop])
            # h1 = np.array(newT[0:len(newT)//])
            HM = np.argmax(h)  # np.max(h1)/2
            fwhm = len(h[h > h.max() / 2])
            totI = np.sum(newT[start + HM - (fwhm // 2) : start + HM + (fwhm // 2)])
            
            print(int((n+1)*E[0]*(1/dE)))
            print(newT[int((n+1)*E[0]*(1/dE))])
            
            Isums.append(totI)
            hMax.append(newT[int((n+1)*E[0]*(1/dE))])
            
            plt.axvline(x=start + HM - (fwhm // 2), linestyle = ':')#, color='green')
            plt.axvline(x=start + HM + (fwhm // 2), linestyle = ':')#, color='blue')
#
#            plt.axvline(x=start + HM-fwhm/2, linestyle = ':', color='black')#, label='FWHM')
#            plt.axvline(x=start + HM+fwhm/2, linestyle = ':', color='black')
            if n==0:
                plt.text(HM+fwhm+100,h.max()/2,'FWHM: {} eV'.format(round_sig(fwhm*dE)), color='black')
#
#            print(' ')
#            print(HM-fwhm/2)

        # h1 = np.array(newT[0:len(newT)//5])
        # HM = np.argmax(h1)#np.max(h1)/2
        # fwhm = len(h1[h1>h1.max()/2])

        # print(h1.max())

        # plt.plot(newT, label=names[i])#'Multi Electron')
        # plt.axvline(x=HM-fwhm/2, linestyle = ':', color='black')#, label='FWHM')
        # plt.axvline(x=HM+fwhm/2, linestyle = ':', color='black')
        if Elim:
            plt.xticks(
                [len(newT) * a for a in np.arange(0,1,0.02)],
                [dE * len(newT) * a for a in np.arange(0,1,0.02)],fontsize=fsize
            )
        else:
            plt.xticks(
                [len(newT) * a for a in [0, 1 / 5, 2 / 5, 3 / 5, 4 / 5, 1]],
                [dE * len(newT) * a for a in [0, 1 / 5, 2 / 5, 3 / 5, 4 / 5, 1]],
                fontsize=fsize
            )
            # getting harmonic content ratio
            HC = [np.interp(m*E[0]*(1/dE),ex,newT)*1e-8 for m in  [1,2,3,4,5]]
            print("harmonics")
            print(HC)
            print(hMax)
            print(Isums)
        plt.yticks(fontsize=fSize)
        plt.ylabel("Flux [ph/s/.1\%bw]",fontsize=fsize)
#        plt.ylabel("Intensity [ph/s/.1\%bw/mm$^2$]",fontsize=fsize)
        # plt.text(HM+fwhm+100,h1.max()/2,'FWHM: {} eV'.format(round_sig(fwhm*dE)), color='black')
        plt.legend()#loc="upper right")
        plt.xlabel("Photon Energy [eV]",fontsize=fsize)
        # fig.tight_layout()
    if Elim:
        plt.xlim(Elim[0]*(1/dE),Elim[1]*(1/dE))        
        plt.axvline(x=E[0]*(1/dE),color='gray',linestyle=':')
    else:
        [plt.axvline(x=m*E[0]*(1/dE),color='gray',linestyle=':') for m in range(1,numpeaks + 1)]
#        plt.axvline(x=E[0]*(1/dE),color='gray',linestyle=':')
        pass
    plt.legend(fontsize=(2/3)*fsize)#loc='upper center',fontsize=5)
    if savePath:
        plt.savefig(savePath,format='eps')
    else:
        pass
    plt.show()
    
    

    return Isums, hMax


#datfileEUV = "/home/jerome/Downloads/res_spec_me(2).dat"
#datfileBEUV = "/home/jerome/Downloads/res_spec_me(3).dat"
#
#E = [90.44, 184.76]
#
#Isums = plotSpectrumME(
#    [datfileEUV, datfileBEUV], E=E, n=2, names=["E = 90.44 eV", "E = 184.76 eV"]
#)

#datfile92 = '/home/jerome/Documents/PhD/Data/92/res_spec_se_14.3m_B0.6839.dat'
#datfile185 = '/home/jerome/Documents/PhD/Data/185/res_spec_se_14.3m_B0.4605.dat'
#datfile293 = '/home/jerome/Documents/PhD/Data/293/res_spec_se_14.3m_B0.3448.dat'

#E = [92.0,185.0,293.0]
save = False
pylab.rcParams['figure.figsize'] = (5.0, 2.5)
fSize = 10
dirPath = '/home/jerome/Documents/PhD/Data/'
energy = 185
#293
Bfield = [0.4605,0.4605] 
#[0.4605,0.4571,0.453] # all detunings - same WBS
#[0.4605,0.4605] # single detuning - different WBS
#[0.4605,0.4605,0.4571,0.4571,0.453,0.453] # all detunings - different WBS
#0.4571
wbsX,wbsY = [0.84,4],[1,3] # single detuning - different WBS
#[0.84,0.84,0.84],[1,1,1] # all detunings - same WBS
#[4,4,4],[3,3,3] # all detunings - same WBS
#[0.84,4],[1,3] # single detuning - different WBS
#[0.84,4,0.84,4,0.84,4],[1,3,1,3,1,3]
detuning = ['0\%','0\%']
#['0\%', '-0.738\%', '-1.63\%'] # all detunings - same WBS
#['0\%','0\%'] # single detuning - different WBS
#['0\%','0\%', '-0.738\%','-0.738\%', '-1.63\%','-1.63\%']  # all detunings - different WBS
C = [colours[3],colours[5]]
#[colours[5],colours[3],colours[0]] # all detunings - same WBS
#[colours[3],colours[5]] # single detuning - different WBS
#[colours[5],colours[5],colours[3],colours[3],colours[0],colours[0]]  # all detunings - different WBS
L = [':','-']
#['-','-','-']  # all detunings - same WBS
#[':','-'] # single detuning - different WBS
#['--','-','--','-','--','-']  # all detunings - different WBS

Elimit = None
#[175,200]
#None
#[140,220]

if save:
    savePath = dirPath + '/' + str(energy) + '/UndulatorSpectrum_B'+ str(Bfield[0]) + 'Intensity.eps'
else:
    savePath = None

names = ['WBS = ' + str(x) + r'$\times$' + str(y) + ' mm$^2$' for x,y in zip(wbsX,wbsY)]
#['WBS=' + str(x) + 'x' + str(y) + 'mm$^2$, ' + d + ' detuning' for x,y,d in zip(wbsX,wbsY,detuning)]

files = ['/res_spec_me_14.3m_' + str(x) + 'x' + str(y) + 'WBS_B' + str(b) + '.dat' for x,y,b in zip(wbsX,wbsY,Bfield)]
#['/res_spec_me_14.3m_0.84x1WBS_B0.3448.dat','/res_spec_me_14.3m_4x3WBS_B0.3448.dat']
#['/res_spec_me_PUS_14.3m_0.84x1WBS_B0.3448.dat','/res_spec_me_PUS_14.3m_4x3WBS_B0.3448.dat']
#['/res_spec_se_14.3m_B0.3448.dat','/res_spec_me_PUS_14.3m_0.84x1WBS_B0.3448.dat','/res_spec_me_PUS_14.3m_4x3WBS_B0.3448.dat']

# 185 eV
#['/res_spec_se_14.3m_B0.4605.dat','/res_spec_me_PUS_14.3m_0.84x1WBS_B0.4605.dat','/res_spec_me_PUS_14.3m_4x3WBS_B0.4605.dat']
#['/res_spec_me_14.3m_0.84x1WBS_B0.4605.dat','/res_spec_me_14.3m_4x3WBS_B0.4605.dat']
#['/res_spec_me_PUS_14.3m_0.84x1WBS_B0.4605.dat','/res_spec_me_PUS_14.3m_4x3WBS_B0.4605.dat']
# 92 eV
#['/res_spec_me_PUS_14.3m_0.84x1WBS_B0.6839.dat','/res_spec_me_PUS_14.3m_4x3WBS_B0.6839.dat']
#['/res_spec_me_14.3m_0.84x1WBS_B0.6839.dat','/res_spec_me_14.3m_4x3WBS_B0.6839.dat']
#['/res_spec_se_14.3m_B0.6839.dat','/res_spec_me_PUS_14.3m_0.84x1WBS_B0.6839.dat','/res_spec_me_PUS_14.3m_4x3WBS_B0.6839.dat']


E = [energy]*len(files)
print(E)

print(names)


Isums, Hmax = plotSpectrumME(
    [dirPath + str(energy) + f for f in files], E=E, n=len(files), names=names, colours=C, linestyles=L, Elim = Elimit, fsize=fSize,savePath=savePath
)


print([i*1e-9 for i in Isums])
print([h*1e-9 for h in Hmax])



# large WBS
## intensity HC
#HC0 = [2.7579046543999843, 0.24211744539999683, 1.443013762399972, 0.3233712223999934, 1.0338984299999872]
#HC1 = [4.25488735519999, 0.7599316359999949, 2.129378140000009, 1.4428164991999926, 1.0094900580000035]
#HC2 = [4.8734584864, 1.387417580799996, 1.462379674400005, 1.9729589599999988, 0.9156544939999985]
## flux HC
#HC0 = [33.09484968959981, 2.9054105215999617, 17.31616372479966, 3.8804543999999206, 12.406777759999848]
#HC1 = [51.05865105919989, 9.119179750399939, 25.552535193600107, 17.31379704319991, 12.113878720000042]
#HC2 = [58.4814975232, 16.649011443199953, 17.548556019200063, 23.675508019199988, 10.987852895999982]
#
#small WBS
## flux HC
#HC0 = [9.601841164799971, 0.7840858679999888, 8.161153967999855, 1.4029113599999627, 6.052673599999913]
#HC1 = [10.373134633600019, 1.8594073871999968, 5.245392112000129, 4.258431232000011, 1.4920700600000345]
#HC2 = [5.736751427200041, 1.420325798400006, 0.5656065854000139, 1.8547698432000148, 0.49165643499999884]
#M = [0,-0.738,-1.63]
#plt.plot(M,[h[0]/np.sum(h[1:4]) for h in [HC0,HC1,HC2]])
#plt.show()