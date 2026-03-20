#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 12:32:42 2025

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle
import tifffile



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

def wl(E):
        #return wavelength for energy E in keV
        return  12.39e-10/E

def harmonicContam(T,eta,n):
    hc = T / (n*eta + T)
    return hc

def opticalAxisIntercept(d, l, offset, theta=0, m = 1):
    """ return distance from grating plan at which m= 1 order intercepts optical axis
    when grating is displaced by 'offset' from optical axis."""
    
    #tan theta = d / offset   CHECK THIS  46r
    #return offset*np.tan(diffractionAngle(d,l,theta,m))
    return offset / (2*np.tan(diffractionAngle(d,l,theta,m)))


def diffractionAngle(wl, p, phi=0, m = 1):
    # Use grating equation to determine diffraction angle  
    # (m = order; l = lambda, wavelength; d = spacing)
    theta = np.arcsin(np.sin(phi) + m*wl/p)
    return theta

def michelsonContrast(A):
    
    C = (np.max(A) - np.min(A)) / (np.max(A) + np.min(A)) 
    return C

def analyticalAE(x,A1,A2,AT,pT,wT,k,theta,z,R):
    # a = k*x*np.sin(theta)
    # b = z + ((x**2)/(2*R))
    # c = -pT - ((x**2)/(wT**2))
    
    I = (A1**2 + A2**2 + (AT**2)*np.exp(2*(-pT - ((x**2)/(wT**2)))) + 
         2*A1*A2*np.cos(2*(k*x*np.sin(theta))) + 
         2*A1*AT*np.exp((-pT - ((x**2)/(wT**2))))*np.cos((k*x*np.sin(theta))+(z + ((x**2)/(2*R)))) + 
         2*A2*AT*np.exp*((-pT - ((x**2)/(wT**2))))*np.sin((k*x*np.sin(theta))+(z + ((x**2)/(2*R)))))
    
    return I

def aerialImageI(E1a,E2a,E1p,E2p,E3,k,theta,x,w,t,show=True,coherent=True):
    
    E1 = E1a * np.exp((1j * k * x * np.sin(theta)) - (w*t) - E1p)
    E2 = E2a * np.exp((-1j * k * x * np.sin(theta)) - (w*t) - E2p)
    
    # E3 = E3a * np.exp((1j * k * x) - (w*t) - E3p)
    if coherent:
        E = E1 + E2 + E3
        
        I = abs(E)**2
    else:
        I = abs(E1 + E2)**2 + abs(E3)**2
    
    if show:
        # plt.plot([a*1e6 for a in x],I)
        plt.plot([a*1e9 for a in x],abs(E3)**2)
        plt.plot([a*1e9 for a in x],np.angle(E3)/np.pi)
        plt.xlabel('x [nm]')
        plt.ylabel('I [a.u]')
        # plt.ylim(0,1)
        plt.show()
    
    return I
#    print(I)

def aerialImageITE(E1a,E2a,E3,E1p,E2p,k,theta,x,z,show=True):
    
    E1 = E1a * np.exp(1j * ((k * x * np.sin(theta)) - (k * z * np.cos(theta))) - E1p)
    E2 = E2a * np.exp(1j * ((-k * x * np.sin(theta)) - (k * z * np.cos(theta))) - E2p)
    
    
    E = E1 + E2 + E3
    
    I = abs(E)**2
    
    if show:
        # plt.plot([a*1e6 for a in x],I)
        plt.plot([a*1e9 for a in x],abs(E3)**2)
        plt.plot([a*1e9 for a in x],np.angle(E3)/np.pi)
        plt.xlabel('x [nm]')
        plt.ylabel('I [a.u]')
        # plt.ylim(0,1)
        plt.show()
    
    return I
    
def aerialImageV(k,d,SLW,z):
    V = abs( (np.sin((k*d*SLW) / (2*z))) / ((k*d*SLW) / (2*z)) ) 
    return V    

def aerialImageDistance(d,p,m,wl):
    z = (d*np.sqrt((p**2) - ((m**2)*(wl**2))))/(2*m*wl)
    return z

