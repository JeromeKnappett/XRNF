# -*- coding: utf-8 -*-

"""

Created on Thu Jan 23 13:43:22 2020

@author: jerome knappett

"""

import os
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
#import imageio
#import tifffile
plt.rcParams["figure.figsize"] = (10,6) # added by GVR to make plots bigger and easier to read
# plt.style.use(['science','high-vis','no-latex']) # 'ieee', high-vis, high-contrast

from matplotlib import rc
rc('font', **{'family':'serif','serif':['Palatino']})
#rc('text', usetex=True)

#SINC FUNCTION DEFINITION
def sinc(x):
    z = np.where(x==0.0, 1.0, np.sin(x)/x)
    return z


def sumTiffs(tiffs, mean=True, savePath=None, writeType=None):
    """
    tiffs: List of tiffs to sum and average into a single tiff file
    mean: specify whether to take the mean of summed tiffs
    savePath: path to save final tiff file
    writeType: specify file type to save summed tiff as
    
    returns:
        tF: Final tiff file
        
    ## Uses tifffile to read as imageio was giving errors
    """
    
    T = []
    for t in tiffs:
        _t = plt.imread(t) #tifffile.imread(t)
        T.append(_t)
    
    if mean == True:
        tF = np.mean(np.array(T), axis=0)
    else:
        tF = np.array(T).sum(axis=0)
    
    if savePath != None:
        if writeType=='float16':
            imageio.imwrite(savePath, np.float16(tF))
        if writeType=='float32':
            imageio.imwrite(savePath, np.float32(tF))
        if writeType=='float64':
            imageio.imwrite(savePath, np.float64(tF))
        if writeType=='float128':
            imageio.imwrite(savePath, np.float128(tF))
        elif writeType=='uint8':
            imageio.imwrite(savePath, np.uint8(tF))
        elif writeType=='uint16':
            imageio.imwrite(savePath, np.uint16(tF))
        elif writeType=='uint32':
            imageio.imwrite(savePath, np.uint32(tF))
        else:
            imageio.imwrite(savePath, tF)
        print('Summed tiff written to: {}'.format(savePath))
    
    return tF

def getVisibility(Iprofile,n, showPlot=False):
    """
    I: Intensity profile
    n: Number of pixels from center of profile to sample
    showPlot: True/False - Enable/Disable plotting of intensity profile central peak
    
    returns:
        V: Visibility
        Imax: Maximum intensity value
        Imin: Minimum intensity value
    """
    if showPlot == True:
        #gvr #plt.plot(Iprofile[int(len(Iprofile)/2-n)-20:int(len(Iprofile)/2+n)-20])  #plotting central fringe
        plt.plot(Iprofile[int(len(Iprofile)/2-n):int(len(Iprofile)/2+n)])  #plotting central fringe
        #plt.ticklabel_format(axis='x', style='sci', scilimits=(-4,4))
        plt.title("Central Fringe")
        plt.show()
    #gvr
    # Imax = max(Iprofile[int(len(Iprofile)/2-n)-20:int(len(Iprofile)/2+n)-20]) # fringe maxima
    # Imin = min(Iprofile[int(len(Iprofile)/2-n)-20:int(len(Iprofile)/2+n)-20]) # fringe minima
    
    Imax = max(Iprofile[int(len(Iprofile)/2-n):int(len(Iprofile)/2+n)]) # fringe maxima
    Imin = min(Iprofile[int(len(Iprofile)/2-n):int(len(Iprofile)/2+n)]) # fringe minima
    
    print('Imax:')
    print(Imax)
    print('Imin')
    print(Imin)
    
    V = (Imax-Imin)/(Imax+Imin) # visibility
    
    print('Visibility:')
    print(V)
    
    return V, Imax, Imin


def ydsInterference(x,u,I,a,b,z,lam,dlam,delta,dx=0, showPlot=False):
    """
    x: Range of horizontal positions
    u: Degree of Coherence
    I: Central Intensity
    a: slit width
    b: slit separation
    z: distance from YDS to image plane
    lam: wavelength of radiation
    dlam: wavelength spread
    delta: spatial resolution of detector
    dx: horizontal drift - default is 0
    showPlot: True/False - Enable/Disable plotting of interference profile
    
    returns:
        Ix: Interference intensity profile
    """
    
#    eF = (sinc(np.pi*a*(x+dx)/(lam*z)))**2 # envelope function
#    iF = np.cos((2*np.pi*b*(x+z)/(lam*z))) # interference function
#    
#    Ix = I*(eF*(1+u*(sinc((np.pi*dlam*(x+z))/(lam*z)))*(sinc((np.pi*delta*b)/(lam*z)))*iF))
#    
    x=x+dx
    eF = (sinc(np.pi*a*(x)/(lam*z)))**2 # envelope function
    iF = np.cos((2*np.pi*b*(x)/(lam*z))) # interference function
    
    Ix = I*(eF*(1+u*(sinc((np.pi*dlam*(x))/(lam*z)))*(sinc((np.pi*delta*b)/(lam*z)))*iF))
   
#    plt.plot(eF, label="envelope")
#    plt.plot(iF, label="interference")
#    plt.plot(Ix, label="total")
#    plt.legend()
#    plt.show()
    
    return Ix


def prepYDSTiffs(Itiffs, Dtiffs, slits, sumDarks=True,sumLights=True, path=None):
    """

    Parameters
    ----------
    Itiffs : 
        Array of paths to intensity tiff files.
        If sumLights is False --> Itiffs is the path to the summed intensity tiff
    Dtiffs : 
        Array of paths to darkfield tiff files.
        If sumDarks is False --> Dtiffs is the path to the summed darkfield tiff
    slits : 
        Array of exit slit separations.
    sumDarks :  optional - The default is True.
        Specify whether to sum the array of darkfield tiffs
    sumLights : optional - The default is True.
        Specify whether to sum the array of darkfield tiffs
    path : optional - The default is None.
        Save path to save summed intensity and darkfield tiffs

    Returns
    -------
    Iprofiles :
        array of intensity line profiles 

    """
    
    # SUMMING DARK FIELDS TO SUBTRACT FROM DATA
    #sumDarks = True         # enable/disable dark field summing
    #sumLights = True        # enable/disable intensity summing
    
    # path = '/home/jerome/dev/data/YDS/'
    if path!=None:
        darkPath = path + 'summedDarkField.tif'
        # lightPath = path + 'summedIntensity.tif'
        
        
    if sumDarks == True:
        print(" ")
        print("----- Summing dark field tiff files -----")
    #    dark_fields = [path + '/darkFields/M17186_13' + str(i) + '.tif' for i in range(602,702)]
        if path!=None:
            darkF = sumTiffs(Dtiffs, mean=True, savePath=darkPath) #,writeType='float16')
        elif path==None:
            darkF = sumTiffs(Dtiffs, mean=True)
    
    elif sumDarks == False:
        print(" ")
        print("----- Darkfield summing disabled -----")
        darkF = plt.imread(Dtiffs) # tifffile.imread(Dtiffs) #plt.imread(Dtiffs)
    
    
    # DEFINING TIFF FILES FOR EACH EXIT SLIT SETTING
    if sumLights !=False:
        numT = np.shape(Itiffs)[0]
    else:
        # print(Itiffs)
        numT = np.shape(Itiffs)[1]
    print(" ")
    print("Number of tiffs to analyse: {}".format(numT))
    
    tiff_files = Itiffs
    horSlits = slits
    
    print("Shape of array of intensity tiff files: {}".format(np.shape(tiff_files)))
    
    # SUMMING INTENSITY DATA FOR EACH EXIT SLIT SETTING
    if sumLights == True:
        print(" ")
        print("----- Summing Intensity tiff files for each exit slit setting -----")
        Isums = []
        #for r in range(0,np.shape(tiff_files)[0]):
        for i, s in enumerate(horSlits):    
#            print(s)
#            print(np.shape(tiff_files[i]))
#            print(tiff_files[i])
            print(" ")
            print("Summing " + str(np.squeeze(np.shape(tiff_files[i]))) + " tiff files for exit slit setting #"+ str(i+1))
            if path!=None:
                print(tiff_files[i])
                I = sumTiffs(tiff_files[i],mean=True,savePath=path+str(s)+'.tif') #,writeType='float16')
            else:
                print(tiff_files[i])
                I = sumTiffs(tiff_files[i],mean=True,savePath=None) #,writeType='float16')
#            except IndexError:
#                print(np.shape(tiff_files[i][0]))
#                print(tiff_files[i][0])                
#                print("Summing " + str(np.squeeze(np.shape(tiff_files[i][0]))) + " tiff files for exit slit setting #"+ str(i+1))
            
#                I = sumTiffs(tiff_files[i][0],savePath=None)
            
            print("Shape of summed intensity file: {}".format(np.shape(I)))
            
            nX,nY = np.shape(I)
            
            A = np.mean(I[0,0:5])
            B = np.mean(darkF[0,0:5])
            
            print('A = {}, B={}'.format(A,B))
            print('Min: ' + str(np.min(A)))
            
            Inew = np.subtract(I,darkF)
            print('Min: {}'.format(np.min(Inew)))
            #print('Min: ' + str(np.min(Inew)))
            Inew = Inew -5
            Inew[Inew<0] = 0   #gvr
            #Inew = Inew + (0- np.min(Inew))
            
            print('Min: {}'.format(np.min(Inew)))
            
            Isums.append(Inew)
           
            plt.imshow(np.log(darkF), cmap='gray')
            plt.title("log(Dark Field)") #602-701
            plt.colorbar()
            plt.show()
          
            plt.title("log(Summed intensity #" + str(i+1))
            plt.imshow(np.log(I), cmap='gray')
            plt.colorbar()
            plt.show()
            
            plt.imshow(np.log(Inew+1), cmap='gray')
            plt.title("log(Intensity - Dark Field) #" + str(i+1))
            plt.colorbar()
            plt.show()

            
