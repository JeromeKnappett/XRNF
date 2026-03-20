
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from skimage import io,  exposure, img_as_uint, img_as_float
from tqdm import tqdm
import os

from matplotlib.pyplot import figure

# figure(figsize=(3,3))
plt.rcParams["figure.figsize"] = (5,4)
plt.rcParams.update({'font.size': 50})

def transmission(wl,T,beta):
    k = (2*np.pi) / wl
    trans = np.exp((-2*k * beta * T)) # np.exp(((-k) / (beta * T))) # changed to -2k from -1k by JK - 29/10/24
    return trans
# %%
def sumImages(path,name,sumNum,imgType=".tif",darkfield=None,average=False,savePath=None,hist=False,show=False,verbose=False):
    """
    Parameters
    ----------
    path : str
        Path to directory containing images.
    name : str
        File name proceeding number.
    sumNum : int
        Number of images to sum.
    imgType : str, optional
        Type of image. The default is ".tif".
    darkfield : str, optional
        Path to directory containing processed darkfield image. The default is None.
    average : bool, optional
        Specify whether to average the images instead of summing. The default is False.
    savePath : str, optional
        Path to directory to save the processed image. The default is None.
    hist : bool, optional
        Specify whether to plot a histogram of intensity values before and after darkfield subtraction. The default is False.
    show : bool, optional
        Specify whether to display processed image. The default is False.
    verbose : bool, optional
        Specify whether to display information of processes. The default is False.

    Returns
    -------
    finalImages: processed images
    iTot: summed intensity for each processed image
    erT: error in summed intensity
    """
    # sorting images in path
    images = []
    for file in os.listdir(path):
        if file.endswith(str(imgType)) and file.startswith(name):
            images.append(file)
    sortSkip = len(name)
    # print(images)
    # print([i[sortSkip:-len(imgType)] for i in images])
    sortedNames = sorted(images, key=lambda x: float(x[sortSkip:-len(imgType)]))
    imgNumbers = [int(i[sortSkip:-len(imgType)]) for i in sortedNames]
    
    # print(imgNumbers)
    # print(sortedNames)
    
    if verbose:
        print(" ")
        print(f"Number of images to process: {len(images)}")
    
    img_list = []
    iTot = []
    erT = []
    finalImages = []
    
    # print(min(imgNumbers))
    # print(max(imgNumbers))
    
    # Looping through the images
    for i in tqdm(range(min(imgNumbers), max(imgNumbers))):
        try:
            # print(path + str(name) + str(i) + str(imgType))
            _path = path + '/' + str(name) + str(i) + str(imgType)
            image = io.imread(_path)
            img_list.append(image)
        except:
            if verbose:
                print(f"Missing image #{i}")
                print(f"Missing image path:   {_path}")
            pass
    # Summing or averaging every sumNum images
        if sumNum != len(images) and i % int(sumNum) == 0 or i+1==max(imgNumbers):
            if verbose:
                print(f"Summing {len(img_list)} images")
            if average:
                img_sum = np.mean(img_list,axis=0)
            else:
                img_sum = np.sum(img_list,axis=0)
            
            # finding total intensity
            iTot.append(np.sum(img_sum))
            # finding error in total intensity
            errorTOT = np.std([np.sum(i) for i in img_list])
            erT.append(errorTOT)
            
            if hist:
                img_before_dfsub = img_sum
            
            if darkfield:
                bg = io.imread(darkfield)
                if verbose:
                    print("Subtracting darkfield... ")
                # Subtracting the averaged darkfield image
                n = np.mean(img_sum[0:100,0:100])/np.mean(bg[0:100,0:100]) 
                print('\n n = ', n)
                img_sum = img_sum - (n*bg)
                print(np.mean(img_sum[0:100,0:100]))
                # seting all values less than 10 to 0 
                # img_sum[abs(img_sum) < 10] = 0
                b = np.where(img_sum < 0, 1, 0)
                print('sum: ', np.sum(b))
                img_sum[img_sum < 1] = 0
                # print(np.min(img_sum))
        
            if hist:
                bg[0,0] = np.max(img_before_dfsub)
                jk = (img_sum[0,0],img_sum[1,0])
                img_sum[0,0] = 0
                img_sum[1,0] = np.max(img_before_dfsub)
                numBins = 200
                #plot the histogram of intensity before darkfield subtraction
                counts,bins = np.histogram(img_before_dfsub,bins=numBins)
                # Using non-equal bin sizes, such that they look equal on a log scale
                # logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
                fig,ax = plt.subplots(3,1,sharey=False,sharex=True)
                ax[0].hist(bins[:-1],bins=bins,weights=counts)
                ax[0].set_title('Raw image')
                #overplot the histogram of intensity after bg subtraction.
                counts,bins = np.histogram(img_sum,bins=bins)
                # logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
                ax[1].hist(bins[:-1],bins=bins,weights=counts)
                ax[1].set_title('Processed image')
                counts,bins = np.histogram(bg,bins=bins)
                # logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
                ax[2].hist(bins[:-1],bins=bins,weights=counts)
                # ax[2].hist(bg)
                ax[2].set_title('Background')
                # for a in ax:
                #     a.set_xscale('log')
                fig.tight_layout()
                plt.show()
                
                img_sum[0,0] = jk[0]
                img_sum[1,0] = jk[1]
                
            
            if show:
                plt.imshow(img_sum,aspect='auto')
                plt.colorbar()
                plt.xlabel('x')
                plt.ylabel('y')
                plt.show()
                
            if savePath:            
                # Save the summed images with subtracted bg to disk
                print(f'Saving processed image to: {savePath + str(i) + imgType}')
                io.imsave(savePath + '/' + str(i) + imgType,  img_sum.astype(np.uint16))

            finalImages.append(img_sum)
            img_sum = np.zeros_like(img_sum)
            img_list = []
        
    return finalImages, iTot, erT
