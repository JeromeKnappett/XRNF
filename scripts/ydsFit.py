# -*- coding: utf-8 -*-

"""

Created on Thu Jan 23 13:43:22 2020

@author: jerome knappett

"""

import os
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import imageio
import tifffile

# plt.style.use(['science', 'ieee','no-latex']) # 'ieee', high-vis, high-contrast
plt.rcParams["figure.figsize"] = (
    6,
    4,
)  # added by GVR to make plots bigger and easier to read

colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]


# SINC FUNCTION DEFINITION
def sinc(x):
    z = np.where(x == 0.0, 1.0, np.sin(x) / x)
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
        _t = tifffile.imread(t)
        T.append(_t)

    if mean == True:
        tF = np.mean(np.array(T), axis=0)
    else:
        tF = np.array(T).sum(axis=0)

    if savePath != None:
        if writeType == "float16":
            imageio.imwrite(savePath, np.float16(tF))
        if writeType == "float32":
            imageio.imwrite(savePath, np.float32(tF))
        if writeType == "float64":
            imageio.imwrite(savePath, np.float64(tF))
        if writeType == "float128":
            imageio.imwrite(savePath, np.float128(tF))
        elif writeType == "uint8":
            imageio.imwrite(savePath, np.uint8(tF))
        elif writeType == "uint16":
            imageio.imwrite(savePath, np.uint16(tF))
        elif writeType == "uint32":
            imageio.imwrite(savePath, np.uint32(tF))
        else:
            imageio.imwrite(savePath, tF)
        print("Summed tiff written to: {}".format(savePath))

    return tF


def getVisibility(Iprofile, n, showPlot=True):
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
        plt.plot(
            Iprofile[int(len(Iprofile) / 2 - n) - 20 : int(len(Iprofile) / 2 + n) - 20]
        )  # plotting central fringe
        # plt.ticklabel_format(axis='x', style='sci', scilimits=(-4,4))
        plt.title("Central Fringe")
        plt.show()

    Imax = max(
        Iprofile[int(len(Iprofile) / 2 - n) - 20 : int(len(Iprofile) / 2 + n) - 20]
    )  # fringe maxima
    Imin = min(
        Iprofile[int(len(Iprofile) / 2 - n) - 20 : int(len(Iprofile) / 2 + n) - 20]
    )  # fringe minima

    print("Imax:")
    print(Imax)
    print("Imin")
    print(Imin)

    V = (Imax - Imin) / (Imax + Imin)  # visibility

    print("Visibility:")
    print(V)

    return V, Imax, Imin


def ydsInterference(x, u, I, a, b, z, lam, dlam, delta, dx=0, showPlot=False):
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

    eF = (sinc(np.pi * a * (x + dx) / (lam * z))) ** 2  # envelope function
    iF = np.cos((2 * np.pi * b * (x + z) / (lam * z)))  # interference function

    Ix = I * (
        eF
        * (
            1
            + u
            * (sinc((np.pi * dlam * (x + z)) / (lam * z)))
            * (sinc((np.pi * delta * b) / (lam * z)))
            * iF
        )
    )

    if showPlot:
        plt.plot(x * 1e3, Ix / np.max(Ix), label="total")
        plt.plot(
            x * 1e3, eF / np.max(eF), label="envelope", color=colours[1]
        )  # eF*np.max(Ix)
        plt.plot(
            x * 1e3,
            (eF / np.max(Ix)) * (1 - (np.max(Ix) - np.max(eF))),
            color=colours[1],
            linestyle="--",
        )  # , label="envelope")
        # plt.plot(iF, label="interference")
        plt.ylabel("Intensity [a.u]", size=15)
        plt.xlabel("Position [mm]", size=15)
        plt.xlim(-0.1,0.1)
        plt.xticks(size=15)
        plt.yticks(size=15)
        
        plt.legend()
        plt.show()

        plt.plot(eF, label="envelope")
        plt.plot(iF, label="interference")
        plt.legend()
        plt.show()

    return Ix


