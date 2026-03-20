#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
June 2020

@author: gvanriessen

test grating mask generation and metrics calculation methods


Status: IN DEVELOPMENT/TESTING
"""



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
    
    
    
    
    
    
    