# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 11:54:29 2022

@author: jknappett
"""

#import phidl.geometry as pg
#from phidl import Device, Layer, LayerSet
#from phidl import quickplot as qp
import numpy as np
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import scipy.interpolate
from math import floor, log10
from matplotlib.pyplot import figure

plt.rcParams["figure.figsize"] = (16,12)

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
            return x

def centeredDistanceMatrix(n,xoff,yoff):
    # make sure n is odd
    x,y = np.meshgrid(range(int(n)),range(int(n)))
    X = x - xoff
    Y = y - yoff
    r = np.sqrt((X-(n/2)+1)**2+(Y-(n/2)+1)**2)
    return r

class FZP():
    def __init__(self, D, wl, delta_r,f,px=1e-8,verbose=False):
        '''
        D: Lens diameter [m]
        wl: wavelength [m]
        delta_r: Outzone thickness [m]
        f: focal length [m]
        px: pixel size [m]
        '''
        self.D = D
        self.wl = wl
        self.px = px
        
        if f != None:
            self.f = f
            self.delta_r = (self.f*self.wl)/self.D
        else:
            self.delta_r = delta_r
            self.f = (self.D*self.delta_r)/self.wl #approx
            
        self.num_zones = self.D/(4*self.delta_r)
        self.centralzone = np.sqrt((self.f * self.wl))
        # self.r1 = self.D / (2 * np.sqrt(self.num_zones))
        if verbose:
            pass
            print(f"Outermost zone thickness:                    {self.delta_r*1e9} nm")
            print(f'Number of zones:                             {self.num_zones}')
            print(f'Focal length @ {self.wl*1e9} nm wavelength:  {self.f} m')
            print(f'Width of central zone:                       {self.centralzone*1e6} um')
        
    def generate(self,apSize,offX,offY,show=True,verbose=False):
        """
        apSize: Size of aperture defining illuminated FZP area [m]
        offX, offY: horizontal and vertical offsets for shifted FZP [m]
        """
        n_raddii = np.zeros(int(self.num_zones))

        for n in range(1,int(self.num_zones)):
            n_raddii[-n] = np.sqrt(n*self.wl*self.f)
        
        # Creating 1D line profile of FZP
        l = np.zeros(int(self.D/(2*self.px)))
        R = range(0,int(self.num_zones),2)
        # Getting the inner and outer zone radius in pixels for each zone
        innerRadPx, outerRadPx = [int((n_raddii[-r] + (n_raddii[-r]-n_raddii[-r-1])/2)/self.px) for r in R], [int((n_raddii[-r] - (n_raddii[-r]-n_raddii[-r-1])/2)/self.px) for r in R]
        for i, o in zip(innerRadPx, outerRadPx):
            l[i:o] = 1
            
        # OLD METHOD
        #R = range(2,int(self.num_zones),2)
        #for r in R:
        #    innerRad = n_raddii[-r] + (n_raddii[-r]-n_raddii[-r-1])/2
        #    outerRad = n_raddii[-r] - (n_raddii[-r]-n_raddii[-r-1])/2
        #    innerRadPx = int(innerRad/self.px)
        #    outerRadPx = int(outerRad/self.px)
        #        
        #    l[innerRadPx:outerRadPx] = 1
        
        # Converting line profile to 2D array
        n = self.D/self.px
        apSp = apSize/self.px
        offXp, offYp = offX/self.px, offY/self.px
        minRx = np.sqrt(((apSize/2)**2) + ((offX + (apSize/2))**2))
        thetaX, thetaY = np.arcsin(offX/self.f),  np.arcsin(offY/self.f)
        
        if verbose:
            # pass
            print(f'Radius of fzp array (pixels):              {(n/2)}')
            print(f'Length of line profile (pixels):           {len(l)}')
            print(f'Size of aperture (pixels):                 {apSp}')
            print(f'Size of offset (x,y) (pixels):             {offXp,offYp}')
            print(f'Minimum radius for offset and aperture:    {minRx*1e6} um')
            print(f'Radius of FZP:                             {(self.D/2)*1e6} um')
            print(f'Angle of diffraction (x,y):                {thetaX, thetaY} rad')
            print(f'Angle of diffraction (x,y):                {np.degrees(thetaX), np.degrees(thetaY)} deg')
            
            
            
        if minRx > self.D/2:
            print('---!APERTURE & OFFSET TOO LARGE FOR FZP SIZE!---')
            print(f'Change D in FZP function to greater than {minRx*2}')
        
        if float(len(l)) != (n/2):
            print('---!RADIUS OF FZP & LENGTH OF LINE PROFILE MUST BE EQUAL!---')
            print(f'Try changing D to {round_sig(self.D + 1e-6,5)}')
        
        c = centeredDistanceMatrix(apSp, offXp,offYp)
        f = scipy.interpolate.interp1d(np.arange(n/2), l)
        zp = f(c.flat).reshape(c.shape)
        
        if show:
            x = np.linspace(-self.D/2,self.D/2,int(n))
            plt.plot(x,np.concatenate([np.flip(l),l]))
            plt.xlabel('x [m]')
            plt.ylabel('Thickness')
            plt.show()
        
            plt.imshow(zp,cmap='gray')
            plt.xticks([int((apSp-1)*(b/(5-1))) for b in range(0,5)],
                       [round_sig(apSp*self.px*(a/(5-1))) for a in range(-int((5-1)/2),int((5/2 + 1)))])
            plt.yticks([int((apSp-1)*(b/(5-1))) for b in range(0,5)],
                       [round_sig(apSp*self.px*(a/(5-1))) for a in range(-int((5-1)/2),int((5/2 + 1)))])
            plt.xlabel('x [m]')
            plt.ylabel('y [m]')
            plt.colorbar()
            plt.show()
        return zp
    
    def toGDS(self,zp,filename):
        import gdspy
        
        
        # The GDSII file is called a library, which contains multiple cells.
        lib = gdspy.GdsLibrary()
        gdspy.current_library=gdspy.GdsLibrary()
        
        # Geometry must be placed in cells.
        unitCell = lib.new_cell('CELL')
        square = gdspy.Rectangle((0.0, 0.0), (1.0, 1.0), layer=0)
        unitCell.add(square)
        width, height = np.shape(zp)[0], np.shape(zp)[1]
        
        grid =  lib.new_cell("GRID")
        
        for x in range(width):
            for y in range(height):
                if zp[y,x] == 0:
                    print("({0}, {1}) is black".format(x, y))
                    cell = gdspy.CellReference(unitCell, origin=(x, height - y - 1))
                    grid.add(cell)
        
        scaledGrid = gdspy.CellReference(
            grid, origin=(0, 0))
        
        # Add the top-cell to a layout and save
        top = lib.new_cell("TOP")
        top.add(scaledGrid)
        lib.write_gds(filename)
        
    
if __name__=='__main__':
    # fzp = FZP(D = 1001e-6,wl = 6.7e-9, f = 10.0e-3, delta_r = None,px=2.5e-7,verbose=True)
    # zp = fzp.generate(apSize=700.0e-6,offX=0.0e-6,offY=0.0e-6,show=True,verbose=True)
    path = '/user/home/opt/xl/xl/'
    fileName = '/user/home/opt/xl/xl/experiments/focusedOffAxis6/FZP_20um.tif'
    # '/home/jerome/Downloads/FZP_GDS.gds'
    apS = 50e-6    # size of aperture to define FZP area
    offX = 223.0e-6  # x offset
    offY = 0.0e-6   # y offset
    D = 501.0e-6    # FZp diameter
    wl = 0.1486627e-9# 6.7e-9     # optimal incident wavelength
    f = None #10.0e-3      # focal length
    F = 0.0010746268656716418 
    dr = 90.0e-9   #outermost zone thickness
    px = 10.0e-9
    
    fzp = FZP(D,wl,f=f, delta_r = dr, px=px,verbose=True)
    zp = fzp.generate(apSize=apS,offX=offX,offY=offY,show=True,verbose=True)
    # fzp.toGDS(zp,fileName)
    import tifffile
    zp8bit = np.uint8(np.multiply(zp,255/np.max(zp))) # np.array(zp,dtype=np.uint8)#(zp/np.max(zp))*255
    tifffile.imwrite(path + 'FZP_' + str(round(apS*1e6)) + 'um_' + str(int(offX*1e6)) + 'offX' + str(int(offY*1e6)) + 'offY.tif',zp8bit)#,dtype=np.uint8)
    
    
    plt.imshow(zp,aspect='auto')
    plt.show()
    
    plt.imshow(zp8bit,aspect='auto')
    plt.show()