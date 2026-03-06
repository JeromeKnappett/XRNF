#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 14:35:52 2024

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
import tifffile
import pickle
from focusedFZP import focusedFZP
import pylab
#plt.style.use(['science','no-latex']) # 'ieee', 
pylab.rcParams['figure.figsize'] = (5.0, 5.0)

def loadImage(path2image):
    I = tifffile.imread(path2image)
    return I


def test():
    path90 = '/user/home/opt/xl/xl/experiments/diamondFZP_EUV/data/'
    path185 = '/user/home/opt/xl/xl/experiments/diamondFZP/data/'
    
    names = ['FZPincident_ssa50bda500','FZPincident_ssa100bda300','FZPincident_ssa350bda100']
    SSAsize = [50,100,350]
    FZPsize = [500,300,100] 
    
    f90 = []
    f185 = []
    ff90,ff185 = [],[]
    if90,if185 = [],[]
    d90,d185 = [],[]
    s90,s185 = [],[]
    fmin90,fmax90 = [],[]
    smin90,smax90 = [],[]
    smin185,smax185 = [],[]
    for i,n in enumerate(names):
        pick90 = pickle.load(open(path90 + n + '/' + n + '.pkl','rb'))
        res90 = (pick90[1],pick90[2])
        tiff90 = pick90[0]
        
        pick185 = pickle.load(open(path185 + n + '/' + n + '.pkl','rb'))
        res185 = (pick185[1],pick185[2])
        tiff185 = pick185[0]
        
        
        
        # Ga = bda[e]*1.0e-6 #50.0e-6
        

        # eff = 0.1  # grating E = 10%
        # #0.027501275406876923
        # #0.03935212451203237 # cff = 3, grating E = 10%
        # #0.04451154279639219 # cff = 2, grating E = 10% - fixed angle
        # #0.03267384491294766 # cff = 1.4, grating E = 10%
                
        # # 0.03737340348858282, 0.02216367235357039, 0.004297207161730262, 0.0005147820098211518
        
        # print('\n')
        # print(bw)
        # I = I * bw/0.1 * eff
        
        # # converting from ph/s/mm^2 to ph/s
        # I = (I / 1.0e-6) * (dx*dy)
        
        # from FWarbValue import getFWatValue
        # fwhmx,fwhmy = getFWatValue(I,frac=0.5,dx=dx,dy=dy,cuts='xy',
        #                             centered=True,smoothing='gauss',
        #                             verbose=False,show=True)

    
        # G, C, S = IoverGrating(I, GA=Ga, dx=dy, dy=dy, show=True)
        # _G, _C, _S = IoverGrating(I, GA=1.0e-3, dx=dy, dy=dy, show=True)
        
        # q = 1.60218e-19
        
        
        
        
        # convering from ph/s/0.1%bw/mm^2 to ph/s/mm^2
        grad = 0.000396378#*0.628324754030457
        intercept = 0.019051304
        slv = SSAsize[i] #(2/1.4)*SSAsize[i]
        bw = (slv*grad) + intercept
        bw = bw/0.1
        
        # [ph/s/mm^2]
        tiff90 = tiff90 * bw
        tiff185 = tiff185 * bw
        
        # converting from ph/s/mm^2 to ph/s
        tiff90 = (tiff90 / 1.e-6) * (res90[0]*res90[1]) * 0.1 # 0.1 is to account for 10% efficiency of the monochromator
        tiff185 = (tiff185 / 1.e-6) * (res185[0]*res185[1]) * 0.1
        
        # total flux in each image [ph/s]
        F90 = np.sum(tiff90)
        F185 = np.sum(tiff185)
        if i == 0:
            F90 = 1746589313.824963 * bw
            F185 = 225434418.56226215 * bw
        elif i == 1:
            F90 = 11867330105.995707 * bw
            F185 = 1576455222.111428  * bw
        elif i == 2:
            F90 = 17692979925.653637 * bw
            F185 = 1817204381.862511 * bw
        else:
            print('here.......')
            F90 = np.sum(tiff90)
            F185 = np.sum(tiff185)
            
        F90 = 0.1*F90
        
        f90.append(F90)
        f185.append(F185)
        
        f_size = 10.0e-9 # size of focused beam
        nmin = 0.01
        nmax = 0.1
        n = 0.05          # efficienty of FZP
        Dr = 50.0        # required dose-on-mask
        
        Dmin_90, Dmax_90 = 7.49, 73.8
        Dmin_185, Dmax_185 = 33.2, 73.8
        
        for _n in [nmin,n,nmax]:
            Fmin90,Imin90,Dmin90,Smin90 = focusedFZP(f_size, F90, _n, 90, Dmin_90)
            Fmax90,Imax90,Dmax90,Smax90 = focusedFZP(f_size, F90, _n, 90, Dmax_90)
            Fmin185,Imin185,Dmin185,Smin185 = focusedFZP(f_size, F185, _n, 185, Dmin_185)
            Fmax185,Imax185,Dmax185,Smax185 = focusedFZP(f_size, F185, _n, 185, Dmax_185)       
            Ff90,If90,D90,S90 = focusedFZP(f_size, F90, _n, 90, Dr)
            Ff185,If185,D185,S185 = focusedFZP(f_size, F185, _n, 185, Dr)     
            smin90.append(Smin90)
            smax90.append(Smax90)
            smin185.append(Smin185)
            smax185.append(Smax185)
            s90.append(S90)
            s185.append(S185)
            
        
        # Fmin90,Imin90,Dmin90,Smin90 = focusedFZP(f_size, F90, n, 90, Dmin_90)
        # Fmax90,Imax90,Dmax90,Smax90 = focusedFZP(f_size, F90, n, 90, Dmax_90)
        # Fmin185,Imin185,Dmin185,Smin185 = focusedFZP(f_size, F185, n, 185, Dmin_185)
        # Fmax185,Imax185,Dmax185,Smax185 = focusedFZP(f_size, F185, n, 185, Dmax_185)
        
        # Ff90,If90,D90,S90 = focusedFZP(f_size, F90, n, 90, Dr)
        # Ff185,If185,D185,S185 = focusedFZP(f_size, F185, n, 185, Dr)
        
        ff90.append(Ff90)
        ff185.append(Ff185)
        if90.append(If90)
        if185.append(If185)
        d90.append(D90)
        d185.append(D185)
        # s90.append(S90)
        # s185.append(S185)
        
        # fmin90.append(Fmin90)
        # fmax90.append(Fmax90)
        # smin90.append(Smin90)
        # smax90.append(Smax90)
        # smin185.append(Smin185)
        # smax185.append(Smax185)
        
        
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()
    
    print(fmin90)
    # plotting incident flux
    ax1.plot(FZPsize,[f*1.e-9 for f in f90],linewidth=1, marker="o", linestyle='dashed',
          markerfacecolor='none',label='90 eV')
    ax1.plot(FZPsize,[f*1.e-9 for f in f185],linewidth=1, marker="o", linestyle='dashed',
          markerfacecolor='none',label='185 eV')
    ax1.set_xlabel('FZP size [um]')
    ax1.set_ylabel('Incident coherent flux [ph/s] x$10^{9}$')
    ax1.legend()
    ax2.plot(SSAsize,[f*1e-9 for f in f90],'',alpha=0.0)
    ax2.plot(SSAsize,[f*1e-9 for f in f185],'',alpha=0.0)
    # ax1.fill_between(FZPsize,[f*1e-9 for f in fmin90], [f*1e-9 for f in fmax90], alpha = 0.25, edgecolor = '#CC4F1B', facecolor='#FF9848')
    ax2.invert_xaxis()
    ax2.set_xlabel('SSA size [um]')
    # plt.grid()
    ax1.grid()
    plt.tight_layout()
    plt.show()
    
    print(f90)
    print(f185)
    print('Here')
    print(s90)
    print(s185)
    
    
    # fig = plt.figure()
    # ax1 = fig.add_subplot(111)
    # ax2 = ax1.twiny()
    
    # # plotting focused flux
    # ax1.plot(FZPsize,ff90,linewidth=0, marker="o",
    #      markerfacecolor='none',label='90 eV')
    # ax1.plot(FZPsize,ff185,linewidth=0, marker="o",
    #      markerfacecolor='none',label='185 eV')
    # ax1.set_xlabel('FZP size [um]')
    # ax1.set_ylabel('Focused Flux [ph/s]')# x$10^{10}$')
    # ax1.legend()
    # ax2.plot(SSAsize,[f*1e-10 for f in f90],'',alpha=0.0)
    # ax2.plot(SSAsize,[f*1e-10 for f in f185],'',alpha=0.0)
    # ax2.invert_xaxis()
    # ax2.set_xlabel('SSA size [um]')
    # # plt.grid()
    # ax1.grid()
    # plt.tight_layout()
    # plt.show()
    
    print('here')
    print(s90[2::3])
    
    
    
    # plotting write speed (n=0.01)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()
    
    ax1.plot(FZPsize,[s for s in smin90[0::3]],linewidth=1, marker="o", color='C0', linestyle='dashed',
          label='90 eV')# ($D = $' + str(Dr) + ' mJ/s/cm$^2$)')
    ax1.plot(FZPsize,[s for s in smax90[0::3]],linewidth=1, marker="o", color='C0', linestyle='dashed',
          markerfacecolor='none')# ($D = $' + str(Dr) + ' mJ/s/cm$^2$)')
    ax1.plot(FZPsize,[s for s in smin185[0::3]],linewidth=1, marker="o", color='#FF9848', linestyle='dashed',
          label='185 eV')# ($D = $' + str(Dr) + ' mJ/s/cm$^2$)')
    ax1.plot(FZPsize,[s for s in smax185[0::3]],linewidth=1, marker="o", color='#FF9848', linestyle='dashed',
          markerfacecolor='none')# ($D = $' + str(Dr) + ' mJ/s/cm$^2$)')
    ax1.set_xlabel('FZP size [um]')
    ax1.set_ylabel('Write Speed [mm/s]')
    ax1.legend()
    ax2.plot(SSAsize,[s for s in s90[0::3]],'',alpha=0.0)
    ax2.plot(SSAsize,[s for s in s185[0::3]],'',alpha=0.0)
    
    ax1.fill_between(FZPsize, [s for s in smax90[0::3]], [s for s in smin90[0::3]], alpha = 0.25, color = 'C0',label='90 eV')#, facecolor= #CC4F1B', facecolor='#FF9848')
    ax1.fill_between(FZPsize, [s for s in smax185[0::3]], [s for s in smin185[0::3]], alpha = 0.25, edgecolor= '#CC4F1B', facecolor='#FF9848',label='185 eV')
    ax2.invert_xaxis()
    ax2.set_xlabel('SSA size [um]')
    # plt.grid()
    ax1.grid()
    ax1.set_title('1% efficiency')
    plt.tight_layout()
    plt.show()
    
    
    # plotting write speed (n=0.1)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()
    # ax3 = ax1.twinx()
    
    ax1.plot(FZPsize,[s for s in smin90[2::3]],linewidth=1, marker="o", color='C0', linestyle=':',
          label='90 eV')# ($D = $' + str(Dr) + ' mJ/s/cm$^2$)')
    ax1.plot(FZPsize,[s for s in smax90[2::3]],linewidth=1, marker="o", color='C0', linestyle=':',
          markerfacecolor='none')# ($D = $' + str(Dr) + ' mJ/s/cm$^2$)')
    ax1.plot(FZPsize,[s for s in smin185[2::3]],linewidth=1, marker="o", color='#FF9848', linestyle=':',
          label='185 eV')# ($D = $' + str(Dr) + ' mJ/s/cm$^2$)')
    ax1.plot(FZPsize,[s for s in smax185[2::3]],linewidth=1, marker="o", color='#FF9848', linestyle=':',
          markerfacecolor='none')# ($D = $' + str(Dr) + ' mJ/s/cm$^2$)')
    ax1.set_xlabel('FZP size [um]')
    ax1.set_ylabel('Write Speed [mm/s]')
    ax1.legend()
    ax2.plot(SSAsize,[s for s in s90[2::3]],'',alpha=0.0)
    ax2.plot(SSAsize,[s for s in s185[2::3]],'',alpha=0.0)
    
    # ax3.plot(FZPsize,[f*1.e-9 for f in f90],linewidth=1, marker="x", linestyle='--', color='C0',
    #       markerfacecolor='none',label='90 eV')
    # ax3.plot(FZPsize,[f*1.e-9 for f in f185],linewidth=1, marker="x", linestyle='--', color='#FF9848',
    #       markerfacecolor='none',label='185 eV')
    # ax3.set_ylabel('Incident coherent flux [ph/s] x$10^{9}$')
    ax1.fill_between(FZPsize, [s for s in smax90[2::3]], [s for s in smin90[2::3]], alpha = 0.25, color = 'C0')#, facecolor= #CC4F1B', facecolor='#FF9848')
    ax1.fill_between(FZPsize, [s for s in smax185[2::3]], [s for s in smin185[2::3]], alpha = 0.25, edgecolor= '#CC4F1B', facecolor='#FF9848')
    ax2.invert_xaxis()
    ax2.set_xlabel('SSA size [um]')
    # plt.grid()
    ax1.grid()
    ax1.set_title('10% efficiency')
    plt.tight_layout()
    plt.show()
    
    
    # fig = plt.figure()
    # ax1 = fig.add_subplot(111)
    # ax2 = ax1.twiny()
    
    # # plotting write speed flux
    # ax1.plot(FZPsize,[s for s in s90[2::3]],linewidth=0, marker="o",
    #       markerfacecolor='none',label='90 eV (min)')
    # ax1.plot(FZPsize,[s for s in s185[2::3]],linewidth=0, marker="o",
    #       markerfacecolor='none',label='185 eV')
    # ax1.set_xlabel('FZP size [um]')
    # ax1.set_ylabel('Write Speed [mm/s]')
    # ax1.legend()
    # # ax2.plot(SSAsize,[f*1e-10 for f in f90],'',alpha=0.0)
    # # ax2.plot(SSAsize,[f*1e-10 for f in f185],'',alpha=0.0)
    
    # ax1.fill_between(FZPsize, [s for s in smax90[0::3]], [s for s in smin90[2::3]], alpha = 0.25, color = 'C0')#, facecolor= #CC4F1B', facecolor='#FF9848')
    # ax1.fill_between(FZPsize, [s for s in smax185[0::3]], [s for s in smin185[2::3]], alpha = 0.25, edgecolor= '#CC4F1B', facecolor='#FF9848')
    # ax2.invert_xaxis()
    # ax2.set_xlabel('SSA size [um]')
    # # plt.grid()
    # ax1.grid()
    # plt.tight_layout()
    # plt.show()
    
    
    


    
    
if __name__ == '__main__':
    test()