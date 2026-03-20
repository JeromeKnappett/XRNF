#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 17:20:48 2021

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
import imageio

def round_sig(x, sig=2):
    from math import floor, log10
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x
colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]

dirPath = '/home/jerome/dev/data/sourceNdBeam/' #'/home/jerome/dev/experiments/beamPolarisation13/data/' #'/home/jerome/dev/data/sourceNdBeam/'

files =  ['res_trjHOR.dat','res_trjVER.dat','res_trj45.dat','res_trjCIR.dat'] #
labels = ['Single Electron', 'Multi-Electron']
# common files for copying and pasting
# ['res_spec_se.dat','res_spec_me(2).dat'] ['res_spec_se.dat','res_spec_me.dat'] # ['res_trjHOR.dat','res_trjVER.dat','res_trj45.dat','res_trjCIR.dat'] #['res_brillianceVerDiv.dat','res_brillianceHorDiv.dat'] #['res_trjHOR.dat','res_trjVER.dat','res_trj45.dat','res_trjCIR.dat']

plotType ='eTraj' #'meSpectrum' #'eTraj' # 'divergence' #'eTraj'

save = True
savePath = '/home/jerome/Documents/MASTERS/Figures/plots/'

meSpec = []
seSpec = []
aperture = []
energyRes = []
harMax = []
FWHM = []

