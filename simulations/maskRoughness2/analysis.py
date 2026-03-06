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

#import xl.runner as runner

dirPath = '/user/home/opt/xl/xl/experiments/maskRoughness2/data/'

batchOutputFile = dirPath + '10/results.pickle'

ran = [1,2]###,3]#,8,12,14]#range(1,5,1)

folders = [str(r) + '/' for r in ran]#['1/', '2/', '3/', '4/']
pickles = [str(r*10) + '.pkl' for r in ran]

fromPickles = True

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
    

#        
#results = pickle.load( open(batchOutputFile, 'rb')  )
Yprofiles = []

for i, t in enumerate(folders):
    plt.clf()
    plt.close()
    name = t[0:len(str(t))-1]
    print("Analysing trial: {}".format(name))
    if fromPickles == True:
        name = str(pickles[i])[0:len(str(pickles[i]))-4]      
        print("Loading pickled wavefield")
        with open(dirPath + t + str(pickles[i]), 'rb') as f:
            r = pickle.load(f)
##        nx = r['results']['params/Mesh/nx']
#        xMax = r['results']['params/Mesh/xMax']
#        xMin = r['results']['params/Mesh/xMin']
#        rx = np.subtract(xMax,xMin)
#        dx = np.divide(rx,nx)
#        # resolutionX.append(dx)
#        # nX.append(nx)
##        ny = r['results']['params/Mesh/ny']
#        yMax = r['results']['params/Mesh/yMax']
#        yMin = r['results']['params/Mesh/yMin']
#        ry = np.subtract(yMax,yMin)
#        dy = np.divide(ry,ny)   
#        # resolutionY.append(dy)
        # nY.append(ny)
    
#        print("(xMin,xMax) [m]: {}".format((xMin,xMax)))
#        print("x-Range [m]: {}".format(rx))
#        print("(yMin,yMax) [m]: {}".format((yMin,yMax)))
#        print("y-Range [m]: {}".format(ry))
#        print("Dimensions (Nx,Ny) [pixels]: {}".format((nx,ny)))
#        print("Resolution (dx,dy) [m]: {}".format((dx,dy)))
        print(r['results']['Intensity/Total/X/profile'])
        Ix = r['results']['Intensity/Total/X/profile']
        Iy = r['results']['Intensity/Total/Y/profile']
        IxH = r['results']['Intensity/Horizontal/X/profile']
        IyH = r['results']['Intensity/Horizontal/Y/profile']
        IxV = r['results']['Intensity/Vertical/X/profile']
        IyV = r['results']['Intensity/Vertical/Y/profile']
        print("HERE")
        Yprofiles.append(Iy)
mid = 13477
N = 100

for i,y in enumerate(Yprofiles):
    plt.plot(y, label=i)
#    plt.xlim(mid-N,mid+N)
    #plt.xlim(int(len(y)/8),int(len(y)/4))
plt.legend()
#plt.plot(np.squeeze(Yprofiles))
plt.show()

key = 'intensitySum'
values = listValues(results, key)
#==============================================================================
 
#print("-----RESULTS KEYS-----")
#print(resultsKeys(results))
#print("-----TRIALS-----")
#print(trials(results))
#print("-----PARAMETER KEYS-----")
#print(parameterKeys(results))
      
# 
# # plot(results,y='Intensity/Horizontal/Y/integratedOpticalDensity', x='op_Mask_Watchpoint_L')
# # plot(results,y='Intensity/Vertical/Y/integratedOpticalDensity', x='op_Mask_Watchpoint_L')
# # plot(results,y='Intensity/Total/Y/integratedOpticalDensity', x='op_Mask_Watchpoint_L')
# 
# 
# # plot(results,y='Intensity/Horizontal/Y/contrastMichelson', x='op_Mask_Watchpoint_L')
# # plot(results,y='Intensity/Vertical/Y/contrastMichelson', x='op_Mask_Watchpoint_L')
# # plot(results,y='Intensity/Total/Y/contrastMichelson', x='op_Mask_Watchpoint_L')
# 
# # # histograms
# # for h,b in  zip(listValues(results, 'Intensity/Total/Y/histogram'), listValues(results, 'Intensity/Total/Y/histogramBins')):
# #     plt.plot(b,h)
# # plt.show()
# 
# #number of pixels, range, resolution
# ny = listValues(results,'params/Mesh/ny')
# yMax = listValues(results,'params/Mesh/yMax')
# yMin = listValues(results, 'params/Mesh/yMin')
# resolutionY  = np.divide(np.subtract(yMax,yMin),ny)
# 
# y = listValues(results, 'y')
#  
# 
# #number of pixels, range, resolution
nx = listValues(results,'params/Mesh/nx')
xMax = listValues(results,'params/Mesh/xMax')
xMin = listValues(results, 'params/Mesh/xMin')
resolutionX  = np.divide(np.subtract(xMax,xMin),nx)
# 
# x = listValues(results, 'x')
# 
# 
# # plt.plot(ff[0],fa[0],'.')
# # plt.show()
# 
# # #intensity profiles
# # for v in listValues(results, 'Intensity/Total/Y/profile'):
# #     plt.plot(v,y)
# #     plt.title('Intensity (x=0)')
# # plt.show()
# 
# # #intensity profiles
# # for v in listValues(results, 'Intensity/Total/X/profile'):
# #     plt.plot(v,x)
# #     plt.title('Intensity (y=0)')
# # plt.show()
# 
# #print(" ")
# #print("Results Key")
# #print(resultsKeys(results))
# 
Yprofiles = listValues(results, 'Intensity/Total/Y/profile')
Xprofiles = listValues(results, 'Intensity/Total/X/profile')
YprofilesH = listValues(results, 'Intensity/Horizontal/Y/profile')
XprofilesH = listValues(results, 'Intensity/Horizontal/X/profile')
YprofilesV = listValues(results, 'Intensity/Vertical/Y/profile')
XprofilesV = listValues(results, 'Intensity/Vertical/X/profile')
# #maskThickness = listValues(results, 'op_Mask_thick')
# trials = trials(results)
# 
# #import utilMask
# 
# 
# #Efield = listValues(results, 'params/wEFieldUnit')
# #print(Efield)
# 
# pathPX = dirPath + 'ProfilesX.png'
# pathPY = dirPath + 'ProfilesY.png'
# pathPXh = dirPath + 'ProfilesX_hor.png'
# pathPYh = dirPath + 'ProfilesY_hor.png'
# pathPXv = dirPath + 'ProfilesX_ver.png'
# pathPYv = dirPath + 'ProfilesY_ver.png'
# 
# polarisation = ['Lin Hor','Lin Ver','Lin Diag','Cir Right','Cir Left']
# 
# e0 = []
# e1 = []
# en1 = []
 
