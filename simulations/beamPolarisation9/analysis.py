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
#import xl.runner as runner


import srwl_bl as srwl_bl
from srwlib import SRWLWfr, srwl_wfr_prop_drifts
from xl.srwl_blx import *
from wpg.wavefront import Wavefront

from matplotlib.pyplot import figure

# %%
def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x



dirPath = '/user/home/opt/xl/xl/experiments/beamPolarisation9/data/'
folders = ['LH/', 'LV/', 'L45/', 'L135/', 'CR/', 'CL/']
pickles = ['exlh.pkl', 'exlv.pkl', 'ex45.pkl', 'ex135.pkl', 'excr.pkl', 'excl.pkl']

batchOutputFile = dirPath + 'CL/results.pickle'

import h5py

# Propagation Parameters for prop_drifts
# S = Sampled area
# R = Resolution
                       #Sx,  Rx,  Sy,  Ry                                
pp = [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# Number of propagation steps and step size
nz = 250
dz = 1.e-6

for n, pk in zip(folders, pickles):
    
    """ METHOD #1 """
    
    wfr_file = dirPath + n + 'wf_final.hdf'
    print(" ")
    print('-----Loading wavefront from file {} -----'.format(wfr_file) )
    w = Wavefront()
    w.load_hdf5(wfr_file)
    
    I = w.get_intensity()
    plt.clf()
    plt.close()
    plt.imshow(I[:,:,0])
    plt.title("Intensity (wavefront())- loaded from hdf5 #1")
    plt.savefig(dirPath + 'plots/' + pk[0:len(str(pk))-4] + 'intensity.png')
    plt.show()
    plt.clf()
    plt.close()
        
    P = w.get_phase()
    plt.imshow(P[:,:,0])
    plt.title("Phase (wavefront()) - loaded from hdf5 #1")
    plt.savefig(dirPath + 'plots/' + pk[0:len(str(pk))-4] + 'phase.png')
    plt.show()
    plt.clf()
    plt.close()
    
    nx = w.params.Mesh.nx
    ny = w.params.Mesh.ny
    zMin = w.params.Mesh.zCoord
    eMin = w.params.photonEnergy #Initial Photon Energy [eV]
    xMin = w.params.Mesh.xMin #Initial Horizontal Position [m]
    xMax = w.params.Mesh.xMax #Final Horizontal Position [m]
    yMin = w.params.Mesh.yMin #Initial Vertical Position [m]
    yMax = w.params.Mesh.yMax #Final Vertical Position [m]
    Eh = w._srwl_wf.arEx
    Ev = w._srwl_wf.arEy
    
    plt.plot(Eh)
    plt.title("E-field (horizontal) #1")
    plt.show()
    plt.savefig(dirPath + 'plots/' + pk[0:len(str(pk))-4] + 'Ehor.png')
    plt.clf()
    plt.close()
    
    plt.plot(Ev)
    plt.title("E-field (vertical) #1")
    plt.show()
    plt.savefig(dirPath + 'plots/' + pk[0:len(str(pk))-4] + 'Ever.png')
    plt.clf()
    plt.close()    
    
    wf = SRWLWfr() #Initial Electric Field Wavefront    
    
    wf.allocate(1, nx, ny) #Numbers of points vs Photon Energy (1), Horizontal and Vertical Positions (dummy)
    wf.mesh.zStart = zMin #Longitudinal Position [m] at which Electric Field has to be calculated, i.e. the position of the first optical element
    wf.mesh.eStart = eMin #Initial Photon Energy [eV]
    wf.mesh.eFin = eMin #Final Photon Energy [eV]
    wf.mesh.xStart = xMin #Initial Horizontal Position [m]
    wf.mesh.xFin = xMax #Final Horizontal Position [m]
    wf.mesh.yStart = yMin #Initial Vertical Position [m]
    wf.mesh.yFin = yMax #Final Vertical Position [m]
    wf.arEx = Eh
    wf.arEy = Ev
    wf.mesh.ne = 1
    # wf.presFT = 0
    
    wD = srwl_wfr_prop_drifts(_wfr=wf, _dz=dz, _nz=nz, _pp=pp, _do3d=False, _nx=nx, _ny=ny, _pol=0, _type=0)
    
    propPath = dirPath +  pk[0:len(str(pk))-4] + 'prop.pkl'
            
    with open(propPath, "wb") as g:
        pickle.dump(wD, g)
    print("Propagation array written to: {}".format(propPath))

    Izx = np.reshape(wD[0], (nx,nz+1))
    
    plt.clf()
    plt.close()  
    figure(figsize=(8, 8), dpi=80)
    plt.imshow(Izx, aspect='auto')
    plt.savefig(dirPath + 'plots/' + pk[0:len(str(pk))-4] + 'propPlotX.png')
    plt.show()
    
    Izy = np.reshape(wD[1], (ny,nz+1))
    
    plt.clf()
    plt.close()
    figure(figsize=(8, 8), dpi=80)
    plt.imshow(Izy, aspect='auto')
    plt.savefig(dirPath + 'plots/' + pk[0:len(str(pk))-4] + 'propPlotY.png')
    plt.show()

    plt.clf()
    plt.close()
    plt.plot(wD[0])
    plt.title("x-intensity vs z, P: " + pk[0:len(str(pk))-4])
    print("Saving x-intensity vs z plot...")
    plt.savefig(dirPath + "plots/" + pk[0:len(str(pk))-4] + "XvsZ.png")
    plt.show()
    
    plt.clf()
    plt.close()
    figure(figsize=(8, 8), dpi=80)
    plt.plot(wD[1])
    plt.title("y-intensity vs z, P: " + pk[0:len(str(pk))-4])
    print("Saving y-intensity vs z plot...")
    plt.savefig(dirPath + "plots/" + pk[0:len(str(pk))-4] + "XvsZ.png")
    plt.show()
    
    plt.clf()
    plt.close()
    figure(figsize=(8, 8), dpi=80)
    plt.plot(wD[4])
    plt.title("y-intensity vs z, P: " + pk[0:len(str(pk))-4])
    print("Saving y-intensity vs z plot...")
    plt.savefig(dirPath + "plots/" + pk[0:len(str(pk))-4] + "XvsZ.png")
    plt.show()
    
    plt.clf()
    plt.close()
    figure(figsize=(8, 8), dpi=80)
    plt.plot(wD[5])
    plt.title("y-intensity vs z, P: " + pk[0:len(str(pk))-4])
    print("Saving y-intensity vs z plot...")
    plt.savefig(dirPath + "plots/" + pk[0:len(str(pk))-4] + "XvsZ.png")
    plt.show()

    
    """ METHOD #2 """
    
#     #f = h5py.File(wfr_file, 'r')
    
#     # with h5py.File(wfr_file, "r") as f:
#     # List all groups
#     print("Keys: %s" % f.keys())
#     data_key = list(f.keys())[0]
#     params_key = list(f.keys())[1]
#     mesh_key = list(f.keys())[1][0]
#     version_key = list(f.keys())[2]
    

#     # Get the data
#     data = list(f[data_key])
#     params = list(f[params_key])
# #    mesh = list(f[mesh_key])
# #    version = list(f[version_key])
    
# #    wf = f['data']
# #    
# #    print(wf)
# #    
#     Eh = np.array(f['data']['arrEhor'], dtype=float)
#     Ev = np.array(f['data']['arrEver'], dtype=float)
# #    
# #    E = np.array(Eh) + np.array(Ev)
    
#     print("Data keys: {}".format(data))
#     print("Params keys: {}".format(params))
# #    print("Mesh keys: {}".format(mesh))
# #    
#     Rx = np.array(f['params']['Rx'])
#     dRx = np.array(f['params']['dRx'])
#     Nx = Rx/dRx
#     nx = int(np.array(f['params']['Mesh']['nx']))
#     ny = int(np.array(f['params']['Mesh']['ny']))
#     mesh = list(f['params']['Mesh'])
#     ne = np.array(f['params']['Mesh']['nSlices'])
#     energy = np.array(f['params']['photonEnergy'])
#     xMin = np.array(f['params']['Mesh']['xMin'])
#     xMax = np.array(f['params']['Mesh']['xMax'])
#     yMin = np.array(f['params']['Mesh']['yMin'])
#     yMax = np.array(f['params']['Mesh']['yMax'])
#     zCoord = np.array(f['params']['Mesh']['zCoord'])
    
#     print("Rx: {}".format(Rx))
#     print("dRx: {}".format(dRx))
#     print("Nx: {}".format(Nx))
#     print("3150/21: {}".format(3150/21))
#     print("nx: {}".format(nx))
#     print("Mesh: {}".format(mesh))
    
#     #w = SRWLWfr(_arEx=Eh, _arEy=Ev, _eStart=energy, _eFin=energy, _ne=ne, _xStart=xMin, _xFin=xMax, _nx=nx,
#     #            _yStart=yMin, _yFin=yMax, _ny=ny, _zStart=zCoord)
    
#     wfr = SRWLWfr() #, _eStart=energy, _eFin=energy, _ne=ne, _xStart=xMin, _xFin=xMax, _nx=nx,
#             #_yStart=yMin, _yFin=yMax, _ny=ny, _zStart=zCoord)
#     wfr.allocate(ne, nx, ny) #Numbers of points vs Photon Energy (1), Horizontal and Vertical Positions (dummy)
#     wfr.mesh.zStart = zCoord #Longitudinal Position [m] at which Electric Field has to be calculated, i.e. the position of the first optical element
#     wfr.mesh.eStart = energy #Initial Photon Energy [eV]
#     wfr.mesh.eFin = energy  #Final Photon Energy [eV]
#     wfr.mesh.xStart = xMin #Initial Horizontal Position [m]
#     wfr.mesh.xFin = xMax #Final Horizontal Position [m]
#     wfr.mesh.yStart = yMin #Initial Vertical Position [m]
#     wfr.mesh.yFin = yMax #Final Vertical Position [m]
#     wfr.arEx = Eh.flatten()
#     wfr.arEy = Ev.flatten()
#     wfr.mesh.ne = 1
    
#     #wf = Wavefront(srwl_wavefront=w)

# ##    print("Version keys: {}".format(version))
# #    
# #    w = Wavefront(np.array(wf))
# ##    w.load_hdf5(wfr_file)
# #

#     #wf = Wavefront(srwl_wavefront=wfr)
#     #    print(wf.srw_info())


#     #phase = wf.get_phase()
#     #intensity = wf.get_intensity()

# #    plt.imshow(intensity)
# #    plt.title("intensity")
# #    plt.savefig(dirPath + 'plots/' + pk[0:len(str(pk))-3] + 'intensity.png')
# #    plt.show()
# #    plt.imshow(phase)
# #    plt.title("phase")
# #    plt.savefig(dirPath + 'plots/' + pk[0:len(str(pk))-3] + 'phase.png')
# #    plt.show()

#     nz = 2
#     print("----- Number of Trials: {} -----".format(nz))
#     #print("Starting trial #{}".format(i+1))

#     wD = srwl_wfr_prop_drifts(_wfr=wfr, _dz=10e-6, _nz=nz, _pp=pp, _do3d=False, _nx=nx, _ny=ny, _pol=0, _type=0)   # wD = [resIntVsZX, resIntVsZY, resIntVsZXY, resMesh, resFWHMxVsZ, resFWHMyVsZ]


#     #wD = srwl_wfr_prop_drifts(_wfr=w, _dz=1e-6, _nz=149, _pp=pp)
    
#     print("shape of wD: {}".format(np.shape(wD)))
#     print("wD[0]: {}".format(np.shape(wD[0])))
#     print("wD[1]: {}".format(np.shape(wD[1])))
#     print("wD[2]: {}".format(np.shape(wD[2])))
#     print("wD[3]: {}".format(np.shape(wD[3])))
#     print("wD[4]: {}".format(np.shape(wD[4])))
#     print("wD[5]: {}".format(np.shape(wD[5])))
    
#     Iz = np.reshape(wD[0], (nx,nz+1))
    
#     #pk[0:len(str(pk))-3]
    
#     plt.clf()
#     plt.close()  
#     figure(figsize=(8, 8), dpi=80)
#     plt.imshow(Iz, aspect='auto')
#     plt.savefig(dirPath + 'plots/' + pk[0:len(str(pk))-3] + 'propPlotX.png')
#     plt.show()
    
#     Izy = np.reshape(wD[1], (nx,nz+1))
    
#     plt.clf()
#     plt.close()
#     figure(figsize=(8, 8), dpi=80)
#     plt.imshow(Izy, aspect='auto')
#     plt.savefig(dirPath + 'plots/' + pk[0:len(str(pk))-3] + 'propPlotY.png')
#     plt.show()

#     plt.clf()
#     plt.close()
#     plt.plot(wD[0])
#     plt.title("x-intensity vs z, P: " + pk[0:len(str(pk))-3])
#     print("Saving x-intensity vs z plot...")
#     plt.savefig(dirPath + "plots/" + pk[0:len(str(pk))-3] + "XvsZ.png")
#     plt.show()
    
#     plt.clf()
#     plt.close()
#     figure(figsize=(8, 8), dpi=80)
#     plt.plot(wD[1])
#     plt.title("y-intensity vs z, P: " + pk[0:len(str(pk))-3])
#     print("Saving y-intensity vs z plot...")
#     plt.savefig(dirPath + "plots/" + pk[0:len(str(pk))-3] + "XvsZ.png")
#     plt.show()
    
#     plt.clf()
#     plt.close()
#     figure(figsize=(8, 8), dpi=80)
#     plt.plot(wD[4])
#     plt.title("y-intensity vs z, P: " + pk[0:len(str(pk))-3])
#     print("Saving y-intensity vs z plot...")
#     plt.savefig(dirPath + "plots/" + pk[0:len(str(pk))-3] + "XvsZ.png")
#     plt.show()
    
#     plt.clf()
#     plt.close()
#     figure(figsize=(8, 8), dpi=80)
#     plt.plot(wD[5])
#     plt.title("y-intensity vs z, P: " + pk[0:len(str(pk))-3])
#     print("Saving y-intensity vs z plot...")
#     plt.savefig(dirPath + "plots/" + pk[0:len(str(pk))-3] + "XvsZ.png")
#     plt.show()
    
        
        
    
    
    
        


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
ny = listValues(results,'params/Mesh/ny')
yMax = listValues(results,'params/Mesh/yMax')
yMin = listValues(results, 'params/Mesh/yMin')
resolutionY  = np.divide(np.subtract(yMax,yMin),ny)

y = listValues(results, 'y')
 

#number of pixels, range, resolution
nx = listValues(results,'params/Mesh/nx')
xMax = listValues(results,'params/Mesh/xMax')
xMin = listValues(results, 'params/Mesh/xMin')
resolutionX  = np.divide(np.subtract(xMax,xMin),nx)

x = listValues(results, 'x')


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

Yprofiles = listValues(results, 'Intensity/Total/Y/profile')
Xprofiles = listValues(results, 'Intensity/Total/X/profile')
YprofilesH = listValues(results, 'Intensity/Horizontal/Y/profile')
XprofilesH = listValues(results, 'Intensity/Horizontal/X/profile')
YprofilesV = listValues(results, 'Intensity/Vertical/Y/profile')
XprofilesV = listValues(results, 'Intensity/Vertical/X/profile')
#maskThickness = listValues(results, 'op_Mask_thick')
trials = trials(results)
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


