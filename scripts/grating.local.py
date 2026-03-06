#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
June 2020

@author: gvanriessen

In development... still needs testing

"""

import numpy as np
import matplotlib.pyplot as plt
import imageio
import copy
import scipy.ndimage
import roughness as rough
from scipy import signal
from diffractio import degrees, mm,  sp, um, nm#, np
import string


#from diffractio.scalar_masks_X import Scalar_mask_X
#from diffractio.scalar_masks_XZ import Scalar_mask_XZ
from diffractio.scalar_masks_XY import Scalar_mask_XY

#from diffractio.scalar_fields_XY import Scalar_field_XY
#from diffractio.utils_drawing import draw_several_fields

from matplotlib import rcParams
rcParams['figure.figsize']=(1,2)
rcParams['figure.dpi']=300
rcParams.update({'font.size': 4})


#import extensions.interferenceGratingModels2 as gm


class grating():

    # will construct everything along x-direction then rotate about centre, shifty is currently ignored
 
    def __init__(self, 
                 nx = 512, 
                 ny = 512, 
                 xdim = 10.0e-6, ydim = 10.0e-6, 
                 height=100e-9,
                 blockHeight = 1,
                 symmetry= 4, 
                 rotationCell = 0,
                 rotationMask=0,
                 gratingType = 'binary',
                 radius=5e-6,
                 period=None,
                 VERBOSE = True):
        
        '''
        Not yet implemented:
         _m – output (diffraction) order    (here we assume normal incidence transmission geometry only)
        _mirSub – SRWLOptMir (or derived) type object defining substrate of the grating
        _grAng – angle between the grove direction and the saggital direction of the substrate [rad] (by default, groves are made along saggital direction (_grAng=0))
        '''
        
        ''' 
        
        parameter: gratingType
            'binary','sine','sineEdge','blazed','forked','2D','2DChess'
            
        
        parameter: nx, ny
            number of pixels for one grating cell.  Mask size will depend on 
            symmetry and rotation.
            
        parameter: xdim, ydim:
            dimensions in units of meters of one grating cell
        
        parameter: symmetry
            n = 1, one grating cell
            n = 2, 180°: dyad arrangement of cells
            n = 3, 120°: triad arrangement of cells
            n = 4, 90°: tetrad arrangement of cells
            n = 6, 60°: hexad arrangement of cells
            n = 8, 45°: octad arrangement of cells
            ...
            
            Be default, angle zero corresponds to the +ve axis and other cells are 
            arranged relatively, clockwise.  
            
        parameter: radius
             radius of circle on which multiple grating cells are located (units m)
             
        parameter: rotationCell
            rotation of each grating cell wrt unrotated reference frame.  
            To be made consistent with definition: '_grAng – angle between the
            grove direction and the saggital direction of the substrate [rad] 
            (by default, groves are made along saggital direction (_grAng=0))'
            
        parameter: rotationMask
            rotation angle for entire mask, applied after rotationCell applied.

        '''
        gratingsSupported = ['binary','sine','sineEdge','blazed','forked','2D','2DChess']
        
        if gratingType in gratingsSupported: 
            self.gratingType = gratingType
        else:
            raise ValueError('Grating type not supported')

        self.nx = nx
        self.ny = ny
        self.xdim = xdim 
        self.ydim = ydim 
        self.xres = self.xdim/self.nx
        self.yres = self.ydim/self.ny
        
        self.height = height
        self.period = period
        
        self.symmetry = symmetry 
        self.radius = radius
        self.rotationCell = rotationCell  #rotation of basis cell
        self.rotationMask = rotationMask  #rotation of set of cells
        
        self.center = [int(self.nx/2), int(self.ny/2)]  # center of array
        
        self.X = None # will be set to x positions over mask 
        self.Y = None #  will be set to y positions over mask
        
        self.blockHeight = blockHeight
        
        if VERBOSE == True:
            print("Mask Cell Dimensions: {} x {}".format(self.nx, self.ny))
            print("Mask Cell Size: {} m x {} m".format(self.xdim, self.ydim))
            print("Mask Resolution, x: {} m, y: {} m ".format(self.xres,self.yres))
    
    
    def rotate(self,A, angle, pivot):
        ''' rotate about pivot. 
        note that for coloured images we have to deal with other channels:
            imgP = np.pad(img, [padY, padX, [0, 0]], 'constant')
        '''
        padX = [A.shape[1] - pivot[0], pivot[0]]
        padY = [A.shape[0] - pivot[1], pivot[1]]
        imgP = np.pad(A, [padY, padX], 'constant')
        imgR = scipy.ndimage.rotate(imgP, angle, order=1, reshape=False) # order = 1 should avoid overshoot
        return imgR 
    
    
    def pattern(self):
        
        if self.cell is not None:
            A = self.cell
    
            if self.symmetry == 1:
                Cn = A
                
#            if self.symmetry == 2:
#                 A = np.pad(A,
#                            ((0,0),(int((self.radius - self.xdim/2)/self.xres),0)),
#                             mode='constant', constant_values=np.max(self.cell))
#                 Cn =  np.concatenate(( np.flip(A), A), axis=1)
#                 if self.rotationMask != 0:
#                    Cn = scipy.ndimage.rotate(Cn, self.rotationMask, reshape=True) 

            if self.symmetry > 1:
                pad = self.xdim/2  #added 13/10/20
                mdim = 2 * np.sqrt(  np.square(pad+self.xdim/2) + np.square(self.radius + self.ydim/2) )
                
                C0      = self.height*np.ones((int(mdim/self.xres), int(mdim/self.yres)))
                block0  = self.blockHeight*np.ones((int(mdim/self.xres), int(mdim/self.yres)))
                centre  = [int(C0.shape[0]/2),int(C0.shape[1]/2)]
                
                # insert Cell at first position on x axis 
                shifty = centre[0] + int((self.radius-(self.xdim/2))/self.xres )#+ int((self.radius)/self.xres)  #int((mdim-self.xdim)/self.xres)
                shiftx = centre[1] - int((self.ydim/2)/self.yres)
                
                C0[shiftx:shiftx+A.shape[0],shifty:shifty+A.shape[1]] = A
                block0[shiftx:shiftx+A.shape[0],shifty:shifty+A.shape[1]] = np.zeros_like(A)
                
                if self.rotationMask != 0:
                    C0 = scipy.ndimage.rotate(C0, self.rotationMask, reshape=False, order=1)
                    block0 = scipy.ndimage.rotate(block0, self.rotationMask, reshape=False, order=1)
                # now we have one mask cell at starting position. Next we add 
                # rotated copies for each additional cell
                Cn = copy.deepcopy(C0)
                blockn = copy.deepcopy(block0)
                
                for angle in np.arange(360/self.symmetry, 360, 360/self.symmetry):
                    #Ca = self.rotate(C0,angle,centre)
                    Ca = scipy.ndimage.rotate(C0, angle, reshape=False,order=1)
                    Cn += Ca
                    
                    blocka = scipy.ndimage.rotate(block0, angle, reshape=False, mode='constant', cval=self.blockHeight,order=1)
                    blockn = np.minimum(blockn, np.clip(blocka,a_min=0,a_max=None))
                    
            xw = Cn.shape[1] * self.xres
            yw = Cn.shape[0] * self.yres
            self.X = np.linspace(-xw/2,xw/2,Cn.shape[0]) 
            self.Y = np.linspace(-yw/2,yw/2,Cn.shape[1]) 
            
            
            
        return Cn, blockn
    
    
    
    def idealSubstrate(self):
        # work in progres... 
        return 255*np.ones_like(self.mask)
    
    def setRoughness(self, tx=1e-6, ty=1e-6, s=100e-9):
        ''' creates a roughness mask
        
        wraps diffractIO roughness method which implements method of Oglivy (see diffractio docs)
        
        parameters:
            t (float, float) – (tx, ty), correlation length of roughness
            s (float) – std of heights
            UNITS IN METRES

        Returns:	
            (numpy.array) Topography of roughnness in microns.
        '''
        from diffractio.utils_optics import roughness_2D
        unit=1#e6

        self.roughness = roughness_2D(self.X, self.Y, (tx*unit,ty*unit), s*unit)
        
        return self.roughness
    
    def generateRandomRoughness2D(self,  h=100e-9, sigma=50e-9, clx=0, cly=0):
        '''
        Generates randomly rough surface with Gaussian distribution of heights, with 
        width given by sigma and height h. 
        Correlation is (optionally) introduced along x and y by
        convolution with a gaussian of width equal to the correlation length in x and y.
        
        ** TODO: check/understand relationship between correlation length input parameters
        and resulting correlation length as measured by conventional approaches.
        
        Parameters:
            
        Nx, Ny: number of points along x and y
        Lx, Ly: length of sides along x and y direction
        clx, cly: correlation length along x and y
        h: rms height
            
        Returns:
        z: heights
        x, y: positions in length units of input parameters
        '''

        Nx, Ny = self.mnx, self.mny 
        Rx, Ry = self.xres*1000, self.yres*1000
        x, y = rough.generateGrid(Nx,Ny,Rx,Ry)
    
        # generare uncorrlated Gaussian random height distribution with mean 0 and std deviation h
        z = h + sigma * np.random.randn(Nx*Ny)
        z = np.reshape(z, (Ny, Nx))
    
        if clx != 0 or cly != 0:
        
            # Gaussian kernel
            F = np.exp(-(np.square(x)/(np.square(clx)/2)+np.square(y)/(np.square(cly)/2)))
    
            # correlated surface generation
            #f = 2/np.sqrt(pi)*  Rx/N/sqrt(clx)/sqrt(cly)*    ifft2(fft2(z).*fft2(F))
            z = signal.fftconvolve(z, F, mode='same')
         
        rms=np.sqrt(np.mean(z**2))
        z = h*z/rms   # normalise  RMS... added gvr 28/9/20
        self.roughness = z
         
        return self.roughness

    def updateMaskRange(self):
        self.maskMax = np.max(self.mask)
        self.maskMin = np.min(self.mask)
        

    def addRoughnessToMaskEverywhere(self,):
        '''adds roughness amplitude to mask amplitude'''
        self.mask = self.mask + np.subtract(self.roughness, np.mean(self.roughness))
        self.updateMaskRange()

   
    def addRoughnessToMaskSubstrate(self,threshold=0.1):
        '''adds roughness amplitude to mask amplitude everywhere except 
           where grating lines exist.  To handle greyscale masks, we use a 
           threshold to determine areas of substrate only'''
        idx =  np.where(self.mask<threshold*np.max(self.mask))
        self.mask[idx] += self.roughness[idx] 
        self.updateMaskRange()

    def addRoughnessToMaskLines(self,threshold=0.5):
        '''adds roughness amplitude to mask amplitude only in areas where grating lines exist'''
        idx =  np.where(self.mask>threshold*np.max(self.mask))
        self.mask[idx] = self.mask[idx] - np.subtract(self.roughness[idx], np.mean(self.roughness[idx]))
        self.updateMaskRange()
    
    def pad(self,A,x=None,y=None):
        return np.pad(A, [x,y], mode='constant')
    
    def writeCell(self,path, dtype='uint8'):
        self.write(self.cell, path, dtype)
    
    def writeMask(self, path, dtype='uint8'):
        self.write(self.mask, path, dtype)

    def writeRoughness(self, path, dtype='uint8'):
        self.write(self.roughness, path, dtype)

    def writeBlock(self, path, dtype='uint8'):
        self.write(self.block, path, dtype)

    def write(self,A,path,dtype='uint8', norm=True):
        
        if dtype == 'uint8':
            if norm == True:
                lo = np.min(A)
                if lo < 0:
                    A = A+lo
                A = A-np.min(A)
                A = np.uint8(255*A/np.max(A))
            imageio.imwrite(path,np.uint8(A))
        else:
            if dtype == 'float32':
                imageio.imwrite(path,np.float32(A))
            else:
                raise ValueError("dtype not supported by write")
        print ('Wrote ' + path)  

    def invert(self):
        #todo
        pass
    
    def grayscale(self):
        #todo...
        pass


    def getMultisliceObject(self,N):
        '''
        from extensions.multisliceOptE import gretscaleToSlices
    
        scaled = 255*self.mask/np.max(self.mask)
        return greyscaleToSlices(scaled,slices=N,invert=False)
        '''
        pass


    def showRoughness(self):
        unit=1e6
        plt.imshow(self.roughness, 
                   'gray', interpolation=None, 
                   extent=[np.min(self.X)*unit,
                           np.max(self.X)*unit,
                           np.min(self.Y)*unit,
                           np.max(self.Y)*unit])
    
        plt.xlabel('x / um')
        plt.ylabel('y / um')
        #plt.colorbar()
        plt.show()


    def showBlock(self):
        unit=1e6
        plt.imshow(self.block, 
                   'gray', interpolation=None, 
                   extent=[np.min(self.X)*unit,
                           np.max(self.X)*unit,
                           np.min(self.Y)*unit,
                           np.max(self.Y)*unit])
    
        plt.xlabel('x / um')
        plt.ylabel('y / um')
        #plt.colorbar()
        plt.show()


    def showMask(self):
        unit=1e6
        plt.imshow(self.mask, 
                   'gray', interpolation=None, 
                   extent=[np.min(self.X)*unit,
                           np.max(self.X)*unit,
                           np.min(self.Y)*unit,
                           np.max(self.Y)*unit])
    
        plt.xlabel('x / um')
        plt.ylabel('y / um')
        #plt.colorbar()
        plt.show()


    def showCell(self):
        unit=1e6
        plt.imshow(self.cell,
                   'gray', interpolation=None, 
                   extent=[np.min(-self.xdim/2)*unit,
                           np.max(self.xdim/2)*unit,
                           np.min(-self.ydim/2)*unit,
                           np.max(self.ydim/2)*unit])
    
        plt.xlabel('x / um')
        plt.ylabel('y / um')
        #plt.colorbar()
        plt.show()


    def shift(self, A):
        ''' shift (by padding) an array A, typically containing a grating cell, such
        that the cell is centred on a circle of radius self.radius that is centred at 0,0 
        '''
        if self.cell:
            shiftxPx =  int((self.radius + self.xdim/2)/self.xres)
            return  np.pad(A,(shiftxPx,),'constant')


    def srwl_opt_mask():
        ''' generate parameters that can be used to include mask in an SRW wavefront
        propagation simulation 
        
        or 
        
        generate srwl_uti_smp object?
        
        TODO
        
        '''
        
        
#        name = 'Mask'
#        
#        op = srwl_uti_smp.srwl_opt_setup_transm_from_file(
#                file_path=v.op_Mask_file_path,
#                resolution=v.op_Mask_resolution,
#                thickness=v.op_Mask_thick,
#                delta=v.op_Mask_delta,
#                atten_len=v.op_Mask_atten_len,
#                xc=v.op_Mask_horizontalCenterCoordinate,
#                yc=v.op_Mask_verticalCenterCoordinate,
#                area=None if not v.op_Mask_cropArea else (
#                    v.op_Mask_areaXStart,
#                    v.op_Mask_areaXEnd,
#                    v.op_Mask_areaYStart,
#                    v.op_Mask_areaYEnd,
#                ),
#                extTr=v.op_Mask_extTransm,
#                rotate_angle=v.op_Mask_rotateAngle,
#                rotate_reshape=bool(int(v.op_Mask_rotateReshape)),
#                cutoff_background_noise=v.op_Mask_cutoffBackgroundNoise,
#                background_color=v.op_Mask_backgroundColor,
#                tile=None if not v.op_Mask_tileImage else (
#                    v.op_Mask_tileRows,
#                    v.op_Mask_tileColumns,
#                ),
#                shift_x=v.op_Mask_shiftX,
#                shift_y=v.op_Mask_shiftY,
#                invert=bool(int(v.op_Mask_invert)),
#                is_save_images=True,
#                prefix='Mask_sample',
#                output_image_format=v.op_Mask_outputImageFormat,
#            )
#        
#        return op, name
        
        

    def generateMask(self):
        
        if self.gratingType == 'binary':
            self.cell,self.cx,self.cy = self.binaryGratingCell()
        if self.gratingType == 'sine':
            self.cell,self.cx,self.cy = self.sineGratingCell()
        if self.gratingType == 'sineEdge':
            self.cell,self.cx,self.cy = self.sineEdgeGratingCell()
        if self.gratingType == 'blazed':
            self.cell,self.cx,self.cy = self.blazedGratingCell()
        if self.gratingType == 'forked':
            self.cell,self.cx,self.cy = self.forkedGratingCell()
        if self.gratingType == '2D':
            self.cell,self.cx,self.cy = self.twoDimGratingCell()
        if self.gratingType == '2DChess':
            self.cell,self.cx,self.cy = self.chess2DGratingCell()
        
        pattern, block = self.pattern()
        self.mask =  pattern
        self.block = block
        self.mnx, self.mny = np.shape(pattern)
    
        self.updateMaskRange()
    
        return self.mask, self.block, self.mnx, self.mny
    
    
    def binaryGratingCell(self, wavelength=None):
    
        x0 = np.linspace(-self.xdim/2, self.xdim/2, self.nx)
        y0 = np.linspace(-self.ydim/2, self.ydim/2, self.ny)
        
        t = Scalar_mask_XY(x=x0, y=y0, wavelength=wavelength)
        t.binary_grating(
            period=self.period,
            amin=0,
            amax=self.height*1e6,
            phase=1,
            x0=0,
            fill_factor=0.5,
            angle=self.rotationCell*degrees)
        
        return abs(t.u), x0, y0
    
    
    def sineGratingCell(self, wavelength=None):
    
        x0 = np.linspace(-self.xdim/2, self.xdim/2, self.nx)
        y0 = np.linspace(-self.ydim/2, self.ydim/2, self.ny)
        
        t = Scalar_mask_XY(x=x0, y=y0, wavelength=wavelength)
        t.sine_grating(
            period=self.period,
            amp_min=0,
            amp_max=self.height*1e6,
            x0=0,
            angle=self.rotationCell*degrees)
        
        return abs(t.u), x0, y0


    def sineEdgeGratingCell(self, wavelength=None):
        #todo
        pass
    
    def blazedGratingCell(self,wavelength=None):
        #todo
        pass
    
    def forkedGratingCell(self, wavelength=None):
        #todo
        pass
    
    def twoDimGratingCell(self, wavelength=None):
        #todo
        pass
    
    def chess2DGratingCell(self, wavelength=None):
        #todo
        pass
        
        
#    def transmissionFunction(self):
#        from wpg.wpg_optmask import opt_from_array
#        
#        return opt_from_array(<<<<<<<MODIFY THIS TO USE ACTUAL THICKNESS
#                    self.mask, self.xres, self.yres, delta, atten_len,
#                    arTr, extTr=0, fx=1e+23, fy=1e+23,
#                    background_color=None,  invert=None)

def testMetrics(savePath='', profileWidth=10, axis = 'y' ):
    
   # create grating object
    gr = grating (nx = 4000, ny = 4000,
                 xdim = 10.0e-6, ydim = 10.00e-6,
                 height=72e-9/1000000,  #GVR HACK TO MAKE mask and roughness map scales similar
                 blockHeight=255,
                 symmetry = 2,
                 rotationCell = 0.0,
                 rotationMask=90,
                 gratingType = 'binary',
                 radius=13.75e-6,
                 period=0.1e-6,
                 VERBOSE =True)
    
    gr.generateMask()   # do this once only     
    
    # write noiseless mask cell
    gr.writeCell(savePath + 'cell.tif')
    
 
    numHeights = 1
    numCorrLengths = 10
    inB = list(string.ascii_lowercase)[0:numHeights]
    c_length = np.linspace(100.0e-9,10.0e-9,numCorrLengths)
    Rh = np.linspace(19.0e-9,1.0e-9,numHeights)
    sigma=200e-9
    cly = 100e-9

     
    # write header to csv file
    with open(savePath + 'metricsTest.csv', "w") as file:
       #file.write('# Mask parameters.  Num. Heights: {}, Num. Corr. Lengths: {}, path: {}\n'.format(numHeights,numCorrLengths,savePath))
       file.write('index, op_Mask_thick, op_Roughness_thick, roughnessSigma, \
                  roughnesRMS, roughnessCorrLenX, roughnessCorrLenY, \
                  op_Mask_file_path, op_Block_file_path\n')
    
    for x,L,clx in zip(inB,range(numCorrLengths),c_length):
        for height in Rh:
            
            gr.generateRandomRoughness2D( h=height,sigma=sigma,clx=clx,cly=cly)
            
            maskHeight = np.max(gr.mask)
            rmsRough = np.sqrt(np.mean(gr.roughness[0,:]**2))
            print ('Height of mask: {}, RMS roughness: {}.  Difference = {}'.format(maskHeight, rmsRough, abs(maskHeight-rmsRough)))
        
            #gr.addRoughnessToMaskEverywhere()
            gr.addRoughnessToMaskLines(threshold=0.01)
            
            fileStem = savePath +   f'{height*1e9:.5f}_{clx*1e9:.5f}_{cly*1e9:.5f}'  #    str(round(((height/2)*1e9)-1)) + x 
            

            gr.showRoughness()
            rough.plotHDF(gr.roughness,bins='auto', outFileName= fileStem + '_roughness.png')
            acfx, xv,  acfy, yv = rough.getACF(gr.roughness,gr.X,gr.Y,lags=gr.nx/5)
            rough.plotACF(acfx,xv,outFileName= fileStem + '_ACF_XV.png')
            rough.plotACF(acfy,yv,outFileName= fileStem + '_ACF_YV.png')
            #corrx, corry = rough.getCorrelationLength(acfx,xv), rough.getCorrelationLength(acfy,yv)
            #print('Correlation lengths: lx = {} m, ly = {} m'.format(corrx,corry))
            
            
            if profileWidth > 1:
                profilelo, profilehi = profileWidth//2, profileWidth//2
            else:    
                profilelo, profilehi = 1, 0 
            
            
            x =  gr.cx
            y =  gr.cy
            metrics = {}
            metrics['x'] = x
            metrics['y'] = y
            ny=len(y)
            nx=len(x)
            
            if  axis == 'x':
                ROI = ((0,ny//2-profilelo),(nx,ny//2+profilehi))
                axisVals = x
            if axis == 'y':
                ROI = ((nx//2-profilelo,0),(nx//2+1,ny+profilehi))
                axisVals = y
 
            prof = gm.lineProfile(gr.cell, ROI=ROI, AXIS = 0 if axis =='x' else 1)
            Cm = gm.gratingContrastMichelson(prof)
            Crms = gm.gratingContrastRMS(prof)
             
            C, C1, C2 = gm.meanDynamicRange(prof) 
            IOD, IODM, H, binEdges, binCenters =gm.integralOpticalDensity(prof)
            Cf,  Am, Fr, peakFr  = gm.gratingContrastFourier(prof,axisVals, show=False)
                        
            pkey=''
            metrics.update({
                                  pkey+'profile' : prof,
                                  pkey+'contrastMichelson' : Cm,
                                  pkey+'contrastRMS': Crms,
                                  pkey+'meanDynamicRangeC' : C,
                                  pkey+'meanDynamicRangeC1' : C1,
                                  pkey+'meanDynamicRangeC2' : C2,
                                  pkey+'integratedOpticalDensity' : IOD,
                                  pkey+'integratedOpticalDensityMax' : IODM,
                                  pkey+'histogram' : H,
                                  pkey+'histogramBins' : binEdges,
                                  pkey+'contrastFourier' : Cf,
                                  pkey+'fundamentalFrequency' : peakFr,
                                  pkey+'fourierFrequency' : Fr,
                                  pkey+'fourierAmplitude' : Am,
                                  pkey+'maskHeight' : maskHeight,
                                  pkey + 'pkey' : height,
                                  pkey + 'sigma' : sigma,
                                  pkey + 'RMS' : rmsRough,
                                  pkey + 'correlationLengthX': clx,
                                  pkey + 'correlationLengthY' : cly,
                                  pkey + 'cellFile' : fileStem+"_cell.tif",
                                  pkey + 'roughFile' : fileStem+"_rough.tif"
                                  })
                    
    
    
    
            file.write('index, op_Mask_thick, op_Roughness_thick, roughnessSigma, \
                  roughnesRMS, roughnessCorrLenX, roughnessCorrLenY, \
                  op_Mask_file_path, op_Block_file_path\n')

            if savePath is not None:
                gr.writeCell(fileStem + '_cell.tif')
                gr.writeRoughness(fileStem + '_rough.tif')
                
                
            line = f"{L},{maskHeight},{height},{sigma},{rmsRough},{clx},{cly}," +fileStem+"_cell.tif," + savePath + '_rough.tif' + "\n"
            with open(savePath + 'parameters.csv', "a") as file:
                 file.write(line)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def testGratingSimple(savePath='./', display=True):
    
    # create grating object
    gr = grating (nx = 4000, ny = 4000,
                 xdim = 10.0e-6, ydim = 10.00e-6,
                 height=72e-9/1000000,  #GVR HACK TO MAKE mask and roughness map scales similar
                 blockHeight=255,
                 symmetry = 2,
                 rotationCell = 0.0,
                 rotationMask=90,
                 gratingType = 'binary',
                 radius=13.75e-6,
                 period=0.1e-6,
                 VERBOSE =True)
   
    ''' Generate a single mask '''
     
    gr.generateMask()
    gr.setRoughness(tx=5e-8, ty=1e-7,  s=20e-9)   #units in m??
    gr.addRoughnessToMaskEverywhere()
    #gr.addRoughnessToMaskSubstrate()
#    gr.addRoughnessToMaskLines()


    if display is True:
        gr.showCell()
        gr.showMask()
        
    if display is True:
        gr.showRoughness()
        rough.plotHDF(gr.roughness,bins='auto', outFileName='roughness.png')
        acfx, xv,  acfy, yv = rough.getACF(gr.roughness,gr.X,gr.Y,lags=gr.nx/5)
        rough.plotACF(acfx,xv)
        rough.plotACF(acfy,yv)
        corrx, corry = rough.getCorrelationLength(acfx,xv), rough.getCorrelationLength(acfy,yv)
        print('Correlation lengths: lx = {} m, ly = {} m'.format(corrx,corry))
            
    if savePath is not None:
        gr.writeMask(savePath  +'ideal_mask.tif')
        print('Wrote {}'.format(savePath +'ideal_mask.tif'))
        gr.writeRoughness( savePath + '/roughness_ideal.tif')
        print('Wrote {}'.format(savePath +'roughness_ideal.tif'))    
     
        gr.writeBlock(savePath + 'block.tif')

        # Make substrate will integrate this better later...
        gr.write(gr.idealSubstrate(),savePath  + 'substrate.tif',norm=False)

    
    
    

def testGrating(savePath='./', display=True):
    
    # create grating object
    gr = grating (nx = 4000, ny = 4000,
                 xdim = 10.0e-6, ydim = 10.00e-6,
                 height= 20e-9/1000000,  #GVR HACK TO MAKE mask and roughness map scales similar
                 blockHeight=255,
                 symmetry = 2,
                 rotationCell = 0.0,
                 rotationMask=90,
                 gratingType = 'binary',
                 radius=13.75e-6,
                 period=0.1e-6,
                 VERBOSE =True)
   
    ''' Generate a single mask 
     !!!!COMMENT OUT IF GENERATING MULTIPLE MASKS!!!!'''
     
#    gr.generateMask()
#    gr.setRoughness(tx=5e-8, ty=1e-7,  s=20e-9)   #units in m??
#    #gr.addRoughnessToMaskEverywhere()
#    #gr.addRoughnessToMaskSubstrate()
#    #gr.addRoughnessToMaskLines()
#
#
#    if display is True:
#        gr.showCell()
#        gr.showMask()
#        
#    if display is True:
#        gr.showRoughness()
#        rough.plotHDF(gr.roughness,bins='auto', outFileName='roughness.png')
#        acfx, xv,  acfy, yv = rough.getACF(gr.roughness,gr.X,gr.Y,lags=gr.nx/5)
#        rough.plotACF(acfx,xv)
#        rough.plotACF(acfy,yv)
#        corrx, corry = rough.getCorrelationLength(acfx,xv), rough.getCorrelationLength(acfy,yv)
#        print('Correlation lengths: lx = {} m, ly = {} m'.format(corrx,corry))
#            
#    if savePath is not None:
#        gr.writeMask('/home/jerome/data/masks/' +'ideal_mask.tif')
#        print('Wrote {}'.format('/home/jerome/data/masks/'+'ideal_mask.tif'))
#        gr.writeRoughness( savePath + '/roughness_ideal.tif')
#        print('Wrote {}'.format('/home/jeromegener/data/masks/'+'roughness_ideal.tif'))

    ''' Generate multiple masks
     !!!!COMMENT OUT IF GENERATING A SINGLE MASK!!!!'''
     
     
    gr.generateMask()   # do this once only

    # write photon block            
    gr.writeMask(savePath + 'vert_mask.tif')

    # write ideal mask (no roughness)
    gr.writeBlock(savePath + 'vert_block.tif')

    # Make substrate will integrate this better later...
    gr.write(gr.idealSubstrate(),savePath  + 'vert_substrate.tif',norm=False)


    numHeights = 5
    numCorrLengths = 5
    inB = list(string.ascii_lowercase)[0:numHeights]
    c_length = [1.0e-9, 5.0e-9, 10.0e-9, 15.0e-9, 25.0e-9]#np.linspace(15.0e-9,5.0e-9,numCorrLengths)    
    Rh = [1.0e-9, 2.0e-9, 5.0e-9, 10.0e-9, 15.0e-9] #np.linspace(45.0e-9,5.0e-9,numHeights)
    sigma=200e-9
    cly = 100e-9

    
     
    # write header to csv file
    with open(savePath + 'parameters.csv', "w") as file:
       #file.write('# Mask parameters.  Num. Heights: {}, Num. Corr. Lengths: {}, path: {}\n'.format(numHeights,numCorrLengths,savePath))
       file.write('index, op_Mask_thick, op_Roughness_thick, roughnessSigma, \
                  roughnesRMS, roughnessCorrLenX, roughnessCorrLenY, \
                  op_Mask_file_path, op_Block_file_path\n')
       

        
    
    for x,L,clx in zip(inB,range(numCorrLengths),c_length):
        for height in Rh:
            
            gr.generateRandomRoughness2D( h=height,sigma=sigma,clx=clx,cly=cly)
            
            maskHeight = np.max(gr.mask)
            rmsRough = np.sqrt(np.mean(gr.roughness[0,:]**2))
            print ('Height of mask: {}, RMS roughness: {}.  Difference = {}'.format(maskHeight, rmsRough, abs(maskHeight-rmsRough)))
        
#            gr.addRoughnessToMaskEverywhere()
            gr.addRoughnessToMaskLines(threshold=0.01)
            
            fileStem = savePath +   f'{height*1e9:.5f}_{clx*1e9:.5f}_{cly*1e9:.5f}'  #    str(round(((height/2)*1e9)-1)) + x 
            
            if display is True:
                #gr.showCell()
                gr.showMask()
                gr.showBlock()
                
            if display is True:
                gr.showRoughness()
                rough.plotHDF(gr.roughness,bins='auto', outFileName= fileStem + '_roughness.png')
                acfx, xv,  acfy, yv = rough.getACF(gr.roughness,gr.X,gr.Y,lags=gr.nx/5)
                rough.plotACF(acfx,xv,outFileName= fileStem + '_ACF_XV.png')
                rough.plotACF(acfy,yv,outFileName= fileStem + '_ACF_YV.png')
                #corrx, corry = rough.getCorrelationLength(acfx,xv), rough.getCorrelationLength(acfy,yv)
                #print('Correlation lengths: lx = {} m, ly = {} m'.format(corrx,corry))
                    
            if savePath is not None:
            
                gr.writeCell(fileStem + '_cell.tif')
                gr.writeMask(fileStem +'_mask.tif')
                gr.writeRoughness(fileStem + '_AbsorberRoughness.tif')
                
                
            line = f"{L},{maskHeight},{height},{sigma},{rmsRough},{clx},{cly}," +fileStem+"_mask.tif," + savePath + 'vert_block.tif' + "\n"
            with open(savePath + 'parameters.csv', "a") as file:
                file.write(line)
                

def diffractionAngle(d, l, theta=0, m = 1):
    # Use grating equation to determine diffraction angle  
    # (m = order; l = lambda, wavelength; d = spacing)
    return np.arcsin(np.sin(theta) - m*l/d)


def wl(E):
        #return wavelength for energy E in keV
        return  12.39e-10/E


def opticalAxisIntercept(d, l, offset, theta=0, m = 1):
    """ return distance from grating plan at which m= 1 order intercepts optical axis
    when grating is displaced by 'offset' from optical axis."""
    
    #tan theta = d / offset   CHECK THIS  46r
    #return offset*np.tan(diffractionAngle(d,l,theta,m))
    return offset / (2*np.tan(diffractionAngle(d,l,theta,m)))

def interferenceGrating():    
    """ Tool for choosing grating dimensions 
    
    SEE SEABERG'S SUMMARY OF PAGANIN ET AL FOR DIVERGENT BEAM CORRECTION TO POSITION OF 
    PLANES FOR PHASE GRATING....FRACTIONAL TALBOT DISTANCES
    """
    pass
    

if __name__ == "__main__":
    
    testGrating(savePath='/user/home/opt/xl/xl/experiments/masks/T20nm_',display=True)
    #testGrating(savePath='/Users/gvanriessen/code/wpg/extensionsjk/experiments/maskPosition21/masks/', display=False)
    #testGrating()
    #pass
    #testMetrics()
    pass