#            fig, axs = plt.subplots(3,1)
#            MAX = np.max(I)
#            MIN = np.min(I)
#            im = axs[0].imshow(darkF, cmap='gray', vmax=MAX, vmin=MIN)
#            axs[0].set_title("Dark Fiel)") #602-701
#            axs[1].imshow(np.log10(I), cmap='gray')
#          
#            axs[1].set_title("log(Summed intensity) #" + str(i+1))
#            axs[2].imshow(I-darkF, cmap='gray', vmax=MAX, vmin=MIN)
#            axs[2].set_title("Intensity - Dark Field")
#            fig.subplots_adjust(right=0.8)
#            cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#            #fig.colorbar(im, cax=cbar_ax)       
#            
            if path!=None:
                plt.savefig(path + 'plots/' + str(i) + 'Intensity_s' + str(s) + '.png')
                imageio.imwrite(path + str(s) + '.tif', np.float32(Inew))
                print('Summed intensity written to: {}'.format(path + str(s) + '.tif'))
            plt.show()
    else:
        Isums = []
        for i in range(0,numT):
            I = tifffile.imread(Itiffs[i])  #tiff_files[0] #[path + str(s) + '.tif' for s in horSlits]
            
            Isums.append(I)
            
            
            fig, axs = plt.subplots(2,1)
            MAX = np.max(I)
            MIN = np.min(I)
            im = axs[0].imshow(darkF, cmap='gray', vmax=MAX, vmin=MIN)
            axs[0].set_title("Dark Field") #602-701
            axs[1].imshow(I, cmap='gray')
            axs[1].set_title("Summed intensity #" + str(i+1))
            # axs[2].imshow(I-darkF, vmax=MAX, vmin=MIN)
            # axs[2].set_title("Intensity - Dark Field")
            fig.subplots_adjust(right=0.8)
            cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
            fig.colorbar(im, cax=cbar_ax)
            if path!=None:
                fnam=path + 'plots/' + str(i) + 'Intensity_s' + str(s) + '.png'
                plt.savefig(fnam)
                print('Wrote ' + fnam)
            plt.show()        
            
            
    
    
    
    # TAKING LINE PROFILES OF EACH SUMMED INTENSITY TIFF
    Imid = [190,221]
    N = 3  # Number of pixels from the center to average for line profile
   
    
    Iprofiles = []
#    print(Isums)
    print("Shape of Isums: {}".format(np.shape(Isums)))
    
    for n, i in enumerate(Isums):
    #    print(i)
    
        i = i[:,500:2048-500]
        nX,nY = np.shape(i)
        print('nY: {}'.format(nY))
         
        Dx = nY*13.5e-6   #gvr
        #print('Dx  = {}'.format(Dx))
        
        xRange=np.linspace(-Dx/2,Dx/2,nY)
        
        if N == 0:
            Icut = i[Imid,:]
            Iprofile = Icut
        else:
            Iprofile=np.zeros_like(xRange)
            for y in Imid:
                Icut = i[y-N:y+N,:]
                Iprofile += Icut.mean(0)
        
        plt.clf()
        plt.close()
        plt.plot(xRange,Iprofile)
        plt.title("I Cut")
        plt.show()
        if path!=None:
            plt.savefig(path + 'plots/' + str(n) + 'IntensityCut_s' + str(s) + '.tif')

        Iprofiles.append(Iprofile)
    
    return Iprofiles


def fitYDSInterference(Iprofiles,detRange,iG,constraints,weights=None,savePath=None):
    """

    Parameters
    ----------
    Iprofiles :
        Array of intensity profiles (generated from prepYDSTiffs()).
    detRange : 
        Detector range [m], along axis of interference.
    iG : 
        Array of initial guess values for fit.
#    known : 
#        Boolean array specifying which values are known
#        0=unknown
#        1=known
    savePath:
        Path to save intensity plots with fits

    Returns
    -------
    vis :
        Visibility of central interference fringe.
    coherence : 
        Degree of coherence from final fit.

    """
    
    vis = []
    coherence = [] 
    err_c = []
    paramNames = ['Degree of Coherence',
                 'Central Intensity',
                 'Slit Width',
                 'Slit Separation',
                 'Distance from YDS to Detector',
                 'Wavelength',
                 'Wavelength Spread',
                 'Detector Resolution',
                 'Horizontal Drift']
  
    
    p0 = iG
    p0_r=[]
    constraints_r = []
    for p,c in zip(p0,constraints):
        if c[0] != c[1]:
            p0_r.append(p)
            constraints_r.append(c)
      
    constraints_r = list(zip(*constraints_r))
    constraints_r = [list(constraints_r[0]),list(constraints_r[1])]
        
    for pNum, Iprof in enumerate(Iprofiles):
        
        print("------ Fitting interference profile #{} ------".format(pNum+1))
        #n = 1000 #number of data points sampled from centre
        n = 30#int(np.size(Iprof) /2)
        #print('n = ' + str(n))
        V, Imax, Imin = getVisibility(Iprof, n, showPlot=False)
        vis.append(V)
        nY = len(Iprof)
        xRange=np.linspace(-detRange/2,detRange/2,nY)

        #update intensity guess and constraints
        constraints_r[0][1] = Imax*0.375
        constraints_r[1][1] = Imax#*0.75
        p0_r[1] = Imax*0.5
        p0[1] = p0_r[1]
        # update mu guess
        p0_r[0] = V
        p0[0]=p0_r[0]
        
        print("I - [max/min/guess]: {}".format([Imax*0.4,Imax,Imax*0.6]))
        
        #update mu constraints - added by jerome
#        constraints_r[0][0] = V*0.25
        if V+(V*0.1) > 1:
            constraints_r[1][0] = 1
        else:
            constraints_r[1][0] = V #+(V*0.1)
        
        
        
        # SET BOUNDS FOR VARIABLES

       
#        param_bounds = bounds    
#        for i, k in enumerate(known):
#            if k == 1:
#                param_bounds[0][i] = iG[i]-iG[i]
#                param_bounds[1][i] = iG[i]+iG[i]
#                print("Value of {} is known... restricting fit".format(paramNames[i]))
#            if iG[i] < param_bounds[0][i]:
#                print(" ")
#                print("Initial guess for {} less than lower bounds... adjusting bounds".format(paramNames[i]))
#                p_old = param_bounds[0][i]
#                param_bounds[0][i] = iG[i]-iG[i]
#                print("Guess Value: {},  Initial Lower Bound Value: {},  New Lower Bound: {}".format((iG[i]),(p_old),(param_bounds[0][i])))
#            elif iG[i] > param_bounds[1][i]:
#                print(" ")
#                print("Initial guess for {} greater than upper bounds... adjusting bounds".format(paramNames[i]))
#                p_old = param_bounds[1][i]
#                param_bounds[1][i] = iG[i]+iG[i]                
#                print("Guess Value: {},  Initial Upper Bound Value: {},  New Upper Bound: {}".format((iG[i]),(p_old),(param_bounds[1][i])))
#                
#                


        # Arrays for plotting evolution of parameters
        dC = []
        I_0 = []
        W = []
        S = []
        Z = []
        wL = []
        dwL = []
        R = []
        dX = []
        
        guess = ydsInterference(xRange,                  # x-range       
                                p0[0],                  # u-degree of coherence
                                p0_r[1],                  # I-central intensity
                                p0[2],                  # a-slit width
                                p0[3],                  # b-slit separation
                                p0[4],                  # z-dist from YDS to image
                                p0[5],                  # lam- wavelength
                                p0[6],                  # dlam- wavelength spread
                                p0[7],                  # delta- detector resolution
                                p0[8])                  # dx-horizontal drift
        
        dC.append(p0[0])
        I_0.append(p0_r[1])
        W.append(p0[2])
        S.append(p0[3])
        Z.append(p0[4])
        wL.append(p0[5])
        dwL.append(p0[6])
        R.append(p0[7])
        dX.append(p0[8])
        
        # curve_fit() function takes the f-function
        # x-data and y-data as argument and returns
        # the coefficient u in param and
        # the estimated covariance of param in param_cov
        #range(len(Iprof)),
        #param, param_cov = curve_fit(ydsInterference, Iprof, xRange, p0=p0, bounds=param_bounds)
        
        
        def f (x,u,I,a,b,z,dx):
            """
            x: Range of horizontal positions
            u: Degree of Coherence
            I: Central Intensity
            a: slit width
            b: slit separation
            z: distance from YDS to image plane
            lam: wavelength of radiation
            dlam: wavelength spread
            delta: spatial resolution of detector
            dx: horizontal drift - default is 0
            showPlot: True/False - Enable/Disable plotting of interference profile
            """
            return ydsInterference( x,
                                    u,
                                    I, 
                                    a,
                                    b,
                                    z,
                                    iG[5],
                                    iG[6],
                                    iG[7],
                                    dx,
                                    showPlot=False )
        
 
        
        #print(p0_r)
        #print(constraints_r)
        
        
        
        
        #param, param_cov = curve_fit(ydsInterference, Iprof, xRange, p0=p0, bounds=constraints)
        param, param_cov = curve_fit(f, Iprof, xRange, p0=p0_r, bounds=constraints_r,sigma=weights,absolute_sigma=True)
        
        perr = np.sqrt(np.diag(param_cov))
        
        print(" ")
        print("Covariance Matrix: {}".format(param_cov))
        
        print(" ")
        print("Error: ")
        print("/mu:                      {}".format(perr[0]))
        print("Central intensity:        {}".format(perr[1]))
        print("slit width:               {}".format(perr[2]))
        print("slit separation:          {}".format(perr[3]))
        print("z distance:               {}".format(perr[4]))
        print("x drift:                  {}".format(perr[5]))
        
        
        
        # ans stores the new y-data according to
        # the coefficient given by curve-fit() function
        
#        y_fit = ydsInterference(xRange,
#                                param[0],  
#                                param[1], 
#                                param[2],
#                                param[3],
#                                param[4],
#                                param[5],
#                                param[6],
#                                param[7],
#                                param[8])
               
        y_fit = f(xRange,*param)

        plt.clf()
        plt.close()
        plt.plot(Iprof, color ='red', label ="data")
        plt.plot(guess, color = 'green', label="Initial Guess")
        plt.ticklabel_format(axis='x', style='sci', scilimits=(-4,4))
        plt.legend()
        if savePath !=None:
            plt.savefig(savePath + str(pNum) + 'initialGuess.png')
        plt.show()
        
        #plt.plot(Iprof, '.', color ='red', label ="data")
        #plt.plot(y_fit, '--', color ='blue', label ="Model Fit")
        #plt.ticklabel_format(axis='x', style='sci', scilimits=(-4,4))
        #plt.legend()
        #plt.show()