def prepYDSTiffs(Itiffs, Dtiffs, slits, sumDarks=True, sumLights=True, path=None):
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
    # sumDarks = True         # enable/disable dark field summing
    # sumLights = True        # enable/disable intensity summing

    # path = '/home/jerome/dev/data/YDS/'
    if path != None:
        darkPath = path + "summedDarkField.tif"
        # lightPath = path + 'summedIntensity.tif'

    if sumDarks == True:
        print(" ")
        print("----- Summing dark field tiff files -----")
        #    dark_fields = [path + '/darkFields/M17186_13' + str(i) + '.tif' for i in range(602,702)]
        if path != None:
            darkF = sumTiffs(
                Dtiffs, mean=True, savePath=darkPath
            )  # ,writeType='float16')
        elif path == None:
            darkF = sumTiffs(Dtiffs, mean=True)

    elif sumDarks == False:
        print(" ")
        print("----- Darkfield summing disabled -----")
        darkF = tifffile.imread(Dtiffs)  # plt.imread(Dtiffs)

    # DEFINING TIFF FILES FOR EACH EXIT SLIT SETTING
    if sumLights != False:
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
        # for r in range(0,np.shape(tiff_files)[0]):
        for i, s in enumerate(horSlits):
            #            print(s)
            #            print(np.shape(tiff_files[i]))
            #            print(tiff_files[i])
            print(" ")
            print(
                "Summing "
                + str(np.squeeze(np.shape(tiff_files[i])))
                + " tiff files for exit slit setting #"
                + str(i + 1)
            )
            if path != None:
                I = sumTiffs(
                    tiff_files[i], mean=True, savePath=path + str(s) + ".tif"
                )  # ,writeType='float16')
            else:
                I = sumTiffs(
                    tiff_files[i], mean=True, savePath=None
                )  # ,writeType='float16')
            #            except IndexError:
            #                print(np.shape(tiff_files[i][0]))
            #                print(tiff_files[i][0])
            #                print("Summing " + str(np.squeeze(np.shape(tiff_files[i][0]))) + " tiff files for exit slit setting #"+ str(i+1))

            #                I = sumTiffs(tiff_files[i][0],savePath=None)

            print("Shape of summed intensity file: {}".format(np.shape(I)))

            nX, nY = np.shape(I)
            Inew = I - darkF
            Inew[Inew<0] = 0
            Isums.append(Inew)

            fig, axs = plt.subplots(3, 1)
            MAX = None #np.max(I)
            MIN = None #np.min(I)
            im = axs[0].imshow(np.log(darkF), cmap="gray", vmax=MAX, vmin=MIN)
            axs[0].set_title("Dark Field (log)")  # 602-701
            axs[1].imshow(np.log(I), cmap="gray")
            axs[1].set_title("Summed intensity (log) #" + str(i + 1))
            axs[2].imshow(np.log(Inew), cmap="gray", vmax=MAX, vmin=MIN)
            axs[2].set_title("Intensity - Dark Field (log)")
            fig.subplots_adjust(right=0.8)
            cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
            fig.colorbar(im, cax=cbar_ax)
            #            if path!=None:
            ##                plt.savefig(path + 'plots/' + str(i) + 'Intensity_s' + str(s) + '.png')
            ##                imageio.imwrite(path + str(s) + '.tif', np.float32(Inew))
            #                print('Summed intensity written to: {}'.format(path + str(s) + '.tif'))
            plt.tight_layout()
            plt.show()
    else:
        Isums = []
        for i in range(0, numT):
            I = tifffile.imread(
                Itiffs[i]
            )  # tiff_files[0] #[path + str(s) + '.tif' for s in horSlits]

            fig, axs = plt.subplots(2, 1)
            MAX = np.max(I)
            MIN = np.min(I)
            im = axs[0].imshow(darkF, cmap="gray", vmax=MAX, vmin=MIN)
            axs[0].set_title("Dark Field")  # 602-701
            axs[1].imshow(I, cmap="gray")
            axs[1].set_title("Summed intensity #" + str(i + 1))
            # axs[2].imshow(I-darkF, vmax=MAX, vmin=MIN)
            # axs[2].set_title("Intensity - Dark Field")
            fig.subplots_adjust(right=0.8)
            cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
            fig.colorbar(im, cax=cbar_ax)
            #            if path!=None:
            #                plt.savefig(path + 'plots/' + str(i) + 'Intensity_s' + str(s) + '.png')
            plt.show()

            Isums.append(I)

    # TAKING LINE PROFILES OF EACH SUMMED INTENSITY TIFF
    Imid = 205
    N = 3  # Number of pixels from the center to average for line profile
    Dx = 0.007  # Horizontal detector size
    # xRange=np.linspace(-Dx/2,Dx/2,nY)

    Iprofiles = []
    # print(Isums)
    print("Shape of Isums: {}".format(np.shape(Isums[0])))

    for n, i in enumerate(Isums):
        #    print(i)
        nX, nY = np.shape(i)

        xRange = np.linspace(-Dx / 2, Dx / 2, nY)
        if N == 0:
            Icut = i[Imid, :]
            Iprofile = Icut
        else:
            Icut = i[Imid - N : Imid + N, :]
            Iprofile = Icut.mean(0)

        plt.clf()
        plt.close()
        plt.plot(xRange, Iprofile)
        plt.title("I Cut")
        plt.show()
        #        if path!=None:
        #            plt.savefig(path + 'plots/' + str(n) + 'IntensityCut_s' + str(s) + '.tif')

        Iprofiles.append(Iprofile)

    return Iprofiles


