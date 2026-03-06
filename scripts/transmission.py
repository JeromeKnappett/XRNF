#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 15:54:16 2023

@author: -
"""


import numpy as np
import matplotlib.pyplot as plt
import xraydb as xrdb

def transmission(wl,T,beta):
    k = (2*np.pi) / wl
    trans = np.exp((-2*k * beta * T)) # np.exp(((-k) / (beta * T)))
    return trans

def AofPeak(m,M,W):
    Hp = M-m
    A = 0.5*(W*Hp) + W*m
    return A

# %%
def WLtoE(wl):
    """ 
    takes wavelength in [m] and returns energy in [eV]
    """
    h = 4.135667696e-15
    c = 299792458
    E = (h*c)/wl
    return E

def transmittedContam(T,eta,n):
    Tc = T / (n*eta + T)
    return Tc

def testTrans():
    wl1 = 6.7e-9
    wl2 = 13.5e-9
    wl3 = 4.23156e-9
    Tsi = 40e-9 #33e-9 #40e-9
    Tta = 150e-9
    E1 = WLtoE(wl1)
    E2 = WLtoE(wl2)
    E3 = WLtoE(wl3)
    E = [E1,E2,E3]
    eta = 0.1
    
    materials = ['SiO2','Si3N4','Ta']
    
    D = [xrdb.get_material(m) for m in materials]
    print(D)
    # delta1,beta1,atlen1 = [xrdb.xray_delta_beta(m, d[1], WLtoE(wl1)) fpr m,d in zip(materials,D)]
    b1,b2,b3 = [],[],[]
    for i,m in enumerate(D):
        delta1,beta1,atlen1 = xrdb.xray_delta_beta(m[0],m[1],E[0])
        delta2,beta2,atlen2 = xrdb.xray_delta_beta(m[0],m[1],E[1])
        delta3,beta3,atlen3 = xrdb.xray_delta_beta(m[0],m[1],E[2])
        
        b1.append(beta1)
        b2.append(beta2)
        b3.append(beta3)
        
        
    # (d1,b1,atlen1) = [xrdb.xray_delta_beta(m,d[1],E[0]) for m,d in zip(materials,D)]
    # (d2,b2,atlen2) = [xrdb.xray_delta_beta(m,d[1],E[1]) for m,d in zip(materials,D)]
    # (d3,b3,atlen3) = [xrdb.xray_delta_beta(m,d[1],E[2]) for m,d in zip(materials,D)]
    
    # print(d2)
    # print(b2)
    print(b1)
    print(b2)
    print(b3)
    
    # betaSi02 = 5.30286832e-3
    # betaSi3N4 = 0.00913389772
    # betaTa = 1.939377e-2
    
    tB = [transmission(wl1,T,b) for T,b in zip([Tsi,Tsi,Tta],b1)]
    tE = [transmission(wl2,T,b) for T,b in zip([Tsi,Tsi,Tta],b2)]
    tS = [transmission(wl3,T,b) for T,b in zip([Tsi,Tsi,Tta],b3)]
    # tSi02_B = transmission(wl1,Tsi,b1[0])#betaSi02)
    # tSi02_B = transmission(wl1,Tsi,b1[1])
    # tSi02_B = transmission(wl1,Tsi,b1[2])
    # tSi3N4_B = transmission(wl1,Tsi,betaSi3N4)
    # tTa_B = transmission(wl1,Tta,betaTa)
    # tSi02_E = transmission(wl2,Tsi,betaSi02)
    # tSi3N4_E = transmission(wl2,Tsi,betaSi3N4)
    # tTa_E = transmission(wl2,Tta,betaTa)
    
    print(" ")
    print('------    6.7 nm      ------')
    print(f"Si02 transmission:         {tB[0]:.5}")
    print(f"Si3N4 transmission:        {tB[1]:.5}")
    print(f"Ta absorption:             {(1 - tB[2]):.5}")
    print(" ")
    print('------    13.5 nm     ------')
    print(f"Si02 transmission:         {tE[0]:.5}")
    print(f"Si3N4 transmission:        {tE[1]:.5}")
    print(f"Ta absorption:             {(1 - tE[2]):.5}")
    print(" ")
    print('------    4.23 nm     ------')
    print(f"Si02 transmission:         {tS[0]:.5}")
    print(f"Si3N4 transmission:        {tS[1]:.5}")
    print(f"Ta absorption:             {(1 - tS[2]):.5}")
    print(" ")
    # print(f"T_B / T_E  (SiO2):         {1/(tSi02_B/tSi02_E)}")
    # print(f"T_B / T_E  (Si3N4):        {1/(tSi3N4_B/tSi3N4_E)}")
    # print(f"T_B / T_E  (Ta):           {1/(tTa_B/tTa_E)}")
    
    TcB = transmittedContam(tB[2], eta, n=2)
    TcE = transmittedContam(tE[2], eta, n=2)
    TcS = transmittedContam(tS[2], eta, n=2)
    
    print('Transmitted contamination @...')
    print(f'6.7 nm:                     {TcB:.5}')
    print(f'13.5 nm:                    {TcE:.5}')
    print(f'4.23 nm:                    {TcS:.5}')
    # dT_Si02 = tSi02_B - tSi02_E
    # dT_Si3N4 = tSi3N4_B - tSi3N4_E
    
    # print(dT_Si02/tSi02_E *100)
    # print(dT_Si3N4/tSi3N4_E *100)
    
    
    
def testPeak():
    from usefulWavefield import intensity2power
    W = (50e-9)/(2.5e-9)
    m100 = 0.05e12*(2.5e-9 * 2.5e-9) / 1e6
    M100 = 0.2e12*(2.5e-9 * 2.5e-9) / 1e6
    m200 = 0.15e12*(2.5e-9 * 2.5e-9) / 1e6
    M200 = 0.8e12*(2.5e-9 * 2.5e-9) / 1e6
    m300 = 0.205e12*(2.5e-9 * 2.5e-9) / 1e6
    M300 = 1.5e12*(2.5e-9 * 2.5e-9) / 1e6
    
    m = 0.2e12*(2.5e-9 * 2.5e-9) / 1e6
    M = 1.0e12*(2.5e-9 * 2.5e-9) / 1e6
    
    Pm100 = intensity2power(m100, 184.76)/ (2.5e-9 * 2.5e-9)*10000
    PM100 = intensity2power(M100, 184.76)/ (2.5e-9 * 2.5e-9)*10000
    Pm200 = intensity2power(m200, 184.76)/ (2.5e-9 * 2.5e-9)*10000
    PM200 = intensity2power(M200, 184.76)/ (2.5e-9 * 2.5e-9)*10000
    Pm300 = intensity2power(m300, 184.76)/ (2.5e-9 * 2.5e-9)*10000
    PM300 = intensity2power(M300, 184.76)/ (2.5e-9 * 2.5e-9)*10000
    
    Pm = intensity2power(m, 184.76)/ (2.5e-9 * 2.5e-9)*10000
    PM = intensity2power(M, 184.76)/ (2.5e-9 * 2.5e-9)*10000
    
    print('P100um: ', PM100)
    print('P200um: ', PM200)
    print('P300um: ', PM300)
    
    A100 = AofPeak(Pm100,PM100,W)
    A200 = AofPeak(Pm200,PM200,W)
    A300 = AofPeak(Pm300,PM300,W)
    A = AofPeak(Pm, PM, W)
    
    print('A100um: ', A100*1e4)
    print('A200um: ', A200*1e3)
    print('A300um: ', A300*1e3)
    print('A: ', A)
    
    print(W)
    
def test():
    import xraydb
    pin = 'Pt'#'C8H8' 
    #'Ni'#'Pt'#'Pt' #'Pt'
    ch,d = xraydb.get_material(pin)
    E = 8340.0
    WL = 1.486627e-10
    T = np.linspace(1.0,60,28)
    
    (delta,beta,atlen) = xraydb.xray_delta_beta(pin,d,E)
    
    print('(delta, beta, at len): ', (delta,beta,atlen))
    
    trans = [transmission(WL,t*1e-6,beta) for t in T]
    
    plt.plot(T/8.02721,[t*1.0 for t in trans],'x')
    plt.xlabel('Distance from aperture edge [um]')
    plt.ylabel('Transmission')
    plt.title(pin + ' pinhole transmission @ 8340 eV')
    plt.yscale('log')
    plt.show()
    
    t1 = 1.1#5.0
    t2 = 15.24#2.6#12.
    tr1 = transmission(WL,t1*1e-6,beta)
    tr2 = transmission(WL,t2*1e-6,beta)
    
    
    print('Transmission at ', t1,' um:    ', tr1 )
    print('Transmission at ', t2,' um:    ', tr2 )
    
    
if __name__ == "__main__":
    # test()
    testTrans()
    # testPeak()