#        
#        print(" ")
#        print("----- Coeffients-----")
#        print("Degree of Coherence (u):            {}".format(param[0]))
#        print("Central Intensity (I0):             {}".format(param[1]))
#        print("Slit Width [m] (a):                 {}".format(param[2]))
#        print("Slit Separation [m] (b):            {}".format(param[3]))
#        print("Distance from YDS to Image [m] (z): {}".format(param[4]))
#        print("Wavelength [m] (lam):               {}".format(param[5]))
#        print("Wavelength Spread [m] (dlam):       {}".format(param[6]))
#        print("Detector Resolution [m] (delta):    {}".format(param[7]))
#        print("Horizontal Drift [m] (dx):          {}".format(param[8]))
        
        text =("\n\mu = {}\n  \
               I0 = {}\n \
               a = {} m\n \
               b = {} m \n \
               z = {} m \n \
               \lambda = {} m \n \
               \delta\lambda = {} \n \
               px = {} m \n \
               dx = {} \n \
               ".format(param[0],
                       param[1],
                       param[2],
                       param[3],
                       param[4],
                       p0[5],
                       p0[6],
                       p0[7],
                       param[5]))
        

        #print(" ")
        #print("Covariance of coefficients:")
#        #print(param_cov)
#        print(text)
        
        dC.append(param[0])
        I_0.append(param[1])
        W.append(param[2])
        S.append(param[3])
        Z.append(param[4])
#        wL.append(param[5])
#        dwL.append(param[6])
#        R.append(param[7])
        dX.append(param[5])
        
        iterations = 50 # number of iterations of the curve_fit() function in while loop below
        i=1

        plt.clf()
        plt.close()        
        plt.plot(Iprof, '.', color ='red', label ="data")
        plt.plot(y_fit, ':', color = 'green', label="Model Fit - Initial")
        plt.ticklabel_format(axis='x', style='sci', scilimits=(-4,4))
#        
#        print("Degree of coherence: {}".format(dC))
        coherence.append(dC[1])
        err_c.append(perr[0])
#        paramN=param
#        while i < iterations:
#            print("Refining fitting... attempt #{}".format(i))
#            #param1, param_cov1 = curve_fit(ydsInterference, Iprof, xRange, p0=param, bounds=param_bounds)
#            paramN1=paramN
#            paramN, param_cov = curve_fit(f, Iprof, xRange, p0=p0_r, bounds=constraints_r,sigma=weights,absolute_sigma=True)
#
#        
#        
##            y_fit1 = ydsInterference(xRange,
##                                    param1[0],
##                                    param1[1],
##                                    param1[2],
##                                    param1[3],
##                                    param1[4],
##                                    param1[5],
##                                    param1[6],
##                                    param1[7],
##                                    param1[8])
#            y_fit = f(xRange,*paramN)
#            
#            #plt.plot(y_fit1, '--', label ="Model Fit - #" + str(i))
#            plt.plot(y_fit, '--', label ="Model Fit - #" + str(i))
#            plt.show()
#            
##            print(" ")
##            print("----- Coeffients-----")
##            print("Degree of Coherence (u):            {}".format(param1[0]))
##            print("Central Intensity (I0):             {}".format(param1[1]))
##            print("Slit Width [m] (a):                 {}".format(param1[2]))
##            print("Slit Separation [m] (b):            {}".format(param1[3]))
##            print("Distance from YDS to Image [m] (z): {}".format(param1[4]))
##            print("Wavelength [m] (lam):               {}".format(param1[5]))
##            print("Wavelength Spread [m] (dlam):       {}".format(param1[6]))
##            print("Detector Resolution [m] (delta):    {}".format(param1[7]))
##            print("Horizontal Drift [m] (dx):          {}".format(param1[8]))
##            print(" ")
##            
#            print(" ")
#            print("----- Coeffients-----")
#            print("Degree of Coherence (u):            {}".format(paramN[0]))
#            print("Central Intensity (I0):             {}".format(paramN[1]))
#            print("Slit Width [m] (a):                 {}".format(paramN[2]))
#            print("Slit Separation [m] (b):            {}".format(paramN[3]))
#            print("Distance from YDS to Image [m] (z): {}".format(paramN[4]))
#    #        print("Wavelength [m] (lam):               {}".format(param[5]))
#    #        print("Wavelength Spread [m] (dlam):       {}".format(param[6]))
#    #        print("Detector Resolution [m] (delta):    {}".format(param[7]))
#            print("Horizontal Drift [m] (dx):          {}".format(paramN[5]))
#            
#        #    print("Covariance of coefficients:")
#        #    print(param_cov1)
#            
#            dC.append(paramN[0])
#            I_0.append(paramN[1])
#            W.append(paramN[2])
#            S.append(paramN[3])
#            Z.append(paramN[4])
##            wL.append(paramN[5])
##            dwL.append(paramN[6])
##            R.append(paramN[7])
#            dX.append(paramN[5])
#            
#            if np.all(paramN) == np.all(paramN1):
#                print(" ")
#                print("----- Fitting parameters have reached equilibrium after {} iterations -----".format(i))
#                coherence.append(paramN[0])
#                break
#            
#        else:
#            coherence.append(paramN[0])
#            print(" ")
#            print("----- Completed {} iterations without stagnation -----".format(iterations))
#            
#        
        plt.legend()
        if savePath !=None:
            plt.savefig(savePath + str(pNum) + 'fittingPlot.png')
        #plt.show()

#        plt.clf()
#        plt.close()
#        plt.plot(np.log(Iprof), '.', color ='red', label ="data")
##        plt.plot(y_fit1, '--', color ='blue', label ="Final Fit")
#        plt.plot(np.log(y_fit.astype(int)), '--', color ='blue', label ="Final Fit")
#        plt.plot(np.log(guess.astype(int)), ':', color = 'green', label="Initial Guess")
#        plt.ticklabel_format(axis='x', style='sci', scilimits=(-4,4))
#        plt.legend()
#        if savePath !=None:
#            plt.savefig(savePath + str(pNum) + 'finalPlot.png')
#        plt.show()
        
       
        plt.plot((Iprof), '.-', color ='red', label ="data")
#        plt.plot(y_fit1, '--', color ='blue', label ="Final Fit")
        plt.plot((y_fit.astype(int)), '--', color ='blue', label ="Final Fit")
        plt.plot((guess.astype(int)), ':', color = 'green', label="Initial Guess")
        plt.ticklabel_format(axis='x', style='sci', scilimits=(-4,4))
        plt.legend()
        plt.text(2,1,text)
        if savePath !=None:
            plt.savefig(savePath + str(pNum) + 'finalPlot.png')
        plt.show()
        
#        plt.plot((Iprof), '.-', color ='red', label ="data")
##        plt.plot(y_fit1, '--', color ='blue', label ="Final Fit")
#        plt.plot((y_fit.astype(int)), '-', color ='blue', label ="Final Fit")
#        plt.plot((guess.astype(int)), ':', color = 'green', label="Initial Guess")
#        plt.ticklabel_format(axis='x', style='sci', scilimits=(-4,4))
#        plt.legend()
#        plt.xlim( [100, 650])
#        if savePath !=None:
#            plt.savefig(savePath + str(pNum) + 'finalPlot.png')
#        plt.show()
#
#
#        plt.clf()
#        plt.close()
#==============================================================================
#         fig, axs = plt.subplots(3,3)
#         
#         axs[0,0].plot(dC)
#         axs[0,0].set_title("Degree of Coherence")
#         axs[0,0].set_ylim(param_bounds[0][0],param_bounds[1][0])
#         axs[0,1].plot(I_0)
#         axs[0,1].set_title("Central Intensity")
#         axs[0,1].set_ylim(param_bounds[0][1],param_bounds[1][1])
#         axs[0,2].plot(W)
#         axs[0,2].set_title("Slit Width")
#         axs[0,2].set_ylim(param_bounds[0][2],param_bounds[1][2])
#         axs[1,0].plot(S)
#         axs[1,0].set_title("Slit Separation")
#         axs[1,0].set_ylim(param_bounds[0][3],param_bounds[1][3])
#         axs[1,1].plot(Z)
#         axs[1,1].set_title("Image Plane Distance")
#         axs[1,1].set_ylim(param_bounds[0][4],param_bounds[1][4])
#         axs[1,2].plot(wL)
#         axs[1,2].set_title("Wavelength")
#         axs[1,2].set_ylim(param_bounds[0][5],param_bounds[1][5])
#         axs[2,0].plot(dwL)
#         axs[2,0].set_title("Wavelength spread")
#         axs[2,0].set_ylim(param_bounds[0][6],param_bounds[1][6])
#         axs[2,1].plot(R)
#         axs[2,1].set_title("Resolution")
#         axs[2,1].set_ylim(param_bounds[0][7],param_bounds[1][7])
#         axs[2,2].plot(dX)
#         axs[2,2].set_title("Horizontal Drift")
#         axs[2,2].set_ylim(param_bounds[0][8],param_bounds[1][8])
#         if savePath !=None:
#             plt.savefig(savePath + str(pNum) + 'parametersPlot.png')        
#         plt.show()
#==============================================================================
    
    return vis, coherence, err_c
    

def testYDSfitManual():
    """ Testing the fitting function for the manually aquired YDS interference intensity tiff files"""
    
    # NUMBER OF AQUISITIONS PER EXIT SLIT SEPARATION FOR EACH YDS
    # aqus = [[4,3]] # test
    aqus =       [[4,    3,    3,    3,    3,    3,    3,    3,    4,    5,    6,    6],#    7],#    20,   22],     # YDS-1
                  [3,    3,    3,    3,    3,    3,    3,    3,    4,    5,    6,    6],#    7],#    20,   22],     # YDS-2
                  [4,    4,    4,    4,    4,    5,    6,    5,    5,    6,    8,    6]]#,    7]]#,    20,   22]]     # YDS-3
    # SLIT SEPARATIONS FOR EACH YDS
    # horSlits = [[1100,1000]] # test
    horSlits =   [[1100, 1000, 900,  800,  700,  600,  500,  400,  350,  300,  250,  200],#,  150],#  100,  50],     # YDS-1
                  [1100, 1000, 900,  800,  700,  600,  500,  400,  350,  300,  250,  200],#,  150],#  100,  50],     # YDS-2
                  [1100, 1000, 900,  800,  700,  600,  500,  400,  350,  300,  250,  200]]#,  150]]#,  100,  50]]     # YDS-3
    # STARTING FILE NUMBER FOR EACH EXIT SLIT SEPARATION FOR EACH YDS
    # fileStarts = [[13715,13719]] # test
    fileStarts = [[13715,13719,13722,13725,13728,13731,13734,13740,13744,13748,13753,13759],#13767],#13777,13798],  # YDS-1
                  [13822,13827,13830,13833,13836,13839,13842,13845,13848,13852,13857,13863],#13869],#13876,13896],  # YDS-2
                  [13919,13923,13927,13931,13935,13939,13944,13950,13955,13960,13966,13974]]#,13980]]#,13987,14007]]  # YDS-3
    
    # Setting up an array of ranges to specify file names
    # ran = range(fileStarts[0],fileStarts[0] + aqus[0]) # test
    ran = [[range(fileStarts[n][i],fileStarts[n][i]+aqus[n][i]) for i in range(0,len(aqus[n]))] for n in range(0,len(aqus))]
    