def fitYDSInterference(Iprofiles, detRange, iG, known, savePath=None):
    """

    Parameters
    ----------
    Iprofiles :
        Array of intensity profiles (generated from prepYDSTiffs()).
    detRange :
        Detector range [m], along axis of interference.
    iG :
        Array of initial guess values for fit.
    known :
        Boolean array specifying which values are known
        0=unknown
        1=known
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
    paramNames = [
        "Degree of Coherence",
        "Central Intensity",
        "Slit Width",
        "Slit Separation",
        "Distance from YDS to Detector",
        "Wavelength",
        "Wavelength Spread",
        "Detector Resolution",
        "Horizontal Drift",
    ]

    for pNum, Iprof in enumerate(Iprofiles):
        print("------ Fitting interference profile #{} ------".format(pNum + 1))
        n = 20  # number of data points sampled from centre
        V, Imax, Imin = getVisibility(Iprof, n, showPlot=True)
        vis.append(V)
        nY = len(Iprof)
        xRange = np.linspace(-detRange / 2, detRange / 2, nY)

        # SET BOUNDS FOR VARIABLES

        param_bounds = (
            # ---------------------- MINIMUM VALUES:
            [
                0.1,  # u-degree of coherence
                Imax / 4,  # I-central intensity
                0.5e-6,  # a-slit width
                5e-6,  # b-slit separation
                0.1,  # z- dist from YDS to image
                6.69e-9,  # lam - wavelength
                0,  # dlam- wavelength spread
                1e-9,  # delta - detector resolution
                -2e-4,
            ],  # z-horizontal drift
            # ---------------------- MAXIMUM VALUES:
            [
                1,  # u-degree of coherence
                Imax,  # I-central intensity
                15e-6,  # a-slit width
                100e-6,  # b-slit separation
                1.2,  # z-dist from YDS to image
                6.72e-9,  # lam- wavelength
                5e-9,  # dlam- wavelength spread
                5e-4,  # delta - detector resolution
                2e-4,
            ],
        )  # z-horizontal drift

        for i, k in enumerate(known):
            if k == 1:
                param_bounds[0][i] = iG[i] - iG[i] * 1e-6
                param_bounds[1][i] = iG[i] + iG[i] * 1e-6
                print("Value of {} is known... restricting fit".format(paramNames[i]))
            if iG[i] < param_bounds[0][i]:
                print(" ")
                print(
                    "Initial guess for {} less than lower bounds... adjusting bounds".format(
                        paramNames[i]
                    )
                )
                p_old = param_bounds[0][i]
                param_bounds[0][i] = iG[i] - iG[i] * 1e-6
                print(
                    "Guess Value: {},  Initial Lower Bound Value: {},  New Lower Bound: {}".format(
                        (iG[i]), (p_old), (param_bounds[0][i])
                    )
                )
            elif iG[i] > param_bounds[1][i]:
                print(" ")
                print(
                    "Initial guess for {} greater than upper bounds... adjusting bounds".format(
                        paramNames[i]
                    )
                )
                p_old = param_bounds[1][i]
                param_bounds[1][i] = iG[i] + iG[i] * 1e-6
                print(
                    "Guess Value: {},  Initial Upper Bound Value: {},  New Upper Bound: {}".format(
                        (iG[i]), (p_old), (param_bounds[1][i])
                    )
                )

        # print(param_bounds)

        # # INITIAL GUESS
        # p0 = [0.8,                                      # u-degree of coherence
        #       Imax/2,                                   # I-central intensity
        #       5e-6,                                     # a-slit width
        #       20e-6,                                    # b-slit separation
        #       0.3,                                      # z-dist from YDS to image
        #       6.710553853647976e-9,                                   # lam- wavelength
        #       1e-10,                                    # dlam- wavelength spread
        #       10e-9,                                     # delta- detector resolution
        #       0.1e-4]                                   # dx-horizontal drift

        p0 = iG

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

        guess = ydsInterference(
            xRange,  # x-range
            p0[0],  # u-degree of coherence
            p0[1],  # I-central intensity
            p0[2],  # a-slit width
            p0[3],  # b-slit separation
            p0[4],  # z-dist from YDS to image
            p0[5],  # lam- wavelength
            p0[6],  # dlam- wavelength spread
            p0[7],  # delta- detector resolution
            p0[8],
        )  # dx-horizontal drift

        dC.append(p0[0])
        I_0.append(p0[1])
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
        # range(len(Iprof)),
        param, param_cov = curve_fit(
            ydsInterference, Iprof, xRange, p0=p0, bounds=param_bounds
        )

        # ans stores the new y-data according to
        # the coefficient given by curve-fit() function

        y_fit = ydsInterference(
            xRange,
            param[0],
            param[1],
            param[2],
            param[3],
            param[4],
            param[5],
            param[6],
            param[7],
            param[8],
        )

        plt.clf()
        plt.close()
        plt.plot(Iprof, color="red", label="data")
        #        plt.plot(guess, color = 'green', label="Initial Guess")
        plt.ticklabel_format(axis="x", style="sci", scilimits=(-4, 4))
        plt.xlabel("x position")
        plt.ylabel("Intensity [a.u]")
        plt.legend()
        if savePath != None:
            plt.savefig(savePath + str(pNum) + "_intensityProfile.png")
        plt.show()

        # plt.plot(Iprof, '.', color ='red', label ="data")
        # plt.plot(y_fit, '--', color ='blue', label ="Model Fit")
        # plt.ticklabel_format(axis='x', style='sci', scilimits=(-4,4))
        # plt.legend()
        # plt.show()

        print(" ")
        print("----- Coeffients-----")
        print("Degree of Coherence (u):            {}".format(param[0]))
        print("Central Intensity (I0):             {}".format(param[1]))
        print("Slit Width [m] (a):                 {}".format(param[2]))
        print("Slit Separation [m] (b):            {}".format(param[3]))
        print("Distance from YDS to Image [m] (z): {}".format(param[4]))
        print("Wavelength [m] (lam):               {}".format(param[5]))
        print("Wavelength Spread [m] (dlam):       {}".format(param[6]))
        print("Detector Resolution [m] (delta):    {}".format(param[7]))
        print("Horizontal Drift [m] (dx):          {}".format(param[8]))

        # print(" ")
        # print("Covariance of coefficients:")
        # print(param_cov)

        dC.append(param[0])
        I_0.append(param[1])
        W.append(param[2])
        S.append(param[3])
        Z.append(param[4])
        wL.append(param[5])
        dwL.append(param[6])
        R.append(param[7])
        dX.append(param[8])

        iterations = (
            50  # number of iterations of the curve_fit() function in while loop below
        )
        i = 1

        plt.clf()
        plt.close()
        plt.plot(Iprof, ".", color="red", label="data")
        plt.plot(y_fit, ":", color="green", label="Model Fit - Initial")
        plt.ticklabel_format(axis="x", style="sci", scilimits=(-4, 4))

        while i < iterations:
            print("Refining fitting... attempt #{}".format(i))
            param1, param_cov1 = curve_fit(
                ydsInterference, Iprof, xRange, p0=param, bounds=param_bounds
            )

            y_fit1 = ydsInterference(
                xRange,
                param1[0],
                param1[1],
                param1[2],
                param1[3],
                param1[4],
                param1[5],
                param1[6],
                param1[7],
                param1[8],
            )

            plt.plot(y_fit1, "--", label="Model Fit - \#" + str(i))

            print(" ")
            print("----- Coeffients-----")
            print("Degree of Coherence (u):            {}".format(param1[0]))
            print("Central Intensity (I0):             {}".format(param1[1]))
            print("Slit Width [m] (a):                 {}".format(param1[2]))
            print("Slit Separation [m] (b):            {}".format(param1[3]))
            print("Distance from YDS to Image [m] (z): {}".format(param1[4]))
            print("Wavelength [m] (lam):               {}".format(param1[5]))
            print("Wavelength Spread [m] (dlam):       {}".format(param1[6]))
            print("Detector Resolution [m] (delta):    {}".format(param1[7]))
            print("Horizontal Drift [m] (dx):          {}".format(param1[8]))
            print(" ")

            #    print("Covariance of coefficients:")
            #    print(param_cov1)

            dC.append(param1[0])
            I_0.append(param1[1])
            W.append(param1[2])
            S.append(param1[3])
            Z.append(param1[4])
            wL.append(param1[5])
            dwL.append(param1[6])
            R.append(param1[7])
            dX.append(param1[8])

            if np.all(param) == np.all(param):
                print(" ")
                print(
                    "----- Fitting parameters have reached equilibrium after {} iterations -----".format(
                        i
                    )
                )
                coherence.append(param1[0])
                break
            else:
                param = param1
                i += 1
        else:
            coherence.append(param1[0])
            print(" ")
            print(
                "----- Completed {} iterations without stagnation -----".format(
                    iterations
                )
            )

        plt.legend()
        if savePath != None:
            plt.savefig(savePath + str(pNum) + "fittingPlot.png")
        plt.show()

        plt.clf()
        plt.close()
        plt.plot(Iprof, ".", color="red", label="data")
        plt.plot(y_fit1, "--", color="blue", label="Final Fit")
        plt.plot(guess, ":", color="green", label="Initial Guess")
        plt.ticklabel_format(axis="x", style="sci", scilimits=(-4, 4))
        plt.legend()
        if savePath != None:
            plt.savefig(savePath + str(pNum) + "finalPlot.png")
        plt.show()

        plt.clf()
        plt.close()
        fig, axs = plt.subplots(3, 3)

        axs[0, 0].plot(dC)
        axs[0, 0].set_title("Degree of Coherence")
        axs[0, 0].set_ylim(param_bounds[0][0], param_bounds[1][0])
        axs[0, 1].plot(I_0)
        axs[0, 1].set_title("Central Intensity")
        axs[0, 1].set_ylim(param_bounds[0][1], param_bounds[1][1])
        axs[0, 2].plot(W)
        axs[0, 2].set_title("Slit Width")
        axs[0, 2].set_ylim(param_bounds[0][2], param_bounds[1][2])
        axs[1, 0].plot(S)
        axs[1, 0].set_title("Slit Separation")
        axs[1, 0].set_ylim(param_bounds[0][3], param_bounds[1][3])
        axs[1, 1].plot(Z)
        axs[1, 1].set_title("Image Plane Distance")
        axs[1, 1].set_ylim(param_bounds[0][4], param_bounds[1][4])
        axs[1, 2].plot(wL)
        axs[1, 2].set_title("Wavelength")
        axs[1, 2].set_ylim(param_bounds[0][5], param_bounds[1][5])
        axs[2, 0].plot(dwL)
        axs[2, 0].set_title("Wavelength spread")
        axs[2, 0].set_ylim(param_bounds[0][6], param_bounds[1][6])
        axs[2, 1].plot(R)
        axs[2, 1].set_title("Resolution")
        axs[2, 1].set_ylim(param_bounds[0][7], param_bounds[1][7])
        axs[2, 2].plot(dX)
        axs[2, 2].set_title("Horizontal Drift")
        axs[2, 2].set_ylim(param_bounds[0][8], param_bounds[1][8])
        #        if savePath !=None:
        #            plt.savefig(savePath + str(pNum) + 'parametersPlot.png')
        plt.show()

    return vis, coherence


def testYDSfitManual():
    """Testing the fitting function for the manually aquired YDS interference intensity tiff files"""

    # NUMBER OF AQUISITIONS PER EXIT SLIT SEPARATION FOR EACH YDS
    # aqus = [[4,3]] # test
    aqus = [
        [4, 3, 3, 3, 3, 3, 3, 3, 4, 5, 6, 6, 7, 20, 22],  # YDS-1
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 5, 6, 6, 7, 20, 22],  # YDS-2
        [4, 4, 4, 4, 4, 5, 6, 5, 5, 6, 8, 6, 7, 20, 22],
    ]  # YDS-3
    # SLIT SEPARATIONS FOR EACH YDS
    # horSlits = [[1100,1000]] # test
    horSlits = [
        [
            1100,
            1000,
            900,
            800,
            700,
            600,
            500,
            400,
            350,
            300,
            250,
            200,
            150,
            100,
            50,
        ],  # YDS-1
        [
            1100,
            1000,
            900,
            800,
            700,
            600,
            500,
            400,
            350,
            300,
            250,
            200,
            150,
            100,
            50,
        ],  # YDS-2
        [1100, 1000, 900, 800, 700, 600, 500, 400, 350, 300, 250, 200, 150, 100, 50],
    ]  # YDS-3
    # STARTING FILE NUMBER FOR EACH EXIT SLIT SEPARATION FOR EACH YDS
    # fileStarts = [[13715,13719]] # test
    fileStarts = [
        [
            13715,
            13719,
            13722,
            13725,
            13728,
            13731,
            13734,
            13740,
            13744,
            13748,
            13753,
            13759,
            13767,
            13777,
            13798,
        ],  # YDS-1
        [
            13822,
            13827,
            13830,
            13833,
            13836,
            13839,
            13842,
            13845,
            13848,
            13852,
            13857,
            13863,
            13869,
            13876,
            13896,
        ],  # YDS-2
        [
            13919,
            13923,
            13927,
            13931,
            13935,
            13939,
            13944,
            13950,
            13955,
            13960,
            13966,
            13974,
            13980,
            13987,
            14007,
        ],
    ]  # YDS-3

    # Setting up an array of ranges to specify file names
    # ran = range(fileStarts[0],fileStarts[0] + aqus[0]) # test
    ran = [
        [
            range(fileStarts[n][i], fileStarts[n][i] + aqus[n][i])
            for i in range(0, len(aqus[n]))
        ]
        for n in range(0, len(aqus))
    ]

    #    print(ran[0])
    #    print(" ")
    #    print(ran[1])
    #    print(" ")
    #    print(ran[2])

    # DEFINING TIFF FILES FOR EACH EXIT SLIT SETTING
    path = "/home/jerome/dev/data/YDS/YDSdata/"
    tiff_f = []

    num = 0
    for n in range(0, len(aqus)):
        print("Setting up tiff file array for YDS #{}".format(n + 1))
        for a in ran[n]:
            #            print(ran[n])
            # t = [path + 'yds' + str(num+1) + '/' + str(s) + '/' + 'M17186_' + str(i) + '.tif' for i in a]
            #            t = [path + 'yds' + str(num+1) + '/' + 'M17186_' + str(i) + '.tif' for i in a]
            t = [path + "/M17186_" + str(i) + ".tif" for i in a]
            tiff_f.append(t)
        num += 1

    tiff_files = np.squeeze(tiff_f).reshape(np.shape(aqus)[0], np.shape(aqus)[1])

    # tiff_files = [path + 'yds' + str(num+1) + '/' + 'M17186_' + str(i) + '.tif' for i in ran]

    #                  ]
    # print(" ")
    # print(tiff_files[0])
    #    print(" ")
    #    print(tiff_files[1])
    #    print(" ")
    #    print(tiff_files[2])
    #    print(" ")
    print("Shape of tiff files array: {}".format(np.shape(tiff_files)))

    dark_fields = [
        path + "/darkFields/M17186_13" + str(i) + ".tif" for i in range(602, 702)
    ]

    dR = 0.007  # Horizontal detector size

    # YDS-1 Analysis
    Ip1 = prepYDSTiffs(
        Itiffs=tiff_files[0],
        Dtiffs=dark_fields,  # path + 'summedDarkField.tif'
        slits=horSlits,
        sumDarks=True,
        sumLights=True,
        path=path,
    )

    # # Testing
    # Ip1 = prepYDSTiffs(Itiffs = [[path + 'yds1/1100.tif', path + 'yds1/1000.tif']], #tiff_files[0]
    #                  Dtiffs = path + 'summedDarkField.tif', #dark_fields,
    #                  slits = horSlits,
    #                  sumDarks = False,
    #                  sumLights = False,
    #                  path = None) #path+'yds1/')
    #    v1, c1 = fitYDSInterference(Ip1,detRange=dR)

    V, Imax, Imin = getVisibility(Ip1[0], n, showPlot=True)
    # INITIAL GUESS
    p0 = [
        1,  # u-degree of coherence
        Imax / 4,  # I-central intensity
        4.e-6,  # a-slit width
        50e-6,  # b-slit separation
        0.8,  # z-dist from YDS to image
        6.710308278912389e-9,  # lam- wavelength
        1e-10,  # dlam- wavelength spread
        11e-6,  # delta- detector resolution
        0.5e-4,
    ]  # dx- horizontal drift (+: left, -: right)

    # IF PARAMETER IS KNOWN EXACTLY PUT 1
    exact = [
        0,  # u-degree of coherence
        0,  # I-central intensity
        0,  # a-slit width
        0,  # b-slit separation
        0,  # z-dist from YDS to image
        1,  # lam- wavelength
        1,  # dlam- wavelength spread
        1,  # delta- detector resolution
        0,
    ]  # dx- horizontal drift

    v1, c1 = fitYDSInterference(
        Ip1, detRange=dR, iG=p0, known=exact, savePath=path + "plots/yds1_"
    )  # None)# path + 'plots/' ) # need to manually create the 'plots' folder or else put None

    print("Visibility Values: {}".format(v1))
    print("Coherence Values: {}".format(c1))

    #    fig, axs = plt.subplots(2,1)
    #    axs[0].plot(horSlits[0], v1)
    #    axs[0].set_title("Visibility")
    #    axs[1].plot(horSlits[0], c1)
    #    axs[1].set_title("Coherence")
    #    #axs[1].set_xtitle("Exit slit separation")
    #    plt.show()

    # YDS-2 Analysis
    Ip2 = prepYDSTiffs(
        Itiffs=tiff_files[1],
        Dtiffs=path + "darkFields/summedDarkField.tif",
        slits=horSlits,
        sumDarks=False,
        sumLights=True,
        path=path,
    )

    v2, c2 = fitYDSInterference(
        Ip2, detRange=dR, iG=p0, known=exact, savePath=path + "plots/yds2_"
    )

    print("Visibility Values: {}".format(v2))
    print("Coherence Values: {}".format(c2))

    #    fig, axs = plt.subplots(2,1)
    #    axs[0].plot(horSlits[1], v2)
    #    axs[0].set_title("Visibility")
    #    axs[1].plot(horSlits[1], c2)
    #    axs[1].set_title("Coherence")
    #    #axs[1].set_xtitle("Exit slit separation")
    #    plt.show()

    # YDS-3 Analysis
    Ip3 = prepYDSTiffs(
        Itiffs=tiff_files[2],
        Dtiffs=path + "darkFields/summedDarkField.tif",
        slits=horSlits,
        sumDarks=False,
        sumLights=True,
        path=path,
    )

    v3, c3 = fitYDSInterference(
        Ip3, detRange=dR, iG=p0, known=exact, savePath=path + "plots/yds3_"
    )

    print("Visibility Values: {}".format(v3))
    print("Coherence Values: {}".format(c3))


#    fig, axs = plt.subplots(2,1)
#    axs[0].plot(horSlits[0], v3)
#    axs[0].set_title("Visibility")
#    axs[1].plot(horSlits[0], c3)
#    axs[1].set_title("Coherence")
#    #axs[1].set_xtitle("Exit slit separation")
#    plt.show()


def testYDSfitAuto():
    """Testing the fitting function for the automatically aquired YDS interference intensity tiff files"""
    # NUMBER OF AQUISITIONS PER EXIT SLIT SEPARATION FOR EACH YDS
    aqus = [4, 4, 4, 4, 4, 5, 6, 5, 5, 6, 8, 6, 7, 20, 22]  # test

    # SLIT SEPARATIONS FOR EACH YDS
    horSlits = [
        1100,
        1000,
        900,
        800,
        700,
        600,
        500,
        400,
        350,
        300,
        250,
        200,
        150,
        100,
        50,
    ]  # test

    # STARTING FILE NUMBER FOR 1ST YDS RUN
    fileStart = 14048
    numRuns = 1  # 5

    ran = []
    # Setting up an array of ranges to specify file names
    for n in range(0, numRuns):
        print(" ")
        print("Setting up range for YDS run #{} ".format(n + 1))
        print("Starting file number:      {}".format(fileStart))
        ranges = [
            range(fileStart + sum(aqus[0:i]), fileStart + sum(aqus[0 : i + 1]))
            for i in range(0, len(aqus))
        ]
        fileStart += sum(aqus)
        # print("New starting file number: {}".format(fileStart))
        ran.append(ranges)

    # print(ran)
    # print(ran[0])
    # print(" ")
    # print(ran[1])
    # print(" ")
    # print(ran[2])

    # DEFINING TIFF FILES FOR EACH EXIT SLIT SETTING
    path = "/home/jerome/dev/data/YDS/autoRun/"  # path to save data into/move tiff files into
    tiffPath = "/home/jerome/dev/data/YDS/"  # original path of tiff files
    tiff_f = []

    for n in range(0, numRuns):
        print(" ")
        print("Setting up tiff file array for YDS #{}".format(n + 1))
        os.makedirs(
            os.path.dirname(path + "yds" + str(n + 1) + "/"), exist_ok=True
        )  # making directories for each YDS
        for a in ran[n]:
            #            print(ran[n])
            t = [path + "yds" + str(n + 1) + "/M17186_" + str(i) + ".tif" for i in a]
            try:
                [
                    os.rename(
                        tiffPath + "M17186_" + str(i) + ".tif",
                        path + "yds" + str(n + 1) + "/M17186_" + str(i) + ".tif",
                    )
                    for i in a
                ]  # moving tiff files into desired folders
            except FileNotFoundError:
                pass
                # print("FILE OR DIRECTORY NOT FOUND: {} ".format(t))
            tiff_f.append(t)

    # print(tiff_f)

    # PATH TO DARKFIELD TIFFS
    dark_fields = [
        tiffPath + "darkFields/M17186_13" + str(i) + ".tif" for i in range(602, 702)
    ]

    dR = 0.007  # Horizontal detector size    - used for plotting

    # YDS-1 Analysis
    Ip1 = prepYDSTiffs(
        Itiffs=tiff_f,  # array of intensity tiff paths
        Dtiffs=dark_fields,  # array of darkfield tiff paths     #dark_fields, path + 'summedDarkField.tif'
        slits=horSlits,  # array of exit slit separations
        sumDarks=True,  # If true - darkfield tiff files in Dtiffs are summed, if false darkfield tiff file Dtiff is a single previously summed darkfield tiff
        sumLights=True,  # If true - tiff files in Itiffs are summed for each exit slit setting, if false - each exit slit setting uses only 1 tiff file (assumed previously summed)
        path=None,
    )  # Save path for data (summed tiff files)

    print("Shape of profiles array: {}".format(np.shape(Ip1)))

    print(" ")
    print("Finding central fringe visibility")

    # FINDING VISIBILITY OF FRINGES
    vis = []
    n = 20  # number of data points sampled from centre
    V, Imax, Imin = getVisibility(Ip1[0], n, showPlot=True)
    vis.append(V)

    # INITIAL GUESS
    p0 = [
        V,  # u-degree of coherence
        Imax / 4,  # I-central intensity
        5e-6,  # a-slit width
        75e-6,  # b-slit separation
        0.8,  # z-dist from YDS to image
        6.710308278912389e-9,  # lam- wavelength
        1e-10,  # dlam- wavelength spread
        100e-9,  # delta- detector resolution
        0.5e-4,
    ]  # dx- horizontal drift (+: left, -: right)

    # IF PARAMETER IS KNOWN EXACTLY PUT 1
    exact = [
        0,  # u-degree of coherence
        0,  # I-central intensity
        0,  # a-slit width
        0,  # b-slit separation
        0,  # z-dist from YDS to image
        1,  # lam- wavelength
        0,  # dlam- wavelength spread
        0,  # delta- detector resolution
        0,
    ]  # dx- horizontal drift

    v1, c1 = fitYDSInterference(
        Ip1, detRange=dR, iG=p0, known=exact, savePath=None
    )  # path + 'plots/' ) # need to manually create the 'plots' folder or else put None

    print("Visibility Values: {}".format(v1))
    print("Coherence Values: {}".format(c1))

    fig, axs = plt.subplots(2, 1)
    axs[0].plot(horSlits, v1)
    axs[0].set_title("Visibility")
    axs[0].set_xlabel("Exit slit separation")
    axs[1].plot(horSlits, c1)
    axs[1].set_title("Coherence")
    axs[1].set_xlabel("Exit slit separation")
    plt.show()


def testI():
    p = 10
    Xi = 0.008 * p  # 0.008
    Xrange = 0.08  # Xi #*25
    ri = (0.004 / 1000) * (1 / 2) * (1 / 100)
    rtest = 0.004 / 1000 * 2 * 100  # *(1/0.05)
    # (0.004*2*0.1*10/1000*2*100*0.05) #1000*2*100*0.05
    # print(ri)
    # print(rtest)
    # print(ri-rtest)
    res = 5e-6 / 2  # 1e-6*2
    nx = int(Xrange / res)
    print(nx)

    X = np.linspace(-(Xrange / 2), (Xrange / 2), nx)

    Y = ydsInterference(
        x=X,
        u=0.8,
        I=1.0,
        a=3.50e-6,
        b=35.0e-6,
        z=0.03,
        lam=13.5e-9,#6.710308278912389e-9,
        dlam=0.01e-9,
        delta=res,
        showPlot=True,
    )
        # u-degree of coherence
        # I-central intensity
        # a-slit width
        # b-slit separation
        # z-dist from YDS to image
        # lam- wavelength
        # dlam- wavelength spread
        # delta- detector resolution
        # dx- horizontal drift
    # plt.plot(X,Y)


def fringeSpace(lam, z, b):
    """
    Parameters
    ----------
    lam : Wavelength [m]
    z : Propagation distance [m]
    b : Slit separation [m]

    Returns
    -------
    delta :
        YDS intensity fringe spacing [m]

    """

    delta = (lam * z) / b

    return delta


def testFringeSpace():
    lam = 6.710308278912389e-9
    L = 1
    W = 100e-6

    d = fringeSpace(lam, L, W)

    print(d)


def ydsV(I1, I2, c):
    V = ((2 * (np.sqrt(I1) * np.sqrt(I2))) / (I1 + I2)) * c

    return V


def testYDSV():
    I1 = 1
    I2 = np.linspace(0.8, 1.2, 100)
    c = 1

    V = [ydsV(I1, a, c) for a in I2]

    plt.plot(I2 / I1, V)
    plt.ylabel("Visibility")
    plt.xlabel("$I_2/I_1$")
    plt.show()


if __name__ == "__main__":
#    testYDSfitManual()
    testI()
#   testYDSfitAuto()
#    testFringeSpace()
#    testYDSV()