def testI():
    c = 299792458
    
    E10 = 0.50    # E10 + E20 = 1.0
    E20 = 0.50 
    
    E30 = [harmonicContam(t, eta, 2) for t,eta in zip([5.55895E-04,9.93627E-02],[0.06,0.06])]
    # E30 = [harmonicContam(t, 0.06, 2) for t in [5.55895E-04,9.93627E-02]]
    # [0.0744,0.2711]#[0.0,0.19,0.30]#0.50,0.8]#[0.01,0.02,0.05,0.1]#,0.15] #np.linspace(0.005,0.1,500)#0.05 #0.83 #75/100 # value of transmission through mask in Masters thesis
    E1p = 0 * 1/2 * np.pi
    E2p = 0*np.pi
    E3p = 0.8*np.pi
    wl = 6.7e-9 # 13.5e-9 #6.7e-9
    k = (2*np.pi)/wl
    p = 200.0e-9
    theta = diffractionAngle(wl,p)
    w=c*k#1/wl
    
    Show = False
    
    xR = 0.300e-6
    xN = 5000
    
    x = np.linspace(-xR/2,xR/2,xN)
    
    z = aerialImageDistance(100e-6, p=p, m=1, wl=wl)
    #1.5e-12 
    # range(0,10)
    # 0#1.0*1e-6
    
    t =  0*z/c
    # [(Z*1e-1)/c for Z in z]
    # z/c #1.0e-9
    
    # Wo = 10.0e-6
    Wz = 10.0e-3   #beam size at z (1/e^2)
    R = 25.0         #radius of curvature
    Z = 9.5          #propagation distance from waist
    
    
    # E3 = E3a * np.exp((-1j * k * x) - E3p)
    # E3 = E3a * np.exp(-1j * ((k*Z) + (k * ((x**2)/(2*R))) - E3p))

    Ca, Cb = [],[]
    MA, MB = [],[]
    E3_array = []
    for e in range(0,len(E30)):#range(0,500):
        
        ratio_sum = E10 + E20
        E1a = E10 / ratio_sum * (1 - E30[e])
        E2a = E20 / ratio_sum * (1 - E30[e])
        E3a = E30[e]
        print(f"E3a: {E3a}")

        E3 = E3a * np.exp((-(x**2))/((Wz**2))) * np.exp(-1j * ((k*Z) + (k * ((x**2)/(2*R))) - E3p))
    
        Ia = aerialImageI(E1a,E2a,E1p,E2p,E3,k,theta,x,w,t,show=Show)
        Ib = aerialImageITE(E1a, E2a, E3, E1p, E2p, k, theta, x, z,show=Show)
        # 
        # print(np.shape(Ia))
        
        ma = Ia[np.shape(Ia)[0]//2]
        mb = Ib[np.shape(Ib)[0]//2]
        # print(ma)
        # print(mb)
        
        CMa = (ma - np.min(Ia)) / (ma + np.min(Ia))# (np.max(Ia) - np.min(Ia)) / (np.max(Ia) + np.min(Ia))
        CMb = (mb - np.min(Ib)) / (mb + np.min(Ib)) # (np.max(Ib) - np.min(Ib)) / (np.max(Ib) + np.min(Ib))
        
        # print('contrast (sahoo):    ',   CMa)
        # print('contrast (wang):    ',    CMb)
        Ca.append(CMa)
        Cb.append(CMb)
        MA.append(ma)
        MB.append(mb)
        E3_array.append(E3)
    
    # print('E3: ', E3)
    plt.plot(E30,Ca, label='sahoo')
    plt.plot(E30,Cb, label='wang')
    plt.ylabel('Aerial image contrast')
    plt.xlabel('% contamination from transmitted beam')
    plt.legend()
    plt.show()
        
    plt.plot(E30,MA, label='sahoo')
    plt.plot(E30,MB, label='wang')
    plt.ylabel('Peak intensity height ratio')
    plt.xlabel('% contamination from transmitted beam')
    plt.legend()
    plt.show()
            
    # ------    6.7 nm      ------
    # Si02 transmission:         0.68486
    # Si3N4 transmission:        0.53235
    # Ta absorption:             0.99941
     
    # ------    13.5 nm     ------
    # Si02 transmission:         0.73232
    # Si3N4 transmission:        0.76718
    # Ta absorption:             0.99814
     
    # ------    4.23 nm     ------
    # Si02 transmission:         0.86455
    # Si3N4 transmission:        0.78203
    # Ta absorption:             0.99648
 
    # T_B / T_E  (SiO2):         1.2218820140251576
    # T_B / T_E  (Si3N4):        1.412222456503743
    # T_B / T_E  (Ta):           6.247604907357123
    
    
    
    Ia = aerialImageI(E1a,E2a,E1p,E2p,E3,k,theta,x,w,t,show=Show)
    Ib = aerialImageITE(E1a, E2a, E3, E1p, E2p, k, theta, x, z,show=Show)
    # 
    # print(np.shape(Ia))
    
    ma = Ia[np.shape(Ia)[0]//2]
    mb = Ia[np.shape(Ib)[0]//2]
    print(ma)
    print(mb)
    
    CMa = (ma - np.min(Ia)) / (ma + np.min(Ia))# (np.max(Ia) - np.min(Ia)) / (np.max(Ia) + np.min(Ia))
    CMb = (mb - np.min(Ib)) / (mb + np.min(Ib)) # (np.max(Ib) - np.min(Ib)) / (np.max(Ib) + np.min(Ib))
    
    print('contrast (sahoo):    ',   CMa)
    print('contrast (wang):    ',    CMb)
    dirPath = '/user/home/opt_old/xl/xl/experiments/BEUVcoherence/data/50um_50SSA/50um_50SSA.pkl'
    # '/user/home/opt_old/xl/xl/experiments/correctedAngle_roughness/data/ideal/ideal.pkl'#idealintensity.tif'

    pick = pickle.load(open(dirPath, 'rb'))
    I = pick[0]
    res = (pick[1],pick[2])

    N = 1200                            # number of pixels to take for line profile  - 1200 for roughness aerial images
    n = 16                             # number of pixels to average over for line profile - 15 for roughness aerial images
    plotRange = 1000                       # range of aerial image plot in nm

    # res and middle pixels of images

    # res = [2.5011882651601634e-09, 2.426754806976689e-07]
    mid = np.shape(I)[0]//2, np.shape(I)[1]//2 - 93 #[196, 12188]
    ran_pix = int((xR*1e-3)/res[0])

    pitch = 25e-9

    numlines = 40 #int(Y//hp-2)# 125
    shiftY = 2
    extraY = 3

    pitch = pitch / res[0] #pixels
    hp = pitch/2

    print('Half pitch (pixels):   ', hp )
    print('Range of pixels for simulation: ', ran_pix)
    print(mid[0])

    # I = tifffile.imread(dirPath)
    # print(np.shape(I))

    I = I[mid[0]-n:mid[0]+n,mid[1]-(ran_pix//2):mid[1]+(ran_pix//2)+1]
    I=I.mean(0)
    xi = np.linspace(-xR/2,xR/2, ran_pix)
    
    plt.plot([a*1e9 for a in x],Ia,'--',label='Sahoo')
    plt.plot([a*1e9 for a in x],Ib,'--',label='Wang')
    # plt.plot([a*1e6 for a in xi],I/np.max(I),'-',label='simulated',alpha=0.5)
    # plt.vlines(0, 0, 1)
    plt.xlabel('x [nm]')
    plt.ylabel('I [a.u]')
    # plt.ylim(0,1)
    plt.legend()
    plt.show()
    
    
    I_array = [aerialImageI(E1a,E2a,E1p,E2p,_e,k,theta,x,w,t,show=Show,coherent=False) for _e in E3_array]
    
    CM = [(np.max(i) - np.min(i)) / (np.max(i) + np.min(i)) for i in I_array] 
    
    labels = [str(i*100) + '%' for i in E30]
    # ['28%', '30%', '32%']
    # ['1%', '2%', '5%', '10%']#,'15%']
    colours = ['black','r','b','g']#,'y']
    for e,i in enumerate(I_array):
        plt.plot([a*1e9 for a in x], i, '--', color=colours[e], label=labels[e])
    plt.xlabel('$x$ [nm]')
    plt.ylabel('$I$ [a.u]')
    plt.legend(title='$\zeta_{T}=$')
    plt.title('Incoherent Interference')
    # plt.savefig('/user/home/opt_old/xl/xl/experiments/BEUVcoherence/plots/analytical.svg')
    plt.show()
    
    print(f"Incoherent contrasts: {CM}")
    
    I_array = [aerialImageI(E1a,E2a,E1p,E2p,_e,k,theta,x,w,t,show=Show,coherent=True) for _e in E3_array]
    
        
    CM = [(np.max(i) - np.min(i)) / (np.max(i) + np.min(i)) for i in I_array] 
    
    labels = [str(i*100) + '%' for i in E30]
    # ['28%', '30%', '32%']
    # ['1%', '2%', '5%', '10%']#,'15%']
    colours = ['black','r','b','g']#,'y']
    for e,i in enumerate(I_array):
        plt.plot([a*1e9 for a in x], i, '--', color=colours[e], label=labels[e])
    plt.xlabel('$x$ [nm]')
    plt.ylabel('$I$ [a.u]')
    plt.legend(title='$\zeta_{T}=$')
    plt.title('Coherent Interference')
    # plt.savefig('/user/home/opt_old/xl/xl/experiments/BEUVcoherence/plots/analytical.svg')
    plt.show()
    
    print(f"Coherent contrasts: {CM}")
    
    # Iarray = []
    
    # for T in t:
    #     I = aerialImageI(E1a,E2a,E30,E1p,E2p,k,theta,x,w,T)
    #     Iarray.append(I)
    
    # print(np.shape(Iarray))
    # I = np.mean(Iarray,axis=0)
    # print(np.shape(I))

    # plt.plot([a*1e6 for a in x],I)
    # plt.xlabel('x [nm]')
    # plt.ylabel('I [a.u]')
    # plt.ylim(0,1)
    # plt.show()

def testVisibilityTran():
    E1a = 0.45
    E2a = 0.55
    E3a = 0.075/100 # value of transmission through mask in Masters thesis
    E1p = 0*np.pi
    E2p = 0*np.pi
    wl = 6.7e-9
    k = (2*np.pi)/wl
    p=50.0e-9
    theta = diffractionAngle(wl,p)
    w=1/wl
    t = 0#1.0e-9
    
    x = np.linspace(-100e-6,100.0e-6,1000)
    
    I = aerialImageI(E1a,E2a,E3a,E1p,E2p,k,theta,x,w,t)
    
def testVisibilitySSA():
    wl = 6.7e-9
    k = (2*np.pi)/wl
    
    
    SLW1 = 50.0e-6
    SLW2 = 350.0e-6
    d0 = 27.5e-6
    
    SLW = np.linspace(20e-6,2000e-6,1000)
    d = np.linspace(10.0e-6,300.0e-6,1000)#25.0e-6
    z = 9.5
    
    visSLW = aerialImageV(k,d0,SLW,z)
    visd1 = aerialImageV(k,d,SLW1,z)
    visd2 = aerialImageV(k,d,SLW2,z)
    
    plt.plot([s*1e6 for s in SLW],visSLW)
    plt.xlabel('Slit width [um]')
    plt.ylabel('Aerial image visibility')
    plt.show()
    
    
    plt.plot([s*1e6 for s in d],visd1,label='SSA = 50 um')
    plt.plot([s*1e6 for s in d],visd2,label='SSA = 350 um')
    plt.xlabel('d [um]')
    plt.ylabel('Aerial image visibility')
    plt.legend()
    plt.show()
    
    dirPath = '/user/home/opt_old/xl/xl/experiments/BEUVcoherence/data/'
    files = ['contrastMetrics50_2d.pkl','contrastMetrics350_2d.pkl']
    picks = [pickle.load(open(dirPath + f, 'rb')) for f in files]

    mC = [p[1] for p in picks]
    labels = [p[0] for p in picks]
    SSA = [50,75,100,125,150,175,200,300]

    print(mC)
    # [labels,np.squeeze(mC),np.squeeze(rC),np.squeeze(cC),np.squeeze(Nrms),np.squeeze(F),np.squeeze(NI)]

    NILS50 = [2.8706083545041152, 2.8811122789153063, 2.870744614488765, 2.893850374345269, 2.773522775434887, 2.80172111792031, 2.642213450364398, 1.9606921638190036]
    NILS350 = [2.8373913133227404, 2.659960117602982, 2.3710150395048393, 2.083147578025207, 1.7397288577995194, 1.4233246657116705, 1.0793228774712333]
    CM50 = [0.97375596, 0.9710654, 0.96677995, 0.97276497, 0.96853113, 0.9665473, 0.9351784, 0.8690773]
    CM350 = [0.949562, 0.92230034, 0.8666157, 0.8599906, 0.81295055, 0.81691766, 0.74594104]

    plt.plot(SSA,[n/np.pi for n in NILS50],'xr',label='$W_{SSA}$ = 50 \u03bcm (model)')
    plt.plot(SSA[0:7],[n/np.pi for n in NILS350],'x', color='black',label='$W_{SSA}$ = 350 \u03bcm (model)')
    # plt.plot(SSA,CM50,'xr',label='$W_{SSA}$ = 50 \u03bcm (model)')
    # plt.plot(SSA[0:7],CM350,'x',color='black',label='$W_{SSA}$ = 350 \u03bcm (model)')
    # for i,m in enumerate(mC):
    #     try:
    #         plt.plot(SSA,m,'xr',label='$W_{SSA}$ = 50 \u03bcm (simulated)')
    #         # plt.plot(SSA,[p/np.pi for p in m],'xr',label='$W_{SSA}$ = 50 \u03bcm (simulated)')
    #         # plt.plot(SSA,[p[0]/0.6 for p in m],'xr',label='$W_{SSA}$ = 50 \u03bcm (simulated)')
    #     except:
    #         plt.plot(SSA[0:7],m,'x',color='black',label='$W_{SSA}$ = 350 \u03bcm (simulated)')
    #         # plt.plot(SSA[0:7],[p/np.pi for p in m],'x',color='black',label='$W_{SSA}$ = 350 \u03bcm (simulated)')
    #         # plt.plot(SSA[0:7],[p[0]/0.6 for p in m],'x',color='black',label='$W_{SSA}$ = 350 \u03bcm (simulated)')
    
    plt.plot([s*1e6 for s in d],visd1,'r',label = "$W_{SSA} = 50$ \u03bcm (Eqn. 4.25)") #(|sinc($k d W_{SSA} / 2 z_0$)|)") #label='SSA = 50 um (analytical)')
    plt.plot([s*1e6 for s in d],visd2,'black',label = "$W_{SSA} = 350$ \u03bcm (Eqn. 4.25)")#(|sinc($k d W_{SSA} / 2 z_0$)|)") #label='SSA = 350 um (analytical)')
    plt.xlabel('$d$ [\u03bcm]')
    plt.ylabel('Aerial image visibility')
    # plt.ylabel('$C_M$')
    # plt.ylabel('NILS/$\pi$')
    plt.legend()
    plt.savefig( '/user/home/opt_old/xl/xl/experiments/BEUVcoherence/visibility_comparison_NILS.svg')#,format='pdf')
    plt.show()
    
def testAnalyticalAEI():
    c = 299792458
    
    E10 = 0.50    # E10 + E20 = 1.0
    E20 = 0.50 
    E30 = 0.008 #0.83 #75/100 # value of transmission through mask in Masters thesis
    E1p = 0 * 1/2 * np.pi
    E2p = 0*np.pi
    E3p = 0.8*np.pi
    wl = 6.7e-9 # 13.5e-9 #6.7e-9
    k = (2*np.pi)/wl
    p = 200.0e-9
    theta = diffractionAngle(wl,p)
    w=c*k#1/wl
    
    Show = False
    
    xR = 250.0e-6
    xN = 100
    
    x = np.linspace(-xR/2,xR/2,xN)
    
    z = aerialImageDistance(100e-6, p=p, m=1, wl=wl)
    #1.5e-12 
    # range(0,10)
    # 0#1.0*1e-6
    
    t =  0*z/c
    # [(Z*1e-1)/c for Z in z]
    # z/c #1.0e-9
    
    # Wo = 10.0e-6
    Wz = 1.0e-3   #beam size at z (1/e^2)
    R = 25.0         #radius of curvature
    Z = 9.5          #propagation distance from waist
    
    ratio_sum = E10 + E20
    E1a = E10 / ratio_sum * (1 - E30)
    E2a = E20 / ratio_sum * (1 - E30)
    E3a = E30
    
    I = analyticalAE(x, E1a, E2a, E3a, E3p, Wz, k, theta, z, R)
    
    plt.plot(x,I)
    plt.show()
    
if __name__ == '__main__':
    # testAnalyticalAEI()
    testI()
    # testVisibilitySSA()