#    print(ran[0])
#    print(" ")
#    print(ran[1])
#    print(" ")
#    print(ran[2])

    # DEFINING TIFF FILES FOR EACH EXIT SLIT SETTING
    path = '/user/home/opt/xl/xl/experiments/YDS/'
    tiff_f = []
    
    num=0
    for n in range(0,len(aqus)):
        print("Setting up tiff file array for YDS #{}".format(n+1))
        for a in ran[n]:
#            print(ran[n])
            # t = [path + 'yds' + str(num+1) + '/' + str(s) + '/' + 'M17186_' + str(i) + '.tif' for i in a]
            t = [path + 'yds' + str(num+6) + '/' + 'M17186_' + str(i) + '.tif' for i in a]
            try:
                [os.rename(path + 'tiffs/M17186_' + str(i) + '.tif', path + 'yds' + str(num+6) + '/M17186_' + str(i) + '.tif') for i in a] # moving tiff files into desired folders
            except FileNotFoundError:
                print("FILE OR DIRECTORY NOT FOUND: {} ".format(t))
                pass
            tiff_f.append(t)
        num +=1
    
    
    tiff_files = np.squeeze(tiff_f).reshape(np.shape(aqus)[0],np.shape(aqus)[1])
    
    
    # tiff_files = [path + 'yds' + str(num+1) + '/' + 'M17186_' + str(i) + '.tif' for i in ran]
    
#                  ]
#    print(" ")
#    print(tiff_files[0])
#    print(" ")
#    print(tiff_files[1])
#    print(" ")
#    print(tiff_files[2])
#    print(" ")
    print("Shape of tiff files array: {}".format(np.shape(tiff_files[2])))
    
    dark_fields = [path + 'tiffs/M17186_13' + str(i) + '.tif' for i in range(602,702)]
    
#    dR = 0.007 # Horizontal detector size   
    
#    print(tiff_files)
    
    #YDS-1 Analysis
#    Ip1 = prepYDSTiffs(Itiffs = tiff_files[0], 
#                      Dtiffs = dark_fields,  #path + 'summedDarkField.tif', #dark_fields, 
#                      slits = horSlits,
#                      sumDarks = True,
#                      sumLights = True,
#                      path = None) #path+'yds1/')
    
    # YDS-1 Analysis
    Ip6 = prepYDSTiffs(Itiffs = tiff_files[0],            # array of intensity tiff paths
                      Dtiffs = dark_fields,        # array of darkfield tiff paths     #dark_fields, path + 'summedDarkField.tif'
                      slits = horSlits[0],            # array of exit slit separations
                      sumDarks = True,             # If true - darkfield tiff files in Dtiffs are summed, if false darkfield tiff file Dtiff is a single previously summed darkfield tiff
                      sumLights = True,            # If true - tiff files in Itiffs are summed for each exit slit setting, if false - each exit slit setting uses only 1 tiff file (assumed previously summed)  
                      path = None )#'./yds0/')                 # Save path for data (summed tiff files)

    # YDS-2 Analysis
    Ip7 = prepYDSTiffs(Itiffs = tiff_files[1],            # array of intensity tiff paths
                      Dtiffs = dark_fields,        # array of darkfield tiff paths     #dark_fields, path + 'summedDarkField.tif'
                      slits = horSlits[1],            # array of exit slit separations
                      sumDarks = True,             # If true - darkfield tiff files in Dtiffs are summed, if false darkfield tiff file Dtiff is a single previously summed darkfield tiff
                      sumLights = True,            # If true - tiff files in Itiffs are summed for each exit slit setting, if false - each exit slit setting uses only 1 tiff file (assumed previously summed)  
                      path =None )# './yds0/')                 # Save path for data (summed tiff files)

    # YDS-3 Analysis
    Ip8 = prepYDSTiffs(Itiffs = tiff_files[2],            # array of intensity tiff paths
                      Dtiffs = dark_fields,        # array of darkfield tiff paths     #dark_fields, path + 'summedDarkField.tif'
                      slits = horSlits[2],            # array of exit slit separations
                      sumDarks = True,             # If true - darkfield tiff files in Dtiffs are summed, if false darkfield tiff file Dtiff is a single previously summed darkfield tiff
                      sumLights = True,            # If true - tiff files in Itiffs are summed for each exit slit setting, if false - each exit slit setting uses only 1 tiff file (assumed previously summed)  
                      path =None )# './yds0/')                 # Save path for data (summed tiff files)

    
    # # Testing
    # Ip1 = prepYDSTiffs(Itiffs = [[path + 'yds1/1100.tif', path + 'yds1/1000.tif']], #tiff_files[0]
    #                  Dtiffs = path + 'summedDarkField.tif', #dark_fields, 
    #                  slits = horSlits,
    #                  sumDarks = False,
    #                  sumLights = False,
    #                  path = None) #path+'yds1/')
    
    
    
    #FINDING VISIBILITY OF FRINGES
    vis = []
    n = 200 #number of data points sampled from centre
    px = 13.5e-6
   
  
   # V, Imax, Imin = getVisibility(Ip1[0], n, showPlot=False)
    
    #vis.append(V)
    
    #V = 0.75
    # INITIAL GUESS
    
     # Settings for YDS # 6
    p6 = [0.6,                                        # u-degree of coherence
            100,                                 # I-central intensity
            #420,
            0.85e-6,                                   # a-slit width
            4e-6,                                  # b-slit separation
            0.91   ,                                 # z-dist from YDS to image
            6.710308278912389e-9,                   # lam- wavelength
            0,                                  # dlam- wavelength spread
            px,                                 # delta- detector resolution
            1.9e-4
            ]                                 # dx- horizontal drift (+: left, -: right)
    
    cons6 = [ [0.4,0.8],            # u-degree of coherence
                    [1,1000],    # I-central intensity
                    #[300,1000],    # I-central intensity
                    [0.55e-6,0.995e-6],      # a-slit width
                    [2.95e-6,4.15e-6],    # b-slit separation
                    [0.905,0.935],        # z-dist from YDS to image
                    [6.710308278912389e-9, 6.710308278912389e-9],    # lam- wavelength
                    [0,0],                   # dlam- wavelength spread
                    [px, px],                # delta- detector resolution
                    [1.81e-4,2.9e-4]       # dx- horizontal drift (+: left, -: right)
                    ]
             
    # Settings for YDS # 7
    p7 = [0.9,                                        # u-degree of coherence
            100,                                 # I-central intensity
            #420,
            0.85e-6,                                   # a-slit width
            8.0e-6,                                  # b-slit separation
            0.91   ,                                 # z-dist from YDS to image
            6.710308278912389e-9,                   # lam- wavelength
            0,                                  # dlam- wavelength spread
            px,                                 # delta- detector resolution
            2.5e-4
            ]                                 # dx- horizontal drift (+: left, -: right)
    
    cons7 = [ [0.1,1.0],            # u-degree of coherence
                    [1,1000],    # I-central intensity
                    #[300,1000],    # I-central intensity
                    [0.75e-6,0.95e-6],      # a-slit width
                    [7.75e-6,8.25e-6],    # b-slit separation
                    [0.897,0.915],        # z-dist from YDS to image
                    [6.710308278912389e-9, 6.710308278912389e-9],    # lam- wavelength
                    [0,0],                   # dlam- wavelength spread
                    [px, px],                # delta- detector resolution
                    [2e-4,2.9e-4]       # dx- horizontal drift (+: left, -: right)
                    ]             
    
    # Settings for YDS # 8
    p8 = [0.8,                                        # u-degree of coherence
            100,                                 # I-central intensity
            #420,
            0.5e-6,                                   # a-slit width
            12e-6,                                  # b-slit separation
            0.91   ,                                 # z-dist from YDS to image
            6.710308278912389e-9,                   # lam- wavelength
            0,                                  # dlam- wavelength spread
            px,                                 # delta- detector resolution
            2.5e-4
            ]                                 # dx- horizontal drift (+: left, -: right)
    
    cons8 = [ [0.1,1.0],            # u-degree of coherence
                    [1,150],    # I-central intensity
                    #[300,1000],    # I-central intensity
                    [0.45e-6,0.65e-6],      # a-slit width
                    [10.5e-6,16.5e-6],    # b-slit separation
                    [0.897,0.915],        # z-dist from YDS to image
                    [6.710308278912389e-9, 6.710308278912389e-9],    # lam- wavelength
                    [0,0],                   # dlam- wavelength spread
                    [px, px],                # delta- detector resolution
                    [2.e-4,4.e-4]       # dx- horizontal drift (+: left, -: right)
                    ]    
    
    weights=None
   
    print(" ")
    print("YDS #6")
    v6, c6 = fitYDSInterference(Ip6,
                                detRange=len(Ip6[0]) * px, 
                                iG = p6,
                                constraints = cons6,
                                weights = weights,
                                savePath = './yds6/')
    
    print(" ")
    print("YDS #7")
    v7, c7 = fitYDSInterference(Ip7,
                                detRange=len(Ip7[0]) * px, 
                                iG = p7,
                                constraints = cons7,
                                weights = weights,
                                savePath = './yds7/')
    print(" ")
    print("YDS #8")
    v8, c8 = fitYDSInterference(Ip8,
                                detRange=len(Ip8[0]) * px, 
                                iG = p8,
                                constraints = cons8,
                                weights = weights,
                                savePath = './yds8/')# path + 'plots/' ) # need to manually create the 'plots' folder or else put None
            
    
    fig, axs = plt.subplots(2,1)
    axs[0].plot(horSlits[0], v6, label='yds #6')
    axs[0].plot(horSlits[0], v7, label='yds #7')
    axs[0].plot(horSlits[0], v8, label='yds #8')
    axs[0].legend()
    axs[0].set_ylabel("Visibility")
    axs[1].plot(horSlits[0], c6, label='yds #6')
    axs[1].plot(horSlits[0], c7, label='yds #7')
    axs[1].plot(horSlits[0], c8, label='yds #8')
    axs[1].legend()
    axs[1].set_ylabel("Coherence")
    axs[1].set_xlabel("Exit slit separation")
    plt.show()

    plt.plot(Ip6[4][int(len(Ip6[4])/2-30):int(len(Ip6[4])/2+30)]/np.max(Ip6[4]), label='#6')
    plt.plot(Ip7[4][int(len(Ip7[4])/2-30):int(len(Ip7[4])/2+30)]/np.max(Ip7[4]), label='#7')
    plt.plot(Ip8[4][int(len(Ip8[4])/2-30):int(len(Ip8[4])/2+30)]/np.max(Ip8[4]), label='#8')
