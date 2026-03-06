#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 12:31:23 2022

@author: jerome
"""
import numpy as np
try:
    from wpg.srwlib import SRWLStokes, SRWLWfr
    from wpg.wavefront import Wavefront
except ImportError:
    pass
import matplotlib.pyplot as plt
import pickle
from matplotlib.colors import hsv_to_rgb
import time
from math import log10, floor


# %%
def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
            return x

def diffractionAngle(wl,D):
    theta = (1.22 * wl) / D
    return theta

def fresnelZoneWidth(phase_profile):
    
    n = np.len(phase_profile)
    p0 = phase_profile[n//2]
    
    
def fresnelZoneWidth(phase_array):
    # Get the center indices
    y0, x0 = phase_array.shape[0] // 2, phase_array.shape[1] // 2
    
    # Get the center value
    center_value = phase_array[y0, x0]
    
    # Extract horizontal and vertical profiles
    horizontal_profile = phase_array[y0, :]
    vertical_profile = phase_array[:, x0]
    
    # Function to find index and distance of the closest point with a difference of pi or more
    def closest_pi_diff(profile, center_index, center_value):
        # Calculate the absolute difference from pi
        diff = np.abs(profile - center_value)
        
        # Find indices where the difference is pi or more
        pi_diff_indices = np.where(diff >= np.pi)[0]
        
        if pi_diff_indices.size == 0:
            return None, None  # Return None if no such point exists
        
        # Find the closest index to the center
        closest_index = pi_diff_indices[np.argmin(np.abs(pi_diff_indices - center_index))]
        
        # Calculate the distance from the center
        distance = np.abs(closest_index - center_index)
        
        return distance
    
    # Find the closest indices with pi difference for horizontal and vertical
    xWidth = closest_pi_diff(horizontal_profile, x0, center_value)
    yWidth = closest_pi_diff(vertical_profile, y0, center_value)
    
    # # Return the results as (row, column) coordinates and distances
    # horizontal_result = ((y0, closest_horizontal_index), horizontal_distance) if closest_horizontal_index is not None else (None, None)
    # vertical_result = ((closest_vertical_index, x0), vertical_distance) if closest_vertical_index is not None else (None, None)
    
    return xWidth,yWidth

    

# %%
def WLtoE(wl):
    """ 
    takes wavelength in [m] and returns energy in [eV]
    """
    h = 4.135667696e-15
    c = 299792458
    E = (h*c)/wl
    return E
# %%
def EtoWL(E):
    """ 
    takes energy in [eV] and returns wavelength in [m]
    """
    h = 4.135667696e-15
    c = 299792458
    wl = (h*c)/E
    return wl

def beamSizeApertureDiffraction(Ax,Ay,wl,z,shape='r',verbose=False):
    
    theta_x = diffractionAngle(wl, Ax)
    theta_y = diffractionAngle(wl, Ay)
    
    Sx = (Ax + (2 * z * np.tan(theta_x)))
    Sy = (Ay + (2 * z * np.tan(theta_y)))
    
    if shape == 'r':
        S = Sx * Sy #(Ax + (2 * z * np.tan(theta_x))) * (Ay + (2 * z * np.tan(theta_y)))
    elif shape == 'c':
        S = Sx * Sy * np.pi
    
    if verbose:
        print(f"Aperture size (x,y):                               {(Ax,Ay)}")
        print(f"Aperture area [m^2]:                               {Ax*Ay}")
        print(f"Beam size after prop from ap (x,y):                {(Sx,Sy)}")
        print(f"Beam area after prop from ap:                      {S}")
    
    return S

def Complex2HSV(z, rmin, rmax, hue_start=90):
    # get amplidude of z and limit to [rmin, rmax]
    amp = np.abs(z)
    amp = np.where(amp < rmin, rmin, amp)
    amp = np.where(amp > rmax, rmax, amp)
    ph = np.angle(z, deg=1) + hue_start
    # HSV are values in range [0,1]
    h = (ph % 360) / 360
    s = 0.85 * np.ones_like(h)
    v = (amp -rmin) / (rmax - rmin)
    return hsv_to_rgb(np.dstack((h,s,v)))

# %%
def getComplex(w, polarization=None, verbose=False):
    """ 
    Give the complex representation of a wavefield
    Parameters
    ----------
    w: scalar wavefield
    polarization: polarization component of wavefield to extract. Can be "total", "horizontal" or "vertical".
    returns:
        cwf: complex wavefield
    """
    
    re = w.get_real_part(polarization = polarization)      # get real part of wavefield
    im = w.get_imag_part(polarization = polarization)      # get imaginary part of wavefield
    
    
    cwf = re + im*1j
    
    if verbose:
        print("Shape of real part of wavefield: {}".format(np.shape(re)))
        print("Shape of imaginary part of wavefield: {}".format(np.shape(im)))
        print("Shape of complex wavefield: {}".format(np.shape(cwf)))
        print("Polarization of complex wavefield: {}".format(polarization))
    else:
        pass
    
    return cwf

# %%
def wavefrontFromPickle(path, wavefront=False):
    import pickle
    
    with open(path, 'rb') as wav:
        w = pickle.load(wav)
    
    if wavefront != False:
        w = Wavefront(srwl_wavefront=w)
    
    return w
def wavefieldFromE(Ex,Ey,N,res,E):
    """
    Ex, Ey: x/y components of complex electric field array
    N: x/y number of pixels in electric field array
    res: x/y resolution of electric field array
    E: Energy
    -----------
    returns: SRWLWfr object
    """
    
    # Defining parameters
    nx,ny = N[0], N[1]
    
    wf = SRWLWfr() #Initial Electric Field Wavefront    
    wf.allocate(1, nx, ny) #Numbers of points vs Photon Energy (1), Horizontal and Vertical Positions (dummy)
    wf.mesh.zStart = 0 #Longitudinal Position [m] at which Electric Field has to be calculated, i.e. the position of the first optical element
    wf.mesh.eStart = E #Initial Photon Energy [eV]
    wf.mesh.eFin = E #Final Photon Energy [eV]
    wf.mesh.xStart = (-nx/2)*res[0] #Initial Horizontal Position [m]
    wf.mesh.xFin = (nx/2)*res[0] #Final Horizontal Position [m]
    wf.mesh.yStart = (-ny/2)*res[1] #Initial Vertical Position [m]
    wf.mesh.yFin = (ny/2)*res[1] #Final Vertical Position [m]
    wf.arEx = Ex
    wf.arEy = Ey
    wf.mesh.ne = 1        
    
    return wf

def getIPfromComplex(Ex,Ey,N,res,E):
    
    wf = wavefieldFromE(Ex,Ey,N,res,E)
    w = Wavefront(srwl_wavefront=wf)
    
    
    _Ex = np.reshape(w._srwl_wf.arEx, (w.params.Mesh.nx, w.params.Mesh.ny, 2))
    _Ey = np.reshape(w._srwl_wf.arEy, (w.params.Mesh.nx, w.params.Mesh.ny, 2))
        
    Ex = _Ex.flatten()
    Ey = _Ey.flatten()
    
    plt.imshow(_Ex[:,:,0])
    plt.show()
    plt.imshow(_Ey[:,:,0])
    plt.show()
    
    plt.plot(Ex)
    plt.show()
    plt.plot(Ey)
    plt.show()
    
    I = np.squeeze(w.get_intensity(polarization='total'))
    P = np.squeeze(w.get_phase(polarization='total'))
    
    return I,P



def ItoW(I,dx,dy):
    """
    Converts intensity (ph/s/.1%bw/mm^2) to power (W/m^2)
    I: Intensity
    dx,dy: resolution in x,y
    """
    _c = 299792458
    epsilon = 8.854187817e-12
    
    Imtot_w = I*(_c/2*epsilon) # W/m^2
    ITOT = Imtot_w*(1/1.602e-19)*(1/185)*0.0001
    
    Imtot = np.sum(ITOT*dx*dy)
    
    return Imtot
    

def colorize(z):
#    from colorsys import hls_to_rgb
#    n,m = z.shape
#    c = np.zeros((n,m,3))
#    c[np.isinf(z)] = (1.0, 1.0, 1.0)
#    c[np.isnan(z)] = (0.5, 0.5, 0.5)
#
#    idx = ~(np.isinf(z) + np.isnan(z))
#    A = (np.angle(z[idx]) + np.pi) / (2*np.pi)
#    A = (A + 0.5) % 1.0
#    B = 1.0 - 1.0/(1.0+abs(z[idx])**0.3)
#    c[idx] = [hls_to_rgb(a, b, 0.8) for a,b in zip(A,B)]
#    return c
    from colorsys import hls_to_rgb
    r = np.abs(z)
    arg = np.angle(z) 

    h = (arg + np.pi)  / (2 * np.pi) + 0.5
    l = 1.0 - 1.0/(1.0 + r**0.3)
    s = 0.8

    c = np.vectorize(hls_to_rgb) (h,l,s) # --> tuple
    c = np.array(c)  # -->  array of (3,n,m) shape, but need (n,m,3)
    c = c.swapaxes(0,2) 
    return c

    
def test():
    import tifffile
    
#    path = '/user/home/opt/xl/xl/experiments/lowEnergyBeam/data/atM18000/'
#    file1 = path + 'atM18000EforS.pkl'
    path = '/user/home/opt/xl/xl/experiments/farField/data/farField/'
#    '/user/home/opt/xl/xl/experiments/testBeamline/data/Vgrad150000/'
    file1 = path + 'farfield.pkl'
#    'Vgrad150000EforS.pkl'
#    path = '/user/home/opt/xl/xl/experiments/correctedAngle_coherence3/data/'
#    file1 = path + 'sx175sy100/sx175sy100EforS.pkl'
    intensityFile = path + 'intensity.tif'
#    E = 184.76  #photon energy
#    picks = pickle.load(open(file1, 'rb'))
#    N = (int(picks[2]),int(picks[3]))
##    nTot = [n[0]*n[1] for n in N]
#    res = (picks[4],picks[5])
#    Ex = picks[0]
#    Ey = picks[1]
    
    h5Path = path
#    '/user/home/opt/xl/xl/experiments/testBeamline/data/Vgrad/'
    
    wfile = Wavefront()
    wfile.load_hdf5(h5Path + 'wf_final.hdf')
    plt.imshow(np.squeeze(wfile.get_intensity()))
    plt.title("I from HDF5")
    plt.show()
    
    plt.imshow(np.squeeze(wfile.get_phase()))
    plt.title("P from HDF5")
    plt.show()
    
    EX = wfile._srwl_wf.arEx 
    EY = wfile._srwl_wf.arEy
    
    plt.plot(EX)
    plt.title("Ex from HDF5")
    plt.show()
    plt.plot(EY)
    plt.title("Ey from HDF5")
    plt.show()
    
    import array
    _EX = array.array('f',[0]*len(EX))
    _EY = array.array('f',[0]*len(EY))
    for i in range(int(len(EX)/2)):
            i2 = i*2
            i2p1 = i2 + 1
            reEx = EX[i2]
            imEx = EX[i2p1]
            reEy = EY[i2]
            imEy = EY[i2p1]
            _EX[i] = reEx
            _EX[int(len(EX)/2) + i] = imEx
            _EY[i] = reEy
            _EY[int(len(EY)/2) + i] = imEy
    
    plt.plot(_EX)
    plt.title('deconstructed Ex from HDF5')
    plt.show()
    plt.plot(_EY)
    plt.title('deconstructed Ey from HDF5')
    plt.show()
#    
    wf = wavefieldFromE(Ex,Ey,N,res,E)
    I, P = getIPfromComplex(Ex,Ey,N,res,E)
    w = Wavefront(srwl_wavefront=wf)
    C1 = getComplex(w)
    C2 = I + P*1j
    
#    print(C1.shape())
    print(np.shape(C1))
    img1 = colorize(np.squeeze(C1)) #Complex2HSV(C1, np.min(abs(C1)), np.max(abs(C1)))
    img2 = Complex2HSV(C2, np.min(abs(C2)), np.max(abs(C2)))
#    print "Complex2HSV method: "+ str (t1 - t0) +" s"
    plt.imshow(img1,aspect='auto')
    plt.title("E from .dat #1")
    plt.colorbar()
    plt.show()
    plt.imshow(img2,aspect='auto')
    plt.title("E from .dat #2")
    plt.colorbar()
    plt.show()
#    
    
    # method 2
    file = path + 'Vgrad150000Efields.pkl'
#    file = path + 'HgradEfields.pkl'
    #'/user/home/opt/xl/xl/experiments/correctedAngle_coherence3/data/sx175sy100/sx175sy100Efields.pkl'
    pick = pickle.load(open(file, 'rb'))
    EhR = pick[0]
    EhI = pick[1]
    EvR = pick[2]
    EvI = pick[3]
    res = (pick[4],pick[5])
    
    Eh = EhR + EhI*1j 
    Ev = EvR + EvI*1j 
    cE = Eh + Ev 
    
    img3 = Complex2HSV(cE, np.min(abs(cE)), np.max(abs(cE)))
    plt.imshow(img3, aspect='auto')
    plt.title("E from .dat #3")
    plt.colorbar()
    plt.show()
    
#    Icheck = tifffile.imread(intensityFile)
#    
#    plt.imshow(Icheck, aspect='auto')
#    plt.title("SE intensity")
#    plt.show()
    
    plt.imshow(I,aspect='auto')
    plt.title("I from .dat")
    plt.show()
    plt.imshow(P,aspect='auto')
    plt.title("P from .dat")
    plt.colorbar()
    plt.show()
#    
#    

def testBeamsize():
    
    A = 5.0e-6
    wl = 4.5e-9
    Z = 1.0
    shape = 'c'
    
    beamSizeApertureDiffraction(A,A,wl,Z,shape,verbose=True)
    
def testWavefieldVectors():
    dirpath =  '/user/home/opt/xl/xl/experiments/correctedAngle_AEcoherence/data/aerialImageEfield/'
    file = 'aerialImageEfieldEfieldsNEW.pkl'
    
    wavefield = wavefrontFromPickle(dirpath + file)
    Ex = [r + i*1j for r,i in zip(wavefield[0], wavefield[1])]
    Ey = [r + i*1j for r,i in zip(wavefield[2], wavefield[3])]
    # ExR = wavefield[0]
    # ExI = wavefield[1]
    # EyR = wavefield[2]
    # EyI = wavefield[3]
    dx,dy = wavefield[4],wavefield[5]
    E = 185
    Nx,Ny = np.shape(Ex)[1], np.shape(Ex)[0]
    
    I,P = getIPfromComplex(Ex, Ey, [Nx,Ny], [dx,dy], E)
    
    theta = np.tan(P)
    
    
if __name__=='__main__':
    testBeamsize()
    # test()