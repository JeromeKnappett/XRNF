#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 22 16:16:38 2025

@author: -
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np

nCM = 30
nME = 100

folder = 'data/atMask/'
#data/aerialImage/

filename ='/user/home/opt_cmd/xl/xl/experiments/coherentModeProp/' + folder + 'cm' + str(nCM) + '_me' + str(nME) + '/test_cmd_res_pr_ae.h5'
# '/user/home/opt_cmd/xl/xl/experiments/coherentModeTest/data/test_ch61/test_cmd_mi.h5'#test_cmd_res_pr_dcx.h5' #test_cmd_cm.h5' #test_cmd_res_pr.h5'

CM=0
DC=0
I=1

if "_cm_" in filename:
    CM = 1
elif "_res_pr_" in filename:
    if '_dc' in filename:
        DC = 1
    else:
        I = 1

with h5py.File(filename, "r") as f:
    # Print all root level object names (aka keys) 
    # these can be group or dataset names 
    print("Keys: %s" % f.keys())
    # get first object name/key; may or may NOT be a group
    a_group_key = list(f.keys())[0]

    # get the object type for a_group_key: usually group or dataset
    print(type(f[a_group_key])) 


        

    # If a_group_key is a group name, 
    # this gets the object names in the group and returns as a list
    data = f[a_group_key]

    print(np.shape(data))
    
    atr_keys = [k for k in list(f.attrs.keys())]
    print("Attributes: " )
    for a in atr_keys:
        print(f"{a}:    \n             {f.attrs[a]}")
    
    dx = (f.attrs['xFin'] - f.attrs['xStart']) / f.attrs['nx']
    dy = (f.attrs['yFin'] - f.attrs['yStart']) / f.attrs['ny']
    
    
    if I:
        data = np.reshape(data,(f.attrs['ny'],f.attrs['nx']))    
        # data.reshape(len(data)//2,len(data)//2)
        
        # plt.imshow(data,aspect='auto',extent=[f.attrs['yStart'],f.attrs['yFin'],f.attrs['xStart'],f.attrs['xFin']])
        # plt.xlabel('x [m]')
        # plt.ylabel('y [m]')
        # plt.colorbar(label='Intensity [ph/s/.1%bw/mm^2]')
        # plt.show()
        
        NX = 100
        
        plt.imshow(data[:,4000-NX:4000+NX],aspect='auto',extent=[f.attrs['yStart'],f.attrs['yFin'],-dx*NX,dx*NX])
        plt.title(str(nCM) + ' CMs, ' + str(nME) + ' MEs')
        plt.colorbar(label='Intensity [ph/s/0.1%bw/mm$^2$]')
        plt.show()
    
    elif DC:
        try:
            data = np.reshape(data,(f.attrs['ny'],f.attrs['ny']))   
        except:
            data = np.reshape(data,(f.attrs['nx'],f.attrs['nx']))   
        # data.reshape(len(data)//2,len(data)//2)
        
        fig, ax = plt.subplots(1,3)
        # ax[0].plot(data[:,int(np.sqrt(len(data)))//2])
        ax[0].plot(data[:,150])
        ax[0].set_xlabel('y-cut (x=0)')
        # ax[2].plot(data[int(np.sqrt(len(data)))//2,:])
        ax[2].plot(data[150,:])
        ax[2].set_xlabel('x-cut (y=0)')
        ax[1].imshow(data)
        # plt.colorbar()
        fig.title(str(nCM) + ' CMs, ' + str(nME) + ' MEs')
        fig.tight_layout()
        plt.show()

    elif CM:
        for e,d in enumerate(data):
            dr = d[::2]
            di = d[1::2]
            d = dr + 1j*di
            
            i = abs(d)**2
            p = np.angle(d)
            
            i = np.reshape(i,(int(np.sqrt(len(i))),int(np.sqrt(len(i)))))
            p = np.reshape(p,(int(np.sqrt(len(p))),int(np.sqrt(len(p)))))
            
            plt.imshow(i,extent=[f.attrs['yStart'],f.attrs['yFin'],f.attrs['xStart'],f.attrs['xFin']])
            # plt.imshow(np.log(i),extent=[f.attrs['yStart'],f.attrs['yFin'],f.attrs['xStart'],f.attrs['xFin']])
            plt.vlines(-2.0e-3,-1.5e-3,1.5e-3,linestyles=':')
            plt.vlines(2.0e-3,-1.5e-3,1.5e-3,linestyles=':')
            plt.hlines(-1.5e-3,-2.0e-3,2.0e-3,linestyles=':')
            plt.hlines(1.5e-3,-2.0e-3,2.0e-3,linestyles=':')
                       # int(f.attrs['nx'])//2 - (int(2.0e-3 / dx)),
                       # int(f.attrs['ny'])//2 - (int(1.5e-3 / dy)),
                       # int(f.attrs['ny'])//2 + (int(1.5e-3 / dy)))
            
            plt.colorbar()
            plt.title('CM: ' + str(e+1))
            plt.show()
            
            plt.imshow(p,extent=[f.attrs['yStart'],f.attrs['yFin'],f.attrs['xStart'],f.attrs['xFin']])
            plt.colorbar()
            plt.show()
            # plt.plot(d[0:10000])
            # plt.plot(d[10000:2])
            # plt.show()
            # print(np.min(d[::2]))
            # print(np.min(d[1::2]))
            
    # If a_group_key is a dataset name, 
    # this gets the dataset values and returns as a list
    data = list(f[a_group_key])
    # preferred methods to get dataset values:
    ds_obj = f[a_group_key]      # returns as a h5py dataset object
    ds_arr = f[a_group_key][()]  # returns as a numpy array