# %%
def findCorrelation(path,imgType,name,area=None,show=True,verbose=True):
    from tqdm import tqdm
    from scipy import signal
    import cv2
    
    # sorting images in path
    images = []
    for file in os.listdir(path):
        if file.endswith(str(imgType)):
            images.append(file)
    sortSkip = len(name)
    sortedNames = sorted(images, key=lambda x: float(x[sortSkip:-len(imgType)]))
    imgNumbers = [int(i[sortSkip:-len(imgType)]) for i in sortedNames]
    
    if verbose:
        print(f"Number of images to process: {len(images)}")
    
    C = []
    
    # loading 1st image - cropping if area is specified
    if area:
        image1 = io.imread(path + str(name) + str(min(imgNumbers)) + str(imgType))
        image1 = image1[(np.shape(image1)[0] - area[1])//2:(np.shape(image1)[0] + area[1])//2,
                        (np.shape(image1)[1] - area[0])//2:(np.shape(image1)[1] + area[0])//2]
    else:
        image1 = io.imread(path + str(name) + str(min(imgNumbers)) + str(imgType))
    
    # Looping through the images
    for i in tqdm(range(min(imgNumbers), max(imgNumbers))):
        try:
            image = io.imread(path + str(name) + str(i) + str(imgType))
            if area:
                image = image[(np.shape(image)[0] - area[1])//2:(np.shape(image)[0] + area[1])//2,
                              (np.shape(image)[1] - area[0])//2:(np.shape(image)[1] + area[0])//2]
        except:
            if verbose:
                print(f"Missing image #{i}")
            pass        
        cor = np.mean(signal.correlate2d (image1, image))
        # cor2 = np.mean(cv2.filter2D(image1, ddepth=-1, kernel=image))
        C.append(cor)
        # C2.append(cor2)
        
    if show:
        plt.plot(C,label='1')
        plt.xlabel('Image Number')
        plt.ylabel('Correlation to Image #1')
        # plt.legend()
        plt.show()
    
    return C
# %%
def cropImage(image,x0,y0,xL,yL):
    """
    Parameters
    ----------
    image : 2D array
        input image for cropping
    x0 : int
        center pixel x-coordinate.
    y0 : int
        center pixel y-coordinate.
    xL : int
        length of new image in x (pixels).
    yL : int
        length of new image in y (pixels).

    Returns
    -------
    im : 2D array
        cropped image.
    """
    im = image[y0-(yL//2):y0+(yL//2),x0-(xL//2):x0+(xL//2)]
    return im
# %%
def IoverGrating(image,GA,dx,dy,show=False):
    """
    Parameters
    ----------
    image : 2D array
        image for processing.
    GA : float
        1D size of grating area (assuming square grating).
    dx : float
        image resolution in x.
    dy : float
        image resolution in x.
    show : bool, optional
        Specify whether to show grating area over image. The default is False.

    Returns
    -------
    Gsum : float
        summed intensity over 4-grating area.
    Csum : float
        summed intensity over central area (equal to single grating size).
    S : float
        Intensity slope over grating area (definition taken from Meng et al - J. Synchrotron Rad. (2021). 28, 902-909
                                           https://doi.org/10.1107/S1600577521003398)
    """
    from utilMask_n import defineOrderROI
    from usefulWavefield import round_sig
    
    lX, lY = int(GA/dx),int(GA/dy)
    G, Isum = defineOrderROI(image,res=(dx,dy),
                             m=1,dX=lX,dY=lY,show=False)
    _G,_Isum = defineOrderROI(np.rot90(image),res=(dx,dy),
                              m=1,dX=lX,dY=lY,show=False)
        
    Gsum = Isum[1] + Isum[2] + _Isum[1] + _Isum[2]
    Csum = Isum[0]
    
    # defining ROIs for grating areas
    nx,ny = np.shape(image)[1],np.shape(image)[0]
    numXticks, numYticks = 15,15
    sF = 1e3
    midX,midY = np.shape(image)[1]//2, np.shape(image)[0]//2
    
    # plt.imshow(image,aspect='auto')
    # plt.show()
    
    ROI_0 = ((int((midX)-(lX/2)),int((midY) - (lY/2))),((int((midX)+(lX/2))),int((midY) + (lY/2))))   
    ROI_r = ((ROI_0[1][0], int((midY) - (lY/2)))), (ROI_0[1][0] + lX, int((midY) + (lY/2)))
    ROI_l = ((ROI_0[0][0] - lX, int((midY) - (lY/2)))),(ROI_0[0][0], int((midY) + (lY/2)))
    ROI_u = ((int((midX)-(lX/2)), ROI_0[1][1]),((int((midX)+(lX/2))), ROI_0[1][1] + lY))
    ROI_d = ((int((midX)-(lX/2)), ROI_0[0][1]-lY),((int((midX)+(lX/2))), ROI_0[0][1]))
    
    # getting intensity slopes over each grating area
    g0 = image[ROI_0[0][1]:ROI_0[1][1],ROI_0[0][0]:ROI_0[1][0]]
    gr = image[ROI_r[0][1]:ROI_r[1][1],ROI_r[0][0]:ROI_r[1][0]]
    gl = image[ROI_l[0][1]:ROI_l[1][1],ROI_l[0][0]:ROI_l[1][0]]
    gu = image[ROI_u[0][1]:ROI_u[1][1],ROI_u[0][0]:ROI_u[1][0]]
    gd = image[ROI_d[0][1]:ROI_d[1][1],ROI_d[0][0]:ROI_d[1][0]]
    
    # if show:
    #     fig,ax = plt.subplots(2,2)
    #     ax[0,0].imshow(gl,aspect='auto')
    #     ax[0,0].set_title('left')
    #     ax[0,1].imshow(gu,aspect='auto')
    #     ax[0,1].set_title('top')
    #     ax[1,0].imshow(gd,aspect='auto')
    #     ax[1,0].set_title('bottom')
    #     ax[1,1].imshow(gr,aspect='auto')
    #     ax[1,1].set_title('right')
    #     plt.show()
        
    #     print(np.shape(gr))
    #     print(np.shape(gl))
    #     print(np.shape(gu))
    #     print(np.shape(gd))
    
    s0 = (np.max(g0)-np.min(g0)) / (np.max(g0) + np.min(g0))
    sr = (np.max(gr)-np.min(gr)) / (np.max(gr) + np.min(gr))
    sl = (np.max(gl)-np.min(gl)) / (np.max(gl) + np.min(gl))
    su = (np.max(gu)-np.min(gu)) / (np.max(gu) + np.min(gu))
    sd = (np.max(gd)-np.min(gd)) / (np.max(gd) + np.min(gd))
    
    S = np.max([sr,sl,su,sd])
    
    if show:
        import matplotlib.patches as patches
    
        figure, ax = plt.subplots(1)
        rect_r = patches.Rectangle((ROI_r[0][0],ROI_r[0][1]),lX,lY, edgecolor='r', facecolor="none",hatch='|||')
        rect_l = patches.Rectangle((ROI_l[0][0],ROI_l[0][1]),lX,lY, edgecolor='r', facecolor="none",hatch='|||')
        rect_u = patches.Rectangle((ROI_u[0][0],ROI_u[0][1]),lX,lY, edgecolor='r', facecolor="none",hatch='---')
        rect_d = patches.Rectangle((ROI_d[0][0],ROI_d[0][1]),lX,lY, edgecolor='r', facecolor="none",hatch='---')
        # plt.imshow(A_0,aspect='auto')
        plt.imshow(image,aspect='auto')
        ax.add_patch(rect_r)
        ax.add_patch(rect_l)
        ax.add_patch(rect_u)
        ax.add_patch(rect_d)
        # plt.title('E = ' + str(90 + (count*10)) + ' eV')
        plt.colorbar(label='Intensity [ph/s/cm$^2$]')#[counts]')
        plt.yticks([int((ny-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],
                   [round_sig(ny*dy*(a/(numYticks-1.0))*sF,1) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=10)
        plt.xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],
                   [round_sig(nx*dx*(a/(numXticks-1.0))*sF,1) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=10)
        plt.xlabel('x [mm]')
        plt.ylabel('y [mm]')
        plt.xlim(midX-100,midX+100)
        plt.ylim(midY-100,midY+100)
        plt.show()
    
    return Gsum, Csum, S
# %%
def test():
    from usefulWavefield import counts2photonsPsPcm2, intensity2power, findBeamCenter, counts2photonsPs, photonsPs2counts
    # from usefulGrating import defineOrderROI
    from FWarbValue import getFWatValue
    import pickle 
    from pathlib import Path
    
    # Location of the images
    imageFolder = '/user/home/data/HarmonicContam/Detector_Comission_August_2023/Beam_profile_90_to_350eV_fixed_slits_cff1.4/'
    #'/user/home/data/HarmonicContam/Detector_Comission_August_2023/Beam_profile_90_to_350eV_attempt2/'
    darkFolder = '/user/home/data/HarmonicContam/Detector_Comission_August_2023/Darkfields2/'
    savePath_images ='/user/home/data/HarmonicContam/Detector_Comission_August_2023/ProcessedImages/BeamProfile_90to350_cff1.4_fixedslits/'
    savePath_dark = '/user/home/data/HarmonicContam/Detector_Comission_August_2023/ProcessedImages/darkfield/'
    savePath_plots = '/user/home/data/HarmonicContam/plots/'
    #None
    fmat='jpg'
    
    simFolder = '/user/home/data/HarmonicContam/Detector_Comission_August_2023/SimulatedIntensity/'
    fitFolder = savePath_images + 'fitsWerr/'
    compareSim = True
    compareFits = True
    gratingArea = True
    pickleResults = False
    
    processImages = False
    processDarkfield = False
    cropImages = True
    findCenter = False
    saveNormalised = False
    justUseFits = True
    
    exposures = 10  # chenged from 100 for uncertainty analysis of fits
    exposure_time = 50e-3
    energy_range0 =  [90,92] + [e for e in np.arange(100, 185,10)] + [185] + [e for e in np.arange(190, 355,10)]
    energy_range = np.repeat(energy_range0,10)
    eLim = (np.min(energy_range0)-10,np.max(energy_range0)+10)
    
    Ga = 50.0e-6
    
    # Creating directories for processed images
    Path(savePath_images + 'normalised_unc/').mkdir(parents=True, exist_ok=True)
    Path(savePath_images + 'averaged_unc/').mkdir(parents=False, exist_ok=True)
    
    if justUseFits:
        pass
    else:
        if processDarkfield:
            print("\n Averaging darkfield images...")
            # sumImages(darkFolder,sumNum=4000,sortSkip=7,imgType=".tif",average=True,darkfield=None,savePath=savePath_dark,show=True,verbose=True)
            sumImages(darkFolder,name='beam_1_',sumNum=3999,imgType='.tif',average=True,
                                  darkfield=None,
                                  savePath=savePath_dark,hist=False,verbose=True,show=True)
        if processImages:
            print("\n Summing/Averaging images...")
            ims,iTot,er = sumImages(imageFolder,name='beam_1_',sumNum=exposures,imgType=".tif",average=True,
                                    darkfield=savePath_dark + '3998.tif',
                                    savePath=savePath_images,hist=True,verbose=True,show=True)
            pEr = [e/i for e,i in zip(er,iTot)] # percentage error for summed intensities
        else:
            print("\n Loading pre-processed images...")
            try:
                imgNums = [e for e in np.arange(exposures,exposures*(len(energy_range)-1),exposures)] + [exposures*len(energy_range)-1]
                # print(imgNums)
                ims = [io.imread(savePath_images + str(i) + '.tif') for i in imgNums]
            except FileNotFoundError:
                pass
            try:
                imgNums = [e for e in np.arange(exposures,exposures*(len(energy_range)),exposures)] + [exposures*len(energy_range)-3]
                # print(imgNums)
                ims = [io.imread(savePath_images + str(i) + '.tif') for i in imgNums]
            except:
                pass
            # print(imgNums)
            ims = [io.imread(savePath_images + str(i) + '.tif') for i in imgNums]
            iTot = [np.sum(i) for i in ims]
            pEr = np.zeros_like(imgNums)
            plt.imshow(ims[0],aspect='auto')
            plt.colorbar()
            plt.show()
        
        if cropImages:
            # defining new ROI for images
            x0,y0 = 590,382
            xL,yL = 800,700 #520, 380
            
            # cropping images to assist with finding the beam center
            ims = [cropImage(i, x0, y0, xL, yL) for i in ims]
            plt.imshow(ims[0],aspect='auto')
            plt.colorbar()
            plt.show()
    
        if findCenter:    
            print(" ")
            print("Finding Beam Center...")
            # finding beam center for each image
            cX,cY = [],[]
            for i in tqdm(ims):
                cx,cy = findBeamCenter(i,show=False)
                # print(cx,cy)
                cX.append(int(cx))
                cY.append(int(cy))
                # print(energy_range)
                # print(len(cX))
            plt.errorbar(energy_range,[(c-cX[0])*11.0 for c in cX],yerr=5.5,fmt='.',label='x')
            plt.errorbar(energy_range,[(c-cY[0])*11.0 for c in cY],yerr=5.5,fmt='.',label='y')
            plt.ylabel('Beam center drift [$\mu$m]')
            plt.xlabel('Photon energy [eV]')
            # plt.yscale('log')
            # plt.xlim(80,250)
            plt.legend()
            plt.show()
            # cropping images again to center them with the calculated beam center
            ims = [cropImage(i,xc,yc,xL-25,yL-25) for i,xc,yc in zip(ims,cX,cY)]
        else:
            cX,cY = [0],[0]
        
        
        # for xc,yc in zip(cX,cY):
        #     if xc-(xL-25) <= 0:
        #         print('ERROR!! LENGTH OF NEW CROPPED IMAGE IS TOO LARGE! REDUCE IN X')
        #     if yc-(yL-25) <= 0:
        #         print('ERROR!! LENGTH OF NEW CROPPED IMAGE IS TOO LARGE! REDUCE IN Y')
        
        if saveNormalised:
            for e,i in enumerate(ims):
                IN = (i/np.max(i))*65535
                io.imsave(savePath_images + '/normalised/' + str(e) + '.tif',  IN.astype(np.uint16))
                io.imsave(savePath_images + '/averaged/' + str(e) + '.tif',  i.astype(np.uint16))
        # print('\n GOT HERE')
        
        # # converting cropped images from detector counts to ph/s/cm^2
        # ims = [counts2photonsPsPcm2(i, e, t=60.0e-3, res=(11.0e-6,11.0e-6), conversion=1.27) for i,e in zip(ims,energy_range)]
        # # converting from ph/s/cm^2 to mJ/s/cm^2
        # Pims = [intensity2power(i, e) for i,e in zip(ims,energy_range)]
        # converting cropped images from detector counts to ph/s
        ims = [counts2photonsPs(i, e, t=exposure_time, conversion=1.27) for i,e in zip(ims,energy_range)]
        # converting from ph/s to mJ/s
        Pims = [intensity2power(i, e) for i,e in zip(ims,energy_range)]
        
        Rx,Ry = np.shape(ims[0])[1]*11.0e-6, np.shape(ims[0])[0]*11.0e-6   # range in meters
        # print("\n range:    ", (Rx,Ry))
        # print("shape of I:  ", np.shape(ims[0]))
        # finding new total intensity (in ph/s/cm^2)
        iTot = [(np.sum(i)/(Rx*Ry*10000)) for i in ims]                      
        er = [p*i for p,i in zip(pEr,iTot)]
        # finding total power (in mJ/s/cm^2)
        pTot = [np.sum(p)/(Rx*Ry) for p in Pims]
        erP = [p*i for p,i in zip(pEr,pTot)]
        
        # finding total intensity and intensity slope over grating area
        # finding FWHM of intensity profile
        gsums, csums, S = [],[],[]
        fwhmX,fwhmY = [],[]
        fwXs,fwYs = [],[]
        # print(" ")
        # print(" ")
        for e,i in enumerate(tqdm(ims)):
            # print(f"number {e}")
            if e==0 or e==9:
                # print('Energy = ', energy_range)
                gs,cs,s = IoverGrating(i, GA=Ga, dx=11.0e-6, dy=11.0e-6,show=False)
            else:
                gs,cs,s = IoverGrating(i, GA=Ga, dx=11.0e-6, dy=11.0e-6,show=False)
                
            # gsPcm = gs/(4*(Ga*Ga))
            gsums.append((gs/(4*Ga*Ga*10000)))
            csums.append((cs/(Ga*Ga*10000)))
            S.append(s)
            
            FWHMx,FWHMy = getFWatValue(i, dx=11.0e-6, dy=11.0e-6,averaging=10,verbose=False,show=False)
            fwhmX.append(FWHMx)
            fwhmY.append(FWHMy)
            if e <= 20:
                FWHMx_sm, FWHMy_sm = getFWatValue(i, dx=11.0e-6, dy=11.0e-6,averaging=10,smoothing='gauss',sparams=100,verbose=False,show=False)
            else:
                FWHMx_sm, FWHMy_sm = getFWatValue(i, dx=11.0e-6, dy=11.0e-6,averaging=10,smoothing='gauss',verbose=False,show=False)
            # FWHMx_sm, FWHMy_sm = getFWatValue(i, dx=11.0e-6, dy=11.0e-6,averaging=10,smoothing='multigauss',show=False)
            fwXs.append(FWHMx_sm)
            fwYs.append(FWHMy_sm)
        # gsums,csums = [IoverGrating(i, GA=Ga, dx=11.0e-6, dy=11.0e-6,show=True) for i in ims]
        
        
    # Loading simulated intensity tiffs
    IGAeuv, IGAbeuv = [],[]
    PGAeuv, PGAbeuv = [],[]
    ItotEUV, ItotBEUV = [],[]
    PtotEUV, PtotBEUV = [],[]
    _Itot,_IGA = [],[]
    ItotB3 = []
    ItotE2,ItotE3 = [],[]
    
    if compareSim:
        import pickle
        
        # xi = -0.02137955022242362 #Initial Horizontal Position [m]
        # xf = 0.021379682150308235 #Final Horizontal Position [m]
        # nx = 4800 #Number of points vs Horizontal Position
        # yi = -0.020631900305629326 #Initial Vertical Position [m]
        # yf = 0.02063190030562931 #Final Vertical Position [m]
        # ny = 4800 #Number of points vs Vertical Position
        
        
        xi = -0.01032586942694636 #Initial Horizontal Position [m]
        xf = 0.010321702563965631 #Final Horizontal Position [m]
        nx = 4800 #Number of points vs Horizontal Position
        yi = -0.0214047430202834 #Initial Vertical Position [m]
        yf = 0.021404743020283393 #Final Vertical Position [m]
        ny = 4800 #Number of points vs Vertical Position
        
        #m3 - 185
        xi3 = -0.01431819301721686 #Initial Horizontal Position [m]
        xf3 = 0.014318220491716497 #Final Horizontal Position [m]
        nx3 = 1600 #Number of points vs Horizontal Position
        yi3 = -0.009279698257955722 #Initial Vertical Position [m]
        yf3 = 0.009279698257955722 #Final Vertical Position [m]
        ny3 = 1600 #Number of points vs Vertical Position
        
        # 250
        xi250 = -0.014582147476253046 #Initial Horizontal Position [m]
        xf250 = 0.01458220090618856 #Final Horizontal Position [m]
        nx250 = 1600 #Number of points vs Horizontal Position
        yi250 = -0.007516856751866583 #Initial Vertical Position [m]
        yf250 = 0.007516856751866588 #Final Vertical Position [m]
        ny250 = 1600 #Number of points vs Vertical Position
        
        xi135 = -0.014042709362348353 #Initial Horizontal Position [m]
        xf135 = 0.014043775691892767 #Final Horizontal Position [m]
        yi135 = -0.009444411376325134 #Initial Vertical Position [m]
        yf135 = 0.00944441137632513 #Final Vertical Position [m]
        
        
        
        EUVpick = pickle.load(open(simFolder + 'EUV/SE_cff1.4offset0_m1_fixed.pkl','rb')) # 'EUVbeamProfile/data/m1_atMask_ME/m1_atMask_ME.pkl', 'rb')) #'EUVbeamProfile/data/check2/atMask_ME/atMask_ME.pkl', 'rb'))
        # EUVres = ((xf-xi)/nx, (yf-yi)/ny) #(EUVpick[1],EUVpick[2])
        # m3res = ((xf3-xi3)/nx3, (yf3-yi3)/ny3)
        EUVtiff = EUVpick[0] 
        EUVres = (EUVpick[1],EUVpick[2])
        EUVtiff_SE =  io.imread(simFolder + 'EUV/SE_cff1.4offset0_m1_LF_sx40sy30_highres.tif')
        BEUVpick = pickle.load(open(simFolder + 'BEUV/ME_cff1.4offset0_m1_LF_sx25sy25_highres.pkl', 'rb')) #'BEUVbeamProfile/data/m1_atMask_ME/m1_atMask_ME.pkl', 'rb'))
        BEUVres = (BEUVpick[1],BEUVpick[2])
        BEUVtiff = BEUVpick[0]
        BEUVtiff_SE = io.imread(simFolder + 'BEUV/SE_cff1.4offset0_m1_LF_sx40sy30_highres.tif')
        
        B3pick =  pickle.load(open(simFolder + 'BEUV/SE_cff1.4offset0_m3.pkl', 'rb'))
        B3 = B3pick[0]#io.imread(simFolder + 'BEUV/SE_cff1.4offset0_m3_LF.tif')
        m3res = (B3pick[1],B3pick[2])
        
        E2pick = pickle.load(open(simFolder + 'EUV/SE_cff1.4offset0_m2_roughM.pkl','rb'))
        E3pick = pickle.load(open(simFolder + 'EUV/SE_cff1.4offset0_m3_roughM.pkl','rb'))
        E2tiff = E2pick[0]
        E3tiff = E3pick[0]
        E2res = (E2pick[1],E2pick[2])
        E3res = (E3pick[1],E3pick[2])
        
        pick135 = pickle.load(open(simFolder + '135_cff1.4offset0_m1_sx25sy25_highres.pkl', 'rb'))
        pick250 = pickle.load(open(simFolder + '250_cff1.4offset0_m1_sx25sy25_highres.pkl', 'rb'))
        
        res135 = (pick135[1],pick135[2]) #((xf135-xi135)/nx250, (yf135-yi135)/ny250)
        res250 = (pick250[1],pick250[2]) #((xf250-xi250)/nx250, (yf250-yi250)/ny250)
        tiff135 = pick135[0] #io.imread(simFolder + 'SE_135_cff1.4offset0_m1_LF_sx40sy30_highres.tif')
        tiff250 = pick250[0] #io.imread(simFolder + 'SE_250_cff1.4offset0_m1_LF_sx40sy30_highres.tif')
            
        EUVranPix = [(11.0e-6 / EUVres[0]) * 800, (11.0e-6 / EUVres[1]) * 700]  
        BEUVranPix = [(11.0e-6 / BEUVres[0]) * 800, (11.0e-6 / BEUVres[1]) * 700]  
        EUVranPix_SE = [(11.0e-6 / EUVres[0]) * 800, (11.0e-6 / EUVres[1]) * 700]  
        BEUVranPix_SE = [(11.0e-6 / BEUVres[0]) * 800, (11.0e-6 / BEUVres[1]) * 700]  
        
        E2ranPix = [(11.0e-6 / E2res[0]) * 800, (11.0e-6 / E2res[1]) * 700]  
        E3ranPix = [(11.0e-6 / E3res[0]) * 800, (11.0e-6 / E3res[1]) * 700]  
        
        
        print('\n EUVranPix: ', EUVranPix)
        print(np.shape(EUVtiff))
        print(EUVres)
        print('\n')
        
        # EUVranPix = [np.shape(EUVtiff)[1],np.shape(EUVtiff)[0]] #xL*11e-6,yL*11e-6]#[5.0e-3,6.6e-3]
        # EUVranPix_SE = [np.shape(EUVtiff_SE)[1],np.shape(EUVtiff_SE)[0]] #xL*11e-6,yL*11e-6]#[5.0e-3,6.6e-3]
        # BEUVranPix = [np.shape(BEUVtiff)[1],np.shape(BEUVtiff)[0]]
        # BEUVranPix_SE = [np.shape(BEUVtiff_SE)[1],np.shape(BEUVtiff_SE)[0]]
        RxEUV,RyEUV = EUVranPix[0]*EUVres[0], EUVranPix[1]*EUVres[1]
        RxEUV_SE,RyEUV_SE = EUVranPix_SE[0]*EUVres[0], EUVranPix_SE[1]*EUVres[1]
        RxBEUV,RyBEUV = BEUVranPix[0]*BEUVres[0], BEUVranPix[1]*BEUVres[1]
        RxBEUV_SE,RyBEUV_SE = BEUVranPix_SE[0]*BEUVres[0], BEUVranPix_SE[1]*BEUVres[1]
        RxB3,RyB3 = np.shape(B3)[1]*m3res[0],np.shape(B3)[0]*m3res[1]
        
        Rx135,Ry135 = np.shape(tiff135)[1]*res135[0],np.shape(tiff135)[0]*res135[1]
        Rx250,Ry250 = np.shape(tiff250)[1]*res250[0],np.shape(tiff250)[0]*res250[1]
        
        RxE2,RyE2 = E2ranPix[0]*E2res[0], E2ranPix[1]*E2res[1]
        RxE3,RyE3 = E3ranPix[0]*E3res[0], E3ranPix[1]*E3res[1]
        
        EUVran = [eran*eres for eran,eres in zip(EUVranPix,EUVres)] #[ran[0]/EUVres[0], ran[1]/EUVres[1]]
        BEUVran = [bran*bres for bran,bres in zip(BEUVranPix,BEUVres)] #[ran[0]/BEUVres[0], ran[1]/BEUVres[1]]
        
        EUVtiff = EUVtiff[int(np.shape(EUVtiff)[0]//2 - EUVranPix[1]//2):int(np.shape(EUVtiff)[0]//2 + EUVranPix[1]//2),
                          int(np.shape(EUVtiff)[1]//2 - EUVranPix[0]//2):int(np.shape(EUVtiff)[1]//2 + EUVranPix[0]//2)]
        BEUVtiff = BEUVtiff[int(np.shape(BEUVtiff)[0]//2 - BEUVranPix[1]//2):int(np.shape(BEUVtiff)[0]//2 + BEUVranPix[1]//2),
                            int(np.shape(BEUVtiff)[1]//2 - BEUVranPix[0]//2):int(np.shape(BEUVtiff)[1]//2 + BEUVranPix[0]//2)]
        
        BEUVtiff_SE = BEUVtiff_SE[int(np.shape(BEUVtiff_SE)[0]//2 - BEUVranPix_SE[1]//2):int(np.shape(BEUVtiff_SE)[0]//2 + BEUVranPix_SE[1]//2),
                                  int(np.shape(BEUVtiff_SE)[1]//2 - BEUVranPix_SE[0]//2):int(np.shape(BEUVtiff_SE)[1]//2 + BEUVranPix_SE[0]//2)]
        EUVtiff_SE = EUVtiff_SE[int(np.shape(EUVtiff_SE)[0]//2 - EUVranPix_SE[1]//2):int(np.shape(EUVtiff_SE)[0]//2 + EUVranPix_SE[1]//2),
                          int(np.shape(EUVtiff_SE)[1]//2 - EUVranPix_SE[0]//2):int(np.shape(EUVtiff_SE)[1]//2 + EUVranPix_SE[0]//2)]
        
        E2tiff = E2tiff[int(np.shape(E2tiff)[0]//2 - E2ranPix[1]//2):int(np.shape(E2tiff)[0]//2 + E2ranPix[1]//2),
                        int(np.shape(E2tiff)[1]//2 - E2ranPix[0]//2):int(np.shape(E2tiff)[1]//2 + E2ranPix[0]//2)]
        E3tiff = E3tiff[int(np.shape(E3tiff)[0]//2 - E3ranPix[1]//2):int(np.shape(E3tiff)[0]//2 + E3ranPix[1]//2),
                        int(np.shape(E3tiff)[1]//2 - E3ranPix[0]//2):int(np.shape(E3tiff)[1]//2 + E3ranPix[0]//2)]
        
        
        print(np.shape(EUVtiff))
        print(RxEUV, RyBEUV)
        print(800*11.0e-6, 700*11.0e-6)
        
        # tiff135 = tif135[int(np.shape(tiff135)[0]//2 - )]
        
        # convering from ph/s/0.1%bw/mm^2 to ph/s/mm^2
        grad = 0.000396378#*0.628324754030457
        intercept = 0.019051304
        slv = (2/1.4)*25
        bw = (slv*grad) + intercept
        bw = bw/0.1
        
        print('\n BW: ', bw)
        
        # EUVeff = 1 #0.03737340348858282
        # BEUVeff = 1 #0.004297207161730262
        # eff135 = 1 # 0.02216367235357039
        # eff250 = 1 #0.0005147820098211518
        B3eff = 0.00010163140848318428 # 0.1% efficiency 
        # 0.000203262816966 # 0.2% efficiency
        # 0.0005081570424159213 # 0.5% efficiency 
                #0.00017687707698421477
                #0.001725356423529401*0.1
                # 0.001725356423529401
        E2eff = 0.00024132746916089536 # 1% efficiency
        E3eff = 5.6163758561068015e-05 # 0.1% efficiency
        
        eff = [0.0780993513893524, 0.0720164819623943, 0.03267384491294766, 0.01650402498848851]   # cff = 1.4, eff = 10%
        # [0.07526344876708212, 0.06850128058818172, 0.027501275406876923, 0.0128083554597108] # cff = 1.4, eff = 10% OLD ANGLE VALUES
        # [0.3737340348858282, 0.2216367235357039, 0.04297207161730261, 0.005147820098211518]
        # [0.07526344876708212, 0.06850128058818172, 0.027501275406876923, 0.0128083554597108]
        # [0.03737340348858282, 0.02216367235357039, 0.004297207161730262, 0.0005147820098211518]
        #[0.37631724383541054, 0.3425064029409086, 0.13750637703438462, 0.064041777298554]
        # B3eff =  0.0035375415396842955*0.001
        #1.7253564235294013e-06 #0.017687707698421474
        
        # 0.03737340348858282, 0.02216367235357039, 0.004297207161730262, 0.0005147820098211518
        
        print('\n')
        print(bw)
        BEUVtiff = BEUVtiff * (bw) * eff[2] #BEUVeff
        BEUVtiff_SE = BEUVtiff_SE * (bw) * eff[2] #BEUVeff
        EUVtiff = EUVtiff * (bw) * eff[0] #EUVeff
        EUVtiff_SE = EUVtiff_SE * (bw) * eff[0] #EUVeff
        
        B3 = B3 * bw * B3eff
        
        E2tiff = E2tiff * bw * E2eff
        E3tiff = E3tiff * bw * E3eff
        
        tiff135 = tiff135 * bw * eff[1] #135
        tiff250 = tiff250 * bw * eff[3] #250
        
        exFluxB1 = 3.5e9 * (3000 - 40) * bw * eff[2]
        exFluxE1 = 3.5e9 * (3000 - 40) * bw * eff[0]
        exFluxB3 = 3.5e9 * (3000 - 40) * bw * B3eff
        exFlux135 = 3.5e9 * (3000 - 40) * bw * eff[1]
        exFlux250 = 3.5e9 * (3000 - 40) * bw * eff[3]
        
        # # convering from ph/s/0.1%bw/mm^2 to ph/s/mm^2
        # BEUVtiff = BEUVtiff * (0.1 / (25*0.396378 + 0.019051304))
        # BEUVtiff_SE = BEUVtiff_SE * (0.1 / (25*0.396378 + 0.019051304))
        # # EUVtiff = EUVtiff * (0.1 / (25*0.396378 + 0.019051304))
        # EUVtiff_SE = EUVtiff_SE * (0.1 / (25*0.396378 + 0.019051304))
        
        # converting from ph/s/mm^2 to ph/s
        EUVtiff = (EUVtiff/1.0e-6)*(EUVres[0]*EUVres[1])
        BEUVtiff =  (BEUVtiff/1.0e-6)*(BEUVres[0]*BEUVres[1]) 
        # BEUVtiff_SE =  BEUVtiff_SE*100
        BEUVtiff_SE = BEUVtiff_SE*(BEUVres[0]*BEUVres[1]) / 1.0e-6 
        EUVtiff_SE = EUVtiff_SE*(EUVres[0]*EUVres[1]) / 1.0e-6 
        B3 = B3 * (m3res[0]*m3res[1]) / 1.0e-6
        tiff135 = tiff135*(res135[0]*res135[1]) / 1.0e-6
        tiff250 = tiff250*(res250[0]*res250[1]) / 1.0e-6
        
        E2tiff = (E2tiff/1.0e-6)*(E2res[0]*E2res[1])
        E3tiff = (E3tiff/1.0e-6)*(E3res[0]*E2res[1])
        
        # convering from ph/s/0.1%bw to ph/s
        # BEUVtiff = BEUVtiff*
        
        # plt.imshow(BEUVtiff_SE,aspect='auto')
        # plt.colorbar()
        # plt.show()
        
        EUVfwhmx,EUVfwhmy = getFWatValue(EUVtiff,frac=0.5,dx=EUVres[0],dy=EUVres[1],cuts='xy',
                                          centered=True,smoothing='gauss',
                                          verbose=False,show=True)
        EUVfwhmxSE,EUVfwhmySE = getFWatValue(EUVtiff_SE,frac=0.5,dx=EUVres[0],dy=EUVres[1],cuts='xy',
                                             centered=True,smoothing=None,
                                             verbose=False,show=True)
        BEUVfwhmx,BEUVfwhmy = getFWatValue(BEUVtiff,frac=0.5,dx=BEUVres[0],dy=BEUVres[1],cuts='xy',
                                           centered=True,smoothing=None,
                                           verbose=False,show=True)
        BEUVfwhmxSE,BEUVfwhmySE = getFWatValue(BEUVtiff_SE,frac=0.5,dx=BEUVres[0],dy=BEUVres[1],cuts='xy',
                                               centered=True,smoothing=None,
                                               verbose=False,show=True)
    
        
        B3fwhmx,B3fwhmy = getFWatValue(B3,frac=0.5,dx=m3res[0],dy=m3res[1],cuts='xy',
                                           centered=True,smoothing=None,
                                           verbose=False,show=True)
        
        fwhmx135,fwhmy135 = getFWatValue(tiff135,frac=0.5,dx=res135[0],dy=res135[1],cuts='xy',
                                         centered=True,smoothing=None,
                                         verbose=False,show=True)
        fwhmx250,fwhmy250 = getFWatValue(tiff250,frac=0.5,dx=res250[0],dy=res250[1],cuts='xy',
                                         centered=True,smoothing=None,
                                         verbose=False,show=True)
    
    
        E2fwhmx,E2fwhmy = getFWatValue(E2tiff,frac=0.5,dx=E2res[0],dy=E2res[1],cuts='xy',
                                       centered=True,smoothing=None,
                                       verbose=False,show=True)
        E3fwhmx,E3fwhmy = getFWatValue(E3tiff,frac=0.5,dx=E3res[0],dy=E3res[1],cuts='xy',
                                       centered=True,smoothing=None,
                                       verbose=False,show=True)
    
        q = 1.60218e-19
        ItotEUV.append(np.sum(EUVtiff))# + exFluxE1)#/(RxEUV*RyEUV*10000))
        ItotEUV.append(np.sum(EUVtiff_SE))# + exFluxE1)#/(RxEUV_SE*RyEUV_SE*10000))
        ItotBEUV.append(np.sum(BEUVtiff))# + exFluxB1)#/(RxBEUV*RyBEUV*10000))
        ItotBEUV.append(np.sum(BEUVtiff_SE))# + exFluxB1)#/(RxBEUV_SE*RyBEUV_SE*10000))
        ItotB3.append(np.sum(B3))# + exFluxB3)#/(RxB3*RyB3*10000))
        PtotEUV.append((np.sum(EUVtiff)*q*90.44*1000)/(RxEUV*RyEUV*10000))
        PtotEUV.append((np.sum(EUVtiff_SE)*q*90.44*1000)/(RxEUV_SE*RyEUV_SE*10000))
        PtotBEUV.append((np.sum(BEUVtiff)*q*184.76*1000)/(RxBEUV*RyBEUV*10000))
        PtotBEUV.append((np.sum(BEUVtiff_SE)*q*184.76*1000)/(RxBEUV_SE*RyBEUV_SE*10000))
        
        ItotE2.append(np.sum(E2tiff))
        ItotE3.append(np.sum(E3tiff))
        
        _Itot.append(np.sum(tiff135))# + exFlux135)# / (Rx135*Ry135*10000))
        _Itot.append(np.sum(tiff250))# + exFlux250)# / (Rx250*Ry250*10000))
        
        print('\n RX, RY = ', RxBEUV, RyBEUV)
        
        if gratingArea:
            Geuv,Ceuv,Seuv = IoverGrating(EUVtiff, GA=Ga, dx=EUVres[0], dy=EUVres[1],show=False)
            GeuvSE,CeuvSE,SeuvSE = IoverGrating(EUVtiff_SE, GA=Ga, dx=EUVres[0], dy=EUVres[1],show=False)
            Gbeuv,Cbeuv,Sbeuv = IoverGrating(BEUVtiff, GA=Ga, dx=BEUVres[0], dy=BEUVres[1],show=False)
            GbeuvSE,CbeuvSE,SbeuvSE = IoverGrating(BEUVtiff_SE, GA=Ga, dx=BEUVres[0], dy=BEUVres[1],show=False)
            GB3,CB3,SB3 = IoverGrating(B3,GA=Ga,dx=m3res[0],dy=m3res[1],show=True)
            GB3 = GB3  / (4 * Ga*Ga*10000)
            
            GE2,CE2,SE2 = IoverGrating(E2tiff,GA=Ga,dx=E2res[0],dy=E2res[1],show=True)
            GE2 = GE2  / (4 * Ga*Ga*10000)
            GE3,CE3,SE3 = IoverGrating(E3tiff,GA=Ga,dx=E3res[0],dy=E3res[1],show=True)
            GE3 = GE3  / (4 * Ga*Ga*10000)
            
            G135,C135,S135 = IoverGrating(tiff135, GA=Ga, dx=res135[0], dy=res135[1],show=True)
            G250,C250,S250 = IoverGrating(tiff250, GA=Ga, dx=res250[0], dy=res250[1],show=True)
            
            Ceuv = Ceuv/(Ga*Ga*10000)
            CeuvSE = CeuvSE/(Ga*Ga*10000)
            Cbeuv = Cbeuv/(Ga*Ga*10000)
            CbeuvSE = CbeuvSE/(Ga*Ga*10000)
            
            IGAeuv.append(Geuv/(4*Ga*Ga*10000)) #IsumEUV[1] + IsumEUV[2] + _IsumEUV[1] + _IsumEUV[2])
            IGAeuv.append(GeuvSE/(4*Ga*Ga*10000)) #IsumEUV[1] + IsumEUV[2] + _IsumEUV[1] + _IsumEUV[2])
            IGAbeuv.append(Gbeuv/(4*Ga*Ga*10000)) #IsumBEUV[1] + IsumBEUV[2] + _IsumBEUV[1] + _IsumBEUV[2])
            IGAbeuv.append(GbeuvSE/(4*Ga*Ga*10000)) #IsumBEUV[1] + IsumBEUV[2] + _IsumBEUV[1] + _IsumBEUV[2])
            PGAeuv.append((Geuv*q*90.44*1000)/(4*Ga*Ga*10000)) #(IsumEUV[1] + IsumEUV[2] + _IsumEUV[1] + _IsumEUV[2])*EtoJ*1000)
            PGAeuv.append((GeuvSE*q*90.44*1000)/(4*Ga*Ga*10000)) #(IsumEUV[1] + IsumEUV[2] + _IsumEUV[1] + _IsumEUV[2])*EtoJ*1000)
            PGAbeuv.append((Gbeuv*q*184.76*1000)/(4*Ga*Ga*10000))
            PGAbeuv.append((GbeuvSE*q*184.76*1000)/(4*Ga*Ga*10000))
            
            _IGA.append(G135 / (4*Ga*Ga*10000))
            _IGA.append(G250 / (4*Ga*Ga*10000))
    
    if compareFits:
        import xraydb
        
        hN = 3
        CF = 'C3H6' # chemical formula for ultralene
        beta1,beta2 = [],[]
        T1,T2 = [],[]
        
        WF = 'H20'
        Wd = 0.9189 #0.0016477111460721195
        Wt = 1.5e-6
        
        CF2 = 'C2H4'
        R = 4/4
        T = 4.064e-6
        DPE = 0.96
        TPP = R*T
        TPE = T - TPP#(1-R)*T
        
        extraCT = -0.00e-6 #1.5e-6
        # minCT = -0.05e-6
        # maxCT = 0.05e-6
        for e in energy_range:
            # print('\n E: ', e)
            # print(CF)
            # print(xraydb.xray_delta_beta(CF, 0.855, int(e)))
            (d1,b1,atlen1) = xraydb.xray_delta_beta(CF, 0.855, int(e)) # density obtained from .... add ref
            beta1.append(b1)
            
            (d1,bw1,atlen1) = xraydb.xray_delta_beta(CF2, DPE, int(e))
            beta1.append(bw1)
            
            (d2,b2,atlen2) = xraydb.xray_delta_beta(CF,0.855,int(e)*hN)
            beta2.append(b2)
            (d2,bw2,atlen2) = xraydb.xray_delta_beta(CF2,DPE,int(e)*hN)
            beta2.append(bw2)
            # (d3,b3,atlen3) = xraydb.xray_delta_beta(CF,0.855,int(e)*3)
            # beta2.append(b2)
            
            wl1 = (4.135667696e-15 * 299792458) / e
            wl2 = (4.135667696e-15 * 299792458) / (hN*e)
            # wl3 = (4.135667696e-15 * 299792458) / (3*e)
            
            # print('\n')
            # print(wl1, wl2)
            tran1 = transmission(wl1,TPP+extraCT,b1)
            tran2 = transmission(wl2,TPP+extraCT,b2)
            tranW1 = transmission(wl1,TPE,bw1)
            tranW2 = transmission(wl2,TPE,bw2)
            # tran3 = transmission(wl3,4.064e-6,b3)
            
            # print('n  --------  HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEERE -------------------- \n')
            # print(tran1,tran2)
            
            T1.append(tran1*tranW1)
            T2.append(tran2*tranW2)#+tran3)/2)
        
        h1 = []
        h3 = []
        for file in os.listdir(fitFolder):
            if file.endswith('1.tif'):
                h1.append(file)
            elif file.endswith('2.tif'):
                h3.append(file)
        sortedH1 = sorted(h1,key=lambda x: float(x[0:-4])) # -11 for fits of counts
        sortedH3 = sorted(h3,key=lambda x: float(x[0:-4]))
        
        import pickle
        fitCalcsX = pickle.load(open(savePath_images + 'averaged/G2x_analysis.pkl', 'rb'))
        FWHM1x = fitCalcsX[0]
        FWHM3x = fitCalcsX[1]
        fitCalcsY = pickle.load(open(savePath_images + 'averaged/G2y_analysis.pkl', 'rb'))
        FWHM1y = fitCalcsY[0]
        FWHM3y = fitCalcsY[1]
        
        # print(sortedH1)
        
        Isum1,Isum3 = [],[]
        Psum1,Psum3 = [],[]
        FW1x,FW1y,FW3x,FW3y = [],[],[],[]
        GSUM1,GSUM3 = [],[]
        CSUM1,CSUM3 = [],[]
        S1,S3 = [],[]
        
        Ier1,Ier3,FXer1,FXer3,FYer1,FYer3,Ger1,Ger3,Ser1,Ser3 = [],[],[],[],[],[],[],[],[],[]
        isum1,isum3,fwx1,fwx3,fwy1,fwy3,gsum1,gsum3,sl1,sl3 = [],[],[],[],[],[],[],[],[],[]
        # print('\n TRANSMISSION 1 :' , T1)
        # print('\n TRANSMISSION 2 :' , T2)
        for i in range(0,len(sortedH1)):
            # print('\n hereherehere \n')
            # print(len(sortedH1))
            # print(i)
            n = i/10
            
            # #loading fits (in counts)
            # i1 = io.imread(fitFolder + sortedH1[i])
            # i3 = io.imread(fitFolder + sortedH3[i])
            
            # converting from ph/s/cm^2 (at fundamental energy) to ph/s
            i1 = io.imread(fitFolder + sortedH1[i])*10000*(11.0e-6 * 11.0e-6)
            i3 = io.imread(fitFolder + sortedH3[i])*10000*(11.0e-6 * 11.0e-6)
            # converting from ph/s (at fundamental energy) to counts at detector
            i1 = photonsPs2counts(i1, energy_range[i], t=exposure_time, conversion=1.27)
            i3 = photonsPs2counts(i3, energy_range[i], t=exposure_time, conversion=1.27)
            # # converting from counts to ph/s and accounting for transmission through ultralene filter
            i1 = counts2photonsPs(i1,energy_range[i],t=exposure_time,conversion=1.27) / T1[i]
            i3 = counts2photonsPs(i3,energy_range[i]*hN,t=exposure_time,conversion=1.27) / T2[i]
            # i1 = i1 / T1[i]
            # i3 = i3 / T2[i]
            
            # # print(np.shape(i1))
            # if i <10 and i<20:
            #     plt.plot(i1[np.shape(i1)[0]//2,:],label='F x')
            #     plt.plot(i3[np.shape(i3)[0]//2,:],label='H x')
            #     plt.plot(i1[:,np.shape(i1)[1]//2],label='F y')
            #     plt.plot(i3[:,np.shape(i3)[1]//2],label='H y')
            #     plt.legend()
            #     plt.show()
            
            pI1 = intensity2power(i1,energy_range[i])
            pI3 = intensity2power(i3,energy_range[i]*hN)
            
            #FWHM measured from gaussian fits
            fwhm1x, fwhm1y = getFWatValue(i1,frac=0.5,dx=11.0e-6,dy=11.0e-6,show=False)
            fwhm3x, fwhm3y = getFWatValue(i3,frac=0.5,dx=11.0e-6,dy=11.0e-6,show=False)
            
            gs1,cs1,s1 = IoverGrating(i1, GA=Ga, dx=11.0e-6, dy=11.0e-6,show=False)
            gs3,cs3,s3 = IoverGrating(i3, GA=Ga, dx=11.0e-6, dy=11.0e-6,show=False)
            
            Rx = np.shape(i1)[1]*11.0e-6; Ry = np.shape(i1)[0]*11.0e-6
            
            isum1.append((np.sum(i1)));isum3.append((np.sum(i3)))
            fwx1.append(fwhm1x);fwx3.append(fwhm3x)
            fwy1.append(fwhm1y);fwy3.append(fwhm3y)
            gsum1.append((gs1) / (4 * Ga * Ga * 10000));gsum3.append(gs3 / (4 * Ga * Ga * 10000))
            sl1.append(s1);sl3.append(s3)
            
            # print(i)
            # print(i%10)
            if i % 10 == 0 and i!=0: # int(n) == n:
                # # print('\n')
                # # print('HEEEEEEEERRRRRREEEEEEE')
                if i == 20:
                    NN = [0,1,2,3,4,5,6,7,8]
                elif i == 30:
                    NN = [0,1,2,3,4]
                else:
                    NN = [0,1,2,3,4,5,6,7,8,9]
                isum1=[isum1[n] for n in NN]
                isum3=[isum3[n] for n in NN]
                gsum1=[gsum1[n] for n in NN]
                gsum3=[gsum3[n] for n in NN]
                fwx1=[fwx1[n] for n in NN];fwx3=[fwx3[n] for n in NN];fwy1=[fwy1[n] for n in NN];fwy3=[fwy3[n] for n in NN]
                sl1=[sl1[n] for n in NN];sl3=[sl3[n] for n in NN]
                # # print(np.mean(isum1))
                erI1,erI3 = np.std(isum1),np.std(isum3)         
                erFx1,erFx3,erFy1,erFy3 = np.std(fwx1),np.std(fwx3),np.std(fwy1),np.std(fwy3)
                ger1,ger3 = np.std(gsum1), np.std(gsum3)
                sler1, sler3 = np.std(sl1), np.std(sl3)
                
                
                Isum1.append((np.mean(isum1)))# / (Rx*Ry*10000)); 
                Isum3.append((np.mean(isum3)))# / (Rx*Ry*10000))
                FW1x.append(np.mean(fwx1));FW1y.append(np.mean(fwy1));FW3x.append(np.mean(fwx3));FW3y.append(np.mean(fwy3))
                GSUM1.append(np.mean(gsum1)); GSUM3.append(np.mean(gsum3))
                S1.append(np.mean(sl1)); S3.append(np.mean(sl3))
                
                Ier1.append(erI1);Ier3.append(erI3)
                FXer1.append(erFx1);FXer3.append(erFx3);FYer1.append(erFy1);FYer3.append(erFy3)
                Ger1.append(ger1);Ger3.append(ger3)
                Ser1.append(sler1);Ser3.append(sler3)
                
                isum1,isum3,fwx1,fwx3,fwy1,fwy3,gsum1,gsum3,sl1,sl3 = [],[],[],[],[],[],[],[],[],[]
            else:
                pass
            
                # Isum1.append((np.sum(i1)))# / (Rx*Ry*10000)); 
                # Isum3.append((np.sum(i3)))# / (Rx*Ry*10000))
                # Psum1.append(np.sum(pI1)/(Rx*Ry*10000)); Psum3.append(np.sum(pI3)/(Rx*Ry*10000))
                # FW1x.append(fwhm1x); FW1y.append(fwhm1y); FW3x.append(fwhm3x); FW3y.append(fwhm3y)
                # GSUM1.append((gs1) / (4 * Ga * Ga * 10000)); GSUM3.append(gs3 / (4 * Ga * Ga * 10000))
                # CSUM1.append(cs1/(Ga*Ga*10000)); CSUM3.append(cs3/(Ga*Ga*10000))
                # S1.append(s1); S3.append(s3)
            
        #     if i == 11:
        #         mx1 = np.shape(i1)[1]//2; my1 = np.shape(i1)[0]//2
        #         H1x = i1[my1,:] / (11.0e-6 * 11.0e-6 * 10000);  H1y = i1[:,mx1] / (11.0e-6 * 11.0e-6 * 10000)
        #         mx3 = np.shape(i3)[1]//2; my3 = np.shape(i3)[0]//2
        #         H3x = i3[my3,:] / (11.0e-6 * 11.0e-6 * 10000);  H3y = i3[:,mx3] / (11.0e-6 * 11.0e-6 * 10000)
                
        #         mxB1 = np.shape(BEUVtiff)[1]//2; myB1 = np.shape(BEUVtiff)[0]//2
        #         B1x = BEUVtiff[myB1,:]; B1y = BEUVtiff[:,mxB1]
        #         mxB3 = np.shape(B3)[1]//2; myB3 = np.shape(B3)[0]//2
        #         B3x = B3[myB3,:];  B3y = B3[:,mxB3]
                
        #         _x = np.linspace(-mx1*11.0e-6,mx1*11.0e-6,len(H1x))
        #         _y = np.linspace(-my1*11.0e-6,my1*11.0e-6,len(H1y))
                
        #         _xB = np.linspace(-np.shape(BEUVtiff)[1]//2 * BEUVres[0], np.shape(BEUVtiff)[1]//2 * BEUVres[0], np.shape(BEUVtiff)[1])
        #         _yB = np.linspace(-np.shape(BEUVtiff)[0]//2 * BEUVres[1], np.shape(BEUVtiff)[0]//2 * BEUVres[1], np.shape(BEUVtiff)[0])
        #         _xB3 = np.linspace(-np.shape(B3)[1]//2 * m3res[0], np.shape(B3)[1]//2 * m3res[0], np.shape(B3)[1])
        #         _yB3 = np.linspace(-np.shape(B3)[0]//2 * m3res[1], np.shape(B3)[0]//2 * m3res[1], np.shape(B3)[0])
                
                
        #         print('\n dx,dy (sim): ', BEUVres[0],BEUVres[1])
        #         # print('\n dx,dy (fit): ', BEUVres[0],BEUVres[1])
                
                
        #         fig, ax = plt.subplots(1,2)
                
        #         # ax[0].plot(_x,H1x,'-',color='green',label='x fit (n=1)')
        #         # ax[0].plot(_x,H3x,'-',color='blue',label='x fit (n=3)')
        #         ax[1].plot(_y,H1y,'-',color='green',label='y fit (n=1)')
        #         ax[1].plot(_y,H3y,'-',color='blue',label='y fit (n=3)')
        #         # ax[0].set_title('Fitted Data')
        #         # ax[0,0].show()
                
                
        #         ax[0].plot(_xB,B1x,'-',color='red',label='x sim (n=1)')
        #         ax[0].plot(_xB3,B3x,'-',color='black',label='x sim (n=3)')
        #         ax[1].plot(_yB,B1y,'-',color='red',label='y sim (n=1)')
        #         ax[1].plot(_yB3,B3y,'-',color='black',label='y sim (n=3)')
        #         # ax[0,0].title('Simulation')
        #         # ax[0,0].legend()
        #         # ax[0].set_title('Simulation')
        #         ax[0].legend()
        #         ax[1].legend()
        #         # for a in ax:
        #         #     a.set_xlim(-0.005,0.005)
        #         fig.tight_layout()
        #         plt.show()
                
        #         # fig, ax = plt.subplots(1,2)
                
        #         # ax[0].plot(_x,H1x+H3x,'-',color='green',label='x fit')
        #         # ax[1].plot(_y,H1y+H3y,'-',color='green',label='y fit')
        #         # ax[0].plot(_xB,B1x,'.',color='red',label='x sim (n=1)')
        #         # ax[0].plot(_xB3,B3x,'.',color='black',label='x sim (n=3)')
        #         # ax[1].plot(_yB,B1y,'.',color='red',label='y sim (n=1)')
        #         # ax[1].plot(_yB3,B3y,'.',color='black',label='y sim (n=3)')
        #         # # ax[0,0].title('Simulation')
        #         # # ax[0,0].legend()
        #         # # ax[0].set_title('Simulation')
        #         # ax[0].legend()
        #         # ax[1].legend()
        #         # fig.tight_layout()
        #         # plt.show()
        # #     image = io.imread(path + str(name) + str(i) + str(imgType))
           

    if findCenter:
        plt.errorbar(energy_range,[(c-cX[0])*11.0 for c in cX],yerr=5.5,fmt='.',label='x')
        plt.errorbar(energy_range,[(c-cY[0])*11.0 for c in cY],yerr=5.5,fmt='.',label='y')
        plt.ylabel('Beam center drift [$\mu$m]')
        plt.xlabel('Photon energy [eV]')
        # plt.yscale('log')
        # plt.xlim(eLim[0],eLim[1])
        plt.legend()
        plt.show()
    
    XPS = pickle.load(open('/user/home/data/HarmonicContam/XPS/LF (cff=1.4).pkl', 'rb'))
    XPS_MFP = pickle.load(open('/user/home/data/HarmonicContam/XPS/LF (cff=1.4)_MFP.pkl', 'rb'))
    XPS_FLUX = pickle.load(open('/user/home/data/HarmonicContam/XPS/LF (cff=1.4)_FLUX.pkl', 'rb'))
    XPS_CRNT = pickle.load(open('/user/home/data/HarmonicContam/XPS/LF (cff=1.4)_CRNT.pkl', 'rb'))
    XPS_HFCRNT = pickle.load(open('/user/home/data/HarmonicContam/XPS/HF (cff=1.4)_CRNT.pkl', 'rb'))
    XPS_HF = pickle.load(open('/user/home/data/HarmonicContam/XPS/HF (cff=1.4)_MFP.pkl', 'rb'))
    # XPS_HFCRNT = pickle.load(open('/user/home/data/HarmonicContam/XPS/HF (standard)_CRNT.pkl', 'rb'))
    # XPS_HF = pickle.load(open('/user/home/data/HarmonicContam/XPS/HF (standard)_MFP.pkl', 'rb'))
    XPSe = [e for e in np.arange(130,185,20)] + [185] + [e for e in np.arange(190,335,20)]
    # print(len(energy_range[0:len(iTot)]))
    # print(len(iTot))
    F = []
    Fhf = []
    for i,c in enumerate(XPS_CRNT):
        print('\n')
        print(c)
        print(XPS[i])
        c1 = c*XPS_MFP[i][0]
        c2 = c*XPS_MFP[i][1]
        c3 = c*XPS_MFP[i][2]
    
        F1 = (3.7 / q) * (c1 / XPSe[i])
        F2 = (3.7 / q) * (c2 / XPSe[i]*2)
        F3 = (3.7 / q) * (c3 / XPSe[i]*3)
        
        print('\n here')
        print(c1, c2, c3)
        print(np.sum([c1,c2,c3]), c)
        print(F1,F2,F3)
        
        F.append([F1,F2,F3])
        
    for i,c in enumerate(XPS_HFCRNT):
        # print('\n')
        # print(c)
        # print(XPS[i])
        c1 = c*XPS_HF[i][0]
        c2 = c*XPS_HF[i][1]
        c3 = c*XPS_HF[i][2]
    
        F1 = (3.7 / q) * (c1 / XPSe[i])
        F2 = (3.7 / q) * (c2 / XPSe[i]*2)
        F3 = (3.7 / q) * (c3 / XPSe[i]*3)
        
        print('\n here')
        print(c1, c2, c3)
        print(np.sum([c1,c2,c3]), c)
        print(F1,F2,F3)
        
        Fhf.append([F1,F2,F3])
    
    print("RIGHT HERE: ", (3.5e9 * (3000 - 40) * bw * eff[2]))
    
    print(Isum1)
    print(Ier1)
    
    print(np.shape(GSUM1))
    
    
    plt.errorbar(energy_range0[0:len(Isum1)],Isum1,yerr=Ier1)
    plt.show()
    
    FSIZE=12
    LSIZE=10
    
    if compareSim and compareFits:
        pass
    else:
        plt.errorbar(energy_range0[0:len(iTot)], iTot, yerr=er, fmt='.',label='data')#,fontsize=FSIZE)
    if compareSim:
        plt.plot(90,ItotEUV[0],'x',color='blue')#,label='sim')
        # plt.plot(90,ItotEUV[1],'o',color='red')#,label='sim')
        plt.plot(185,ItotBEUV[0],'x',color='blue',label='Simulated (n=1)')#,fontsize=FSIZE)
        plt.plot([135,250],_Itot,'x',color='blue')
        plt.plot(185,ItotB3,'x',color='g', label='Simulated (n=3)')#,fontsize=FSIZE)
        # plt.plot(185,ItotBEUV[1],'o',color='red',label='sim (SE)')
        # plt.plot(XPSe,XPS_FLUX,'x',color='black',label='Photodiode')
        plt.plot(XPSe,[f[0] / 100 for f in F],'o',color='black',label='Photodiode (n=1)',markerfacecolor='none')#,fontsize=FSIZE)
        # plt.plot(XPSe,[f[0] for f in Fhf],'o',color='y',label='Photodiode (n=1) HF',markerfacecolor='none')
        # print('\n photodiode:')
        # print([f[0] for f in F])
        # plt.plot(XPSe,[f[1] for f in F],'o',color='red',label='Photodiode (n=2)',markerfacecolor='none')
        # plt.plot(XPSe,[f[2] for f in F],'o',color='green',label='Photodiode (n=3)',markerfacecolor='none')
        # plt.plot(90,ItotE2,'x',color='r', label='Simulated (n=2)')#,fontsize=FSIZE)
        plt.plot(90,ItotE3,'x',color='g')#,fontsize=FSIZE)
    if compareFits:
        # pass
        # plt.plot(energy_range0[0:len(Isum1)],Isum1, '.',color='blue', label='Intensity fit (n = 1)')
        # plt.plot(energy_range0[0:len(Isum1)],Isum3, '.',color='green', label='Intensity fit (n = 3)')
        plt.errorbar(energy_range0[0:len(Isum1)],Isum1,yerr=Ier1,fmt='o',color='blue',label='Measured intensity fit (n=1)',markerfacecolor='none')#,fontsize=FSIZE)
        plt.errorbar(energy_range0[0:len(Isum1)],Isum3,yerr=Ier3,fmt='o',color='green',label='Measured intensity fit (n=3)',markerfacecolor='none')#,fontsize=FSIZE)
    plt.xlabel("Photon Energy [eV]",fontsize=FSIZE)
    plt.ylabel("$\Phi_n$ [ph/s]",fontsize=FSIZE)
    # plt.ylim(-1e11,np.max(iTot[0:41]) + 0.25e12)#2.5e12)#np.max(iTot[0:17]))
    # plt.xlim(eLim[0],eLim[1])
    plt.yscale('log')
    plt.legend(fontsize=LSIZE)
    if savePath_plots:
        plt.savefig(savePath_plots+'Flux_vs_E'+'.'+fmat,format=fmat)
    plt.show()
    
    # if compareSim and compareFits:
    #     pass
    # else:
    #     plt.errorbar(energy_range0[0:len(iTot)], pTot, yerr=erP, fmt='.',label='data')
    # if compareSim:
    #     plt.plot(90,PtotEUV[0],'X',color='red')#,label='sim')
    #     plt.plot(90,PtotEUV[1],'o',color='red')#,label='sim')
    #     plt.plot(185,PtotBEUV[0],'X',color='red', label= 'sim (ME)')
    #     plt.plot(185,PtotBEUV[1],'o',color='red', label= 'sim (SE)')
    # if compareFits:
    #     plt.plot(energy_range0[0:len(Isum1)],Psum1, '.', label='n = 1')
    #     plt.plot(energy_range0[0:len(Isum1)],Psum3, '.', label='n = 3')
    # plt.xlabel("Photon Energy [eV]")
    # plt.ylabel("Total Power [$mJ/s/cm^2$]")
    # # plt.ylim(-0.01,np.max(pTot[0:41])+0.05)
    # # plt.xlim(eLim[0],eLim[1])
    # plt.yscale('log')
    # plt.legend()
    # plt.show()
    
    # print(len(ims))
    # print(len(energy_range0))
    # print(len(gsums))
    
    if compareSim and compareFits:
        pass
    else:
        plt.plot(energy_range0[0:len(iTot)],gsums,'.',label='data')#,fontsize=FSIZE)
    if compareSim:
        plt.plot(90,IGAeuv[0],'x',color='blue')#,label='sim')
        # plt.plot(90,IGAeuv[1],'o',color='red')#,label='sim')
        plt.plot(185,IGAbeuv[0],'x',color='blue', label= 'Simulated (n=1)')#,fontsize=FSIZE)
        plt.plot([135,250],_IGA,'x',color='blue')
        plt.plot(185,GB3,'x',color='g',label='Simulated (n=3)')#,fontsize=FSIZE)
        # plt.plot(185,IGAbeuv[1],'o',color='red', label= 'sim (SE)')
        # plt.plot(90,GE2,'x',color='r',label='Simulated (n=2)')#,fontsize=FSIZE)
        plt.plot(90,GE3,'x',color='g')#,label='Simulated (n=3)')#,fontsize=FSIZE)
    if compareFits:
        # plt.plot(energy_range0[0:len(Isum1)],GSUM1, '.', color='blue',label='n = 1')
        # plt.plot(energy_range0[0:len(Isum1)],GSUM3, '.', color='green',label='n = 3')
        plt.errorbar(energy_range0[0:len(Isum1)],GSUM1,yerr=Ger1,fmt='o',color='blue',label='Measured intensity fit (n=1)',markerfacecolor='none')#,fontsize=FSIZE)
        plt.errorbar(energy_range0[0:len(Isum1)],GSUM3,yerr=Ger3,fmt='o',color='green',label='Measured intensity fit (n=3)',markerfacecolor='none')#,fontsize=FSIZE)
    plt.xlabel("Photon Energy [eV]",fontsize=FSIZE)
    plt.ylabel("$I^G_n$ [ph/s/cm$^2$]",fontsize=FSIZE)
    # plt.ylim(-1e9,np.max(gsums[0:41]) + 0.05e10)#3.25e10) #np.max(gsums[0:17]))
    # plt.xlim(eLim[0],eLim[1])
    plt.yscale('log')
    plt.legend(fontsize=LSIZE)
    if savePath_plots:
        plt.savefig(savePath_plots+'IG_vs_E'+'.'+fmat,format=fmat)
    plt.show()
    
    # print('\n intensity over grating for 91 eV: ', GSUM1[1])
    # print('\n intensity over grating for 185 eV: ', GSUM1[11])
    # print('\n power over grating for 91 eV: ', Psum1[1])
    # print('\n power over grating for 185 eV: ', Psum1[11])
    
    # if compareSim and compareFits:
    #     pass
    # else:
    #     plt.plot(energy_range0[0:len(iTot)],csums,'.',label='data')
    # if compareSim:    
    #     plt.plot(90,Ceuv,'X',color='red')#,label='sim')
    #     plt.plot(90,CeuvSE,'o',color='red')#,label='sim')
    #     plt.plot(185,Cbeuv,'X',color='red', label= 'sim (ME)')
    #     plt.plot(185,CbeuvSE,'o',color='red', label= 'sim (SE)')
    # if compareFits:
    #     plt.plot(energy_range0[0:len(Isum1)],CSUM1, '.', label='n = 1')
    #     plt.plot(energy_range0[0:len(Isum1)],CSUM3, '.', label='n = 3')
    # plt.xlabel("Photon Energy [eV]")
    # plt.ylabel("Total Intensity over Central 100x100 um [$ph/s/cm^2$]")
    # # plt.ylim(-1e8,np.max(csums[0:41]) + 0.05e10)#8e9)#np.max(csums[0:17]))
    # # plt.xlim(eLim[0],eLim[1])
    # plt.yscale('log')
    # plt.legend()
    # plt.show()
    
    if compareSim and compareFits:
        pass
    else:
        plt.plot(energy_range0[0:len(iTot)],S,'.',label='data')#,fontsize=FSIZE)
    if compareSim:
        plt.plot(90,Seuv,'x',color='blue')#,label='sim')
        # plt.plot(90,SeuvSE,'x',color='red')#,label='sim')
        plt.plot(185,Sbeuv,'x',color='blue', label= 'Simulated')#,fontsize=FSIZE)#' (n=1)')
        plt.plot(135,S135,'x',color='blue')#,label='sim')
        plt.plot(250,S250,'x',color='blue')#,label='sim')
        plt.plot(185,SB3,'x',color='black',label='Simulated (n=3)')
        # plt.plot(90,SE2,'x',color='r',label='Simulated (n=2)')
        plt.plot(90,SE3,'x',color='g')#,label='Simulated (n=3)')
        # plt.plot(185,SbeuvSE,'o',color='red', label= 'sim (SE)')
    if compareFits:
        # plt.plot(energy_range0[0:len(Isum1)],S1, '.',color='blue', label='n = 1')
        # plt.plot(energy_range0[0:len(Isum1)],S3, '.',color='green', label='n = 3')
        plt.errorbar(energy_range0[0:len(Isum1)],S1,yerr=Ser1,fmt='o',color='blue',label='Measured intensity fit (n=1)',markerfacecolor='none')#,fontsize=FSIZE)
        plt.errorbar(energy_range0[0:len(Isum1)],S3,yerr=Ser3,fmt='o',color='green',label='Measured intensity fit (n=3)',markerfacecolor='none')#,fontsize=FSIZE)
    plt.xlabel("Photon Energy [eV]",fontsize=FSIZE)
    plt.ylabel("s",fontsize=FSIZE)#"Intensity Slope over Grating")
    # plt.xlim(eLim[0],eLim[1])
    plt.legend(fontsize=LSIZE)#loc='center left')
    plt.yscale('log')
    if savePath_plots:
        plt.savefig(savePath_plots+'slope_vs_E'+'.'+fmat,format=fmat)
    plt.show()
    
    # plt.plot(energy_range0,fwhmX,'.:',label='x')
    # plt.plot(energy_range0,fwhmY,'.:',label='y')
    if compareSim and compareFits:
        pass
    else:
        plt.plot(energy_range0[0:len(iTot)],[f*1e3 for f in fwXs[0:60]], '.',color='blue',label='x (data)')#,fontsize=FSIZE)
        plt.plot(energy_range0[0:len(iTot)],[f*1e3 for f in fwYs[0:60]], '.',color='g',label='y (data)')#,fontsize=FSIZE)
    if compareSim:
        plt.plot(90,EUVfwhmx*1e3,'x',color='r')#,label='x (sim)')
        plt.plot(90,EUVfwhmy*1e3,'x',color='black')#,label='y (sim)')
        # plt.plot(90,EUVfwhmxSE*1e3,'x',color='r')#,label='x (sim)')
        # plt.plot(90,EUVfwhmySE*1e3,'x',color='black')#,label='y (sim)')
        plt.plot(185,BEUVfwhmx*1e3,'x',color='r', label = 'x (simulated)')#,fontsize=FSIZE)
        plt.plot(185,BEUVfwhmy*1e3,'x',color='black', label = 'y (simulated)')#,fontsize=FSIZE)
        plt.plot(135,fwhmx135*1e3,'x',color='r')#,label='x (sim)')
        plt.plot(135,fwhmy135*1e3,'x',color='black')#,label='y (sim)')
        plt.plot(250,fwhmx250*1e3,'x',color='r')#,label='x (sim)')
        plt.plot(250,fwhmy250*1e3,'x',color='black')#,label='y (sim)')
        # plt.plot(185,B3fwhmx*1e3,'x',color='r')
        # plt.plot(185,B3fwhmy*1e3,'x',color='black')
        # plt.plot(90,E2fwhmx*1e3,'x',color='b',label='x (simulated), $n=2$')
        # plt.plot(90,E2fwhmy*1e3,'x',color='g',label='x (simulated), $n=2$')
        # plt.plot(90,E3fwhmx*1e3,'x',color='r')
        # plt.plot(90,E3fwhmy*1e3,'x',color='black')
        # plt.plot(185,BEUVfwhmxSE*1e3,'o',color='r', label= 'sim (SE)')
        # plt.plot(185,BEUVfwhmySE*1e3,'o',color='black')
    # plt.plot(energy_range0,[f*1e3 for f in FW1x], '.', label='n = 1 x')
    # plt.plot(energy_range0,[f*1e3 for f in FW1y], '.', label='n = 1 y')
    # plt.plot(energy_range0,[f*1e3 for f in FW3x], '.', label='H3 x')
    # plt.plot(energy_range0,[f*1e3 for f in FW3y], '.', label='H3 y')
    if compareFits:
        # plt.plot(energy_range0[0:len(Isum1)],[f*1e3 for f in FW1x], '.',color='r', label='x (fit)')
        # plt.plot(energy_range0[0:len(Isum1)],[f*1e3 for f in FW1y], '.',color='black', label='y (fit)')
        # plt.plot(energy_range0[0:len(Isum1)],[f for f in FWHM1x], '.',color='r', label='x (fit)')
        # plt.plot(energy_range0[0:len(Isum1)],[f for f in FWHM1y], '.',color='black', label='y (fit)')
        # plt.plot(energy_range0[0:len(Isum1)],[f*1e3 for f in FW3x], '.', label='n = 3 x')
        # plt.plot(energy_range0[0:len(Isum1)],[f*1e3 for f in FW3y], '.', label='n = 3 y')
        plt.errorbar(energy_range0[0:len(Isum1)],[f*1e3 for f in FW1x],yerr=[f*1e3 for f in FXer1],fmt='o',color='r',label='x (fit)',markerfacecolor='none')#,fontsize=FSIZE)
        plt.errorbar(energy_range0[0:len(Isum1)],[f*1e3 for f in FW1y],yerr=[f*1e3 for f in FYer1],fmt='o',color='black',label='y (fit)',markerfacecolor='none')#,fontsize=FSIZE)
    # plt.plot(energy_range0,FWHM3x, '.', label='H3 x')
    # plt.plot(energy_range0,FWHM3y, '.', label='H3 y')
    plt.xlabel("Photon Energy [eV]",fontsize=FSIZE)
    plt.ylabel("Intensity FWHM [mm] ($n=1$)",fontsize=FSIZE)
    # plt.ylim(0,np.max(fwXs[0:17]))
    # plt.xlim(eLim[0],eLim[1])
    plt.legend(fontsize=LSIZE)
    if savePath_plots:
        plt.savefig(savePath_plots+'FWHM_vs_E'+'.'+fmat,format=fmat)
    plt.show()
    
    
    # plt.plot(90,EUVfwhmx*1e3,'X',color='r')#,label='x (sim)')
    # plt.plot(90,EUVfwhmy*1e3,'X',color='black')#,label='y (sim)')
    plt.plot(185,B3fwhmx*1e3,'x',color='r')
    plt.plot(185,B3fwhmy*1e3,'x',color='black')
    # plt.plot(90,E2fwhmx*1e3,'x',color='b',label='x ($n=2$)')
    # plt.plot(90,E2fwhmy*1e3,'x',color='g',label='x ($n=2$)')
    plt.plot(90,E3fwhmx*1e3,'x',color='r')
    plt.plot(90,E3fwhmy*1e3,'x',color='black')
    plt.errorbar(energy_range0[0:len(Isum1)],[f*1e3 for f in FW3x],yerr=[f*1e3 for f in FXer3],fmt='o',color='r',label='x (fit)',markerfacecolor='none')#,fontsize=FSIZE) '.', color='r', label='x')
    plt.errorbar(energy_range0[0:len(Isum1)],[f*1e3 for f in FW3y],yerr=[f*1e3 for f in FYer3],fmt='o',color='black',label='y (fit)',markerfacecolor='none')#,fontsize=FSIZE) '.', color='black', label='y')
    # plt.errorbar(energy_range0[0:3],[f*1e3 for f in FW1x[0:3]],yerr=[f*1e3 for f in FXer1[0:3]],fmt='o',color='r',markerfacecolor='none')#,fontsize=FSIZE)
    # plt.errorbar(energy_range0[0:3],[f*1e3 for f in FW1y[0:3]],yerr=[f*1e3 for f in FYer1[0:3]],fmt='o',color='black',markerfacecolor='none')#,fontsize=FSIZE)
    plt.xlabel("Photon Energy [eV]",fontsize=FSIZE)
    plt.ylabel("Intensity FWHM [mm] ($n=3$)",fontsize=FSIZE)
    if savePath_plots:
        plt.savefig(savePath_plots+'FWHM_vs_E_n3'+'.'+fmat,format=fmat)
    plt.legend()
    plt.show()
    
    
    plt.plot(90,EUVfwhmx*1e3,'x',color='r')#,label='x (sim)')
    plt.plot(90,EUVfwhmy*1e3,'x',color='black')#,label='y (sim)')
    # plt.plot(90,EUVfwhmxSE*1e3,'x',color='r')#,label='x (sim)')
    # plt.plot(90,EUVfwhmySE*1e3,'x',color='black')#,label='y (sim)')
    plt.plot(185,BEUVfwhmx*1e3,'x',color='r', label = 'x (simulated)')#,fontsize=FSIZE)
    plt.plot(185,BEUVfwhmy*1e3,'x',color='black', label = 'y (simulated)')#,fontsize=FSIZE)
    plt.plot(135,fwhmx135*1e3,'x',color='r')#,label='x (sim)')
    plt.plot(135,fwhmy135*1e3,'x',color='black')#,label='y (sim)')
    plt.plot(250,fwhmx250*1e3,'x',color='r')#,label='x (sim)')
    plt.plot(250,fwhmy250*1e3,'x',color='black')#,label='y (sim)')
    plt.errorbar(energy_range0[0:len(Isum1)],[f*1e3 for f in FW1x],yerr=[f*1e3 for f in FXer1],fmt='o',color='r',label='x ($n=1$)',markerfacecolor='none')#,fontsize=FSIZE)
    plt.errorbar(energy_range0[0:len(Isum1)],[f*1e3 for f in FW1y],yerr=[f*1e3 for f in FYer1],fmt='o',color='black',label='x ($n=1$)',markerfacecolor='none')#,fontsize=FSIZE)
    # plt.plot(90,EUVfwhmx*1e3,'X',color='r')#,label='x (sim)')
    # plt.plot(90,EUVfwhmy*1e3,'X',color='black')#,label='y (sim)')
    plt.plot(185,B3fwhmx*1e3,'x',color='g',label='x ($n=3$) (simulated)')
    plt.plot(185,B3fwhmy*1e3,'x',color='b',label='y ($n=3$) (simulated)')
    # plt.plot(90,E2fwhmx*1e3,'x',color='b',label='x ($n=2$)')
    # plt.plot(90,E2fwhmy*1e3,'x',color='g',label='x ($n=2$)')
    plt.plot(90,E3fwhmx*1e3,'x',color='g')
    plt.plot(90,E3fwhmy*1e3,'x',color='b')
    plt.errorbar(energy_range0[0:len(Isum1)],[f*1e3 for f in FW3x],yerr=[f*1e3 for f in FXer3],fmt='o',color='g',label='x ($n=3$)',markerfacecolor='none')#,fontsize=FSIZE) '.', color='r', label='x')
    plt.errorbar(energy_range0[0:len(Isum1)],[f*1e3 for f in FW3y],yerr=[f*1e3 for f in FYer3],fmt='o',color='b',label='y ($n=3$)',markerfacecolor='none')#,fontsize=FSIZE) '.', color='black', label='y')
    plt.xlabel("Photon Energy [eV]",fontsize=FSIZE)
    plt.ylabel("Intensity FWHM [mm]",fontsize=FSIZE)
    if savePath_plots:
        plt.savefig(savePath_plots+'FWHM_vs_E_n1n3'+'.'+fmat,format=fmat)
    plt.legend()
    plt.show()
    
    HCtot = [g3/(g1 + g3) for g1,g3 in zip(Isum1,Isum3)]
    HCg = [g3/(g1 + g3) for g1,g3 in zip(GSUM1,GSUM3)]
    
    Irel1 = [dF/F for dF,F in zip(Ier1,Isum1)]
    Irel3 = [dF/F for dF,F in zip(Ier3,Isum3)]
    Ier13 = [er1 + er3 for er1,er3 in zip(Ier1,Ier3)]
    I13 = [er1 + er3 for er1,er3 in zip(Isum1,Isum3)]
    Irel13 = [dF/F for dF,F in zip(Ier13,I13)]
    Grel1 = [dF/F for dF,F in zip(Ger1,GSUM1)]
    Grel3 = [dF/F for dF,F in zip(Ger3,GSUM3)]
    Ger13 = [er1 + er3 for er1,er3 in zip(Ger1,Ger3)]
    G13 = [er1 + er3 for er1,er3 in zip(GSUM1,GSUM3)]
    Grel13 = [dF/F for dF,F in zip(Ger13,G13)]
    HCtotE = [_HCtot * np.sqrt(((_Irel1)**2) + ((_Irel13)**2)) for _HCtot,_Irel1,_Irel13 in zip(HCtot,Irel1,Irel13)]
    HCgE = [_HCg * np.sqrt(((_Grel1)**2) + ((_Grel13)**2)) for _HCg,_Grel1,_Grel13 in zip(HCg,Grel1,Grel13)]
    # print(XPS)
    # print(np.shape(XPS))
    # print(XPSe)
    
    # plt.plot(energy_range0[0:len(Isum1)],[g1/(g1 + g3) for g1,g3 in zip(Isum1,Isum3)],'.',label='Fundamental')
    # plt.plot(energy_range0[0:len(Isum1)],[g3/(g1 + g3) for g1,g3 in zip(Isum1,Isum3)],'.',color='black',label='Total I')
    # plt.plot(energy_range0[0:len(Isum1)],[g3/(g1 + g3) for g1,g3 in zip(GSUM1,GSUM3)],'.',color='blue',label='I over grating')
    plt.errorbar(energy_range0[0:len(Isum1)], HCtot, yerr=HCtotE,fmt='o',color='black',label='Total I',markerfacecolor='none')#,fontsize=FSIZE)
    plt.errorbar(energy_range0[0:len(Isum1)], HCg, yerr=HCgE,fmt='o',color='blue',label='I over grating',markerfacecolor='none')#,fontsize=FSIZE)
    # plt.plot(energy_range0[0:len(Isum1)],[(g3/g1)*(t1/t3) for g1,g3,t1,t3 in zip(Isum1,Isum3,T1,T2)],'.',label='Higher')
    # plt.plot(XPSe,[np.sum(x[1::]) for x in XPS],'x',label='XPS data')
    # plt.plot(XPSe,[np.sum(x[2::]) for x in XPS],'x',label='XPS data (n>2)')
    plt.plot(XPSe,[np.sum(x[1::]) for x in XPS_MFP],'x', color='r',label='XPS data')#,fontsize=FSIZE)
    
    # plt.plot(185,GB3/(IGAbeuv[0] + GB3),'x',color='blue',label='Simulation (grating)')
    plt.plot(185,ItotB3/(ItotBEUV[0] + ItotB3),'x',color='green',label='Simulation')#,fontsize=FSIZE)
    plt.plot(185,GB3/(IGAbeuv[0] + GB3),'x',color='b')#,label='Simulation')#,fontsize=FSIZE)
    plt.plot(90,GE3/(IGAeuv[0] + GE3),'x',color='b')#,label='Simulation')#,fontsize=FSIZE)
    plt.plot(90,np.sum([ItotE2,ItotE3])/np.sum([ItotEUV[0],ItotE2,ItotE3]),'x',color='green')#,label='Simulation')
    
    plt.xlabel('Photon Energy [eV]',fontsize=FSIZE)
    plt.ylabel('$\zeta$',fontsize=FSIZE)#'$\Phi_{n>1} / \sum_n \Phi_n$')#'Fraction of Harmonic in Total Intensity')
    plt.legend(fontsize=LSIZE)
    # if savePath_plots:
    #     plt.savefig(savePath_plots+'ZetaOverG_Comparison'+'.'+fmat,format=fmat)
    plt.show()
    
    plt.errorbar(energy_range0[0:len(Isum1)], HCg, yerr=HCgE,fmt='o',color='black',label='Intensity measurement fits',markerfacecolor='none')#,fontsize=FSIZE)
    plt.plot(185,GB3/(IGAbeuv[0] + GB3),'x',color='g',label='Simulation')#,fontsize=FSIZE)
    plt.plot(90,GE3/(IGAeuv[0] + GE3),'x',color='g')#,label='Simulation')#,fontsize=FSIZE)
    
    plt.xlabel('Photon Energy [eV]',fontsize=FSIZE)
    plt.ylabel('$\zeta^G$',fontsize=FSIZE)#'$\Phi_{n>1} / \sum_n \Phi_n$')#'Fraction of Harmonic in Total Intensity')
    plt.legend(fontsize=LSIZE)
    if savePath_plots:
        plt.savefig(savePath_plots+'ZetaOverG_Comparison'+'.'+fmat,format=fmat)
    plt.show()
    
    plt.errorbar(energy_range0[0:len(Isum1)], HCtot, yerr=HCtotE,fmt='o',color='black',label='Intensity measurement fits',markerfacecolor='none')#,fontsize=FSIZE)
    plt.plot(XPSe,[np.sum(x[1::]) for x in XPS_MFP],'x', color='r',label='XPS measurement')#,fontsize=FSIZE)
    plt.plot(185,ItotB3/(ItotBEUV[0] + ItotB3),'x',color='green',label='Simulation')#,fontsize=FSIZE)
    plt.plot(90,np.sum([ItotE2,ItotE3])/np.sum([ItotEUV[0],ItotE2,ItotE3]),'x',color='green')#,label='Simulation')#,fontsize=FSIZE)
    
    plt.xlabel('Photon Energy [eV]',fontsize=FSIZE-5)
    plt.ylabel('$\zeta$',fontsize=FSIZE-5)#'$\Phi_{n>1} / \sum_n \Phi_n$')#'Fraction of Harmonic in Total Intensity')
    # plt.legend(fontsize=LSIZE)
    plt.ylim([-0.001,0.1])
    # Get the current axes and set the aspect
    ax = plt.gca()
    ax.set_aspect(1000)#, adjustable='box')    
    if savePath_plots:
        plt.savefig(savePath_plots+'Zeta_Comparison_closeup'+'.'+fmat,format=fmat)
    plt.show()
    # GSUM1
    # plt.plot(energy_range0,[t2/t1 for t2,t1 in zip(T2,T1)],label='Fundamental')
    # # plt.plot(energy_range0,T2,label='Higher')
    # plt.ylabel('Transmission')
    # plt.xlabel('Fundamental Photon Energy [eV]')
    # # plt.legend()
    # plt.show()
    

    # fig, ax0 = plt.subplots()
    # ax1 = ax0.twinx()
    # # ax0.plot(energy_range0[0:len(Isum1)],[g1/(g1 + g3) for g1,g3 in zip(Isum1,Isum3)],'o',color='red',label='F')
    # ax0.plot(energy_range0[0:len(Isum1)],[g3/(g1 + g3) for g1,g3 in zip(Isum1,Isum3)],'x',color='red',label='H')
    # ax1.plot(energy_range0[0:len(Isum1)],[1/t for t in T1[0:len(Isum1)]],'o',color='black',label='F')
    # ax1.plot(energy_range0[0:len(Isum1)],[1/t for t in T2[0:len(Isum1)]],'x',color='black',label='H')
    # ax0.set_ylabel("% $\Phi$")
    # ax1.set_ylabel('1/Transmission')
    # ax1.spines["left"].set_color('red')
    # ax1.spines["right"].set_color('black')
    # ax0.yaxis.label.set_color('red')
    # ax0.tick_params(axis="y", colors='red')
    # ax1.yaxis.label.set_color('black')
    # ax1.tick_params(axis="y", colors='black')
    # ax0.set_xlabel('Fundamental Photon Energy [eV]')
    # fig.tight_layout()
    # ax1.legend()
    # plt.show()

# #plt.plot(energy_range0[0:21],[h3/(h1+h3) for h1,h3 in zip(H1G,H3G)],'.',label='grating')
# #plt.plot(energy_range0[0:21],[h3/(h1+h3) for h1,h3 in zip(H1C,H3C)],'.',label='center')
# plt.plot(energy_range0[0:21],[h3/(h1+h3) for h1,h3 in zip(T1[0:21],T3[0:21])],'.',label='both')
# plt.xlabel('Photon Energy [eV]')
# plt.ylabel('Fraction of 3rd Harmonic in Total Intensity')
# #plt.legend()
# plt.show()

# #plt.plot(energy_range0[0:21],[h3/h1 for h1,h3 in zip(H1G,H3G)],'.',label='grating')
# #plt.plot(energy_range0[0:21],[h3/h1 for h1,h3 in zip(H1C,H3C)],'.',label='center')
# plt.plot(energy_range0[0:21],[h3/h1 for h1,h3 in zip(T1[0:21],T3[0:21])],'.',label='both')
# plt.xlabel('Photon Energy [eV]')
# plt.ylabel('Ratio of Intensities of 1st and 3rd Harmonic')
# #plt.legend()
# plt.show()

# #plt.plot(energy_range0[1:21],[h1/h3 for h1,h3 in zip(H1G[1::],H3G[1::])],'.',label='grating')
# #plt.plot(energy_range0[1:21],[h1/h3 for h1,h3 in zip(H1C[1::],H3C[1::])],'.',label='center')
# plt.plot(energy_range0[1:21],[h1/h3 for h1,h3 in zip(T1[1:21],T3[1:21])],'.',label='both')
# plt.xlabel('Photon Energy [eV]')
# plt.ylabel('Ratio of Intensities of 3rd and 1st Harmonic')
# #plt.legend()
# plt.show()
    
    # print(Seuv)
    # print(Sbeuv)
    


    simFWX = [EUVfwhmx,BEUVfwhmx,fwhmx135,fwhmx250]
    simFWY = [EUVfwhmy,BEUVfwhmy,fwhmy135,fwhmy250]
    
    HCxps = [np.sum(x[1::]) for x in XPS_MFP]
    HCsim = ItotB3/(ItotBEUV[0] + ItotB3)
    
    simF = [ItotEUV[0],ItotBEUV[0],_Itot[0],_Itot[1],ItotB3]
    simIG = [IGAeuv[0],IGAbeuv[0],_IGA[0],_IGA[1],GB3]
    xpsF = [f[0] / 100 for f in F]
    
    # print(HHC)
    
    if pickleResults:
        results = [energy_range0, XPSe,
                   Isum1,Ier1,Isum3,Ier3,
                   GSUM1,Ger1,GSUM3,Ger3,
                   simF,simIG,
                   xpsF,
                   FW1x,FXer1,FW1y,FYer1,
                   simFWX,simFWY,
                   HCtot,HCtotE,
                   HCsim,HCxps
                   ]
        
        # if compareSim:
        #     if compareFits:
        #         results = [energy_range0,
        #                      [c-cX[0] for c in cX],
        #                      [c-cY[0] for c in cY],
        #                      iTot,er,pTot,erP,
        #                      gsums,csums,S,fwXs,fwYs,
        #                      ItotEUV,ItotBEUV,PtotEUV,PtotBEUV,
        #                      IGAeuv,IGAbeuv,PGAeuv,PGAbeuv,
        #                      CeuvSE, # changed to SE
        #                      Cbeuv,
        #                      SeuvSE, # changed to SE,
        #                      Sbeuv,
        #                      EUVfwhmxSE,EUVfwhmySE, # changed to SE,
        #                      BEUVfwhmx,BEUVfwhmy,
        #                      Isum1,Isum3,Psum1,Psum3,
        #                      GSUM1,GSUM3,CSUM1,CSUM3,S1,S3,
        #                      FW1x,FW1y,FW3x,FW3y,
        #                      FWHM1x,FWHM1y,FWHM3x,FWHM3y,
        #                      XPS,XPSe]
        #     else:
        #         results = [energy_range0,
        #                      [c-cX[0] for c in cX],
        #                      [c-cY[0] for c in cY],
        #                      iTot,er,pTot,erP,
        #                      gsums,csums,S,fwXs,fwYs,
        #                      ItotEUV,ItotBEUV,PtotEUV,PtotBEUV,
        #                      IGAeuv,IGAbeuv,PGAeuv,PGAbeuv,
        #                      Ceuv,Cbeuv,Seuv,Sbeuv,
        #                      EUVfwhmx,EUVfwhmy,BEUVfwhmx,BEUVfwhmy]
        # elif compareFits:
        #     results = [energy_range0,
        #                  [c-cX[0] for c in cX],
        #                  [c-cY[0] for c in cY],
        #                  iTot,er,pTot,erP,
        #                  gsums,csums,S,fwXs,fwYs,
        #                  Isum1,Isum3,Psum1,Psum3,
        #                  GSUM1,GSUM3,CSUM1,CSUM3,S1,S3,
        #                  FW1x,FW1y,FW3x,FW3y,
        #                  FWHM1x,FWHM1y,FWHM3x,FWHM3y]
        # else:
        #     results = [energy_range0,
        #                  [c-cX[0] for c in cX],
        #                  [c-cY[0] for c in cY],
        #                  iTot,er,pTot,erP,
        #                  gsums,csums,S,fwXs,fwYs]
        with open(savePath_images + 'results.pkl','wb') as f:
            pickle.dump(results, f,protocol=2)

if __name__=='__main__':
    test()