""" Plotting Intensity Profiles - Total Polarisation """
plt.clf()
plt.close()
for profile in Xprofiles:
        plt.plot(profile)#, label=p)
        plt.title("horizontal intensity profiles (total P)")
        plt.xlabel("x [m]")
        plt.ylabel("Intensity")
#print("Saving Horizontal Intensity Profiles (tp) to {}".format(pathPX))
plt.legend()
# plt.savefig(pathPX)
plt.show()
 
plt.clf()
plt.close()
for profile in Yprofiles:
        plt.plot(profile)
        plt.title("vertical intensity profiles (total P)")
        plt.xlabel("y [m]")
        plt.ylabel("Intensity")
# print("Saving Vertical Intensity Profiles (tp) to {}".format(pathPY))
plt.legend()
# plt.savefig(pathPY)
plt.show()
 
# """ Plotting Intensity Profiles - Horizontal Polarisation """
# plt.clf()
# plt.close()
# for profile, p in zip(XprofilesH, polarisation):
#         plt.plot(profile, label=p)
#         plt.title("horizontal intensity profiles (horizontal P)")
#         plt.xlabel("x [m]")
#         plt.ylabel("Intensity")
# print("Saving Horizontal Intensity Profiles (hp) to {}".format(pathPXh))
# plt.legend()
# plt.savefig(pathPXh)
# plt.show()
# 
# plt.clf()
# plt.close()
# for profile, p in zip(YprofilesH,  polarisation):
#         plt.plot(profile, label=p)
#         plt.title("vertical intensity profiles (horizontal P)")
#         plt.xlabel("y [m]")
#         plt.ylabel("Intensity")
# print("Saving Vertical Intensity Profiles (hp) to {}".format(pathPYh))
# plt.legend()
# plt.savefig(pathPYh)
# plt.show()
# 
# """ Plotting Intensity Profiles - Vertical Polarisation """
# plt.clf()
# plt.close()
# for profile, p in zip(XprofilesV, polarisation):
#         plt.plot(profile, label=p)
#         plt.title("horizontal intensity profiles (vertical P)")
#         plt.xlabel("x [m]")
#         plt.ylabel("Intensity")
# print("Saving Horizontal Intensity Profiles (vp) to {}".format(pathPXv))
# plt.legend()
# plt.savefig(pathPXv)
# plt.show()
# 
# plt.clf()
# plt.close()
# for profile, p in zip(YprofilesV, polarisation):
#         plt.plot(profile, label=p)
#         plt.title("vertical intensity profiles (vertical P)")
#         plt.xlabel("y [m]")
#         plt.ylabel("Intensity")
# print("Saving Vertical Intensity Profiles (vp) to {}".format(pathPYv))
# plt.legend()
# plt.savefig(pathPYv)
# plt.show()
# 
# 
# #for profile, mask in zip(Xprofiles, maskThickness):
# #	
# #	print(mask)
# #	E0, E1, En1 = utilMask.getEfficiency(incidentI, exitI, profile, m=2, resIN = resolutionXIN, resEX = resolutionXEX, resPR = resolutionX[0], pathI=pathI )
# #	e0.append(E0)
# #	e1.append(E1)
# #	en1.append(En1)
# #	print(e0[-1])
# 
# #print("Shape of e0: {}".format(np.shape(e0)))
# #print("Shape of e1: {}".format(np.shape(e1)))
# #print("Shape of en1: {}".format(np.shape(en1)))
# 
# 
# #plt.clf()
# #plt.close()
# #plt.plot(maskThickness, e0, label="m = 0")
# #plt.plot(maskThickness, e1, label="m = +1")
# #plt.plot(maskThickness, en1, label="m = -1")
# #plt.xlabel("Mask Thickness [m]")
# #plt.ylabel("Efficiency")
# #plt.legend()
# #print("Saving Intensity Plots to: {}".format(pathE))
# #plt.savefig(pathE)
# #plt.show()
# 	
# 
 
 