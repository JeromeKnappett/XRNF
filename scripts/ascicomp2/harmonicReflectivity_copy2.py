#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 11:02:28 2023

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
import xraydb

print(' HERE:    ', xraydb.xray_delta_beta('H2Si2O3', 1.4, 6000))

def plotSpectrumME(datfile):
    T = np.loadtxt(datfile, dtype=str, comments=None, skiprows=10, usecols=(0))
    iE = str(np.loadtxt(datfile, dtype=str, comments=None, skiprows=1, usecols=(0), max_rows=1))[1:]
    fE = str(np.loadtxt(datfile, dtype=str, comments=None, skiprows=2, usecols=(0), max_rows=1))[1:]
    N = str(np.loadtxt(datfile, dtype=str, comments=None, skiprows=3, usecols=(0), max_rows=1))[1:]
    iX = str(np.loadtxt(datfile, dtype=str, comments=None, skiprows=4, usecols=(0), max_rows=1))[1:]
    fX = str(np.loadtxt(datfile, dtype=str, comments=None, skiprows=5, usecols=(0), max_rows=1))[1:]
    apSize = float(fX)-float(iX) #[f-i for f,i in zip(fX,iX)]
    dE = (float(fE)-float(iE))/float(N) #[(f-i)/n for f,i,n in zip(fE,iE,N)]
    print("Aperture Size [m]:      ", apSize)
    print("Energy Resolution [eV]: ", dE)
    
    #Converting to float for plotting
    newT = [float(t) for t in T]
    
    #finding FWHM
    h1 = np.array(newT[0:len(newT)//3])
    HM = np.argmax(h1)#np.max(h1)/2
    fwhm = len(h1[h1>h1.max()/2])
    
    print(h1.max())
    
    plt.plot(newT, label='Multi Electron')
    plt.axvline(x=HM-fwhm/2, linestyle = ':', color='black', label='FWHM')
    plt.axvline(x=HM+fwhm/2, linestyle = ':', color='black')
    plt.xticks([len(newT)*a for a in [0,1/5,2/5,3/5,4/5,1]],[dE*len(newT)*a for a in [0,1/5,2/5,3/5,4/5,1]])
    plt.ylabel('Flux [ph/s/.1%bw]')
    plt.text(2000,h1.max()/2,'FWHM: {} eV'.format(fwhm*dE), color='black')
    plt.legend(loc='upper right')
    plt.xlabel('Photon Energy [eV]')
    # fig.tight_layout()
    plt.show()
    
    
datfile = '/user/home/opt/xl/xl/experiments/EUVThirdOrderAI/res_spec_me.dat'

plotSpectrumME(datfile)

E = [90.44,135,184.76]#,250]#,500] #184.76 # 130 #184.76 #90.44

harmonicWeights = [7.75,1.25,8,3,6.25]

# # # values for cff = 3
# G = [1.6755,1.3718,1.1728]#,0.7104]
# M = [3.35395,2.74524,2.34666]#,1.4265]
# # values for cff = 2
# G = [1.9151]#[2.7358,2.2400,1.9151,1.6466]#,0.7104]
# M = [2.87375]#[4.10686,3.36174,2.87375,2.47058]#,1.4265]
# #values for cff = 1.3
# G = [7.41969,5.19258,4.46423]#,0.7104]
# M = [6.56030,4.59231,3.94842]#,1.4265]
#values for cff = 1.4
G = [4.8343,3.9587,3.3848,2.9104]
#[6.77580,5.54650,4.74139,4.07622]#,0.7104]
M = [5.80506,4.75262,4.06310,3.49330]#,1.4265]

n = [1,2,3,4,5,6,7,8,9] # np.linspace(1,20,4000) # [1,2,3,4,5,6,7,8,9] # np.linspace(1,10,2000) #[1,2,3,4,5]
ef = [0.1,0.00001,0.01,0.00001,0.001,0.00001,0.0001,0.00001,0.00001] # np.ones(len(n)) #[0.1,0.00001,0.01,0.00001,0.001]

IFE = []
EH = []
for _E,g,m in zip(E,G,M):
    
    Eh = np.array([_E*_n for _n in n]) #np.array([184.76,2*184.76,3*184.76,4*184.76,5*184.76])
    EH.append(Eh)
    
    # print(np.shape(Eh))
    hp = True
    
    m1 = 1.3
    m2 = m #2
    m3 = 1.5
    # g = 1.6754999990165185 # 1.173 for 184.76 eV
    
    r1 = xraydb.mirror_reflectivity('Au', np.deg2rad(m1), Eh, polarization='p')
    r2 = xraydb.mirror_reflectivity('Au', np.deg2rad(m2), Eh, polarization='s')
    r3 = xraydb.mirror_reflectivity('Au', np.deg2rad(m3), Eh, polarization='p')
    rgAu = xraydb.mirror_reflectivity('Au', np.deg2rad(g), Eh, polarization='s')
    rgSi = xraydb.mirror_reflectivity('Si', np.deg2rad(g), Eh, polarization='s')
    
    print('R1:', r1)
    print('R2:', r2)
    print('R3:', r3)
    print('RGau:', rgAu)
    print('RGsi:', rgSi)
    IF = []
    for i,e in enumerate(Eh):
        # print(e)
        # print(i)
        # print(n[i])
        I_f = r1[i]*r2[i]*r3[i]*(0.001*rgAu[i])  # without Si reflectivity term
        # I_f = r1[i]*r2[i]*r3[i]*(0.5*abs(rgAu[i] - rgSi[i]))  # without grating efficiency term
        # I_f = r1[i]*r2[i]*r3[i]*(0.5*(0.1**(i+1))*abs(rgAu[i] - rgSi[i]))  # without grating efficiency term
        # I_f = r1[i]*r2[i]*r3[i]*(0.5*ef[i]*(rgAu[i] + rgSi[i]))  # adding reflectivity of Au and Si
        # I_f = r1[i]*r2[i]*r3[i]*(0.5*ef[i]*abs(rgAu[i] - rgSi[i]))# subtracting reflectivity of Au and Si
        # print(" ")
        # print(rgAu[i])
        # print(rgSi[i])
        # print(rgAu[i] - rgSi[i])
        IF.append(I_f)
    
    
    plt.plot(Eh/_E,r1,'.:',label='M1')
    plt.plot(Eh/_E,r2,'.:',label='M2')
    plt.plot(Eh/_E,r3,'.:',label='M3')
    plt.plot(Eh/_E,rgAu,'.:',label='$G_{Au}$')
    plt.plot(Eh/_E,rgSi,'.:',label='$G_{Si}$')
    # plt.yscale('log')
    plt.title(f"E = {_E} eV")
    plt.ylabel('Reflectivity')
    plt.xlabel('Harmonic Number')
    # plt.xlabel("Energy [eV]")
    plt.legend()
    plt.show()
    
    IFE.append(IF)


c = ['blue','orange','green']

for i,e in enumerate(E):
    plt.plot(EH[i]/e,[efe*100 for efe in IFE[i]],'.:',label=f'E = {e} [eV]')
    print(" ")
    print([efe*100 for efe in IFE[i]])
    # plt.vlines(e*1, 0, IFE[i][i==0],color=c[i])
    # plt.vlines(e*2, 0, IFE[i][i==0],color=c[i])
    # plt.vlines(e*3, 0, IFE[i][i==0],color=c[i])
# plt.title(f"E = {E} eV")
plt.ylabel("Beamline Efficiency [%]")
plt.xlabel("Harmonic Number")
# plt.xlabel("Energy [eV]")
plt.legend()
# plt.ylim([np.min(IF),np.max(IF)])
plt.yscale('log')
plt.show()


print('\n n=1', [i[0] for i in IFE])
print('\n n=3', [i[2] for i in IFE])

# for i,e in enumerate(E):
#     # print(e)
#     # print(IFE[i])
#     Eint = int(e / (((e*20) - e) / 4000))
#     E1 = IFE[i][0:Eint]
#     E2 = IFE[i][Eint:2*Eint]
#     E3 = IFE[i][2*Eint:3*Eint]
#     E4 = IFE[i][3*Eint:4*Eint]
#     E5 = IFE[i][4*Eint:5*Eint]
#     EI = [(e2 + e3 + e4 + e5) / e1 for e2,e3,e4,e5,e1 in zip(E2,E3,E4,E5,E1)]
#     # print(EI)
#     # EI = (IFE[i][E==e*2] + IFE[i][E==e*3]) / IFE[i][E==e]
#     plt.plot(EH[i][0:Eint],EI,'-',label=f'E = {e} [eV]')
#     # plt.plot(EH[i]/e,EI,'-',label=f'E = {e} [eV]')
#     # plt.vlines(e*1, 0, IFE[i][i==0],color=c[i])
#     # plt.vlines(e*2, 0, IFE[i][i==0],color=c[i])
#     # plt.vlines(e*3, 0, IFE[i][i==0],color=c[i])
# plt.title(f"E = {E} eV")
# plt.ylabel("Efficiency")
# # plt.xlabel("Harmonic Number")
# plt.xlabel("Energy [eV]")
# plt.legend()
# # plt.ylim([np.min(IF),np.max(IF)])
# # plt.xlim(0,3000)
# # plt.yscale('log')
# plt.show()

# print(IF)

start = 70
stop = 250
num = 990
X = np.linspace(start,stop,num)

# plt.plot(X,xraydb.mirror_reflectivity('Au', np.deg2rad(1.0), X),label='Au: 1 deg')
# plt.plot(X,xraydb.mirror_reflectivity('Si', np.deg2rad(1.0), X),label='Si: 1 deg')
# plt.plot(X,xraydb.mirror_reflectivity('Au', np.deg2rad(4.0), X),'--',label='Au: 4 deg')
# plt.plot(X,xraydb.mirror_reflectivity('Si', np.deg2rad(4.0), X),'--',label='Si: 4 deg')
# plt.plot(X,xraydb.mirror_reflectivity('Au', np.deg2rad(7.0), X),':',label='Au: 7 deg')
# plt.plot(X,xraydb.mirror_reflectivity('Si', np.deg2rad(7.0), X),':',label='Si: 7 deg')
plt.plot(X,xraydb.mirror_reflectivity('Au', np.deg2rad(4.74139), X),':',label='Au: cff: 1.4')
plt.plot(X,xraydb.mirror_reflectivity('Si', np.deg2rad(4.74139), X),':',label='Si: cff: 1.4')
plt.ylabel("Reflectivity")
# plt.xlabel("Harmonic Number")
plt.xlabel("Energy [eV]")
plt.legend(loc='upper right')
plt.show()

plt.plot(X,xraydb.mirror_reflectivity('Au', np.deg2rad(1.0), X) - xraydb.mirror_reflectivity('Si', np.deg2rad(1.0), X),label='Au - Si: 1 deg')
plt.plot(X,xraydb.mirror_reflectivity('Au', np.deg2rad(4.0), X) - xraydb.mirror_reflectivity('Si', np.deg2rad(4.0), X),label='Au - Si: 4 deg')
plt.plot(X,xraydb.mirror_reflectivity('Au', np.deg2rad(7.0), X) - xraydb.mirror_reflectivity('Si', np.deg2rad(7.0), X),label='Au - Si: 7 deg')
# plt.plot(X,xraydb.mirror_reflectivity('Si', np.deg2rad(1.0), X),label='Si: 1 deg')
# plt.plot(X,xraydb.mirror_reflectivity('Si', np.deg2rad(4.0), X),label='Si: 4 deg')
# plt.plot(X,xraydb.mirror_reflectivity('Si', np.deg2rad(7.0), X),label='Si: 7 deg')
plt.ylabel("Reflectivity")
# plt.xlabel("Harmonic Number")
plt.xlabel("Energy [eV]")
plt.legend(loc='upper right')
plt.show()