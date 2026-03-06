#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 09:55:38 2024

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
from  xraydb import get_materials, add_material, material_mu, material_mu_components
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

# Read the CSV file
D = pd.read_csv('/home/jerome/Downloads/res_brilliance.dat', delim_whitespace=True )

E = np.linspace(0.090,10.0, num = 10000)  # energy values 0.090..10 keV

def interp(x_target, x,y):
    f = interp1d(x,y,bounds_error=False, fill_value=0)
    y2 = [f(i) for i in x_target]
    return y2

D['E'] = E    
print(D.head()) 
print(D['E'])
D['f1i'] =  interp(E, D['e1'], D['f1'])
D['f3i'] =  interp(E, D['e3'], D['f3'])
D['f5i'] =  interp(E, D['e5'], D['f5'])
D['f7i'] =  interp(E, D['e7'], D['f7'])
D['f9i'] =  interp(E, D['e9'], D['f9'])

f =  []
for i in range(len(E)):
    max = 0
    for y in ['f1i','f3i','f5i','f7i','f9i']:
        max = D[y][i] if D[y][i] > max else max
    f.append(max)
D['f']  =  f

plt.plot(D['e1'], D['f1'],  label='1st harmonic', color='tab:red')
plt.plot(D['e3'], D['f3'],  label='3rd harmonic', color='tab:orange')
plt.plot(D['e5'], D['f5'],  label='5th harmonic', color='tab:green')
plt.plot(D['e7'], D['f7'],  label='7th harmonic', color='tab:purple')
plt.plot(D['e9'], D['f9'],  label='9th harmonic', color='tab:brown')

plt.plot(D['E'], D['f'],  label='combined', color='tab:pink', lw=4, alpha=0.6)

plt.legend()
plt.title('Source Spectrum')
plt.xlabel('Photon energy (keV)')
plt.ylabel('Flux (Photons/s/0.1\% bandwith)')
plt.yscale("log")
plt.show()
 

reflectivity = pd.read_csv('/home/jerome/Downloads/combinedReflectivity.txt', delim_whitespace=True )

D['transmission'] = interp(D['E'],
                            reflectivity['Photon energy (eV)']/1000, 
                            reflectivity['Reflectivity'])

plt.plot(D['E'], D['transmission'])
plt.title('Beamline Transmission')
plt.xlabel('Photon energy (keV)')
plt.ylabel('Transmission')
plt.yscale("log")
plt.show()

D['radiation'] = np.multiply(D['f'],D['transmission'])

# log plot
plt.plot(D['E'], D['radiation'])
plt.title('Incident X-ray Spectrum')
plt.xlabel('Photon energy (keV)')
plt.ylabel('Intensity (ph/s/0.1\% bw)')
plt.yscale("log")
plt.show()

#linear plot
plt.plot(D['E'], D['radiation'])
plt.title('Incident X-ray Spectrum')
plt.xlabel('Photon energy (keV)')
plt.ylabel('Intensity (ph/s/0.1\% bw)')
plt.show()


def transmission(wl,T,beta):
    k = (2*np.pi) / wl
    trans = np.exp((-2*k * beta * T)) # np.exp(((-k) / (beta * T)))
    return trans

def EtoWL(E):
    """ 
    takes energy in [eV] and returns wavelength in [m]
    """
    h = 4.135667696e-15
    c = 299792458
    wl = (h*c)/E
    return wl

import xraydb
CF = 'Y3Al5O12'
dens_YAG = 4.56

transmissivityYAG = []

#print(D['E'])
for e in D['E']:    
    (delta,beta,atlen) = xraydb.xray_delta_beta(CF,dens_YAG,e*1000)
    wl = EtoWL(e*1000)
    trans = transmission(wl,0.5e-3,beta)
#    print((delta,beta,atlen))
#    print(trans)
#    print(wl)
    transmissivityYAG.append(trans)
    

#YAG = {'mu' : material_mu('yag', D['E']*1000), # in units in 1/cm
#        'thickness' :  0.05  # in units of cm)
#       }
 
#transmissivityYAG = [np.exp(-YAG['thickness'] * mu ) for mu in YAG['mu']]
transmittedIntensityYAG = [I * t for I,t in zip(D['radiation'],transmissivityYAG)] 