#    plt.xlim(len(Ip1[4])/2-100,len(Ip1[4])+100)
    plt.legend()
    plt.show()
    
#    v1, c1 = fitYDSInterference(Ip1,detRange=dR)
#    
#    print("Visibility Values: {}".format(v1))
#    print("Coherence Values: {}".format(c1))
#    
#    fig, axs = plt.subplots(2,1)
#    axs[0].plot(horSlits[0], v1)
#    axs[0].set_title("Visibility")
#    axs[1].plot(horSlits[0], c1)
#    axs[1].set_title("Coherence")
#    #axs[1].set_xtitle("Exit slit separation")
#    plt.show()
#    
#    #YDS-2 Analysis
#    Ip2 = prepYDSTiffs(Itiffs = tiff_files[1],
#                      Dtiffs = path + 'summedDarkField.tif', 
#                      slits = horSlits, 
#                      sumDarks = False,
#                      sumLights = True,
#                      path = path+'yds2/')
#    v2, c2 = fitYDSInterference(Ip2,detRange=dR)
#    
#    print("Visibility Values: {}".format(v2))
#    print("Coherence Values: {}".format(c2))
#    
#    fig, axs = plt.subplots(2,1)
#    axs[0].plot(horSlits[1], v2)
#    axs[0].set_title("Visibility")
#    axs[1].plot(horSlits[1], c2)
#    axs[1].set_title("Coherence")
#    #axs[1].set_xtitle("Exit slit separation")
#    plt.show()
#    
#    #YDS-3 Analysis
#    Ip3 = prepYDSTiffs(Itiffs = tiff_files[2],
#                      Dtiffs = path + 'summedDarkField.tif', 
#                      slits = horSlits,
#                      sumDarks = False,
#                      sumLights = True,
#                      path = path+'yds3/')
#    
#    v3, c3 = fitYDSInterference(Ip3,detRange=dR)
#    
#    print("Visibility Values: {}".format(v3))
#    print("Coherence Values: {}".format(c3))
#    
#    fig, axs = plt.subplots(2,1)
#    axs[0].plot(horSlits[0], v3)
#    axs[0].set_title("Visibility")
#    axs[1].plot(horSlits[0], c3)
#    axs[1].set_title("Coherence")
#    #axs[1].set_xtitle("Exit slit separation")
#    plt.show()


def testYDSfitAuto():
    """ Testing the fitting function for the automatically aquired YDS interference intensity tiff files"""
    # NUMBER OF AQUISITIONS PER EXIT SLIT SEPARATION FOR EACH YDS
    aqus = [4,    4,    4,    4,    4,    5,    6,    5,    5,    6,    8,    6,    7,    20,   22] # test

    # SLIT SEPARATIONS FOR EACH YDS
    horSlits = [1100 , 1000, 900,  800,  700,  600,  500,  400,  350,  300,  250,  200,  150]#,  100,  50] # test
    
    # STARTING FILE NUMBER FOR 1ST YDS RUN
    
    runStart = 1   # Which YDS to start analysis (starting at yds1)
    fileStart = 14048 + (runStart - 1)*sum(aqus)
    numRuns = 2
    numAqus = len(aqus)-5
    
    
    horSlits = horSlits[0: numAqus]
    print(horSlits)
    
    ran = []
    # Setting up an array of ranges to specify file names
    for n in range(runStart-1,runStart+(numRuns-1)):
        print(" ")
        print("Setting up range for YDS run #{} ".format(n+1))
        print("Starting file number:      {}".format(fileStart))
        ranges = [range(fileStart + sum(aqus[0:i]), fileStart+sum(aqus[0:i+1])) for i in range(0,numAqus)] #len(aqus)
        fileStart += sum(aqus)
        # print("New starting file number: {}".format(fileStart))
        ran.append(ranges)
    
#    print(ran)
#    print(ran[0])
#    print(" ")
#    print(ran[1])
#    print(" ")
#    print(ran[2])

    # DEFINING TIFF FILES FOR EACH EXIT SLIT SETTING
    path = '/user/home/opt/xl/xl/experiments/YDS/'         # path to save data into/move tiff files into
    tiffPath = '/user/home/opt/xl/xl/experiments/YDS/tiffs/'     # original path of tiff files
    tiff_f = []
        
        
    for n in range(runStart-1,runStart+(numRuns-1)):
        print(" ")
        print("Setting up tiff file array for YDS #{}".format(n+1))
        os.makedirs(os.path.dirname(path + 'yds' + str(n+1) + '/'), exist_ok=True)   # making directories for each YDS
        for a in ran[n-(runStart-1)]:
#            print(ran[n])
            t = [path + 'yds' + str(n+1) + '/M17186_' + str(i) + '.tif' for i in a]
            try:
                [os.rename(tiffPath + 'M17186_' + str(i) + '.tif', path + 'yds' + str(n+1) + '/M17186_' + str(i) + '.tif') for i in a] # moving tiff files into desired folders
            except FileNotFoundError:
                print("FILE OR DIRECTORY NOT FOUND: {} ".format(t))
                pass
            tiff_f.append(t)
        
    
    print(tiff_f)

    # PATH TO DARKFIELD TIFFS
    dark_fields = [tiffPath + 'M17186_13' + str(i) + '.tif' for i in range(602,702)] 
    
    #gvr dR = 0.007 # Horizontal detector size    - used for plotting
    
    print("Shape of tiff array: {}".format(np.shape(tiff_f)))
    print("Shape of tiff[0] array: {}".format(np.shape(tiff_f[0])))
    
    if numRuns == 1:
        pass
    elif numAqus > 5:
        tiff_f = np.reshape(tiff_f,(numRuns,int(len(tiff_f)/numRuns)))
    else:
        tiff_f = np.reshape(tiff_f,(numRuns,int(len(tiff_f)/numRuns),4))
        
    print("Shape of tiff array: {}".format(np.shape(tiff_f)))
    
    # YDS-1 Analysis
    Ip1 = prepYDSTiffs(Itiffs = tiff_f[0],            # array of intensity tiff paths
                      Dtiffs = dark_fields,        # array of darkfield tiff paths     #dark_fields, path + 'summedDarkField.tif'
                      slits = horSlits,            # array of exit slit separations
                      sumDarks = True,             # If true - darkfield tiff files in Dtiffs are summed, if false darkfield tiff file Dtiff is a single previously summed darkfield tiff
                      sumLights = True,            # If true - tiff files in Itiffs are summed for each exit slit setting, if false - each exit slit setting uses only 1 tiff file (assumed previously summed)  
                      path = None )#'./yds0/')                 # Save path for data (summed tiff files)

    # YDS-2 Analysis
    Ip2 = prepYDSTiffs(Itiffs = tiff_f[1],            # array of intensity tiff paths
                      Dtiffs = dark_fields,        # array of darkfield tiff paths     #dark_fields, path + 'summedDarkField.tif'
                      slits = horSlits,            # array of exit slit separations
                      sumDarks = True,             # If true - darkfield tiff files in Dtiffs are summed, if false darkfield tiff file Dtiff is a single previously summed darkfield tiff
                      sumLights = True,            # If true - tiff files in Itiffs are summed for each exit slit setting, if false - each exit slit setting uses only 1 tiff file (assumed previously summed)  
                      path =None )# './yds0/')                 # Save path for data (summed tiff files)
    # YDS-3 Analysis
    Ip3 = prepYDSTiffs(Itiffs = tiff_f[2],            # array of intensity tiff paths
                      Dtiffs = dark_fields,        # array of darkfield tiff paths     #dark_fields, path + 'summedDarkField.tif'
                      slits = horSlits,            # array of exit slit separations
                      sumDarks = True,             # If true - darkfield tiff files in Dtiffs are summed, if false darkfield tiff file Dtiff is a single previously summed darkfield tiff
                      sumLights = True,            # If true - tiff files in Itiffs are summed for each exit slit setting, if false - each exit slit setting uses only 1 tiff file (assumed previously summed)  
                      path =None )# './yds0/')                 # Save path for data (summed tiff files)

    # YDS-2 Analysis
    Ip4 = prepYDSTiffs(Itiffs = tiff_f[3],            # array of intensity tiff paths
                      Dtiffs = dark_fields,        # array of darkfield tiff paths     #dark_fields, path + 'summedDarkField.tif'
                      slits = horSlits,            # array of exit slit separations
                      sumDarks = True,             # If true - darkfield tiff files in Dtiffs are summed, if false darkfield tiff file Dtiff is a single previously summed darkfield tiff
                      sumLights = True,            # If true - tiff files in Itiffs are summed for each exit slit setting, if false - each exit slit setting uses only 1 tiff file (assumed previously summed)  
                      path =None )# './yds0/')                 # Save path for data (summed tiff files)
    # YDS-3 Analysis
    Ip5 = prepYDSTiffs(Itiffs = tiff_f[4],            # array of intensity tiff paths
                      Dtiffs = dark_fields,        # array of darkfield tiff paths     #dark_fields, path + 'summedDarkField.tif'
                      slits = horSlits,            # array of exit slit separations
                      sumDarks = True,             # If true - darkfield tiff files in Dtiffs are summed, if false darkfield tiff file Dtiff is a single previously summed darkfield tiff
                      sumLights = True,            # If true - tiff files in Itiffs are summed for each exit slit setting, if false - each exit slit setting uses only 1 tiff file (assumed previously summed)  
                      path =None )# './yds0/')                 # Save path for data (summed tiff files)
    
