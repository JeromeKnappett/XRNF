#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 15:24:08 2025

@author: jerome
"""

"""
The following functions are taken from the supporting information from
'Development of EUV interference lithography for 25 nm line/space patterns',
A.K Sahoo et al.

"""
#from __future__ import unicode_literals 
from matplotlib import rc
import numpy as np
import matplotlib.pyplot as plt

def difAngle(wl,p,m=1):
    theta = np.arcsin((m*wl)/p)
    return theta

def aerialImageI(E1a,E2a,E3a,E1p,E2p,k,theta,x,w,t):
    
    E1 = E1a * np.exp((1j * k * x * np.sin(theta)) - (w*t) - E1p)
    E2 = E2a * np.exp((-1j * k * x * np.sin(theta)) - (w*t) - E2p)
    
    E = E1 + E2 + E3a
    
    I = abs(E**2)
    
    plt.plot([a*1e6 for a in x],I)
    plt.xlabel('x [nm]')
    plt.ylabel('I [a.u]')
    plt.show()
    
    return I
#    print(I)
    
def aerialImageV(k,d,SLW,z):
    V = abs( (np.sin((k*d*SLW) / (2*z))) / ((k*d*SLW) / (2*z)) )
    
    return V
    
    
def testI():
    E1a = 1.0
    E2a = 1.0
    E3a = 0.01
    E1p = 0.0#np.pi
    E2p = 0.0
    wl = 6.7e-9
    k = (2*np.pi)/wl
    p=100.0e-9
    theta = difAngle(wl,p)
    w=1/wl
    t = 0.0
    
    x = np.linspace(-100e-6,100.0e-6,1000)
    
    I = aerialImageI(E1a,E2a,E3a,E1p,E2p,k,theta,x,w,t)
#    
    SLW1 = 50.0e-6
    SLW2 = 200.0e-6
    SLW3 = 300.0e-6
    d0 = 200.0e-6 
    dSLS = [75.0e-6,100.0e-6,150.0e-6,200.0e-6]
    #27.5e-6
    
    SLW = np.linspace(20e-6,1000e-6,1000)
    d = np.linspace(1.0e-6,400.0e-6,1000)#25.0e-6
    z = 9.5
    
    visSLW = aerialImageV(k,d0,SLW,z)
    visd1 = aerialImageV(k,d,SLW1,z)
    visd2 = aerialImageV(k,d,SLW2,z)
    visd3 = aerialImageV(k,d,SLW3,z)
    
    for ds in dSLS:
        vis = aerialImageV(k,ds,SLW,z)
        plt.plot([s*1e6 for s in SLW],vis, label='d = ' + str(ds*1e6) + ' um')
    plt.xlabel('$W_{SSA}$ [microns]')
    plt.ylabel('$C_M$')
    plt.legend()
    plt.show()   
    
#    plt.plot([s*1e6 for s in SLW],visSLW, label='d = ' + str(d0*1e6) + ' um')
#    plt.xlabel('Slit width [um]')
#    plt.ylabel('Aerial image visibility')
#    plt.legend()
#    plt.show()
    
    
    plt.plot([s*1e6 for s in d],visd1,label='$W_{SSA}$ = 50 $\mu$m',color='black')
    plt.plot([s*1e6 for s in d],visd2,label='$W_{SSA}$ = 200 $\mu$m',color='r')
    plt.plot([s*1e6 for s in d],visd3,label='$W_{SSA}$ = 300 $\mu$m',color='b')
    plt.plot([s*1e6 for s in d],aerialImageV(k,d,SLW1,6.5),'--',color='black')
    plt.plot([s*1e6 for s in d],aerialImageV(k,d,SLW2,6.5),'--',color='r')
    plt.plot([s*1e6 for s in d],aerialImageV(k,d,SLW3,6.5),'--',color='b')
    plt.xlabel('$d$ [microns]')
    plt.ylabel('$C_M$')
#    plt.text(0,0,'$z_0 = 9.5$ m',fontsize=12)
    plt.ylim(0,1.05)
    plt.xlim(0,400)
    plt.legend()
    plt.text(330,0.88,'$z_0 = 9.5$ m',fontsize=8,rotation=-7)
    plt.text(328,0.75,'$z_0 = 6.5$ m',fontsize=8,rotation=-14)
    plt.savefig('/home/jerome/Documents/PhD/Figures/ModelApplication/vis_vs_d_both.pdf',format='pdf')
    plt.show()
    
    
    
if __name__ == '__main__':
    testI()