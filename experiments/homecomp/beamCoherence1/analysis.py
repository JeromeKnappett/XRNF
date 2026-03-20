#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 17:16:04 2020


This is a basic example of how to handle the pickled results from a batch 
simulation (i.e. from doExperiment/runner)

@author: -
"""
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib.font_manager import FontProperties
from math import log10, floor
import wfCoherence

#import xl.runner as runner

# %%
def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x

dirPath = '/home/jerome/dev/experiments/maskEfficiency8/data/'
batchOutputFile = dirPath + 'CL/results.pickle'

trialData =  [dirPath + '40LH/', dirPath + '50LH/', dirPath + '60LH/', dirPath + '80LH/' ]#[dirPath + '01/', dirPath + '05/', dirPath + '60/', dirPath + '70/', dirPath + '80/', dirPath + '90/', dirPath + '100/']
files = ['stokes0.pkl', 'stokes1.pkl', 'stokes2.pkl']
pickles =['p40-lh.pkl', 'p50-lh.pkl', 'p60-lh.pkl', 'p80-lh.pkl'] # ['eh01.pkl', 'eh05.pkl', 'eh60.pkl', 'eh70.pkl', 'eh80.pkl', 'eh90.pkl', 'eh100.pkl']
data = [ 'res_int_pr_me.dat' ,'res_int_pr_me_dcx.dat', 'res_int_pr_me_dcy.dat', 'res_int_pr_me_mix.dat', 'res_int_pr_me_miy.dat']

polarisation = ['linVertical', 'linHorizontal', 'linDiagonal', 'circRight', 'circLeft']

emittance = [90] # [0.1, 0.5, 60, 70, 80, 90, 100]

pitch = [40, 50, 60, 80]

Ix = []
Iy = []
mIx = []
mIy = []
mIx2 = []
mIy2 = []
cX = []
cY = []
cX2 = []
cY2 = []

nX = []
nY = []
rX = []
rY = []
tX = []
tY = []
clx = []
cly = []

for t, pk, e in zip(trialData, pickles, pitch):
    print("")
    print("----- Analysing trial:" + pk[0:len(str(pk))-3] + " -----")
    """ Getting range, resolution, dimensions """
    with open(t + pk, 'rb') as g:
        r = pickle.load(g)
    nx = r['results']['params/Mesh/nx']
    xMax = r['results']['params/Mesh/xMax']
    xMin = r['results']['params/Mesh/xMin']
    print("xMax: {}".format(xMax))
    print("xMin: {}".format(xMin))
    rx = np.subtract(xMax,xMin)
    print("xRange: {}".format(rx))
    dx = np.divide(rx,nx)
    rX.append(rx)
    nX.append(nx)
    ny = r['results']['params/Mesh/ny']
    yMax = r['results']['params/Mesh/yMax']
    yMin = r['results']['params/Mesh/yMin']
    ry = np.subtract(yMax,yMin)
    dy = np.divide(ry,ny)   
    rY.append(ry)
    nY.append(ny)
    
    Ix = r['results']['Intensity/Total/X/profile']
    Iy = r['results']['Intensity/Total/Y/profile']
    
    plt.plot(Ix, label="horizontal I")
    plt.plot(Iy, label="vertical I")
    plt.legend()
    plt.show()
    
        
    # I = np.reshape(np.loadtxt(t + 'res_int_pr_me.dat',skiprows=11), (nx,ny))          # Intensity
    # cX = np.reshape(np.loadtxt(t + 'res_int_pr_me_dcx.dat',skiprows=11), (nx,ny))     # Horizontal coherence
    # cY = np.reshape(np.loadtxt(t + 'res_int_pr_me_dcy.dat',skiprows=11), (nx,ny))     # Vertical coherence
    # miX = np.reshape(np.loadtxt(t + 'res_int_pr_me_mix.dat',skiprows=11), (nx,ny,2))  # Horizontal mutual intensity
    # miY =  np.reshape(np.loadtxt(t + 'res_int_pr_me_miy.dat',skiprows=11), (nx,ny,2)) # Vertical mutual intensity
    # dCx = np.diagonal(np.squeeze(cX))
    # dCy = np.diagonal(np.squeeze(cY))


    # """ Creating array of custom tick markers for plotting """
    # sF = 1 #e6
    # tickAx = [round_sig(-rx*sF/2),
    #           round_sig(-rx*sF/4),
    #           0,
    #           round_sig(rx*sF/4),
    #           round_sig(rx*sF/2)
    #           ]
    # tX.append(tickAx)
    # tickAy = [round_sig(-ry*sF/2),
    #           round_sig(-ry*sF/4),
    #           0,
    #           round_sig(ry*sF/4),
    #           round_sig(ry*sF/2)]
    # tY.append(tickAy)
    
    
    
    # """ Plotting intensity, coherence """
    # plt.clf()
    # plt.close()
    # plt.imshow(I)
    # plt.xticks(np.arange(0,nx+1,nx/4),tickAx)
    # plt.yticks(np.arange(0,ny+1,ny/4),tickAy)
    # plt.xlabel("position [m]") # [\u03bcm]")
    # plt.xlabel("position [m]") # [\u03bcm]")
    # plt.title("Intensity, e =" + str(e))
    # plt.colorbar()
    # plt.savefig(dirPath + "plots/" + "intensity" + str(e) + ".png")
    # print("Saving intensity plot to: {}".format("plots/" + "intensity" + str(e) + ".png"))
    # plt.show()
    # plt.clf()
    # plt.close()
    
    # plt.imshow(cX)
    # plt.title("Horizontal Coherence, e =" + str(e))
    # plt.colorbar()
    # plt.savefig(dirPath + "plots/" + "coherenceHor" + str(e) + ".png")
    # print("Saving horizontal coherence plot to: {}".format("plots/" + "coherenceHor" + str(e) + ".png"))
    # plt.show()
    # plt.clf()
    # plt.close()
    

    # plt.plot(cX[:,int(ny/2)], '.', markersize = 0.5, label="vertical")
    # plt.plot(cX[int(nx/2),:], '.', markersize = 0.5, label="horizontal")
    # plt.plot(np.diagonal(np.squeeze(cX)), '.', markersize = 0.5, label="diagonal")   
    # plt.plot((I[:,int(ny/2)]/np.max(I[:,int(ny/2)])), '.', markersize = 0.5, label="intensity")
    # plt.xticks(np.arange(0,nx+1,nx/4),tickAx)
    # plt.xlabel("position [m]") # [\u03bcm]")
    # plt.title("Horizontal Coherence (cuts), e =" + str(e))
    # plt.legend()
    # plt.savefig(dirPath + "plots/" + "coherenceHorCuts" + str(e) + ".png")
    # print("Saving horizontal coherence cuts plot to: {}".format("plots/" + "coherenceHorCuts" + str(e) + ".png"))
    # plt.show()
    # plt.clf()
    # plt.close()
    
    # # np.diag(np.fliplr(array))
    # plt.plot((I[:,int(ny/2)]/np.max(I[:,int(ny/2)])), label="Intensity - vertical")
    # plt.plot((I[int(nx/2),:]/np.max(I[int(nx/2),:])), label="Intensity - horizontal")
    # # plt.plot(I[int(nx/2),:], label="Intensity - horizontal")
    # plt.plot(np.diagonal(np.squeeze(cX)), label="diagonal of Cx")   
    # plt.plot(np.diag(np.fliplr(cX)), label="Intensity - diagonal of Cx")
    # plt.title("Comparing intensity")
    # plt.legend()
    # plt.show()
    
    
    
    # plt.imshow(cY)
    # plt.title("Vertical Coherence, e =" + str(e))
    # plt.colorbar()
    # plt.savefig(dirPath + "plots/" + "coherenceVer" + str(e) + ".png")
    # print("Saving vertical coherence plot to: {}".format("plots/" + "coherenceVer" + str(e) + ".png"))
    # plt.show()
    # plt.clf()
    # plt.close()

    # plt.plot(cY[:,int(ny/2)], '.', markersize = 0.5, label="vertical")
    # plt.plot(cY[int(nx/2),:], '.', markersize = 0.5, label="horizontal")
    # plt.plot(np.diagonal(np.squeeze(cY)), '.', markersize = 0.5, label="diagonal")   
    # plt.plot((I[int(nx/2),:]/np.max(I[int(nx/2),:])), '.', markersize = 0.5,  label="intensity")
    # plt.xticks(np.arange(0,ny+1,ny/4),tickAy)
    # plt.xlabel("position [m]") # [\u03bcm]")
    # plt.title("Vertical Coherence (cuts), e =" + str(e))
    # plt.legend()
    # plt.savefig(dirPath + "plots/" + "coherenceVerCuts" + str(e) + ".png")
    # print("Saving vertical coherence cuts plot to: {}".format(dirPath + "plots/" + "coherenceHorCuts" + str(e) + ".png"))
    # plt.show()
    # plt.clf()
    # plt.close()
    
    # plt.clf()
    # plt.close()
    # clX, clY = wfCoherence.getCoherenceLength(dCx, dCy, 0.7, dirPath + "plots/" + "coherenceLen" + str(e) + ".png")
    # print("Horizontal Coherence Length [m]: {}".format(abs(clX*dx)))
    # print("Vertical Coherence Length [m]: {}".format(abs(clY*dy)))
    # clx.append(abs(clX*dx))
    # cly.append(abs(clY*dy))
    # plt.clf()
    # plt.close()
    
    # plt.close()
    # plt.clf()
    # fig, axs = plt.subplots(2, 3)
    # axs[0,0].imshow(miX[:,:,0])
    # axs[0,0].set_title("J - Horizontal (1)")
    # axs[0,1].imshow(miX[:,:,1])
    # axs[0,1].set_title("J - Horizontal (2)")
    # axs[0,2].imshow(miX.mean(2))
    # axs[0,2].set_title("J - Horizontal (mean)")
    # axs[1,0].imshow(np.divide(miX[:,:,0],I,out=np.zeros_like(I), where=I!=0))
    # axs[1,0].set_title("J (1) - Normalised to I")
    # axs[1,1].imshow(np.divide(miX[:,:,1],I,out=np.zeros_like(I), where=I!=0))
    # axs[1,1].set_title("J (2) - Normalised to I")
    # axs[1,2].imshow(np.divide(miX.mean(2),I,out=np.zeros_like(I), where=I!=0))
    # axs[1,2].set_title("J (mean) - Normalised to I")
    # print("Saving horizontal mutual intensity (J) plots to: {}".format(dirPath + "plots/" + "mutualIntensityHor" + str(e) + ".png"))
    # plt.savefig(dirPath + "plots/" + "mutualIntensityHor" + str(e) + ".png")
    # plt.show()
    # plt.close()
    # plt.clf()
        
    # plt.close()
    # plt.clf()
    # fig, axs = plt.subplots(2, 3)
    # axs[0,0].imshow(miY[:,:,0])
    # axs[0,0].set_title("J - Vertical (1)")
    # axs[0,1].imshow(miY[:,:,1])
    # axs[0,1].set_title("J - Vertical (2)")
    # axs[0,2].imshow(miY.mean(2))
    # axs[0,2].set_title("J - Vertical (mean)")
    # axs[1,0].imshow(np.divide(miY[:,:,0],I,out=np.zeros_like(I), where=I!=0))
    # axs[1,0].set_title("J (1) - Normalised to I")
    # axs[1,1].imshow(np.divide(miY[:,:,1],I,out=np.zeros_like(I), where=I!=0))
    # axs[1,1].set_title("J (2) - Normalised to I")
    # axs[1,2].imshow(np.divide(miY.mean(2),I,out=np.zeros_like(I), where=I!=0))
    # axs[1,2].set_title("J (mean) - Normalised to I")
    # print("Saving vertical mutual intensity (J) plots to: {}".format(dirPath + "plots/" + "mutualIntensityVer" + str(e) + ".png"))
    # plt.savefig(dirPath + "plots/" + "mutualIntensityVer" + str(e) + ".png")
    # plt.show()
    # plt.close()
    # plt.clf()
    
    # plt.rcParams["figure.figsize"] = (10,6)
    # """ COMPARING MI to I """
    # # plt.plot((I[:,int(ny/2)]/np.max(I[:,int(ny/2)])), label="Intensity - vertical")
    # # plt.plot((I[int(nx/2),:]/np.max(I[int(nx/2),:])), label="Intensity - horizontal")
    # plt.plot(I[int(nx/2),:], label="Intensity - horizontal")
    # plt.plot(I[:,int(ny/2)], label="Intensity - vertical")
    # plt.plot(np.diagonal(np.squeeze(abs(miX[:,:,0]))), label="diagonal of MI(1)")   
    # plt.plot(np.diag(np.fliplr(abs(miX[:,:,0]))), label="opposite diagonal of MI(1)")
    # plt.plot(np.diagonal(np.squeeze(abs(miX[:,:,1]))), label="diagonal of MI(2)")   
    # plt.plot(np.diag(np.fliplr(abs(miX[:,:,1]))), label="opposite diagonal of MI(2)")
    # plt.plot(np.diagonal(np.squeeze(abs(miX.mean(2)))), label="diagonal of MI(mean)")   
    # plt.plot(np.diag(np.fliplr(abs(miX.mean(2)))), label="opposite diagonal of MI(mean)")
    # plt.title("Comparing intensity")
    # plt.legend()
    # plt.show()
    # plt.rcParams["figure.figsize"] = (10,6)    
    
    
    # # plt.plot((I[:,int(ny/2)]/np.max(I[:,int(ny/2)])), label="Intensity - vertical")
    # # plt.plot((I[int(nx/2),:]/np.max(I[int(nx/2),:])), label="Intensity - horizontal")
    # plt.plot(I[int(nx/2),:], label="Intensity - horizontal")
    # plt.plot(I[:,int(ny/2)], label="Intensity - vertical")
    # plt.plot(abs(miX[int(nx/2),:,0]), label="horizontal of MI(1)")   
    # plt.plot(abs(miX[:,int(ny/2),0]), label="vertical of MI(1)")
    # plt.plot(abs(miX[int(nx/2),:,1]), label="horizontal of MI(2)")   
    # plt.plot(abs(miX[:,int(ny/2),1]), label="vertical of MI(2)")
    # plt.plot(abs(miX.mean(2)[int(nx/2),:]), label="horizontal of MI(mean)")   
    # plt.plot(abs(miX.mean(2)[:,int(ny/2)]), label="vertical of MI(mean)")
    # plt.title("Comparing intensity")
    # plt.legend()
    # plt.show()
    # plt.rcParams["figure.figsize"] = (10,6)
    
    # """ COMPARING MI to Coherence """
    # # plt.plot((I[:,int(ny/2)]/np.max(I[:,int(ny/2)])), label="Intensity - vertical")
    # # plt.plot((I[int(nx/2),:]/np.max(I[int(nx/2),:])), label="Intensity - horizontal")
    # # plt.plot(cX[:,int(ny/2)], label="vertical coherence X")
    # # plt.plot(cX[int(nx/2),:], label="horizontal coherence X")
    # # plt.plot(np.diagonal(np.squeeze(cX)), label="diagonal coherence X")   
    # # plt.plot(np.diagonal(np.squeeze(abs(miX[:,:,0])))/np.max(np.diagonal(np.squeeze(abs(miX[:,:,0])))), label="diagonal of MI(1)")   
    # # plt.plot(np.diag(np.fliplr(abs(miX[:,:,0])))/np.max(np.diag(np.fliplr(abs(miX[:,:,0])))), label="opposite diagonal of MI(1)")
    # plt.plot(np.diagonal(np.squeeze(abs(miX[:,:,1])))/np.max(np.diagonal(np.squeeze(abs(miX[:,:,1])))), label="diagonal of MI(2)")   
    # # plt.plot(np.diag(np.fliplr(abs(miX[:,:,1])))/np.max(np.diag(np.fliplr(abs(miX[:,:,1])))), label="opposite diagonal of MI(2)")
    # # plt.plot(np.diagonal(np.squeeze(abs(miX.mean(2))))/np.max(np.diagonal(np.squeeze(abs(miX.mean(2))))), label="diagonal of MI(mean)")   
    # # plt.plot(np.diag(np.fliplr(abs(miX.mean(2))))/np.max(np.diag(np.fliplr(abs(miX.mean(2))))), label="opposite diagonal of MI(mean)")
    # plt.title("Comparing to coherence")
    # plt.xlim(75,125)
    # plt.legend()
    # plt.show()
    # plt.rcParams["figure.figsize"] = (10,6)    
    
    # print(np.diagonal(np.squeeze(abs(miX[:,:,1]))))
    # print(np.max(np.diagonal(np.squeeze(abs(miX[:,:,1])))))
    
    # plt.plot(cX[:,int(ny/2)], label="vertical coherence X")
    # plt.plot(cX[int(nx/2),:], label="horizontal coherence X")
    # plt.plot(np.diagonal(np.squeeze(cX)), label="diagonal coherence X")   
    # # plt.plot(abs(miX[int(nx/2),:,0])/np.max(abs(miX[int(nx/2),:,0])), label="horizontal of MI(1)")   
    # # plt.plot(abs(miX[:,int(ny/2),0])/np.max(abs(miX[:,int(ny/2),0])), label="vertical of MI(1)")
    # # plt.plot(abs(miX[int(nx/2),:,1])/np.max(abs(miX[int(nx/2),:,1])), label="horizontal of MI(2)")   
    # # plt.plot(abs(miX[:,int(ny/2),1])/np.max(abs(miX[:,int(ny/2),1])), label="vertical of MI(2)")
    # # plt.plot(abs(miX.mean(2)[int(nx/2),:])/np.max(abs(miX.mean(2)[int(nx/2),:])), label="horizontal of MI(mean)")   
    # # plt.plot(abs(miX.mean(2)[:,int(ny/2)])/np.max(abs(miX.mean(2)[:,int(ny/2)])), label="vertical of MI(mean)")
    # plt.title("Comparing to coherence")
    # plt.xlim(75,125)
    # plt.legend()
    # plt.show()
    # plt.rcParams["figure.figsize"] = (10,6)



print("Coherence Lengths (hor): {}".format(clx))
print("Coherence Lengths (ver): {}".format(cly))

plt.plot(emittance, clx, label="Horizontal")
plt.plot(emittance, cly, label="Vertical")
plt.title("Coherence Length vs E-beam emittance")
plt.legend()
plt.xlabel("Horizontal emittance [nm]")
plt.ylabel("Coherence Length [m]")
plt.savefig(dirPath + "plots/" + "coherenceLengths.png")
print("Saving vertical coherence cuts plot to: {}".format("plots/" + "coherenceLengths.png"))
plt.show()
plt.clf()
plt.close()


# for t, e, tx in zip(trialData, emittance, tX):
#     for i, f in enumerate(files):
#         with open(t + f, 'rb') as g:
#             stk = pickle.load(g)
#         print("Shape of pkl array: {}".format(np.shape(stk.arS)))

#         nTot = stk.mesh.nx*stk.mesh.ny*stk.mesh.ne
# #        print("nTot: {}".format(nTot))

#         try:
#             s = np.reshape(stk.arS,(4,stk.mesh.nx,stk.mesh.ny))
#             S0 = np.reshape(s[0,:,:],(stk.mesh.nx,stk.mesh.ny))
#             S1 = np.reshape(s[1,:,:],(stk.mesh.nx,stk.mesh.ny))
#             S2 = np.reshape(s[2,:,:],(stk.mesh.nx,stk.mesh.ny))
#             S3 = np.reshape(s[3,:,:],(stk.mesh.nx,stk.mesh.ny))
#         except ValueError:
#             s = np.reshape(stk.arS,(4,int(np.size(stk.arS)/4)))
#             s0 = np.reshape(s[0,:],(nTot,stk.mesh.nx,stk.mesh.ny,2))
#             s1 = np.reshape(s[1,:],(nTot,stk.mesh.nx,stk.mesh.ny,2))
#             s2 = np.reshape(s[2,:],(nTot,stk.mesh.nx,stk.mesh.ny,2))
#             s3 = np.reshape(s[3,:],(nTot,stk.mesh.nx,stk.mesh.ny,2))

#  #           print("shape of s0: {}".format(np.shape(s0)))
#  #           print("shape of s1: {}".format(np.shape(s1)))
#  #           print("shape of s2: {}".format(np.shape(s2)))
#  #           print("shape of s3: {}".format(np.shape(s3)))


#             _s0 = np.squeeze(s0)#.shape #mean(2)
#             _s1 = np.squeeze(s1)#.shape #mean(2)
#             _s2 = np.squeeze(s2)#.shape #mean(2)
#             _s3 = np.squeeze(s3)#.shape #mean(2)
            
# #            print("shape of _s0: {}".format(np.shape(_s0)))
# #            print("shape of _s1: {}".format(np.shape(_s1)))
# #            print("shape of _s2: {}".format(np.shape(_s2)))
# #            print("shape of _s3: {}".format(np.shape(_s3)))

#             _s01 = _s0[:,:,0]
#             _s02 = _s0[:,:,1]
#             _s11 = _s1[:,:,0]
#             _s12 = _s1[:,:,1]
#             _s21 = _s2[:,:,0]
#             _s22 = _s2[:,:,1]
#             _s31 = _s3[:,:,0]
#             _s32 = _s3[:,:,1]
            
#             S0 = _s01 # abs(_s0.mean(0))
#             S1 = _s11 # abs(_s1.mean(0))
#             S2 = _s21 # abs(_s2.mean(0))
#             S3 = _s31 # abs(_s3.mean(0))
            
#         print("shape of s: {}".format(np.shape(s)))

#         plt.plot(stk.arS)
#         plt.title(str(e) + '_Stokes' + str(i))
#         plt.savefig(dirPath + str(e) + '_arrayStokes' + str(i) + '.png')
#         print("stk.arS plot saved to : {}".format(dirPath + str(e) + '_arrayStokes' + str(i) + '.png'))
#         plt.show()
#         plt.clf()
#         plt.close()

#         smax = np.max([S0,S1,S2,S3])
#         smin = np.min([S0,S1,S2,S3])
#         fig, axs = plt.subplots(2, 2)
#         im = axs[0, 0].imshow(S0, vmin=smin, vmax=smax)
#         axs[0, 0].set_title(str(e) + '_S0_' + str(i))
#         axs[0, 1].imshow(S1, vmin=smin, vmax=smax)
#         axs[0, 1].set_title(str(e) + '_S1_' + str(i))
#         axs[1, 0].imshow(S2, vmin=smin, vmax=smax)
#         axs[1, 0].set_title(str(e) + '_S2_' + str(i))
#         axs[1, 1].imshow(S3, vmin=smin, vmax=smax)
#         axs[1, 1].set_title(str(e) + '_S3_' + str(i))
    
#         for ax in axs.flat:
#             ax.set(xlabel="x-position [pixels]", ylabel="y-position [pixels] ")
#         # Hide x labels and tick labels for top plots and y ticks for right plots.
#         for ax in axs.flat:
#             ax.label_outer()
#         fig.subplots_adjust(right=0.8)
#         cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#         fig.colorbar(im, cax=cbar_ax)
        
#         plt.savefig(dirPath + str(e) + '_reshapedStokes' + str(i) + '.png')
#         print("Reshaped stk.arS plots saved to : {}".format(dirPath + str(e) + '_reshapedStokes' + str(i) + '.png'))
#         plt.show()
#         plt.clf()
#         plt.close()        
      
#         try:
#             smax = np.max([_s02,_s12,_s22,_s32])
#             smin = np.min([_s02,_s12,_s22,_s32])
#             fig, axs = plt.subplots(2, 2)
#             im = axs[0, 0].imshow(_s02, vmin=smin, vmax=smax)
#             axs[0, 0].set_title(str(e) + '_s0_' + str(i))
#             axs[0, 1].imshow(_s12, vmin=smin, vmax=smax)
#             axs[0, 1].set_title(str(e) + '_s1_' + str(i))
#             axs[1, 0].imshow(_s22, vmin=smin, vmax=smax)
#             axs[1, 0].set_title(str(e) + '_s2_' + str(i))
#             axs[1, 1].imshow(_s32, vmin=smin, vmax=smax)
#             axs[1, 1].set_title(str(e) + '_s3_' + str(i))
    
#             for ax in axs.flat:
#                 ax.set(xlabel="x-position [pixels]", ylabel="y-position [pixels] ")
#             # Hide x labels and tick labels for top plots and y ticks for right plots.
#             for ax in axs.flat:
#                 ax.label_outer()
#             fig.subplots_adjust(right=0.8)
#             cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#             fig.colorbar(im, cax=cbar_ax)
        
#             plt.savefig(dirPath + str(e) + '_reshapedSecondStokes' + str(i) + '.png')
#             print("Secondary reshaped stk.arS plots saved to : {}".format(dirPath + str(e) + '_reshapedSecondStokes' + str(i) + '.png'))
#             plt.show()
#             plt.clf()
#             plt.close()
            
# #            difS0 = np.subtract(S0,_s02)
# #            difS1 = np.subtract(S1,_s12)
# #            difS2 = np.subtract(S2,_s22)
# #            difS3 = np.subtract(S3,_s32)

# #            _smax = np.max([difS0,difS1,difS2,difS3])
# #            _smin = np.min([difS0,difS1,difS2,difS3])
# #            fig, axs = plt.subplots(2, 2)
# #            im = axs[0, 0].imshow(difS0, vmin=_smin, vmax=_smax)
# #            axs[0, 0].set_title(str(e) + 'difStokes' + str(i))
# #            axs[0, 1].imshow(difS1, vmin=_smin, vmax=_smax)
# #            axs[0, 1].set_title(str(e) + 'difStokes' + str(i))
# #            axs[1, 0].imshow(difS2, vmin=_smin, vmax=_smax)
# #            axs[1, 0].set_title(str(e) + 'difStokes' + str(i))
# #            axs[1, 1].imshow(difS3, vmin=_smin, vmax=_smax)
# #            axs[1, 1].set_title(str(e) + 'difStokes' + str(i))
    
# #            for ax in axs.flat:
# #                ax.set(xlabel="x-position [pixels]", ylabel="y-position [pixels] ")
# #            # Hide x labels and tick labels for top plots and y ticks for right plots.
# #            for ax in axs.flat:
# #                ax.label_outer()
# #            fig.subplots_adjust(right=0.8)
# #            cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
# #            fig.colorbar(im, cax=cbar_ax)

# #            plt.savefig(dirPath + str(e) + '_diffStokes' + str(i) + '.png')
# #            print("Difference plots saved to : {}".format(dirPath + str(e) + '_diffStokes' + str(i) + '.png'))
# #            plt.show()
# #            plt.clf()  
# #            plt.close()

#         except NameError or ValueError:
#             pass
            
#         if i ==0:
#             #print("mid: {}".format(int((np.shape(S0)[0])/2)))
#             y = S0[:,int((np.shape(S0)[0])/2)]
#             x = S0[int((np.shape(S0)[1])/2),:]
#             plt.plot(x, label="Horizontal Cut")
#             plt.plot(y, label="Vertical Cut")
#             plt.xticks(np.arange(0,len(x)+1,len(x)/4),tx)
#             plt.xlabel("position [m]") # [\u03bcm]")
#             plt.title("Intensity")
#             plt.legend()
#             plt.savefig(dirPath + str(e) + '_IntensityProfiles.png')
#             print("Intensity figure saved to: {}".format(dirPath + str(e) + '_IntensityProfiles.png'))
#             plt.clf()
#             plt.close()
#             Ix.append(x)
#             Iy.append(y)
#         if i ==1:
#             y = S0[:,int((np.shape(S0)[0])/2)]
#             x = S0[int((np.shape(S0)[1])/2),:]
#             y1 = _s01[:,int((np.shape(S0)[0])/2)]
#             x1 = _s01[int((np.shape(S0)[1])/2),:]
#             plt.plot(x, label="Horizontal Cut -s1")
#             plt.plot(y, label="Vertical Cut -s1")
#             plt.plot(x1, label="Horizontal Cut -s2")
#             plt.plot(y1, label="Vertical Cut -s2")
#             plt.title("Mutual Intensity")
#             plt.legend()
#             plt.savefig(dirPath + str(e) + '_MutualIntensityProfiles.png')
#             print("Mutual Intensity figure saved to: {}".format(dirPath + str(e) + '_MutualIntensityProfiles.png'))
#             plt.clf()
#             plt.close()
#             mIx.append(x)
#             mIy.append(y)
#             mIx2.append(x1)
#             mIy2.append(y1)
#         if i ==2:
#             y = S0[:,int((np.shape(S0)[0])/2)]
#             x = S0[int((np.shape(S0)[1])/2),:]
#             y1 = _s01[:,int((np.shape(S0)[0])/2)]
#             x1 = _s01[int((np.shape(S0)[1])/2),:]
#             plt.plot(x, label="Horizontal Cut -s1")
#             plt.plot(y, label="Vertical Cut -s1")
#             plt.plot(x1, label="Horizontal Cut -s2")
#             plt.plot(y1, label="Vertical Cut -s2")
#             plt.title("Coherence")
#             plt.legend()
#             plt.savefig(dirPath + str(e) + '_CoherenceProfiles.png')
#             print("Coherence figure saved to: {}".format(dirPath + str(e) + '_CoherenceProfiles.png'))
#             plt.clf()
#             plt.close()
#             cX.append(x)
#             cY.append(y)
#             cX2.append(x1)
#             cY2.append(y1)

# print("Horizontal tick arrays: {}".format(tX))
# print("Vertical tick arrays: {}".format(tY))

# for x, y, tx, e in zip(Ix, Iy, tX, emittance):
#     plt.plot(x, label="x-cut,p="+e)
#     plt.plot(y, label="y-cut,p="+e)
#     plt.title("Intensity Profiles")
#     plt.xticks(np.arange(0,len(x)+1,len(x)/4),tx)
#     plt.xlabel("position [m]") # [\u03bcm]")
# plt.legend()
# plt.savefig(dirPath + 'intensityprofileplots.png')
# print("intensity profile plots saved to: {}".format(dirPath + 'intensityprofileplots.png'))
# plt.show()
# plt.clf()
# plt.close()


# for x, cx, cx2, y, cy, cy2, tx, e in zip(Ix,cX,cX2,Iy,cY,cY2,tX, emittance):
#     Cx = abs(np.divide(cx, abs(x), out=np.zeros_like(cx), where=x!=0)) #abs(cx/abs(x)**2)
#     Cx2 = abs(np.divide(cx2, abs(x), out=np.zeros_like(cx2), where=x!=0)) #abs(cx2/abs(x)**2)
#     Cy = abs(np.divide(cy, abs(y), out=np.zeros_like(cy), where=y!=0)) #abs(cy/abs(y)**2)
#     Cy2 = abs(np.divide(cy2, abs(y), out=np.zeros_like(cy), where=y!=0)) #abs(cy2/abs(y)**2)
#     plt.plot(Cx, label="x - c1")
#     plt.plot(Cx2, label="x - c2")
#     plt.plot(Cy, label="y - c1")
#     plt.plot(Cy2, label="y - c2")
#     plt.title("Coherence Normalised")
#     plt.xticks(np.arange(0,len(Cx)+1,len(Cx)/4),tx)
#     plt.xlabel("position [m]") # [\u03bcm]")
#     plt.ylabel("Coherence")
#     plt.ylim(0,1.1)
#     plt.legend()
#     plt.savefig(dirPath + str(e) + 'normalisedCoherence.png')
#     print("Normalised coherence plot saved to: {}".format(dirPath + str(e) + 'normalisedCoherence.png'))
#     plt.clf()
#     plt.close()

# #for y, cy, cy2, ty, e in zip(Iy,cY,cY2,tY, emittance):
# #    Cy = abs(np.divide(cy, abs(y), out=np.zeros_like(cy), where=y!=0)) #abs(cy/abs(y)**2)
# #    Cy2 = abs(np.divide(cy2, abs(y), out=np.zeros_like(cy), where=y!=0)) #abs(cy2/abs(y)**2)
# #    plt.plot(Cy, label="coherence1")
# #    plt.plot(Cy2, label="coherence2")
# #    plt.title("Y Coherence Normalised")
# #    plt.xticks(np.arange(0,len(Cy)+1,len(Cy)/4),ty)
# #    plt.xlabel("y-position [m]") #[\u03bcm]")
# #    plt.ylabel("Coherence")
# #    plt.ylim(0,1.1)
# #    plt.legend()
# #    plt.savefig(dirPath + str(e) + 'normalisedCoherenceV.png')
# #    print("Normalised coherence (ver) plot saved to: {}".format(dirPath + str(e) + 'normalisedCoherenceV.png'))
# #    plt.clf()  
# #    plt.close()

# for x, mx, mx2, y, my, my2, tx, e in zip(Ix,mIx,mIx2,Iy,mIy,mIy2,tX, emittance):
#     Cx = abs(np.divide(mx, abs(x), out=np.zeros_like(mx), where=x!=0)) #abs(mx/abs(x)**2)
#     Cx2 = abs(np.divide(mx2, abs(x), out=np.zeros_like(mx2), where=x!=0)) #abs(mx2/abs(x)**2)
#     Cy = abs(np.divide(my, abs(y), out=np.zeros_like(my), where=y!=0)) #abs(my/abs(y)**2)  
#     Cy2 = abs(np.divide(my2, abs(y), out=np.zeros_like(my2), where=y!=0)) #abs(my2/abs(y)**2)
#     plt.plot(Cx, label="x - mi1")
#     plt.plot(Cx2, label="x - mi2")  
#     plt.plot(Cy, label="y - mi1") 
#     plt.plot(Cy2, label="y - mi2")
#     plt.title("MI - Coherence Normalised")
#     plt.xticks(np.arange(0,len(Cx)+1,len(Cx)/4),tx)
#     plt.xlabel("position [m]") #[\u03bcm]")
#     plt.ylabel("Coherence")
#     plt.ylim(0,1.1)
#     plt.legend() 
#     plt.savefig(dirPath + str(e) + 'normalisedCoherenceMI.png')
#     print("Normalised coherence plot (MI) saved to: {}".format(dirPath + str(e) + 'normalisedCoherenceMI.png'))
#     plt.clf()  
#     plt.close()

# #for y, my, my2, ty, e in zip(Iy,mIy,mIy2,tY, emittance):
# #    Cy = abs(np.divide(my, abs(y), out=np.zeros_like(my), where=y!=0)) #abs(my/abs(y)**2)  
# #    Cy2 = abs(np.divide(my2, abs(y), out=np.zeros_like(my2), where=y!=0)) #abs(my2/abs(y)**2)  
# #    plt.plot(Cy, label="coherence1") 
# #    plt.plot(Cy2, label="coherence2")
# #    plt.title("MI - Y Coherence Normalised")
# #    plt.xticks(np.arange(0,len(Cy)+1,len(Cy)/4),ty)
# #    plt.xlabel("y-position [m]") #[\u03bcm]")
# #    plt.ylabel("Coherence")
# #    plt.ylim(0,1.1)
# #    plt.legend() 
# #    plt.savefig(dirPath + str(e) + 'normalisedCoherenceMIV.png')
# #    print("Normalised coherence (MI-ver) plot saved to: {}".format(dirPath + str(e) + 'normalisedCoherenceMIV.png'))
# #    plt.clf()
# #    plt.close()



def trials(results):
        return [k for k,v in results.items()]
       
def resultsKeys(results):
        return [k for k,v  in results['trial_0']['results'].items()]
    
def parameterKeys(results):
        return [k for k,v  in results['trial_0']['parameters'].items()]

    
def listValues(results, key):
        try:
            V =  [results[trial]['results'][key] for trial in trials(results)] 
        except KeyError:
            try:
                V =  [results[trial]['parameters'][key] for trial in trials(results)] 
            except KeyError:
                print('Valid values not found for ' + key)
                V=[]
        
        return V
    
def plot(results,*args,**kwargs):
                
        xKey = kwargs['x']
        yKey = kwargs['y']
            
        x = listValues(results,xKey)
        y = listValues(results,yKey)
               
        if x !=[] and y!=[]:
            fontP = FontProperties()
            fontP.set_size('xx-small')    
            plt.plot(x,y,'o')   #label=...
            plt.xlabel(xKey)
            plt.ylabel(yKey)
            plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5), prop=fontP)
            plt.show()   
    

        
#results = pickle.load( open(batchOutputFile, 'rb')  )


#keyCPLXy = 'cpY_totP'
#valuey = listValues(results, keyCPLXy)
#keyCPLXx = 'cpX_totP'
#valuex = listValues(results, keyCPLXx)

#keyJ = 'mutualIn_j'
#J = listValues(results, keyJ)
#keyJxx = 'mutualIn_jxx'
#Jxx = listValues(results, keyJxx)
#keyJxy = 'mutualIn_jxy'
#Jxy = listValues(results, keyJxy)
#keyJyx = 'mutualIn_jyx'
#Jyx = listValues(results, keyJyx)
#keyJyy = 'mutualIn_jyy'
#Jyy = listValues(results, keyJyy)

#keyS0 = 'S0'
#keyS1 = 'S1'
#keyS2 = 'S2'
#keyS3 = 'S3'
#S0 = listValues(results, keyS0)
#S1 = listValues(results, keyS1)
#S2 = listValues(results, keyS2)
#S3 = listValues(results, keyS3)
#keySTK = 'stokesVector'
#stokes = listValues(results, keySTK)
#keyDP = 'degOfPolarisation'
#P = listValues(results, keyDP)


#print(valuey)
#print(valuex)

#print("-----RESULTS KEYS-----")
#print(resultsKeys(results))
#print("-----TRIALS-----")
#print(trials(results))
#print("-----PARAMETER KEYS-----")
#print(parameterKeys(results))
#     

# plot(results,y='Intensity/Horizontal/Y/integratedOpticalDensity', x='op_Mask_Watchpoint_L')
# plot(results,y='Intensity/Vertical/Y/integratedOpticalDensity', x='op_Mask_Watchpoint_L')
# plot(results,y='Intensity/Total/Y/integratedOpticalDensity', x='op_Mask_Watchpoint_L')


# plot(results,y='Intensity/Horizontal/Y/contrastMichelson', x='op_Mask_Watchpoint_L')
# plot(results,y='Intensity/Vertical/Y/contrastMichelson', x='op_Mask_Watchpoint_L')
# plot(results,y='Intensity/Total/Y/contrastMichelson', x='op_Mask_Watchpoint_L')

# # histograms
# for h,b in  zip(listValues(results, 'Intensity/Total/Y/histogram'), listValues(results, 'Intensity/Total/Y/histogramBins')):
#     plt.plot(b,h)
# plt.show()

#number of pixels, range, resolution
#ny = listValues(results,'params/Mesh/ny')
#yMax = listValues(results,'params/Mesh/yMax')
#yMin = listValues(results, 'params/Mesh/yMin')
#resolutionY  = np.divide(np.subtract(yMax,yMin),ny)

#y = listValues(results, 'y')
 

#number of pixels, range, resolution
#nx = listValues(results,'params/Mesh/nx')
#xMax = listValues(results,'params/Mesh/xMax')
#xMin = listValues(results, 'params/Mesh/xMin')
#resolutionX  = np.divide(np.subtract(xMax,xMin),nx)

#x = listValues(results, 'x')


# plt.plot(ff[0],fa[0],'.')
# plt.show()

# #intensity profiles
# for v in listValues(results, 'Intensity/Total/Y/profile'):
#     plt.plot(v,y)
#     plt.title('Intensity (x=0)')
# plt.show()

# #intensity profiles
# for v in listValues(results, 'Intensity/Total/X/profile'):
#     plt.plot(v,x)
#     plt.title('Intensity (y=0)')
# plt.show()

#print(" ")
#print("Results Key")
#print(resultsKeys(results))

#Yprofiles = listValues(results, 'Intensity/Total/Y/profile')
#Xprofiles = listValues(results, 'Intensity/Total/X/profile')
#YprofilesH = listValues(results, 'Intensity/Horizontal/Y/profile')
#XprofilesH = listValues(results, 'Intensity/Horizontal/X/profile')
#YprofilesV = listValues(results, 'Intensity/Vertical/Y/profile')
#XprofilesV = listValues(results, 'Intensity/Vertical/X/profile')
##maskThickness = listValues(results, 'op_Mask_thick')
#trials = trials(results)
#cXprofiles = listValues(results, 'cpX_totP')
#cYprofiles = listValues(results, 'cpY_totP')
#cXprofilesH = listValues(results, 'cpX_horP')
#cYprofilesH = listValues(results, 'cpY_horP')
#cXprofilesV = listValues(results, 'cpX_verP')
#cYprofilesV = listValues(results, 'cpY_verP')

#J = listValues(results, 'mutualIn_j')
#Jxx = listValues(results, 'mutualIn_jxx')
#Jxy = listValues(results, 'mutualIn_jxy')
#Jyx = listValues(results, 'mutualIn_jyx')
#Jyy = listValues(results, 'mutualIn_jyy')

#S0 = listValues(results, 'S0')
#S1 = listValues(results, 'S1')
#S2 = listValues(results, 'S2')
#S3 = listValues(results, 'S3')
#stokes = listValues(results, 'stokesVector')
#P = listValues(results, 'degOfPolarisation')


#keyX = 'cpX_totP'
#valuesX = listValues(results, keyX)
#keyY = 'cpY_totP'
#valuesY = listValues(resilts, keyY)


#cX = 'cpX_totP'
#cY = 'cpY_totP'
#cXvals = listValues(results, cX)
#cYvals = listValues(results, cY)


#import utilMask
#import wfCoherence

#Efield = listValues(results, 'params/wEFieldUnit')
#print(Efield[0])

#pathP = dirPath + 'Profiles.png'
##pathPY = dirPath + 'ProfilesY.png'
#pathPh = dirPath + 'Profiles_hor.png'
##pathPYh = dirPath + 'ProfilesY_hor.png'
#pathPv = dirPath + 'Profiles_ver.png'
##pathPYv = dirPath + 'ProfilesY_ver.png'
#pathCL = dirPath + 'coherenceLength'
#pathCP = dirPath + 'coherenceProfile'
#pathclp = dirPath + 'cLengthPlot.png'
#pathJP = dirPath + 'Jplot'
#pathDP = dirPath + 'degPol'
#pathS = dirPath + 'stokesPlot'
#pathJH = dirPath + 'JH'
#pathJV = dirPath + 'JV'
#pathJ = dirPath + 'Jcoherence'
#pathJclp = dirPath + 'jClength'
#pathCLj = dirPath + 'anotherJclength'
#
#polarisation = ['Lin_Hor','Lin_Ver','Lin_Diag','Cir_Right','Cir_Left']
#
#e0 = []
#e1 = []
#en1 = []
#
#CLx = []
#CLy = []
#
#jCLx = []
#jCLy = []
#
#""" Plotting Coherence Profiles - Total Polarisation """
#plt.clf()
#plt.close()
#for p1, p2, P, Xpro, Ypro in zip(valuex, valuey, polarisation, Xprofiles, Yprofiles):
#        plt.clf()
#        plt.close()
#        cH, cV, JH, JV, IH, IV = wfCoherence.profileMI(p1, p2, Xpro, Ypro, pathCP + P + '.png')
#        plt.clf()
#        plt.close()
#        plt.plot(JH, label = 'Horizontal Coherence Profile')
#        plt.plot(JV, label = 'Vertical Coherence Profile')
#        plt.plot(Xpro, label = "Horizontal Intensity")
#        plt.plot(Ypro, label = "Vertical Intensity")
#        #plt.plot(1/cH, label = 'Horizontal Profile - Opposite Diagonal (normalised)')
#        #plt.plot(1/cV, label = 'Vertical Profile - Opposite Diagonal (normalised)')
#        plt.xlabel("Point Separation x-x' [pixels]")#[\u03bcm]")
#        plt.ylabel("Degree of Coherence")
#        plt.legend()
#        if pathCP != None:
#            print("Saving Mutual Intensity profiles to: {}".format(pathCP + P + '.png'))
#            plt.savefig(pathCP)
#        plt.show()
#        plt.clf()
#        
#        clX, clY = wfCoherence.getCoherenceLength(cH, cV, 1, pathCL + P + '.png')
#        _clX = clX*resolutionX.mean()
#        _clY = clY*resolutionY.mean()
#        print("Horizontal Coherence Length [m]: {}".format(_clX))
#        print("Vertical Coherence Length [m]: {}".format(_clY))
#        CLx.append(_clX)
#        CLy.append(_clY)
#        plt.clf()
#        plt.close()
#        plt.plot(abs(JH), label="J")
#        plt.plot(abs(IH), label="I")
#        plt.title("JH/IH")
#        plt.legend()
#        plt.savefig(pathJH + P + '.png')
#        plt.plot(abs(JV), label="J")
#        plt.plot(abs(IV), label="I")
#        plt.title("JV/IV")
#        plt.legend()
#        plt.savefig(pathJV + P + '.png')
#
#
#plt.clf()
#plt.close()
#plt.plot(polarisation, CLx, label="horizontal")
#plt.plot(polarisation, CLy, label="vertical")
#plt.legend()
#print("Saving coherence length plot to {}".format(pathclp))
#plt.savefig(pathclp)
#plt.show()
#
#
#""" Plotting coherence from J """
#plt.clf()
#plt.close()
#for pol, j, xpro, ypro in zip(polarisation, J, Xprofiles, Yprofiles):
#        plt.close()         
#        """ Taking line profiles through J, Xpro and Ypro """
#        jnumx = int(np.max(np.shape(j[:,0,0]))) # These are in pixels
#        jnumy = int(np.max(np.shape(j[0,:,0])))        
#        Xnumx = int(np.max(np.shape(xpro[:,0])))
#        Ynumy = int(np.max(np.shape(ypro[:,0])))
#
#        jmidX = int(jnumx/2)
#        jmidY = int(jnumy/2)
#        Xmid = int(Xnumx/2)
#        Ymid = int(Ynumy/2)
#
#        jX = j[:,jmidY]
#        jY = j[jmidX,:]
#        Ix = xpro[Xmid-jmidX:Xmid+jmidX]
#        Iy = ypro[Ymid-jmidY:Ymid+jmidY]
#
#        cX = jX/Ix
#        cY = jY/Iy
#        
#        plt.clf()
#        plt.close()
#        plt.plot(cX, label="horizontal")
#        plt.plot(cY, label="vertical")
#        plt.title("Coherence Profiles from J")
#        plt.legend()
#        print("Saving Coherence profile to: {}".format(pathJ + pol + '.png'))
#        plt.savefig(pathJ + pol + '.png')
#        plt.show()
#        plt.clf()
#        plt.close()
#        clX, clY = wfCoherence.getCoherenceLength(cH, cV, 0.01, pathCLj + P + '.png')
#        _clX = clX*resolutionX.mean()
#        _clY = clY*resolutionY.mean()
#        print("Horizontal Coherence Length [m]: {}".format(_clX))
#        print("Vertical Coherence Length [m]: {}".format(_clY))
#        jCLx.append(_clX)
#        jCLy.append(_clY)
#
#
#plt.clf()
#plt.close()
#plt.plot(polarisation, jCLx, label="horizontal")
#plt.plot(polarisation, jCLy, label="vertical")
#plt.title("Coherence Lengths from J")
#plt.legend()
#print("Saving coherence length plot to {}".format(pathJclp))
#plt.savefig(pathJclp)
#plt.show()
#
#
#
#
#""" Plotting Mutual Intensity Arrays and Polarisation """
#plt.clf()
#plt.close()
#for pol, jxx, jxy, jyx, jyy in zip(polarisation, Jxx, Jxy, Jyx, Jyy):
#        plt.close()
#        jmax = np.max([jxx,jxy,jyx,jyy])
#        jmin = np.min([jxx,jxy,jyx,jyy])
#        fig, axs = plt.subplots(2, 2)
#        im = axs[0, 0].imshow(jxx, vmin=jmin, vmax=jmax)
#        axs[0, 0].set_title('Jxx')
#        axs[0, 1].imshow(jxy, vmin=jmin, vmax=jmax)
#        axs[0, 1].set_title('Jxy')
#        axs[1, 0].imshow(jyx, vmin=jmin, vmax=jmax)
#        axs[1, 0].set_title('Jyx')
#        axs[1, 1].imshow(jyy, vmin=jmin, vmax=jmax)
#        axs[1, 1].set_title('Jyy')
#    
#        for ax in axs.flat:
#            ax.set(xlabel="Point Separation x-x' [pixels]", ylabel="Point Separation y-y'[pixels] ")
#        # Hide x labels and tick labels for top plots and y ticks for right plots.
#        for ax in axs.flat:
#            ax.label_outer()
#        fig.subplots_adjust(right=0.8)
#        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#        fig.colorbar(im, cax=cbar_ax)
#        print("Saving Mutual Intensity Plots to: {}".format(pathJP+pol+'.png'))
#        plt.savefig(pathJP+pol+'.png')
#        plt.show()
#        plt.clf()
#        
#plt.clf()
#plt.close()
#for pol, s0, s1, s2, s3 in zip(polarisation, S0, S1, S2, S3):
#        plt.close()
#        smin = np.min([s0,s1,s2,abs(s3)])
#        smax = np.max([s0,s1,s2,abs(s3)])
#        fig, axs = plt.subplots(2, 2)
#        im = axs[0, 0].imshow(s0, vmin=smin, vmax=smax)
#        axs[0, 0].set_title('S0')
#        axs[0, 1].imshow(s1, vmin=smin, vmax=smax)
#        axs[0, 1].set_title('S1')
#        axs[1, 0].imshow(s2, vmin=smin, vmax=smax)
#        axs[1, 0].set_title('S2')
#        axs[1, 1].imshow(abs(s3), vmin=smin, vmax=smax)
#        axs[1, 1].set_title('S3')
#
#        for ax in axs.flat:
#            ax.set(xlabel="x position [pixels]", ylabel="y position [pixels] ")
#        # Hide x labels and tick labels for top plots and y ticks for right plots.
#        for ax in axs.flat:
#            ax.label_outer()
#        fig.subplots_adjust(right=0.8)
#        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#        fig.colorbar(im, cax=cbar_ax)
#        print("Saving Stokes Plots to: {}".format(pathS+pol+'.png'))
#        plt.savefig(pathS+pol+'.png')
#        plt.show()
#        plt.clf()
#        
#        
#for sV, pol in zip(stokes, polarisation): 
#        plt.close()
#        print("-----Stokes Vector-----")
#        print(abs(sV))
#        
#        print("Polarisation: {}".format(pol))
#        
#
#for dP, pol in zip(P, polarisation):
#        print("Degree of Polarisation: {}".format(dP))
#        #plt.imshow(dP)
#        #plt.title("Degree of Polarisation")
#        #plt.colorbar()
#        #print("Saving degree of polarisation plot to: {}".format(pathDP+pol+'.png'))
#        #plt.savefig(pathDP+pol+'.png')
#        #plt.show()
#        #plt.clf()
#
#
#""" Plotting Intensity Profiles - Total Polarisation """
#plt.clf()
#plt.close()
#for xprof, yprof, p in zip(Xprofiles, Yprofiles, polarisation):
#        plt.plot(xprof, label=p + "horizontal cut")
#        plt.plot(yprof, label=p + "vertical cut")
#        plt.title("Intensity profiles (total P)")
#        plt.xlabel("Position [m]")
#        plt.ylabel("Intensity")
#print("Saving Intensity Profiles (tp) to {}".format(pathP))
#plt.legend()
#plt.savefig(pathP)
#plt.show()
#
#""" Plotting Intensity Profiles - Horizontal Polarisation """
#plt.clf()
#plt.close()
#for xprof, yprof, p in zip(XprofilesH, YprofilesH, polarisation):
#        plt.plot(xprof, label=p + "horizontal cut")
#        plt.plot(yprof, label=p + "vertical cut")
#        plt.title("Intensity profiles (horizontal P)")
#        plt.xlabel("Position [m]")
#        plt.ylabel("Intensity")
#print("Saving Intensity Profiles (hp) to {}".format(pathPh))
#plt.legend()
#plt.savefig(pathPh)
#plt.show()
#
#""" Plotting Intensity Profiles - Vertical Polarisation """
#plt.clf()
#plt.close()
#for xprof, yprof, p in zip(XprofilesV, YprofilesV, polarisation):
#        plt.plot(xprof, label=p + "horizontal cut")
#        plt.plot(yprof, label=p + "vertical cut")
#        plt.title("Intensity profiles (vertical P)")
#        plt.xlabel("Position [m]")
#        plt.ylabel("Intensity")
#print("Saving Horizontal Intensity Profiles (vp) to {}".format(pathPv))
#plt.legend()
#plt.savefig(pathPv)
#plt.show()
#
#
##for profile, mask in zip(Xprofiles, maskThickness):
##	
##	print(mask)
##	E0, E1, En1 = utilMask.getEfficiency(incidentI, exitI, profile, m=2, resIN = resolutionXIN, resEX = resolutionXEX, resPR = resolutionX[0], pathI=pathI )
##	e0.append(E0)
##	e1.append(E1)
##	en1.append(En1)
##	print(e0[-1])
#
##print("Shape of e0: {}".format(np.shape(e0)))
##print("Shape of e1: {}".format(np.shape(e1)))
##print("Shape of en1: {}".format(np.shape(en1)))
#
#
##plt.clf()
##plt.close()
##plt.plot(maskThickness, e0, label="m = 0")
##plt.plot(maskThickness, e1, label="m = +1")
##plt.plot(maskThickness, en1, label="m = -1")
##plt.xlabel("Mask Thickness [m]")
##plt.ylabel("Efficiency")
#plt.legend()
#print("Saving Intensity Plots to: {}".format(pathE))
#plt.savefig(pathE)
#plt.show()
	




