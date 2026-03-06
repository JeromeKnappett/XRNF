#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 14:43:05 2022

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
from math import floor, log10

plt.rcParams["figure.figsize"] = (16,12)

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
            return x

class centoSymGrating():
    def __init__(self, p1, p2, X, Y, px=1e-8,verbose=False):
        '''
        p1 : Pitch of 2nd & 4th quadrants of centosymmetric square grating.
        p2 : Pitch of 1st & 3rd quadrants of centosymmetric square grating.
        X, Y : Grating dimensions in x and y [m]
        px: pixel size [m]
        '''
        self.p1 = p1
        self.p2 = p2
        self.X = X
        self.Y = Y
        self.px = px
        
        self.Nx = int(self.X/self.px)
        self.Ny = int(self.Y/self.px)
        
        self.num_lines1 = self.X/(2*self.p1)
        self.num_lines2 = self.X/(2*self.p2)
        self.linePx1 = self.p1/(2*self.px)
        self.linePx2 = self.p2/(2*self.px)
        
        
        if verbose:
#            pass
            print("Total number of pixels (x,y):             ",(self.Nx, self.Ny))
            print("Number of pixels for each quadrant (x,y): ",(self.Nx/2, self.Ny/2))
            print("Number of lines in Q1 & Q3:               ",self.num_lines1)
            print("Number of lines in Q2 & Q4:               ",self.num_lines2)
            print("p1 line thickness (pixels):               ",self.linePx1)
            print("p2 line thickness (pixels):               ",self.linePx2)
            
        
    def generate(self,show=True):
        
        # creating an array of zeros the size of one quadrant
        x1 = np.zeros(int((self.X/2)/self.px))
        x2 = np.zeros(int((self.X/2)/self.px))
        
        # finding the indexes for the start and end of lines
        indp1 = range(0,int(self.Nx/2 + 1),int(self.linePx1))
        indp2 = range(0,int(self.Nx/2 + 1),int(self.linePx2))
        
        startp1 = indp1[::2]
        endp1 = indp1[1::2]
        startp2 = indp2[::2]
        endp2 = indp2[1::2]
        
        # generating line profiles for p1 and p2
        for i1, o1 in zip(startp1,endp1):
            x1[i1:o1] = 255
        for i2, o2 in zip(startp2,endp2):
            x2[i2:o2] = 255
        
        if len(startp1)>len(endp1):
            x1[startp1[-1]::] = 255
        if len(startp2)>len(endp2):
            x2[startp2[-1]::] = 255
        
        # turning line profiles into 2D grating lines
        q1line = np.tile(x1,(int(self.Ny/2.0),1))
        q2line = np.tile(x2,(int(self.Ny/2.0),1))
        
        # mirroring 2D grating lines along diagonal to create grating quadrants
        Q1 = np.triu(np.fliplr(q1line))
        Q1 = Q1 + Q1.T - np.diag(np.diag(Q1)) 
        
        Q2 = np.triu(np.fliplr(q2line))
        Q2 = Q2 + Q2.T - np.diag(np.diag(Q2)) 
        
        # adding quadrants together to create centrosymmetric grating
        G = np.concatenate((np.concatenate((np.rot90(np.rot90(Q1)),np.rot90(Q2)),axis=1),(np.concatenate((np.fliplr(Q2),Q1),axis=1))), axis=0)
        
        self.grating = G
        
        print(np.shape(G))
        if show:
#            plt.plot(x1)
#            plt.plot(x2)
#            plt.show()
            
#            fig, ax = plt.subplots(1,2)
#            ax[0].imshow(q1line,cmap='gray')
#            ax[1].imshow(q2line,cmap='gray')
#            plt.show()
#            
#            fig, ax = plt.subplots(2,2)
#            
#            ax[0,0].imshow(np.rot90(np.rot90(Q1)))
#            ax[0,0].set_title('np.rot90(np.rot90(Q1))')
#            ax[0,1].imshow(np.rot90(Q2))
#            ax[0,1].set_title('np.rot90(Q2)')
#            ax[1,0].imshow(np.fliplr(Q2))
#            ax[1,0].set_title('np.fliplr(Q2)')
#            ax[1,1].imshow(Q1)
#            ax[1,1].set_title('Q1')
#            plt.show()
            
            plt.imshow(G,cmap='gray')     
            plt.xticks([int((self.Nx-1)*((b/(5.0-1)))) for b in range(0,5)],
                       [round_sig(self.Nx*self.px*(a/(5.0-1))) for a in range(-int((5-1)/2),int((5/2 + 1)))])
            plt.yticks([int((self.Ny-1)*(b/(5.0-1))) for b in range(0,5)],
                       [round_sig(self.Ny*self.px*(a/(5.0-1))) for a in range(-int((5-1)/2),int((5/2 + 1)))])
            plt.xlabel('x [m]')
            plt.ylabel('y [m]')
            plt.show()
        
        return G, Q1, Q2
    
    def idealSubstrate(self,show=True):
        # copied from grating.py
        S = 255*np.ones_like(self.grating)
        
        print(np.shape(S))
        
        if show:
            plt.imshow(S, cmap='gray') 
            plt.xticks([int((self.Nx-1)*((b/(5.0-1)))) for b in range(0,5)],
                       [round_sig(self.Nx*self.px*(a/(5.0-1))) for a in range(-int((5-1)/2),int((5/2 + 1)))])
            plt.yticks([int((self.Ny-1)*(b/(5.0-1))) for b in range(0,5)],
                       [round_sig(self.Ny*self.px*(a/(5.0-1))) for a in range(-int((5-1)/2),int((5/2 + 1)))])
            plt.xlabel('x [m]')
            plt.ylabel('y [m]')
            plt.show()
        return S
    
    
    def gradientMask(self, show=True):
        
        x = np.linspace(0, 255, self.Nx)
        gM = np.tile(x, (self.Nx, 1)).T
        
        if show:
            plt.imshow(gM, cmap='gray')
            plt.colorbar()
            plt.show()
        
        return gM

        
if __name__ == '__main__':
    import tifffile
    p1 = 2e-6
    p2 = 2.5e-6
    X = 0.001 #150e-6
    Y = X
    px = 5e-6#0.025e-6
    
    c = centoSymGrating(p1=p1,p2=p2,X=X,Y=Y,px=px,verbose=True)
#    G, q1, q2 = c.generate(show=True)
#    S = c.idealSubstrate(show=True)
    gM = c.gradientMask(show=True)
    
#    tifffile.imwrite('/user/home/opt/xl/xl/experiments/maskAlignment2/allignmentGrating_' + str(round_sig(p1*1e6)) + 'p1_' + str(round_sig(p2*1e6)) + 'p2.tif', np.uint8(G))
#    tifffile.imwrite('/user/home/opt/xl/xl/experiments/maskAlignment2/substrate_' + str(round_sig(p1*1e6)) + 'p1_' + str(round_sig(p2*1e6)) + 'p2.tif', np.uint8(S))
    tifffile.imwrite('/user/home/opt/xl/xl/experiments/testBeamline/gradientMask.tif',np.uint8(gM))
#    tifffile.imwrite('/user/home/opt/xl/xl/quad2.tif',np.uint8(q2))
    
#    image = tifffile.imread('/home/jerome/Documents/allignmentGratingTest.tif')
#    filename1 = "/home/jerome/Documents/image.bin"   # save data as bin file 
#    bin_file = image.tofile(filename1)