fig, ax1 = plt.subplots()
ax1.set_title(f"X-ray transmission by {0.5e-3} mm of YAG")
#ax1.set_title(f"X-ray transmission by {YAG['thickness']*10.0} mm of YAG")
ax2 = ax1.twinx()
ax1.plot(D['E'], transmittedIntensityYAG,'g-')
ax2.plot(D['E'], transmissivityYAG, 'b-')

ax1.set_xlabel('Photon Energy (eV)')
ax1.set_ylabel('Transmitted intensity (ph/s/0/.1% bw)', color='g')
ax2.set_ylabel('Transmissitvity', color='b')

#ax1.set_yscale("log")
#ax2.set_yscale("log")

plt.show()


# Borosilicate glass 
formula= 'Si45O113B12Na2Al2'
dens_glass = 2.29

#from xraydb import validate_formula
#validate_formula(formula)
#add_material('glass', formula, dens_glass)


transmissivityGlass = []
for e in D['E']:    
    (delta,beta,atlen) = xraydb.xray_delta_beta(formula,dens_glass,e*1000)
    wl = EtoWL(e*1000)
    trans = transmission(wl,3.175e-3,beta)
    transmissivityGlass.append(trans)

#glass = {'mu' : material_mu('glass', D['E']*1000), # in units in 1/cm
#        'thickness' :  0.3175  # in units of cm)
#       }
 
#transmissivityGlass = [np.exp(-glass['thickness'] * mu ) for mu in glass['mu']]
transmittedIntensityGlass = [I * t for I,t in zip(D['radiation'],transmissivityGlass)] #np.multiply(transGlass,D['radiation'])


fig, ax1 = plt.subplots()
ax1.set_title(f"X-ray transmission by {3.175e-3} mm of glass")
ax2 = ax1.twinx()
ax1.plot(D['E']*1000, transmittedIntensityGlass,'g-')
ax2.plot(D['E']*1000, transmissivityGlass, 'b-')

ax1.set_xlabel('Photon Energy (eV)')
ax1.set_ylabel('Transmitted intensity (ph/s/0.1% bw)', color='g')
ax2.set_ylabel('Tranmissivity', color='b')

plt.show()

totalTransmitted = np.multiply(transmissivityYAG, np.multiply(transmissivityGlass,D['radiation']))

#plt.yscale("log")
plt.plot(D['E']*1000, totalTransmitted, label='transmitted')
plt.title(f"X-ray transmission through {3.175e-3} mm of glass \n + {0.5e-3} mm of YAG. ")
plt.xlabel('Photon Energy (eV)')                                                                                                                                                                              
plt.ylabel('Transmitted intensity (ph/s/0/.1% bw)')
plt.show()

totalPhotonsPerSec = np.sum(totalTransmitted)
print(f"The intensity, integrated over the spectrum, expected to be transmitted outside the endstation is {totalPhotonsPerSec:.2e} photons/s.")


def radiantFlux_to_absorbedDose(photons_per_sec, photon_energy_keV, exposure_time_sec=1.0, mass=5.0):
    """
    Convert X-ray photons per second to absorbed Dose, assuming a partial-body dose corresponding to
    the parameters thickness_cm and density. 

    Default parameters are chosen to correspond approximately to absorption in a 5 kg human head in 1 second.

    Parameters:
    - photons_per_sec: array of float, number of photons per second
    - photon_energy_keV: array of float, energy of each photon in keV
    - exposure_time_sec: float, total exposure time in seconds
    - mass: mass of tissue in which absorption occurs, e.g. human head of mass ~ 5.0 kg
    Returns:
    - dose_per_sec: float, dose in Gy (Gray)
    """
    # Constants
    keV_to_J = 1.60218e-16  # 1 keV = 1.60218 × 10⁻¹⁶ J

    # calculate total energy absorbed (J)
    total_energy = 0
    for energy, count in zip(photon_energy_keV, photons_per_sec):
        total_energy += count * energy * keV_to_J * exposure_time_sec
    
    # Calculate absorbed dose (Gy)
    absorbed_dose = total_energy / mass
    
    return absorbed_dose

dose_per_sec = radiantFlux_to_absorbedDose(totalTransmitted, D['E'])
print(f"Absorbed Dose per hour: {dose_per_sec*3600*1e9:.2e} nGy/hr")



dose_per_sec = radiantFlux_to_absorbedDose(transmittedIntensityGlass, D['E'])
print(f"Absorbed Dose per hour (without scintillator): {dose_per_sec*3600*1e9:.2e} nGy/hr")