fig, axs = plt.subplots(2,1)
for i, f in enumerate(files):
    print("Number : ", i)
    if plotType == 'meSpectrum':
        T = np.loadtxt(dirPath+f, dtype=str, comments=None, skiprows=10, usecols=(0))
        iE = str(np.loadtxt(dirPath+f, dtype=str, comments=None, skiprows=1, usecols=(0), max_rows=1))[1:]
        fE = str(np.loadtxt(dirPath+f, dtype=str, comments=None, skiprows=2, usecols=(0), max_rows=1))[1:]
        N = str(np.loadtxt(dirPath+f, dtype=str, comments=None, skiprows=3, usecols=(0), max_rows=1))[1:]
        iX = str(np.loadtxt(dirPath+f, dtype=str, comments=None, skiprows=4, usecols=(0), max_rows=1))[1:]
        fX = str(np.loadtxt(dirPath+f, dtype=str, comments=None, skiprows=5, usecols=(0), max_rows=1))[1:]
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
        print('FWHM: ',fwhm)
        print("Pixels: ", len(newT))
        
        # plt.plot(h1)
        # plt.show()
        
        
        # axs[i].plot(newT, label=labels[1])
        # axs[i].axvline(x=HM-fwhm/2, linestyle = ':', color=colours[1], label='FWHM')
        # axs[i].axvline(x=HM+fwhm/2, linestyle = ':', color=colours[1])
        # axs[i].set_xticks([len(newT)*a for a in [0,1/5,2/5,3/5,4/5,1]])
        # axs[i].set_xticklabels([dE*len(newT)*a for a in [0,1/5,2/5,3/5,4/5,1]])
        # axs[i].set_ylabel('Intensity [ph/s/.1%bw/mm²]')#, loc='bottom')
        # # axs[i].yaxis.set_label_coords(-0.05,-0.15)
        # axs[i].text(20000,h1.max()/2,'FWHM: {} eV'.format(fwhm*dE), color=colours[1])
        # axs[i].legend()
        # axs[i].set_xticks([len(newT)*a for a in [0,1/5,2/5,3/5,4/5,1]])
        # axs[i].set_xticklabels([dE*len(newT)*a for a in [0,1/5,2/5,3/5,4/5,1]])
        # axs[i].set_xlabel('Photon Energy [eV]')
        # axs[i].set_xlim(0,len(newT))
        
        if i==0:
            axs[0].plot(newT, label='Single Electron')
            axs[0].axvline(x=HM-fwhm/2, linestyle = ':', color=colours[1], label='FWHM')
            axs[0].axvline(x=HM+fwhm/2, linestyle = ':', color=colours[1])
            axs[0].set_xticks([len(newT)*a for a in [0,1/5,2/5,3/5,4/5,1]])
            axs[0].set_xticklabels([dE*len(newT)*a for a in [0,1/5,2/5,3/5,4/5,1]])
            axs[0].set_ylabel('Intensity [ph/s/.1%bw/mm²]')#, loc='bottom')
            axs[0].yaxis.set_label_coords(-0.05,-0.15)
            axs[0].text(20000,h1.max()/2,'FWHM: {} eV'.format(fwhm*dE), color=colours[1])
            axs[0].legend()
        elif i==1:
            axs[1].plot(newT, label='Multi Electron')
            axs[1].axvline(x=HM-fwhm/2, linestyle = ':', color=colours[1], label='FWHM')
            axs[1].axvline(x=HM+fwhm/2, linestyle = ':', color=colours[1])
            axs[1].set_xticks([len(newT)*a for a in [0,1/5,2/5,3/5,4/5,1]])
            axs[1].set_xticklabels([dE*len(newT)*a for a in [0,1/5,2/5,3/5,4/5,1]])
            # axs[1].set_ylabel('Flux [ph/s/.1%bw]')
            axs[1].text(2000,h1.max()/2,'FWHM: {} eV'.format(fwhm*dE), color=colours[1])
            axs[1].legend(loc='upper left')
            axs[1].set_xlabel('Photon Energy [eV]')
            
        # plt.plot(newT)
        # plt.axvline(x=HM-fwhm/2, linestyle = ':', color=colours[1], label='FWHM')
        # plt.axvline(x=HM+fwhm/2, linestyle = ':', color=colours[1], label='FWHM')
        # plt.xticks(ticks=[len(newT)*a for a in [0,1/5,2/5,3/5,4/5,1]],
        #             labels=[dE*len(newT)*a for a in [0,1/5,2/5,3/5,4/5,1]])
        # plt.xlabel('Photon Energy [eV]')
        # if i == 0:
        #     meSpec.append(newT)
        #     plt.ylabel('Flux [ph/s/.1%bw]')
        #     plt.text(20000,h1.max()/2,'FWHM: {} eV'.format(fwhm*dE), color=colours[1])
        # elif i == 1:
        #     seSpec.append(newT)
        #     plt.ylabel('Intensity [ph/s/.1%bw/mm²]')
        #     plt.text(20000,h1.max(),'FWHM: {} eV'.format(fwhm*dE), color=colours[1])
        #     #200 + i*3, np.max(Zmin), str(round_sig(np.max(Zmax)-np.max(Zmin)))+' mm', {'color': colours[i], 'fontsize': 6})
        # if save:
        #     plt.savefig(savePath + 'spectrum_{}.pdf'.format(str(f[7:len(str(f))-4])))
        #     plt.savefig(savePath + 'spectrum_{}.png'.format(str(f[7:len(str(f))-4])), dpi=2000)
        # plt.show()
        
        # aperture.append(apSize)
        # energyRes.append(dE)
        # FWHM.append(fwhm)
        # harMax.append(HM)

    if plotType == 'eTraj':
        T = np.loadtxt(dirPath+f, dtype=str, comments=None, skiprows=1)#, max_rows=1, usecols=(0)))
        tX = np.array(T[:,1],dtype='float')
        tY = np.array(T[:,3],dtype='float')
        tZ = np.array(T[:,5],dtype='float')
        bX = np.array(T[:,7],dtype='float')
        bY = np.array(T[:,8],dtype='float')
        bZ = np.array(T[:,9],dtype='float')
        
        #2D plot
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.plot(tZ,1e6*tX, label='x-position', color=colours[0])
        ax1.plot(tZ,1e6*tY, label='y-position', color=colours[1])
        ax2.plot(tZ,bX, ':', label='$B_x$', color=colours[2])
        ax2.plot(tZ,bX, ':', label='$B_y$', color=colours[3])
        ax1.set_xlabel('z-position [m]')
        ax1.set_ylabel('[\u03bcm]')
        ax2.set_ylabel('[T]')
        ax1.legend()
        ax2.legend()
        fig.tight_layout()
        plt.show()
        
        #3D plot
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.view_init(20, -45)#(elev=None, azim=None)
        ax.plot(1e6*tX,tZ,1e6*tY, label='Electron Trajectory [\u03bcm]', color=colours[1])
        # ax.plot(10*bX,1e6*bZ,10*bY, ':', label='magnetic field')
        ax.plot(1e1*bX,tZ,1e1*bY, ':', label=r'$B \times 10^1$ [T]', color=colours[3])
        ax.set_xlabel('x', linespacing=0.1)#'-position [\u03bcm]')
        ax.set_ylabel('z [m]')#'-position [m]')
        ax.set_zlabel('y')#'-position [\u03bcm]')
        ax.legend()
        # ax.set_xticks([-4, 0, 4])#, minor=False)
        # ax.set_zticks([-4,0,4])
        # ax.set_yticks([-1,0,1])
        ax.grid(which='major')
        fig.tight_layout()
        if save:
            plt.savefig(savePath + 'magField_{}.pdf'.format(str(f[7:len(str(f))-4])))
            plt.savefig(savePath + 'magField_{}.png'.format(str(f[7:len(str(f))-4])), dpi=2000)
        plt.show()
    if plotType == 'divergence':
        D = np.loadtxt(dirPath+f, dtype=str, comments=None, skiprows=1)
        f1 = np.array(D[:,0],dtype='float')
        f3 = np.array(D[:,2],dtype='float')
        f5 = np.array(D[:,4],dtype='float')
        e1 = np.array(D[:,1],dtype='float')
        e3 = np.array(D[:,3],dtype='float')
        e5 = np.array(D[:,5],dtype='float')
        
        plt.plot(e1,f1, label='1')
        plt.plot(e3,f3, label='3')
        plt.plot(e5,f5, label='5')
        plt.show()
    
    if plotType == 'seIntensity':
        sePR = 'res_int_se.dat'
        nx = str(np.loadtxt(dirPath+f+sePR, dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:]#[1:3]
        ny = str(np.loadtxt(dirPath+f+sePR, dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:]#[1:3]
        xMin = str(np.loadtxt(dirPath+f+sePR, dtype=str, comments=None, skiprows=4, max_rows=1, usecols=(0)))[1:]#[1:3]
        xMax = str(np.loadtxt(dirPath+f+sePR, dtype=str, comments=None, skiprows=5, max_rows=1, usecols=(0)))[1:]#[1:3]
        rx = float(xMax)-float(xMin)
        dx = np.divide(rx,float(nx))
        yMin = str(np.loadtxt(dirPath+f+sePR, dtype=str, comments=None, skiprows=7, max_rows=1, usecols=(0)))[1:]#[1:3]
        yMax = str(np.loadtxt(dirPath+f+sePR, dtype=str, comments=None, skiprows=8, max_rows=1, usecols=(0)))[1:]#[1:3]
        ry = float(yMax)-float(yMin)
        dy = np.divide(ry,float(ny))
        
        # numC = int(str(np.loadtxt(dirPath+f+sePR, dtype=str, comments=None, skiprows=10, max_rows=1, usecols=(0)))[1:])#[1:3]
        
        print("Resolution (x,y): {}".format((nx,ny)))
        print("xRange: {}".format(rx))
        print("xMax: {}".format(xMax))
        print("xMin: {}".format(xMin))
        print("yRange: {}".format(rx))
        print("yMax: {}".format(xMax))
        print("yMin: {}".format(xMin))
        print("Dx, Dy : {}".format((dx,dy)))
        
        I = np.reshape(np.loadtxt(dirPath+f+sePR,skiprows=10), (int(ny),int(nx)))         # Propagated multi-electron intensity
        # Iflat = I.flatten()
        
    #    plt.plot(Iflat)
    #    plt.show()
              
        """ Creating array of custom tick markers for plotting """
        sF = 1 #e6
        tickAx = [round_sig(-rx*sF/2),
                  round_sig(-rx*sF/4),
                  0,
                  round_sig(rx*sF/4),
                  round_sig(rx*sF/2)
                  ]
        tickAy = [round_sig(-ry*sF/2),
                  round_sig(-ry*sF/4),
                  0,
                  round_sig(ry*sF/4),
                  round_sig(ry*sF/2)]
        
        
        plt.imshow(I, aspect='auto')
        plt.title("Multi-electron intensity")#.format(name))
        plt.colorbar()
#        if SAVE == True:
#            print("Saving propagated intensity plot to: " + dirPath + "plots/" + "Propintensity" + name + ".png")
#            plt.savefig(dirPath + "plots/" + "Propintensity" + name + ".png")
        plt.show()
        
        plt.clf()
        plt.close()
        plt.plot(I[0,:,:][:,int(int(nx)/2)], label='vertical cut')
        plt.legend()
        plt.show()
        
        # imageio.imwrite(dirPath+f+f[0:len(f)-1]+'intensity.tif',np.float32(I[0,:,:]))
        
fig.tight_layout()#pad=-0.0005)
if save:
    plt.savefig(savePath + 'spectrum_{}.pdf'.format(str(f[7:len(str(f))-4])))
    plt.savefig(savePath + 'spectrum_{}.png'.format(str(f[7:len(str(f))-4])), dpi=2000)
plt.show()        

# fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()

# ax1.plot(meSpec)
# ax2.plot(seSpec)

# ax1.set_axvline(x=harMax[0]-FWHM[0]/2, linestyle = ':', color=colours[1], label='FWHM')
# ax1.set_axvline(x=harMax[0]+FWHM[0]/2, linestyle = ':', color=colours[1], label='FWHM')
# plt.text(20000,harMax[0],'FWHM: {} eV'.format(FWHM[0]*energyRes[0]), color=colours[1])
# ax2.set_axvline(x=harMax[1]-FWHM[1]/2, linestyle = ':', color=colours[2], label='FWHM')
# ax2.set_axvline(x=harMax[1]+FWHM[1]/2, linestyle = ':', color=colours[2], label='FWHM')
# plt.text(20000,harMax[1],'FWHM: {} eV'.format(FWHM[1]*energyRes[1]), color=colours[2])
# ax1.set_xticks([len(meSpec)*a for a in [0,1/5,2/5,3/5,4/5,1]])
# ax1.set_xticklabels([energyRes[0]*len(meSpec)*a for a in [0,1/5,2/5,3/5,4/5,1]])
# ax1.set_xlabel('Photon Energy [eV]')
# ax1.set_ylabel('Flux [ph/s/.1%bw]')
# ax2.set_ylabel('Intensity [ph/s/.1%bw/mm²]')
# plt.show()
        