#    # YDS-TEST Analysis
#    Ip1 = prepYDSTiffs(Itiffs = tiff_f,            # array of intensity tiff paths
#                      Dtiffs = dark_fields,        # array of darkfield tiff paths     #dark_fields, path + 'summedDarkField.tif'
#                      slits = horSlits,            # array of exit slit separations
#                      sumDarks = True,             # If true - darkfield tiff files in Dtiffs are summed, if false darkfield tiff file Dtiff is a single previously summed darkfield tiff
#                      sumLights = True,            # If true - tiff files in Itiffs are summed for each exit slit setting, if false - each exit slit setting uses only 1 tiff file (assumed previously summed)  
#                      path = None )#'./yds0/')                 # Save path for data (summed tiff files)


    print("Shape of profiles array: {}".format(np.shape(Ip0)))
    
    print(" ")
    #print("Finding central fringe visibility")
    print("Finding fringe visibility")
    
    #FINDING VISIBILITY OF FRINGES
    vis = []
    n = 200 #number of data points sampled from centre
    px = 13.5e-6
   
  
   # V, Imax, Imin = getVisibility(Ip1[0], n, showPlot=False)
    
    #vis.append(V)
    
    #V = 0.75
    # INITIAL GUESS
    p0 = [0.5,                                        # u-degree of coherence
            100,                                 # I-central intensity
            #420,
            1.2e-6,                                   # a-slit width    1.5e-6
            24e-6,                                  # b-slit separation
            0.91   ,                                 # z-dist from YDS to image  0.91
            6.710308278912389e-9,                   # lam- wavelength
            0,                                  # dlam- wavelength spread
            px,                                 # delta- detector resolution
            3.1e-4
            ]                                 # dx- horizontal drift (+: left, -: right)
    
    constraints = [ [0.6,1.0],            # u-degree of coherence
                    [1,1000],    # I-central intensity
                    #[300,1000],    # I-central intensity
                    [1.05e-6,1.35e-6],      # a-slit width    1.45e-6,1.55e-6
                    [14.0e-6,50e-6],    # b-slit separation
                    [0.905,0.915],        # z-dist from YDS to image    0.897,0.915
                    [6.710308278912389e-9, 6.710308278912389e-9],    # lam- wavelength
                    [0,0],                   # dlam- wavelength spread
                    [px, px],                # delta- detector resolution
                    [2.e-4,4.e-4]       # dx- horizontal drift (+: left, -: right)
                    ]

    
     # Settings for YDS # 5
    p5 = [0.6,                                        # u-degree of coherence
            100,                                 # I-central intensity
            #420,
            1.2e-6,                                   # a-slit width
            6e-6,                                  # b-slit separation
            0.91   ,                                 # z-dist from YDS to image
            6.710308278912389e-9,                   # lam- wavelength
            0,                                  # dlam- wavelength spread
            px,                                 # delta- detector resolution
            2.9e-4
            ]                                 # dx- horizontal drift (+: left, -: right)
    
    cons5 = [ [0.4,0.8],            # u-degree of coherence
                    [1,1000],    # I-central intensity
                    #[300,1000],    # I-central intensity
                    [1.05e-6,1.35e-6],      # a-slit width
                    [5.95e-6,6.15e-6],    # b-slit separation
                    [0.905,0.915],        # z-dist from YDS to image
                    [6.710308278912389e-9, 6.710308278912389e-9],    # lam- wavelength
                    [0,0],                   # dlam- wavelength spread
                    [px, px],                # delta- detector resolution
                    [2.81e-4,2.9e-4]       # dx- horizontal drift (+: left, -: right)
                    ]
             
    # Settings for YDS # 4
    p4 = [0.6,                                        # u-degree of coherence
            100,                                 # I-central intensity
            #420,
            0.65e-6,                                   # a-slit width
            10e-6,                                  # b-slit separation
            0.91   ,                                 # z-dist from YDS to image
            6.710308278912389e-9,                   # lam- wavelength
            0,                                  # dlam- wavelength spread
            px,                                 # delta- detector resolution
            2.9e-4
            ]                                 # dx- horizontal drift (+: left, -: right)
    
    cons4 = [ [0.1,1.0],            # u-degree of coherence
                    [1,1000],    # I-central intensity
                    #[300,1000],    # I-central intensity
                    [0.64e-6,0.68e-6],      # a-slit width
                    [9.1e-6,10.9e-6],    # b-slit separation
                    [0.897,0.915],        # z-dist from YDS to image
                    [6.710308278912389e-9, 6.710308278912389e-9],    # lam- wavelength
                    [0,0],                   # dlam- wavelength spread
                    [px, px],                # delta- detector resolution
                    [2.2e-4,3.5e-4]       # dx- horizontal drift (+: left, -: right)
                    ]             
    
    # Settings for YDS # 3
    p3 = [0.8,                                        # u-degree of coherence
            400,                                 # I-central intensity
            #420,
            0.65e-6,                                   # a-slit width
            14e-6,                                  # b-slit separation
            0.91   ,                                 # z-dist from YDS to image
            6.710308278912389e-9,                   # lam- wavelength
            0,                                  # dlam- wavelength spread
            px,                                 # delta- detector resolution
            3.1e-4
            ]                                 # dx- horizontal drift (+: left, -: right)
    
    cons3 = [ [0.1,1.0],            # u-degree of coherence
                    [1,150],    # I-central intensity
                    #[300,1000],    # I-central intensity
                    [0.65e-6,0.85e-6],      # a-slit width
                    [13.5e-6,16.5e-6],    # b-slit separation
                    [0.897,0.915],        # z-dist from YDS to image
                    [6.710308278912389e-9, 6.710308278912389e-9],    # lam- wavelength
                    [0,0],                   # dlam- wavelength spread
                    [px, px],                # delta- detector resolution
                    [2.e-4,4.e-4]       # dx- horizontal drift (+: left, -: right)
                    ]    
    
    # Settings for YDS # 2
    p2 = [0.4,                                        # u-degree of coherence
            50,                                 # I-central intensity
            #420,
            1.2e-6,                                   # a-slit width
            18e-6,                                  # b-slit separation
            0.91   ,                                 # z-dist from YDS to image
            6.710308278912389e-9,                   # lam- wavelength
            0,                                  # dlam- wavelength spread
            px,                                 # delta- detector resolution
            3.1e-4
            ]                                 # dx- horizontal drift (+: left, -: right)
    
    cons2 = [ [0.1,1.0],            # u-degree of coherence
                    [1,1000],    # I-central intensity
                    #[300,1000],    # I-central intensity
                    [1.15e-6,1.25e-6],      # a-slit width
                    [17.95e-6,18.05e-6],    # b-slit separation
                    [0.897,0.915],        # z-dist from YDS to image
                    [6.710308278912389e-9, 6.710308278912389e-9],    # lam- wavelength
                    [0,0],                   # dlam- wavelength spread
                    [px, px],                # delta- detector resolution
                    [2.5e-4,4.e-4]       # dx- horizontal drift (+: left, -: right)
                    ]
    
#    weights = np.ones_like(Ip1[0])
#    c = np.size(weights)//2
#    weights[c-400:c+400]=0.00000000001
    weights=None
   
    print(" ")
    print("YDS #1")
    v1, c1, ec1 = fitYDSInterference(Ip1,
                                detRange=len(Ip1[0]) * px, 
                                iG = p0,
                                constraints = constraints,
                                weights = weights,
                                savePath = './yds1/')
    
    print(" ")
    print("YDS #2")
    v2, c2, ec2 = fitYDSInterference(Ip2,
                                detRange=len(Ip2[0]) * px, 
                                iG = p2,
                                constraints = cons2,
                                weights = weights,
                                savePath = './yds2/')
    print(" ")
    print("YDS #3")
    v3, c3, ec3 = fitYDSInterference(Ip3,
                                detRange=len(Ip3[0]) * px, 
                                iG = p3,
                                constraints = cons3,
                                weights = weights,
                                savePath = './yds3/')# path + 'plots/' ) # need to manually create the 'plots' folder or else put None
#    
    print(" ")
    print("YDS #4")
    v4, c4, ec4 = fitYDSInterference(Ip4,
                                detRange=len(Ip4[0]) * px, 
                                iG = p4,
                                constraints = cons4,
                                weights = weights,
                                savePath = './yds4/')# path + 'plots/' ) # need to manually create the 'plots' folder or else put None
#    
    print(" ")
    print("YDS #5")
    v5, c5, ec5 = fitYDSInterference(Ip5,
                                detRange=len(Ip0[0]) * px, 
                                iG = p5,
                                constraints = cons5,
                                weights = weights,
                                savePath = './yds5/')# path + 'plots/' ) # need to manually create the 'plots' folder or else put None
    
#    print("Shape of Coherence Values: {}".format(np.shape(c1)))
#    print("Visibility Values: {}".format(v1))
#    print("Coherence Values: {}".format(c1[0]))
#    print("Coherence Values: {}".format(c1[1]))
    
    fig, axs = plt.subplots(2,1)
#    axs[0].errorbar(horSlits, v1, label='24')
    axs[0].plot(horSlits, v1, label='24')
    axs[0].plot(horSlits, v2, label='18')
    axs[0].plot(horSlits, v3, label='14') #yds #3
#    axs[0].plot(horSlits, v8, label='12')
#    axs[0].plot(horSlits, v7, label='8')
    axs[0].plot(horSlits, v4, label='10')
    axs[0].plot(horSlits, v5, label='6')
#    axs[0].plot(horSlits, v6, label='4')
    axs[0].legend(title="YDS Sep [um]")
    axs[0].set_ylabel("Visibility")
    axs[0].invert_xaxis()
    axs[1].errorbar(horSlits, c1, yerr=ec1, label='24')
    axs[1].errorbar(horSlits, c2, yerr=ec2, label='18')
    axs[1].errorbar(horSlits, c3, yerr=ec3, label='14') #yds #3
#    axs[1].errorbar(horSlits, c8, yerr=ec8, label='12')
    axs[1].errorbar(horSlits, c4, yerr=ec4, label='10')
#    axs[1].errorbar(horSlits, c7, yerr=ec7, label='8')
    axs[1].errorbar(horSlits, c5, yerr=ec5, label='6')
#    axs[1].errorbar(horSlits, c6, yerr=ec6, label='4')
    axs[1].legend(title="YDS Sep [um]")
    axs[1].set_ylabel("Coherence")
    axs[1].set_xlabel("Exit slit separation")
    axs[1].invert_xaxis()
    plt.show()
    
    plt.plot(horSlits, ec1, label='24')
    plt.plot(horSlits, ec2, label='18')
    plt.plot(horSlits, ec3, label='14')
