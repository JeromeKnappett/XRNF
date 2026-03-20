
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from skimage import io,  exposure, img_as_uint, img_as_float
from tqdm import tqdm
import os

from matplotlib.pyplot import figure

# figure(figsize=(3,3))
plt.rcParams["figure.figsize"] = (4,4)


def transmission(wl,T,beta):
    k = (2*np.pi) / wl
    trans = np.exp((-1*k * beta * T)) # np.exp(((-k) / (beta * T)))
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
                img_sum = img_sum - bg
                # seting all values less than 10 to 0 
                # img_sum[abs(img_sum) < 10] = 0
                img_sum[img_sum < 1] = 0
                # print(np.min(img_sum))
        
            if hist:
                numBins = 200
                #plot the histogram of intensity before darkfield subtraction
                counts,bins = np.histogram(img_before_dfsub,bins=numBins)
                # Using non-equal bin sizes, such that they look equal on a log scale
                logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
                fig,ax = plt.subplots(3,1,sharey=False,sharex=True)
                ax[0].hist(bins[:-1],bins=logbins,weights=counts)
                ax[0].set_title('Raw image')
                #overplot the histogram of intensity after bg subtraction.
                counts,bins = np.histogram(img_sum,bins=numBins)
                # logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
                ax[1].hist(bins[:-1],bins=logbins,weights=counts)
                ax[1].set_title('Processed image')
                counts,bins = np.histogram(bg,bins=numBins)
                # logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
                ax[2].hist(bins[:-1],bins=logbins,weights=counts)
                # ax[2].hist(bg)
                ax[2].set_title('Background')
                for a in ax:
                    a.set_xscale('log')
                fig.tight_layout()
                plt.show()
                
            
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
    imageFolder = '/user/home/data/HarmonicContam/Detector_Comission_August_2023/Beam_profile_90_to_350eV_cff1.4_offset-3 - Copy/'
    #'/user/home/data/HarmonicContam/Detector_Comission_August_2023/Beam_profile_90_to_350eV_attempt2/'
    darkFolder = '/user/home/data/HarmonicContam/Detector_Comission_August_2023/Darkfields2/'
    savePath_images ='/user/home/data/HarmonicContam/Detector_Comission_August_2023/ProcessedImages/BeamProfile_90to350_cff1.4_offset-3/'
    savePath_dark = '/user/home/data/HarmonicContam/Detector_Comission_August_2023/ProcessedImages/darkfield/'
    
    simFolder = '/user/home/data/HarmonicContam/Detector_Comission_August_2023/SimulatedIntensity/'
    fitFolder = savePath_images + 'fits/'
    compareSim = False
    compareFits = False
    gratingArea = True
    pickleResults = False
    
    processImages = True
    processDarkfield = False
    cropImages = True
    findCenter = False
    saveNormalised = True
    
    exposures = 100
    exposure_time = 25e-3
    energy_range =  [90,92] + [e for e in np.arange(100, 185,10)] + [185] + [e for e in np.arange(190,205,10)] + [e for e in np.arange(290,355,10)]    
    eLim = (np.min(energy_range)-10,np.max(energy_range)+10)
    
    # Creating directories for processed images
    Path(savePath_images + 'normalised/').mkdir(parents=True, exist_ok=True)
    Path(savePath_images + 'averaged/').mkdir(parents=False, exist_ok=True)
    
    if processDarkfield:
        print("\n Averaging darkfield images...")
        # sumImages(darkFolder,sumNum=4000,sortSkip=7,imgType=".tif",average=True,darkfield=None,savePath=savePath_dark,show=True,verbose=True)
        sumImages(darkFolder,name='beam_1_',sumNum=3999,imgType='.tif',average=True,
                              darkfield=None,
                              savePath=savePath_dark,hist=False,verbose=True,show=True)
    if processImages:
        print("\n Summing/Averaging images...")
        ims,iTot,er = sumImages(imageFolder,name='beam_3_',sumNum=exposures,imgType=".tif",average=True,
                                darkfield=savePath_dark + '3998.tif',
                                savePath=savePath_images,hist=True,verbose=True,show=True)
        pEr = [e/i for e,i in zip(er,iTot)] # percentage error for summed intensities
    else:
        print("\n Loading pre-processed images...")
        try:
            imgNums = [e for e in np.arange(exposures,exposures*(len(energy_range)-1),exposures)] + [exposures*len(energy_range)-1]
            print(imgNums)
            ims = [io.imread(savePath_images + str(i) + '.tif') for i in imgNums]
        except FileNotFoundError:
            pass
        try:
            imgNums = [e for e in np.arange(exposures,exposures*(len(energy_range)),exposures)] + [exposures*len(energy_range)-2]
            print(imgNums)
            ims = [io.imread(savePath_images + str(i) + '.tif') for i in imgNums]
        except:
            pass
        # print(imgNums)
        # ims = [io.imread(savePath_images + str(i) + '.tif') for i in imgNums]
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
            gs,cs,s = IoverGrating(i, GA=100.0e-6, dx=11.0e-6, dy=11.0e-6,show=False)
        else:
            gs,cs,s = IoverGrating(i, GA=100.0e-6, dx=11.0e-6, dy=11.0e-6,show=False)
            
        # gsPcm = gs/(4*(100.0e-6*100.0e-6))
        gsums.append((gs/(4*100.0e-6*100.0e-6*10000)))
        csums.append((cs/(100.0e-6*100.0e-6*10000)))
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
    # gsums,csums = [IoverGrating(i, GA=100.0e-6, dx=11.0e-6, dy=11.0e-6,show=True) for i in ims]
    
    
    # Loading simulated intensity tiffs
    IGAeuv, IGAbeuv = [],[]
    PGAeuv, PGAbeuv = [],[]
    ItotEUV, ItotBEUV = [],[]
    PtotEUV, PtotBEUV = [],[]
    if compareSim:
        import pickle
        
        # EUVpick = pickle.load(open(simFolder + 'EUVbeamProfile/data/harmonics/m1atMask_ME.pkl','rb')) # 'EUVbeamProfile/data/m1_atMask_ME/m1_atMask_ME.pkl', 'rb')) #'EUVbeamProfile/data/check2/atMask_ME/atMask_ME.pkl', 'rb'))
        # EUVres = (EUVpick[1],EUVpick[2])
        # EUVtiff = EUVpick[0] #*0.01 # commented out 03/10/23 - Jk
        BEUVpick = pickle.load(open(simFolder + 'atMask_cff2offset0_m1_LF.pkl', 'rb')) #'BEUVbeamProfile/data/m1_atMask_ME/m1_atMask_ME.pkl', 'rb'))
        BEUVres = (BEUVpick[1],BEUVpick[2])
        BEUVtiff = BEUVpick[0]
        BEUVtiff_SE = io.imread(simFolder + 'SE_cff2offset0_m1_LF.tif')
            
        # EUVranPix = [np.shape(EUVtiff)[1],np.shape(EUVtiff)[0]] #xL*11e-6,yL*11e-6]#[5.0e-3,6.6e-3]
        BEUVranPix = [np.shape(BEUVtiff)[1],np.shape(BEUVtiff)[0]]
        BEUVranPix_SE = [np.shape(BEUVtiff_SE)[1],np.shape(BEUVtiff_SE)[0]]
        # RxEUV,RyEUV = EUVranPix[0]*EUVres[0], EUVranPix[1]*EUVres[1]
        RxBEUV,RyBEUV = BEUVranPix[0]*BEUVres[0], BEUVranPix[1]*BEUVres[1]
        RxBEUV_SE,RyBEUV_SE = BEUVranPix_SE[0]*BEUVres[0], BEUVranPix_SE[1]*BEUVres[1]
        # EUVran = [eran*eres for eran,eres in zip(EUVranPix,EUVres)] #[ran[0]/EUVres[0], ran[1]/EUVres[1]]
        # BEUVran = [bran*bres for bran,bres in zip(BEUVranPix,BEUVres)] #[ran[0]/BEUVres[0], ran[1]/BEUVres[1]]
        
        # EUVtiff = EUVtiff[int(np.shape(EUVtiff)[0]//2 - EUVranPix[1]//2):int(np.shape(EUVtiff)[0]//2 + EUVranPix[1]//2),
        #                   int(np.shape(EUVtiff)[1]//2 - EUVranPix[0]//2):int(np.shape(EUVtiff)[1]//2 + EUVranPix[0]//2)]
        BEUVtiff = BEUVtiff[int(np.shape(BEUVtiff)[0]//2 - BEUVranPix[1]//2):int(np.shape(BEUVtiff)[0]//2 + BEUVranPix[1]//2),
                            int(np.shape(BEUVtiff)[1]//2 - BEUVranPix[0]//2):int(np.shape(BEUVtiff)[1]//2 + BEUVranPix[0]//2)]
        
        BEUVtiff_SE = BEUVtiff_SE[int(np.shape(BEUVtiff_SE)[0]//2 - BEUVranPix_SE[1]//2):int(np.shape(BEUVtiff_SE)[0]//2 + BEUVranPix_SE[1]//2),
                                  int(np.shape(BEUVtiff_SE)[1]//2 - BEUVranPix_SE[0]//2):int(np.shape(BEUVtiff_SE)[1]//2 + BEUVranPix_SE[0]//2)]
        
        # convering from ph/s/0.1%bw/mm^2 to ph/s/mm^2
        BEUVtiff = BEUVtiff * (0.1 / (20*0.396378 + 0.019051304))
        BEUVtiff_SE = BEUVtiff_SE * (0.1 / (20*0.396378 + 0.019051304))
        
        # converting from ph/s/mm^2 to ph/s/cm^2
        # EUVtiff = EUVtiff*(EUVres[0]*EUVres[1])/1e-6
        BEUVtiff =  (BEUVtiff/1.0e-6)*(BEUVres[0]*BEUVres[1]) 
        # BEUVtiff_SE =  BEUVtiff_SE*100
        BEUVtiff_SE = BEUVtiff_SE*(BEUVres[0]*BEUVres[1])/1.0e-6 #*0.01
        
        # convering from ph/s/0.1%bw to ph/s
        # BEUVtiff = BEUVtiff*
        
        plt.imshow(BEUVtiff,aspect='auto')
        plt.colorbar()
        plt.show()
        
        # EUVfwhmx,EUVfwhmy = getFWatValue(EUVtiff,frac=0.5,dx=EUVres[0],dy=EUVres[1],cuts='x',
        #                                  centered=True,smoothing=None,
        #                                  verbose=False,show=True)
        BEUVfwhmx,BEUVfwhmy = getFWatValue(BEUVtiff,frac=0.5,dx=BEUVres[0],dy=BEUVres[1],cuts='x',
                                           centered=True,smoothing=None,
                                           verbose=False,show=False)
        
        BEUVfwhmxSE,BEUVfwhmySE = getFWatValue(BEUVtiff_SE,frac=0.5,dx=BEUVres[0],dy=BEUVres[1],cuts='x',
                                               centered=True,smoothing=None,
                                               verbose=False,show=False)
    
        q = 1.60218e-19
        # ItotEUV.append(np.sum(EUVtiff)/(RxEUV*RyEUV*10000))
        ItotBEUV.append(np.sum(BEUVtiff)/(RxBEUV*RyBEUV*10000))
        ItotBEUV.append(np.sum(BEUVtiff_SE)/(RxBEUV_SE*RyBEUV_SE*10000))
        # PtotEUV.append((np.sum(EUVtiff)*q*90.44*1000)/(RxEUV*RyEUV*10000))
        PtotBEUV.append((np.sum(BEUVtiff)*q*184.76*1000)/(RxBEUV*RyBEUV*10000))
        PtotBEUV.append((np.sum(BEUVtiff_SE)*q*184.76*1000)/(RxBEUV_SE*RyBEUV_SE*10000))
        
        print('\n RX, RY = ', RxBEUV, RyBEUV)
        
        if gratingArea:
            # Geuv,Ceuv,Seuv = IoverGrating(EUVtiff, GA=100.0e-6, dx=EUVres[0], dy=EUVres[1],show=False)
            Gbeuv,Cbeuv,Sbeuv = IoverGrating(BEUVtiff, GA=100.0e-6, dx=BEUVres[0], dy=BEUVres[1],show=False)
            GbeuvSE,CbeuvSE,SbeuvSE = IoverGrating(BEUVtiff_SE, GA=100.0e-6, dx=BEUVres[0], dy=BEUVres[1],show=False)
            
            # Ceuv = Ceuv/(100.0e-6*100.0e-6*10000)
            Cbeuv = Cbeuv/(100.0e-6*100.0e-6*10000)
            CbeuvSE = CbeuvSE/(100.0e-6*100.0e-6*10000)
            
            # IGAeuv.append(Geuv/(4*100.0e-6*100.0e-6*10000)) #IsumEUV[1] + IsumEUV[2] + _IsumEUV[1] + _IsumEUV[2])
            IGAbeuv.append(Gbeuv/(4*100.0e-6*100.0e-6*10000)) #IsumBEUV[1] + IsumBEUV[2] + _IsumBEUV[1] + _IsumBEUV[2])
            IGAbeuv.append(GbeuvSE/(4*100.0e-6*100.0e-6*10000)) #IsumBEUV[1] + IsumBEUV[2] + _IsumBEUV[1] + _IsumBEUV[2])
            # PGAeuv.append((Geuv*q*90*1000)/(4*100.0e-6*100.0e-6*10000)) #(IsumEUV[1] + IsumEUV[2] + _IsumEUV[1] + _IsumEUV[2])*EtoJ*1000)
            PGAbeuv.append((Gbeuv*q*185*1000)/(4*100.0e-6*100.0e-6*10000))
            PGAbeuv.append((GbeuvSE*q*185*1000)/(4*100.0e-6*100.0e-6*10000))
    
    if compareFits:
        import xraydb
        
        hN = 3
        CF = 'C3H6' # chemical formula for ultralene
        beta1,beta2 = [],[]
        T1,T2 = [],[]
        for e in energy_range:
            # print('\n E: ', e)
            # print(CF)
            # print(xraydb.xray_delta_beta(CF, 0.855, int(e)))
            (d1,b1,atlen1) = xraydb.xray_delta_beta(CF, 0.855, int(e))
            beta1.append(b1)
            
            (d2,b2,atlen2) = xraydb.xray_delta_beta(CF,0.855,int(e)*2)
            beta2.append(b2)
            # (d3,b3,atlen3) = xraydb.xray_delta_beta(CF,0.855,int(e)*3)
            # beta2.append(b2)
            
            wl1 = (4.135667696e-15 * 299792458) / e
            wl2 = (4.135667696e-15 * 299792458) / (2*e)
            # wl3 = (4.135667696e-15 * 299792458) / (3*e)
            
            # print('\n')
            # print(wl1, wl2)
            tran1 = transmission(wl1,4.064e-6,b1)
            tran2 = transmission(wl2,4.064e-6,b2)
            # tran3 = transmission(wl3,4.064e-6,b3)
            
            # print(tran1,tran2)
            
            T1.append(tran1)
            T2.append(tran2)#+tran3)/2)
        
        h1 = []
        h3 = []
        for file in os.listdir(fitFolder):
            if file.endswith('1.tif'):
                h1.append(file)
            elif file.endswith('2.tif'):
                h3.append(file)
        sortedH1 = sorted(h1,key=lambda x: float(x[0:-4]))
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
        
        for i in range(0,len(sortedH1)):
            # converting from ph/s/cm^2 (at fundamental energy) to ph/s
            i1 = io.imread(fitFolder + sortedH1[i])*10000*(11.0e-6 * 11.0e-6)
            i3 = io.imread(fitFolder + sortedH3[i])*10000*(11.0e-6 * 11.0e-6)
            # converting from ph/s (at fundamental energy) to counts at detector
            i1 = photonsPs2counts(i1, energy_range[i], t=exposure_time, conversion=1.27)
            i3 = photonsPs2counts(i3, energy_range[i], t=exposure_time, conversion=1.27)
            # converting from counts to ph/s and accounting for transmission through ultralene filter
            i1 = counts2photonsPs(i1,energy_range[i],t=exposure_time,conversion=1.27) / T1[i]
            i3 = counts2photonsPs(i3,energy_range[i]*hN,t=exposure_time,conversion=1.27) / T2[i]
            
            # print(np.shape(i1))
            if i <10 and i<20:
                plt.plot(i1[np.shape(i1)[0]//2,:],label='F x')
                plt.plot(i3[np.shape(i3)[0]//2,:],label='H x')
                plt.plot(i1[:,np.shape(i1)[1]//2],label='F y')
                plt.plot(i3[:,np.shape(i3)[1]//2],label='H y')
                plt.legend()
                plt.show()
            
            pI1 = intensity2power(i1,energy_range[i])
            pI3 = intensity2power(i3,energy_range[i]*hN)
            
            #FWHM measured from gaussian fits
            fwhm1x, fwhm1y = getFWatValue(i1,frac=0.5,dx=11.0e-6,dy=11.0e-6,show=False)
            fwhm3x, fwhm3y = getFWatValue(i3,frac=0.5,dx=11.0e-6,dy=11.0e-6,show=False)
            
            gs1,cs1,s1 = IoverGrating(i1, GA=100.0e-6, dx=11.0e-6, dy=11.0e-6,show=False)
            gs3,cs3,s3 = IoverGrating(i3, GA=100.0e-6, dx=11.0e-6, dy=11.0e-6,show=False)
            
            Isum1.append(np.sum(i1)/(Rx*Ry*10000)); Isum3.append(np.sum(i3)/(Rx*Ry*10000))
            Psum1.append(np.sum(pI1)/(Rx*Ry*10000)); Psum3.append(np.sum(pI3)/(Rx*Ry*10000))
            FW1x.append(fwhm1x); FW1y.append(fwhm1y); FW3x.append(fwhm3x); FW3y.append(fwhm3y)
            GSUM1.append(gs1/(4*100.0e-6*100.0e-6*10000)); GSUM3.append(gs3/(4*100.0e-6*100.0e-6*10000))
            CSUM1.append(cs1/(100.0e-6*100.0e-6*10000)); CSUM3.append(cs3/(100.0e-6*100.0e-6*10000))
            S1.append(s1); S3.append(s3)
        #     image = io.imread(path + str(name) + str(i) + str(imgType))
           

    if findCenter:
        plt.errorbar(energy_range,[(c-cX[0])*11.0 for c in cX],yerr=5.5,fmt='.',label='x')
        plt.errorbar(energy_range,[(c-cY[0])*11.0 for c in cY],yerr=5.5,fmt='.',label='y')
        plt.ylabel('Beam center drift [$\mu$m]')
        plt.xlabel('Photon energy [eV]')
        # plt.yscale('log')
        plt.xlim(eLim[0],eLim[1])
        plt.legend()
        plt.show()
    
    # print(len(energy_range[0:len(iTot)]))
    # print(len(iTot))
    plt.errorbar(energy_range[0:len(iTot)], iTot, yerr=er, fmt='.',label='data')
    if compareSim:
        # plt.plot(90,ItotEUV,'X',color='red',label='sim')
        plt.plot(185,ItotBEUV[0],'X',color='red',label='sim (ME)')
        plt.plot(185,ItotBEUV[1],'o',color='red',label='sim (SE)')
    if compareFits:
        plt.plot(energy_range[0:len(Isum1)],Isum1, '.', label='H1')
        plt.plot(energy_range[0:len(Isum1)],Isum3, '.', label='H3')
    plt.xlabel("Photon Energy [eV]")
    plt.ylabel("Total Intensity [$ph/s/cm^2$]")
    # plt.ylim(-1e11,np.max(iTot[0:41]) + 0.25e12)#2.5e12)#np.max(iTot[0:17]))
    plt.xlim(eLim[0],eLim[1])
    plt.yscale('log')
    plt.legend()
    plt.show()
    
    plt.errorbar(energy_range[0:len(iTot)], pTot, yerr=erP, fmt='.',label='data')
    if compareSim:
        # plt.plot(90,PtotEUV,'X',color='red',label='sim')
        plt.plot(185,PtotBEUV[0],'X',color='red', label= 'sim (ME)')
        plt.plot(185,PtotBEUV[1],'o',color='red', label= 'sim (SE)')
    if compareFits:
        plt.plot(energy_range[0:len(Isum1)],Psum1, '.', label='H1')
        plt.plot(energy_range[0:len(Isum1)],Psum3, '.', label='H3')
    plt.xlabel("Photon Energy [eV]")
    plt.ylabel("Total Power [$mJ/s/cm^2$]")
    # plt.ylim(-0.01,np.max(pTot[0:41])+0.05)
    plt.xlim(eLim[0],eLim[1])
    plt.yscale('log')
    plt.legend()
    plt.show()
    
    # print(len(ims))
    # print(len(energy_range))
    # print(len(gsums))
    
    plt.plot(energy_range[0:len(iTot)],gsums,'.',label='data')
    if compareSim:
        # plt.plot(90,IGAeuv,'X',color='red',label='sim')
        plt.plot(185,IGAbeuv[0],'X',color='red', label= 'sim (ME)')
        plt.plot(185,IGAbeuv[1],'o',color='red', label= 'sim (SE)')
    if compareFits:
        plt.plot(energy_range[0:len(Isum1)],GSUM1, '.', label='H1')
        plt.plot(energy_range[0:len(Isum1)],GSUM3, '.', label='H3')
    plt.xlabel("Photon Energy [eV]")
    plt.ylabel("Total Intensity over Grating [$ph/s/cm^2$]")
    # plt.ylim(-1e9,np.max(gsums[0:41]) + 0.05e10)#3.25e10) #np.max(gsums[0:17]))
    plt.xlim(eLim[0],eLim[1])
    plt.yscale('log')
    plt.legend()
    plt.show()
    
    plt.plot(energy_range[0:len(iTot)],csums,'.',label='data')
    if compareSim:    
        # plt.plot(90,Ceuv,'X',color='red',label='sim')
        plt.plot(185,Cbeuv,'X',color='red', label= 'sim (ME)')
        plt.plot(185,CbeuvSE,'o',color='red', label= 'sim (SE)')
    if compareFits:
        plt.plot(energy_range[0:len(Isum1)],CSUM1, '.', label='H1')
        plt.plot(energy_range[0:len(Isum1)],CSUM3, '.', label='H3')
    plt.xlabel("Photon Energy [eV]")
    plt.ylabel("Total Intensity over Central 100x100 um [$ph/s/cm^2$]")
    # plt.ylim(-1e8,np.max(csums[0:41]) + 0.05e10)#8e9)#np.max(csums[0:17]))
    plt.xlim(eLim[0],eLim[1])
    plt.yscale('log')
    plt.legend()
    plt.show()
    
    plt.plot(energy_range[0:len(iTot)],S,'.',label='data')
    if compareSim:
        # plt.plot(90,Seuv,'X',color='red',label='sim')
        plt.plot(185,Sbeuv,'X',color='red', label= 'sim (ME)')
        plt.plot(185,SbeuvSE,'o',color='red', label= 'sim (SE)')
    if compareFits:
        plt.plot(energy_range[0:len(Isum1)],S1, '.', label='H1')
        plt.plot(energy_range[0:len(Isum1)],S3, '.', label='H3')
    plt.xlabel("Photon Energy [eV]")
    plt.ylabel("Intensity Slope over Grating")
    plt.xlim(eLim[0],eLim[1])
    plt.legend()
    plt.yscale('log')
    plt.show()
    
    # plt.plot(energy_range,fwhmX,'.:',label='x')
    # plt.plot(energy_range,fwhmY,'.:',label='y')
    plt.plot(energy_range[0:len(iTot)],[f*1e3 for f in fwXs[0:60]], '.',label='x (data)')
    plt.plot(energy_range[0:len(iTot)],[f*1e3 for f in fwYs[0:60]], '.',label='y (data)')
    if compareSim:
        # plt.plot(90,EUVfwhmx*1e3,'X',color='r',label='x (sim)')
        # plt.plot(90,EUVfwhmy*1e3,'X',color='black',label='y (sim)')
        plt.plot(185,BEUVfwhmx*1e3,'X',color='r', label = 'sim (ME)')
        plt.plot(185,BEUVfwhmy*1e3,'X',color='black')
        plt.plot(185,BEUVfwhmxSE*1e3,'o',color='r', label= 'sim (SE)')
        plt.plot(185,BEUVfwhmySE*1e3,'o',color='black')
    # plt.plot(energy_range,[f*1e3 for f in FW1x], '.', label='H1 x')
    # plt.plot(energy_range,[f*1e3 for f in FW1y], '.', label='H1 y')
    # plt.plot(energy_range,[f*1e3 for f in FW3x], '.', label='H3 x')
    # plt.plot(energy_range,[f*1e3 for f in FW3y], '.', label='H3 y')
    if compareFits:
        plt.plot(energy_range[0:len(Isum1)],FWHM1x, '.', label='H1 x')
        plt.plot(energy_range[0:len(Isum1)],FWHM1y, '.', label='H1 y')
    # plt.plot(energy_range,FWHM3x, '.', label='H3 x')
    # plt.plot(energy_range,FWHM3y, '.', label='H3 y')
    plt.xlabel("Photon Energy [eV]")
    plt.ylabel("Intensity FWHM [mm]")
    # plt.ylim(0,np.max(fwXs[0:17]))
    plt.xlim(eLim[0],eLim[1])
    plt.legend()
    plt.show()
    
    
    plt.plot(energy_range[0:len(Isum1)],[g1/(g1 + g3) for g1,g3 in zip(Isum1,Isum3)],'.',label='Fundamental')
    plt.plot(energy_range[0:len(Isum1)],[g3/(g1 + g3) for g1,g3 in zip(Isum1,Isum3)],'.',label='Higher')
    plt.xlabel('Photon Energy [eV]')
    plt.ylabel('Fraction of Harmonic in Total Intensity')
    plt.legend()
    plt.show()
    
    plt.plot(energy_range,T1,label='T1')
    plt.plot(energy_range,T2,label='T2')
    plt.legend()
    plt.show()

# #plt.plot(energy_range[0:21],[h3/(h1+h3) for h1,h3 in zip(H1G,H3G)],'.',label='grating')
# #plt.plot(energy_range[0:21],[h3/(h1+h3) for h1,h3 in zip(H1C,H3C)],'.',label='center')
# plt.plot(energy_range[0:21],[h3/(h1+h3) for h1,h3 in zip(T1[0:21],T3[0:21])],'.',label='both')
# plt.xlabel('Photon Energy [eV]')
# plt.ylabel('Fraction of 3rd Harmonic in Total Intensity')
# #plt.legend()
# plt.show()

# #plt.plot(energy_range[0:21],[h3/h1 for h1,h3 in zip(H1G,H3G)],'.',label='grating')
# #plt.plot(energy_range[0:21],[h3/h1 for h1,h3 in zip(H1C,H3C)],'.',label='center')
# plt.plot(energy_range[0:21],[h3/h1 for h1,h3 in zip(T1[0:21],T3[0:21])],'.',label='both')
# plt.xlabel('Photon Energy [eV]')
# plt.ylabel('Ratio of Intensities of 1st and 3rd Harmonic')
# #plt.legend()
# plt.show()

# #plt.plot(energy_range[1:21],[h1/h3 for h1,h3 in zip(H1G[1::],H3G[1::])],'.',label='grating')
# #plt.plot(energy_range[1:21],[h1/h3 for h1,h3 in zip(H1C[1::],H3C[1::])],'.',label='center')
# plt.plot(energy_range[1:21],[h1/h3 for h1,h3 in zip(T1[1:21],T3[1:21])],'.',label='both')
# plt.xlabel('Photon Energy [eV]')
# plt.ylabel('Ratio of Intensities of 3rd and 1st Harmonic')
# #plt.legend()
# plt.show()
    
    # print(Seuv)
    # print(Sbeuv)
    
    
    if pickleResults:
        if compareSim:
            if compareFits:
                results = [energy_range,
                             [c-cX[0] for c in cX],
                             [c-cY[0] for c in cY],
                             iTot,er,pTot,erP,
                             gsums,csums,S,fwXs,fwYs,
                             ItotEUV,ItotBEUV,PtotEUV,PtotBEUV,
                             IGAeuv,IGAbeuv,PGAeuv,PGAbeuv,
                             # Ceuv,
                             Cbeuv,
                             # Seuv,
                             Sbeuv,
                             # EUVfwhmx,EUVfwhmy,
                             BEUVfwhmx,BEUVfwhmy,
                             Isum1,Isum3,Psum1,Psum3,
                             GSUM1,GSUM3,CSUM1,CSUM3,S1,S3,
                             FW1x,FW1y,FW3x,FW3y,
                             FWHM1x,FWHM1y,FWHM3x,FWHM3y]
            else:
                results = [energy_range,
                             [c-cX[0] for c in cX],
                             [c-cY[0] for c in cY],
                             iTot,er,pTot,erP,
                             gsums,csums,S,fwXs,fwYs,
                             ItotEUV,ItotBEUV,PtotEUV,PtotBEUV,
                             IGAeuv,IGAbeuv,PGAeuv,PGAbeuv,
                             Ceuv,Cbeuv,Seuv,Sbeuv,
                             EUVfwhmx,EUVfwhmy,BEUVfwhmx,BEUVfwhmy]
        elif compareFits:
            results = [energy_range,
                         [c-cX[0] for c in cX],
                         [c-cY[0] for c in cY],
                         iTot,er,pTot,erP,
                         gsums,csums,S,fwXs,fwYs,
                         Isum1,Isum3,Psum1,Psum3,
                         GSUM1,GSUM3,CSUM1,CSUM3,S1,S3,
                         FW1x,FW1y,FW3x,FW3y,
                         FWHM1x,FWHM1y,FWHM3x,FWHM3y]
        else:
            results = [energy_range,
                         [c-cX[0] for c in cX],
                         [c-cY[0] for c in cY],
                         iTot,er,pTot,erP,
                         gsums,csums,S,fwXs,fwYs]
        with open(savePath_images + 'results.pkl','wb') as f:
            pickle.dump(results, f,protocol=2)

if __name__=='__main__':
    test()