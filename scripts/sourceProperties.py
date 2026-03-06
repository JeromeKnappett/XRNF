#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 11:57:35 2024

@author: jerome
"""

import numpy as np

def checkParams4GSM(wl,size,div,L):
    k = (2*np.pi) / wl
    
    D = k * (div**2) * L
    N = (k * (size**2)) / L
    
    if D > 1 and N > 1:
        print("Dimensionless parameters satisfy GSM :):)")
        print("D = ", D)
        print("N = ", N)
        
    else:
        print("Dimensionless parameters do not satisfy GSM :(:(")
        print("D = ", D)
        print("N = ", N)

def sourceCoherence(wl,size,div):
    term1 = (2 * np.pi * div) / (wl)
    term2 = 1 / (2 * size)
#    print(term1)
#    print(term2)
#    print(term1**2 - term2**2)
#    print((term1**2 - term2**2)**(0.5))
    coh_len = abs( term1**2 - term2**2 )**(-0.5)
    k = (2*np.pi) / wl
    
    # checking emittance
    e = size*div
    if e >= 1/(2*k):
        print('\n emittance satisfies inequality! :)')
        print('e = ', e)
        print('1/2k = ', 1/(2*k))
    elif e <= 1/(2*k):
        print('\n emittance doesnt satisfy inequality! :(')
        print('e = ', e)
        print('1/2k = ', 1/(2*k))
    
    term4 = 4 * (k**2) * (size**2) * (div**2) 
    coh_len2 = (2 * size) / (np.sqrt(abs(term4 - 1)))

    print('here')
#    print(term4)
#    print(np.sqrt(abs(term4 - 1)))
#    print(coh_len2)
#    print(coh_len - coh_len2)
    
    deg_coh = coh_len / size
    term3 = deg_coh**2 + 4
#    print(term3)
    deg_coh_n = deg_coh / (np.sqrt(term3))
    
    return coh_len2, deg_coh, deg_coh_n

def shortestCoherentWavelength(size,div):
    WL = 4 * np.pi * size * div


wl = 6.7e-9
#undulator length
Lu = 1.875

betaX = 9
betaY = 3
emX = 10.0e-9
emY = 0.009e-9

# electron beam
sizeX = np.sqrt(emX * betaX)
sizeY = np.sqrt(emY * betaY)
divX = np.sqrt(emX / betaX)
divY = np.sqrt(emY / betaY)

print('Checking horizontal params...')
checkParams4GSM(wl,sizeX,divX,Lu)
print('Checking vertical params...')
checkParams4GSM(wl,sizeY,divY,Lu)


print('Source size (x,y):       ', (sizeX, sizeY))
print('Source divergence (x,y): ', (divX, divY))

coh_lenX, dcX, dcnX = sourceCoherence(6.7e-9,sizeX,divX)
print('x-coherence length =              ', coh_lenX)
print('x-coherence degree =              ', dcX)
print('x-coherence degree (normalised) = ', dcnX)

coh_lenY, dcY, dcnY = sourceCoherence(6.7e-9,sizeY,divY)
print('y-coherence length =              ', coh_lenY)
print('y-coherence degree =              ', dcY)
print('y-coherence degree (normalised) = ', dcnY)
      
# photon beam
sizeX = 10.06e-9 #np.sqrt(emX * betaX)
sizeY = np.sqrt(emY * betaY)
divX = 0.053 #np.sqrt(emX / betaX)
divY = np.sqrt(emY / betaY)

print('Checking horizontal params...')
checkParams4GSM(wl,sizeX,divX,Lu)
print('Checking vertical params...')
checkParams4GSM(wl,sizeY,divY,Lu)


print('Source size (x,y):       ', (sizeX, sizeY))
print('Source divergence (x,y): ', (divX, divY))

coh_lenX, dcX, dcnX = sourceCoherence(6.7e-9,sizeX,divX)
print('x-coherence length =              ', coh_lenX)
print('x-coherence degree =              ', dcX)
print('x-coherence degree (normalised) = ', dcnX)

coh_lenY, dcY, dcnY = sourceCoherence(6.7e-9,sizeY,divY)
print('y-coherence length =              ', coh_lenY)
print('y-coherence degree =              ', dcY)
print('y-coherence degree (normalised) = ', dcnY))