#    plt.plot(horSlits[2:len(horSlits)-1], ec4[2:len(ec4)-1], label='10')
    plt.plot(horSlits, ec4, label='10')
    plt.plot(horSlits, ec5, label='6')
    plt.legend(title="YDS Sep [um]")
    plt.yscale("log")
    plt.ylabel("/mu Error")
    plt.xlabel("Exit Slit Separation [um]")
    plt.show()
    
    allP = [p0,p2,p3,p4,p5]#,p6,p7,p8]
    allC = [c1,c2,c3,c4,c5]#,c6,c7,c8]
    
    _ydsSep = [p[3]*1e6 for p in allP]
    _mu1 = [c[0] for c in allC]
    _mu2 = [c[1] for c in allC]
    _mu3 = [c[2] for c in allC]
    _mu4 = [c[3] for c in allC]
    _mu5 = [c[4] for c in allC]
    _mu6 = [c[5] for c in allC]
    _mu7 = [c[6] for c in allC]
    _mu8 = [c[7] for c in allC]
    _mu9 = [c[8] for c in allC]
    _mu10 = [c[9] for c in allC]
    _mu11 = [c[10] for c in allC]
#    mu12 = [c[11] for c in [c1,c2,c3,c4,c5]]
#    mu13 = [c[12] for c in [c1,c2,c3,c4,c5]]
    mu1 = [x for _,x in sorted(zip(_ydsSep,_mu1))]
    mu2 = [x for _,x in sorted(zip(_ydsSep,_mu2))]
    mu3 = [x for _,x in sorted(zip(_ydsSep,_mu3))]
    mu4 = [x for _,x in sorted(zip(_ydsSep,_mu4))]
    mu5 = [x for _,x in sorted(zip(_ydsSep,_mu5))]
    mu6 = [x for _,x in sorted(zip(_ydsSep,_mu6))]
    mu7 = [x for _,x in sorted(zip(_ydsSep,_mu7))]
    mu8 = [x for _,x in sorted(zip(_ydsSep,_mu8))]
    mu9 = [x for _,x in sorted(zip(_ydsSep,_mu9))]
    mu10 = [x for _,x in sorted(zip(_ydsSep,_mu10))]
    mu11 = [x for _,x in sorted(zip(_ydsSep,_mu11))]
    
    ydsSep = sorted(_ydsSep)
    
    print("YDS Sep: {}".format(_ydsSep))
    print("mu: {}".format(mu1))
#    pf, cf = [p[4], c[2] for p, c in zip([p0,p2,p3,p4,p5],[c1,c2,c3,c4,c5])]
    plt.plot(ydsSep,mu1,':o', label="1100")       
    plt.plot(ydsSep,mu2,':o', label="1000")         
    plt.plot(ydsSep,mu3,':o', label="900")       
    plt.plot(ydsSep,mu4,':o', label="800")         
    plt.plot(ydsSep,mu5,':o', label="700")         
    plt.plot(ydsSep,mu6,':o', label="600")    
    plt.plot(ydsSep,mu7,':o', label="500")       
    plt.plot(ydsSep,mu8,':o', label="400")         
    plt.plot(ydsSep,mu9,':o', label="350")       
    plt.plot(ydsSep,mu10,':o', label="300")         
    plt.plot(ydsSep,mu11,':o', label="250")         
#    plt.plot(ydsSep,mu12,':o', label="200")         
#    plt.plot(ydsSep,mu13,':o', label="150")      
    plt.legend(title="Exit Slit Separation")
    plt.xlabel("YDS Separation [um]")
    plt.ylabel("/mu")
    plt.show()
    #1100 , 1000, 900,  800,  700,  600,  500,  400,  350,  300,  250,  200,  150]#,  100,  50] # test
#    plt.plot(Ip1[0])#[int(len((Ip1[4])/2)-30):int(len((Ip1[4])/2)+30)]/np.max(Ip1[4]), label='#1')
#    plt.plot(Ip2[4][int(len((Ip2[4])/2)-30):int(len((Ip2[4])/2)+30)]/np.max(Ip2[4]), label='#2')
#    plt.plot(Ip3[4][int(len((Ip3[4])/2)-30):int(len((Ip3[4])/2)+30)]/np.max(Ip3[4]), label='#3')
#    plt.plot(Ip4[4][int(len((Ip4[4])/2)-30):int(len((Ip4[4])/2)+30)]/np.max(Ip4[4]), label='#4')
#    plt.plot(Ip5[4][int(len((Ip5[4])/2)-30):int(len((Ip5[4])/2)+30)]/np.max(Ip5[4]), label='#5')
#    plt.plot(Ip1[2]/np.max(Ip1[4]), label='#1')
#    plt.plot(Ip2[2]/np.max(Ip2[4]), label='#2')
#    plt.plot(Ip3[2]/np.max(Ip3[4]), label='#3')
#    plt.plot(Ip4[2]/np.max(Ip4[4]), label='#4')
#    plt.plot(Ip5[2]/np.max(Ip5[4]), label='#5')
    plt.legend(title="YDS")
    plt.show()




def testI():
    Xi = 0.008
    Xrange = Xi*30
    ri = (0.004/1000)*(1/2)*(1/100)
    ri = 0.02e-6
    rtest = (0.004/1000*2*100)#*(1/0.05)
    # (0.004*2*0.1*10/1000*2*100*0.05) #1000*2*100*0.05
    print(ri)
    print(rtest)
    print(ri-rtest)
    res = ri
    
    X = np.linspace(-(Xrange/2),(Xrange/2),2000)
    
    Y = ydsInterference(x=X, 
                        u=1, 
                        I = 1e15, 
                        a = 0.1e-6, 
                        b = 50e-6, 
                        z = 6, 
                        lam = 6.710308278912389e-9, 
                        dlam = 0.01e-9, 
                        delta = res)
    
    plt.plot(X,Y)

def propMeshDims(initial,propParams): #R,S):
    # initial = [0.008,1000,0.008,1000]
    
    # Rx = propParams[5]
    # Ry = propParams[7]
    # Sx = propParams[6]
    # Sy = propParams[8]
    
    # fRx = initial[0]*Rx
    # fRy = initial[2]*Ry
    # fDx = (initial[0]/initial[1])*(1/Sx)
    # fDy = (initial[2]/initial[3])*(1/Sy)
    
    pp = [P[2] for P in propParams]
    Rx = [r[5] for r in pp]
    Ry = [r[7] for r in pp]
    Sx = [s[6] for s in pp]
    Sy = [s[8] for s in pp]
    
    beamlineElements = [P[0] for P in propParams]
    
    # print(Rx)
    # print(Ry)
    # print(Sx)
    # print(Sy)
     
    _rX = []
    _rY = []       
    _dX = []
    _dY = []
    fRx = []
    fRy = []
    fDx = []
    fDy = []
    
    
    for i in range(0,len(Rx)+1):
        if i == 0:
            print("")
            print("------ Propagating step #1 ------")
            rX = initial[0]*Rx[i]
            rY = initial[2]*Ry[i]
            dX = (initial[0]/initial[1])*(1/Sx[i])
            dY = (initial[2]/initial[3])*(1/Sy[i])
            nX = int(rX/dX)
            nY = int(rY/dY)
    
            # print(rX)
            # print(rY)
            # print(dX)
            # print(dY)
            print("Beamline Element Name:                  {}".format(beamlineElements[i]))
            print("Dimensions of propagated array (x,y):   {}".format((nX,nY)))
            print("Horizontal Range:                       {} m".format(rX))
            print("Vertical Range:                         {} m".format(rY))
            print("Horizontal Resolution:                  {} m".format(dX))
            print("Vertical Resolution:                    {} m".format(dY))
            _rX.append(rX)
            _rY.append(rY)
            _dX.append(dX)
            _dY.append(dY)
            # plt.plot(i, rX, 'o', color='blue', label="horizontal range")
            # plt.plot(i, rY, 'o', color='green',label="vertical range")
            # plt.plot(i, dX, 'o', color='red',label="horizontal resolution")
            # plt.plot(i, dY, 'o', color='orange',label="vertical resolution")
        elif i == len(Rx):
            print(" ")
            print("------ Finished Propagating ------")
            fRx = rX #.append(rX)
            fRy = rY #.append(rY)
            fDx = dX #.append(dX)
            fDy = dY #.append(dY)
            # print('hereeeeeeeeee')
            
        elif i > 0:
            print("")
            print("------ Propagating step #{} ------".format(i+1))
            rX = np.squeeze(rX)*Rx[i]
            rY = np.squeeze(rY)*Ry[i]
            dX = np.squeeze(dX)*(1/Sx[i])
            dY = np.squeeze(dY)*(1/Sy[i])
            nX = int(rX/dX)
            nY = int(rY/dY)
            
            print("Beamline Element Name:                  {}".format(beamlineElements[i]))
            print("Dimensions of propagated array (x,y):   {}".format((nX,nY)))
            print("Horizontal Range:                       {} m".format(rX))
            print("Vertical Range:                         {} m".format(rY))
            print("Horizontal Resolution:                  {} m".format(dX))
            print("Vertical Resolution:                    {} m".format(dY))  
 
            # print(rX)
            # print(rY)
            # print(dX)
            # print(dY)
        _rX.append(rX)
        _rY.append(rY)
        _dX.append(dX)
        _dY.append(dY)
    
    
    beamlineElements.insert(0,'initial')
    # print(beamlineElements)
    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    # ax1.plot(x, y1, 'g-')
    # ax2.plot(x, y2, 'b-')
    
    # ax1.set_xlabel('X data')
    # ax1.set_ylabel('Y1 data', color='g')
    # ax2.set_ylabel('Y2 data', color='b')
    
    # plt.show()
    
    a1 = ax1.plot(_rX[1:(len(_rX))], ':*', label="horizontal range")
    a2 = ax1.plot(_rY[1:(len(_rY))], ':*', label="vertical range") # color='blue'
    a3 = ax2.plot(_dX[1:(len(_dX))], '-o', label="horizontal resolution") # , color='red'
    a4 = ax2.plot(_dY[1:(len(_dY))], '-o', label="vertical resolution")
    lns = a1+a2+a3+a4
    labs = [l.get_label() for l in lns]
    plt.legend(lns, labs, loc=0)
    ax1.set_yscale("log")
    ax2.set_yscale("log")
    ax1.set_xlim(0,len(Rx))
    for ax in fig.axes:
        plt.yscale("log")
        plt.xlim(0,len(Rx))
        plt.xticks(range(0,len(Rx)+1), beamlineElements)#, rotation=45, ha='right')
        ax.set_xticklabels(beamlineElements, rotation=45, ha='right')
    plt.xlabel("Beamline Position")
    ax1.set_ylabel("Range [m]")
    ax2.set_ylabel("Resolution [m]")
    plt.show()
    # print(fRx)
    # print(fRy)
    # print(fDx)
    # print(fDy)
    
    Nx = int(fRx/fDx)
    Ny = int(fRy/fDy)
    
    print("Dimensions of propagated array (x,y):   {}".format((Nx,Ny)))
    print("Final Horizontal Range:                 {} m".format(fRx))
    print("Final Vertical Range:                   {} m".format(fRy))
    print("Final Horizontal Resolution:            {} m".format(fDx))
    print("Final Vertical Resolution:              {} m".format(fDy))
    
    return fRx, fRy, fDx, fDy
    

def testDims():
    
    i = [0.008,1000,0.008,1000]
    # # S = Range
    # # R = Sampling
    #                        #Rx,  Sx,  Ry,  Sy                                
    # pp = [0, 0, 1.0, 0, 0, 2.0, 1.0, 4.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    # propMeshDims(i,pp)
    # [2][]
    # pp = [['op_zero_drift_pp', 'f',                [0, 0, 1.0, 0, 0, 0.25, 4.0, 0.25, 4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'zero_drift'], 
    # ['op_Mask_Aperture_pp', 'f',             [0, 0, 1.0, 0, 0, 0.125, 50.0, 0.125, 50.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Mask_Aperture'],
    # ['op_Obstacle_pp', 'f',                  [0, 0, 1.0, 0, 0, 0.5, 2.0, 0.5, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Obstacle'], # current res at obstacle = 375x375 nm
    # ['op_maskObstacle_pp', 'f',              [0, 0, 1.0, 0, 0, 1.0, 1.0, 4.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'maskObstacle'],
    # ['op_maskSubstrate_pp', 'f',             [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 8.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Substrate'],    
    # ['op_Mask_pp', 'f',                      [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Mask'],
    # ['op_Farfield_Propagation_pp', 'f',      [0, 0, 1.0, 1, 0, 1.0, 1.0, 50.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Farfield_Propagation'],
    # ['op_fin_pp', 'f',                       [0, 0, 1.0, 0, 0, 30.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'final post-propagation (resize) parameters']]


    pp =     [['op_zero_drift_pp', 'f',                [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'zero_drift'],
    ['op_Aperture_pp', 'f',                  [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Aperture'],
    ['op_Aperture_Before_M1_pp', 'f',        [0, 0, 1.0, 1, 0, 2.0, 2.0, 2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Aperture_Before_M1'],
    ['op_Obstacle_pp', 'f',                  [0, 0, 1.0, 0, 0, 0.1, 100.0, 0.1, 100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Obstacle'],
    ['op_Aperture2_pp', 'f',                 [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Aperture2'],
    ['op_Phase_After_YDS_Far_Field_pp', 'f', [0, 0, 1.0, 1, 0, 250.0, 0.1, 250.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Phase_After_YDS_Far_Field'],
    ['op_fin_pp', 'f',                       [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'final post-propagation (resize) parameters']]


    #['op_WBS_pp', 'f',                                      [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'WBS'],
    PP = [['op_WBS_pp', 'f',                                       [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'WBS'],
    #['op_After_WBS_Before_Toroidal_Mirror_pp', 'f',         [0, 0, 1.0, 1, 0, 3.0, 1.0, 3.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'After_WBS_Before_Toroidal_Mirror'],
    ['op_After_WBS_Before_Toroidal_Mirror_pp', 'f',          [0, 0, 1.0, 1, 0, 3.0, 1.0, 3.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'After_WBS_Before_Toroidal_Mirror'],  
    #['op_Toroidal_Mirror_pp', 'f',                          [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Toroidal_Mirror'],
    ['op_Toroidal_Mirror_pp', 'f',                           [0, 0, 1.0, 0, 0, 2.0, 1.0, 2.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Toroidal_Mirror'],
    #['op_After_Toroidal_Mirror_Before_PGM_pp', 'f',         [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'After_Toroidal_Mirror_Before_PGM'],
    ['op_After_Toroidal_Mirror_Before_PGM_pp', 'f',          [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'After_Toroidal_Mirror_Before_PGM'],
    #['op_Planar_Mirror_pp', 'f',                                 [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Planar_Mirror'],
    ['op_Planar_Mirror_pp', 'f',                             [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Planar_Mirror'],
    #['op_Planar_Mirror_Grating_pp', 'f',                         [0, 0, 1.0, 1, 0, 2.0, 1.0, 2.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Planar_Mirror_Grating'],
    ['op_Planar_Mirror_Grating_pp', 'f',                     [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Planar_Mirror_Grating'],
    #['op_Grating_pp', 'f',                                  [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Grating'],
    ['op_Grating_pp', 'f',                                   [0, 0, 1.0, 0, 0, 2.0, 1.0, 2.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Grating'],
    #['op_Grating_Before_Exit_Aperture_pp', 'f',             [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Grating_Before_Exit_Aperture'],
    ['op_Grating_Before_Exit_Aperture_pp', 'f',              [0, 1, 1.0, 1, 0, 3.0, 1.0, 3.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Grating_Before_Exit_Aperture'],
    #['op_Exit_Aperture_pp', 'f',                            [0, 0, 1.0, 0, 0, 0.2, 5.0, 0.2, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Exit_Aperture'],
    ['op_Exit_Aperture_pp', 'f',                             [0, 0, 1.0, 0, 0, 0.03, 40.0, 0.03, 40.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Exit_Aperture'],
    #['op_After_Mask_Aperture_Before_Cylindrical_Mirror_pp', 'f',      [0, 0, 1.0, 1, 0, 2.5,  0.5, 2.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'After_Mask_Aperture_Before_Cylindrical_Mirror'],
    ['op_After_Mask_Aperture_Before_Cylindrical_Mirror_pp', 'f',       [0, 0, 1.0, 1, 0, 4.0,  0.5, 4.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'After_Mask_Aperture_Before_Cylindrical_Mirror'],
    #['op_Cylindrical_Mirror_pp', 'f',                            [0, 0, 1.0, 0, 0, 1.0,  1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Cylindrical_Mirror'],
    ['op_Cylindrical_Mirror_pp', 'f',                            [0, 0, 1.0, 0, 0, 1.0,  1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Cylindrical_Mirror'], 
    #['op_After_Cylindrical_Mirror_Before_Exit_Slit_pp', 'f',    [0, 0, 1.0, 1, 0, 1.2,  1.0, 1.2, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'After_Cylindrical_Mirror_Before_Exit_Slit'],
    ['op_After_Cylindrical_Mirror_Before_Exit_Slit_pp', 'f',     [0, 0, 1.0, 1, 0, 1.0, 1.0, 4.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'After_Cylindrical_Mirror_Before_Exit_Slit'],
    ##['op_Exit_Slits_pp', 'f',                                    [0, 0, 1.0, 0, 0, 0.05, 20.0, 0.05, 20.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Exit_Slits'],
    ##OLD#['op_Exit_Slits_pp', 'f',                                [0, 0, 1.0, 0, 0, 0.05, 20.0, 0.05, 20.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Exit_Slits'],
    #['op_Exit_Slits_pp', 'f',                               [0, 0, 1.0, 0, 0, 0.15, 10.0, 0.15, 10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Exit_Slits'],
    ['op_Exit_Slits_pp', 'f',                                [0, 0, 1.0, 0, 0, 0.1,  100.0, 0.1, 100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Exit_Slits'],
    
    # REsample here.  Target: 2.0 nm.
    #['op_After_Exit_Slit_Before_BDA_pp', 'f',                    [0, 0, 1.0, 1, 0, 5.0,  0.2, 5.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'After_Exit_Slit_Before_BDA'],
    ['op_After_Exit_Slit_Before_BDA_pp', 'f',                [0, 0, 1.0, 1, 0, 22.0,  0.05*20, 3.5, 0.1*5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'After_Exit_Slit_Before_BDA'],
    #['op_BDA_pp', 'f',                                      [0, 0, 1.0, 1, 0, 0.05, 10.0, 0.008, 60.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'BDA'],
    #['op_BDA_pp', 'f',                                       [0, 0, 1.0, 0, 0, 0.1, 5.0, 0.08, 10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'BDA'],
    #['op_BDA_Mask_Aperture_pp', 'f',                             [0, 0, 1.0, 1, 0, 0.8,  6.049635, 0.6, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'BDA_Mask_Aperture'],
    ['op_BDA_Mask_Aperture_pp', 'f',                         [0, 0, 1.0, 1, 0, 1.0,  1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'BDA_Mask_Aperture'],
    #['op_Mask_Aperture_pp', 'f',                                 [0, 0, 1.0, 0, 0, 1.0,  1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Mask_Aperture'],
    #['op_Mask_Aperture_pp', 'f',                             [0, 0, 1.0, 0, 0, 0.4/2.0,  2*0.9608652366201311*2.0393909, 0.4/30.0, 30.428049302099573*2*0.8544558610135526, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Mask_Aperture'],

    #OLD['op_maskObstacle_pp', 'f',                                  [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Obstacle'],
    
    #OLD['op_maskSubstrate_pp', 'f',                                  [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Substrate'],    

    #['op_Mask_pp', 'f',                                          [0, 0, 1.0, 0, 0, 0.04, 100.0, 0.05, 100, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Mask'],
    ['op_Mask_pp', 'f',                                          [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Mask'],

    #['op_Drift_Mask_To_AerialImage_pp', 'f',                               [0, 0, 1.0, 1, 0, 0.2,  4, 0.6, 10, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Drift_Mask_To_AerialImage'],
    # ['op_Drift_Mask_To_AerialImage_pp', 'f',                           [0, 0, 1.0, 1, 0, 0.2,  1, 1.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Drift_Mask_To_AerialImage'],
    ['op_Drift_Mask_To_AerialImage_pp', 'f',                           [0, 0, 1.0, 1.0, 0, 1.0,  1, 1.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Drift_Mask_To_AerialImage'],

    #OLD['op_Mask_Mask_pp', 'f',                                 [0, 0, 1.0, 0, 0, 0.6,  1.0, 0.6, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'final post-propagation (resize) parameters'],


    ['op_fin_pp', 'f',                                           [0, 0, 1.0, 0, 0, 1.0,  1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'final post-propagation (resize) parameters']]





    rx, ry, dx, dy = propMeshDims(i,PP)

    # z0=1
    # wavelength = 6.710308278912389e-9

    # Nx = wavelength*z0/(rx*dx)
    # Z = 2*(rx*dx)/wavelength
    
    # print(Z)
    # print(rx*dx)
    # print(Nx)
    
    
if __name__ == '__main__':
     testYDSfitManual()
#    testI()
#    testYDSfitAuto()
    # testDims()