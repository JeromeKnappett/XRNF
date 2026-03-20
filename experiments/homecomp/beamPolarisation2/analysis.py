#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 17:16:04 2020


This is a basic example of how to handle the pickled results from a batch 
simulation (i.e. from doExperiment/runner)

@author: -
"""
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib.font_manager import FontProperties

#import xl.runner as runner

dirPath = '/data/experiments/beamPolarisation2/data/'
batchOutputFile = dirPath + 'CL/results.pickle'


def trials(results):
        return [k for k,v in results.items()]
       
def resultsKeys(results):
        return [k for k,v  in results['trial_0']['results'].items()]
    
def parameterKeys(results):
        return [k for k,v  in results['trial_0']['parameters'].items()]

    
def listValues(results, key):
        try:
            V =  [results[trial]['results'][key] for trial in trials(results)] 
        except KeyError:
            try:
                V =  [results[trial]['parameters'][key] for trial in trials(results)] 
            except KeyError:
                print('Valid values not found for ' + key)
                V=[]
        
        return V
    
def plot(results,*args,**kwargs):
                
        xKey = kwargs['x']
        yKey = kwargs['y']
            
        x = listValues(results,xKey)
        y = listValues(results,yKey)
               
        if x !=[] and y!=[]:
            fontP = FontProperties()
            fontP.set_size('xx-small')    
            plt.plot(x,y,'o')   #label=...
            plt.xlabel(xKey)
            plt.ylabel(yKey)
            plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5), prop=fontP)
            plt.show()   
    

        
results = pickle.load( open(batchOutputFile, 'rb')  )
resultsIN = pickle.load( open(dirPath + 'incident/results.pickle', 'rb')  )
resultsEX = pickle.load( open(dirPath + 'exit/results.pickle', 'rb')  )

incidentI = listValues(resultsIN, 'Intensity/Total/X/profile')[0]
exitI = listValues(resultsEX, 'Intensity/Total/X/profile')[0]

nxIN = listValues(resultsIN,'params/Mesh/nx')[0]
xMaxIN = listValues(resultsIN,'params/Mesh/xMax')[0]
xMinIN = listValues(resultsIN, 'params/Mesh/xMin')[0]
resolutionXIN  = np.divide(np.subtract(xMaxIN,xMinIN),nxIN)

nxEX = listValues(resultsEX,'params/Mesh/nx')[0]
xMaxEX = listValues(resultsEX,'params/Mesh/xMax')[0]
xMinEX = listValues(resultsEX, 'params/Mesh/xMin')[0]
resolutionXEX  = np.divide(np.subtract(xMaxIN,xMinIN),nxIN)

keyCPLXy = 'cpY_totP'
valuey = listValues(results, keyCPLXy)
keyCPLXx = 'cpX_totP'
valuex = listValues(results, keyCPLXx)

keyJ = 'mutualIn_j'
J = listValues(results, keyJ)
keyJxx = 'mutualIn_jxx'
Jxx = listValues(results, keyJxx)
keyJxy = 'mutualIn_jxy'
Jxy = listValues(results, keyJxy)
keyJyx = 'mutualIn_jyx'
Jyx = listValues(results, keyJyx)
keyJyy = 'mutualIn_jyy'
Jyy = listValues(results, keyJyy)

keyS0 = 'S0'
keyS1 = 'S1'
keyS2 = 'S2'
keyS3 = 'S3'
S0 = listValues(results, keyS0)
S1 = listValues(results, keyS1)
S2 = listValues(results, keyS2)
S3 = listValues(results, keyS3)
keySTK = 'stokesVector'
stokes = listValues(results, keySTK)
keyDP = 'degOfPolarisation'
P = listValues(results, keyDP)
keydPS = 'stkDavg'
D = listValues(results, keydPS)
print(D)

#print(valuey)
#print(valuex)

print("-----RESULTS KEYS-----")
print(resultsKeys(results))
print("-----TRIALS-----")
print(trials(results))
print("-----PARAMETER KEYS-----")
print(parameterKeys(results))
     

# plot(results,y='Intensity/Horizontal/Y/integratedOpticalDensity', x='op_Mask_Watchpoint_L')
# plot(results,y='Intensity/Vertical/Y/integratedOpticalDensity', x='op_Mask_Watchpoint_L')
# plot(results,y='Intensity/Total/Y/integratedOpticalDensity', x='op_Mask_Watchpoint_L')


# plot(results,y='Intensity/Horizontal/Y/contrastMichelson', x='op_Mask_Watchpoint_L')
# plot(results,y='Intensity/Vertical/Y/contrastMichelson', x='op_Mask_Watchpoint_L')
# plot(results,y='Intensity/Total/Y/contrastMichelson', x='op_Mask_Watchpoint_L')

# # histograms
# for h,b in  zip(listValues(results, 'Intensity/Total/Y/histogram'), listValues(results, 'Intensity/Total/Y/histogramBins')):
#     plt.plot(b,h)
# plt.show()

#number of pixels, range, resolution
ny = listValues(results,'params/Mesh/ny')
yMax = listValues(results,'params/Mesh/yMax')
yMin = listValues(results, 'params/Mesh/yMin')
resolutionY  = np.divide(np.subtract(yMax,yMin),ny)

y = listValues(results, 'y')
 

#number of pixels, range, resolution
nx = listValues(results,'params/Mesh/nx')
xMax = listValues(results,'params/Mesh/xMax')
xMin = listValues(results, 'params/Mesh/xMin')
resolutionX  = np.divide(np.subtract(xMax,xMin),nx)

x = listValues(results, 'x')


# plt.plot(ff[0],fa[0],'.')
# plt.show()

# #intensity profiles
# for v in listValues(results, 'Intensity/Total/Y/profile'):
#     plt.plot(v,y)
#     plt.title('Intensity (x=0)')
# plt.show()

# #intensity profiles
# for v in listValues(results, 'Intensity/Total/X/profile'):
#     plt.plot(v,x)
#     plt.title('Intensity (y=0)')
# plt.show()

#print(" ")
#print("Results Key")
#print(resultsKeys(results))

Yprofiles = listValues(results, 'Intensity/Total/Y/profile')
Xprofiles = listValues(results, 'Intensity/Total/X/profile')
YprofilesH = listValues(results, 'Intensity/Horizontal/Y/profile')
XprofilesH = listValues(results, 'Intensity/Horizontal/X/profile')
YprofilesV = listValues(results, 'Intensity/Vertical/Y/profile')
XprofilesV = listValues(results, 'Intensity/Vertical/X/profile')
#maskThickness = listValues(results, 'op_Mask_thick')
trials = trials(results)
#cXprofiles = listValues(results, 'cpX_totP')
#cYprofiles = listValues(results, 'cpY_totP')
#cXprofilesH = listValues(results, 'cpX_horP')
#cYprofilesH = listValues(results, 'cpY_horP')
#cXprofilesV = listValues(results, 'cpX_verP')
#cYprofilesV = listValues(results, 'cpY_verP')

#J = listValues(results, 'mutualIn_j')
#Jxx = listValues(results, 'mutualIn_jxx')
#Jxy = listValues(results, 'mutualIn_jxy')
#Jyx = listValues(results, 'mutualIn_jyx')
#Jyy = listValues(results, 'mutualIn_jyy')

#S0 = listValues(results, 'S0')
#S1 = listValues(results, 'S1')
#S2 = listValues(results, 'S2')
#S3 = listValues(results, 'S3')
#stokes = listValues(results, 'stokesVector')
#P = listValues(results, 'degOfPolarisation')


#keyX = 'cpX_totP'
#valuesX = listValues(results, keyX)
#keyY = 'cpY_totP'
#valuesY = listValues(resilts, keyY)


#cX = 'cpX_totP'
#cY = 'cpY_totP'
#cXvals = listValues(results, cX)
#cYvals = listValues(results, cY)


import utilMask
import wfCoherence

#Efield = listValues(results, 'params/wEFieldUnit')
#print(Efield[0])

#pathP = dirPath + 'Profiles.png'
#pathPY = dirPath + 'ProfilesY.png'
pathPh = dirPath + 'Profiles_hor.png'
#pathPYh = dirPath + 'ProfilesY_hor.png'
pathPv = dirPath + 'Profiles_ver.png'
#pathPYv = dirPath + 'ProfilesY_ver.png'
pathCL = dirPath + 'coherenceLength'
pathCP = dirPath + 'coherenceProfile'
pathclp = dirPath + 'cLengthPlot.png'
pathJP = dirPath + 'Jplot'
pathDP = dirPath + 'degPol'
pathS = dirPath + 'stokesPlot'
pathJH = dirPath + 'JH'
pathJV = dirPath + 'JV'
pathJ = dirPath + 'Jcoherence'
pathJclp = dirPath + 'jClength'
pathCLj = dirPath + 'anotherJclength'
pathdP = dirPath + 'degreeofPolarisation.png'

pathI = dirPath + 'IntensityTest'
pathM = dirPath + 'orderIntensity'
pathE = dirPath + 'efficiencyPlot.png'
pathE0 = dirPath + 'efficiencyPlotM0.png'
pathE1 = dirPath + 'efficiencyPlotM1.png'
pathP = dirPath + 'Profiles'


polarisation = ['Lin_Hor','Lin_Ver','Lin_Diag','Cir_Right','Cir_Left']

e0 = []
e1 = []
en1 = []
re0 = []
re1 = []
ren1 = []

CLx = []
CLy = []

jCLx = []
jCLy = []

""" Plotting Coherence Profiles - Total Polarisation """
plt.clf()
plt.close()
for p1, p2, P, Xpro, Ypro in zip(valuex, valuey, polarisation, Xprofiles, Yprofiles):
        plt.clf()
        plt.close()
        cH, cV, JH, JV, IH, IV = wfCoherence.profileMI(p1, p2, pathCP + P + '.png')
        plt.clf()
        plt.close()
        plt.plot(JH, label = 'Horizontal Coherence Profile')
        plt.plot(JV, label = 'Vertical Coherence Profile')
        plt.plot(Xpro, label = "Horizontal Intensity")
        plt.plot(Ypro, label = "Vertical Intensity")
        #plt.plot(1/cH, label = 'Horizontal Profile - Opposite Diagonal (normalised)')
        #plt.plot(1/cV, label = 'Vertical Profile - Opposite Diagonal (normalised)')
        plt.xlabel("Point Separation x-x' [pixels]")#[\u03bcm]")
        plt.ylabel("Degree of Coherence")
        plt.legend()
        if pathCP != None:
            print("Saving Mutual Intensity profiles to: {}".format(pathCP + P + '.png'))
            plt.savefig(pathCP)
        plt.show()
        plt.clf()
        
        clX, clY = wfCoherence.getCoherenceLength(cH, cV, 1, pathCL + P + '.png')
        _clX = clX*resolutionX.mean()
        _clY = clY*resolutionY.mean()
        print("Horizontal Coherence Length [m]: {}".format(_clX))
        print("Vertical Coherence Length [m]: {}".format(_clY))
        CLx.append(_clX)
        CLy.append(_clY)
        plt.clf()
        plt.close()
        plt.plot(abs(JH), label="J")
        plt.plot(abs(IH), label="I")
        plt.title("JH/IH")
        plt.legend()
        plt.savefig(pathJH + P + '.png')
        plt.plot(abs(JV), label="J")
        plt.plot(abs(IV), label="I")
        plt.title("JV/IV")
        plt.legend()
        plt.savefig(pathJV + P + '.png')


plt.clf()
plt.close()
plt.plot(polarisation, CLx, label="horizontal")
plt.plot(polarisation, CLy, label="vertical")
plt.legend()
print("Saving coherence length plot to {}".format(pathclp))
plt.savefig(pathclp)
plt.show()


""" Plotting coherence from J """
plt.clf()
plt.close()
for pol, j, xpro, ypro in zip(polarisation, J, Xprofiles, Yprofiles):
        plt.close()         
        """ Taking line profiles through J, Xpro and Ypro """
        jnumx = int(np.max(np.shape(j[:,0,0]))) # These are in pixels
        jnumy = int(np.max(np.shape(j[0,:,0])))        
        Xnumx = int(np.max(np.shape(xpro[:,0])))
        Ynumy = int(np.max(np.shape(ypro[:,0])))

        jmidX = int(jnumx/2)
        jmidY = int(jnumy/2)
        Xmid = int(Xnumx/2)
        Ymid = int(Ynumy/2)

        jX = j[:,jmidY]
        jY = j[jmidX,:]
        Ix = xpro[Xmid-jmidX:Xmid+jmidX]
        Iy = ypro[Ymid-jmidY:Ymid+jmidY]

        cX = jX/Ix
        cY = jY/Iy
        
        plt.clf()
        plt.close()
        plt.plot(cX, label="horizontal")
        plt.plot(cY, label="vertical")
        plt.title("Coherence Profiles from J")
        plt.legend()
        print("Saving Coherence profile to: {}".format(pathJ + pol + '.png'))
        plt.savefig(pathJ + pol + '.png')
        plt.show()
        plt.clf()
        plt.close()
        clX, clY = wfCoherence.getCoherenceLength(cH, cV, 0.01, pathCLj + P + '.png')
        _clX = clX*resolutionX.mean()
        _clY = clY*resolutionY.mean()
        print("Horizontal Coherence Length [m]: {}".format(_clX))
        print("Vertical Coherence Length [m]: {}".format(_clY))
        jCLx.append(_clX)
        jCLy.append(_clY)


plt.clf()
plt.close()
plt.plot(polarisation, jCLx, label="horizontal")
plt.plot(polarisation, jCLy, label="vertical")
plt.title("Coherence Lengths from J")
plt.legend()
print("Saving coherence length plot to {}".format(pathJclp))
plt.savefig(pathJclp)
plt.show()




""" Plotting Mutual Intensity Arrays and Polarisation """
plt.clf()
plt.close()
for pol, jxx, jxy, jyx, jyy in zip(polarisation, Jxx, Jxy, Jyx, Jyy):
        plt.close()
        jmax = np.max([jxx,jxy,jyx,jyy])
        jmin = np.min([jxx,jxy,jyx,jyy])
        fig, axs = plt.subplots(2, 2)
        im = axs[0, 0].imshow(jxx, vmin=jmin, vmax=jmax)
        axs[0, 0].set_title('Jxx')
        axs[0, 1].imshow(jxy, vmin=jmin, vmax=jmax)
        axs[0, 1].set_title('Jxy')
        axs[1, 0].imshow(jyx, vmin=jmin, vmax=jmax)
        axs[1, 0].set_title('Jyx')
        axs[1, 1].imshow(jyy, vmin=jmin, vmax=jmax)
        axs[1, 1].set_title('Jyy')
    
        for ax in axs.flat:
            ax.set(xlabel="Point Separation x-x' [pixels]", ylabel="Point Separation y-y'[pixels] ")
        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for ax in axs.flat:
            ax.label_outer()
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        fig.colorbar(im, cax=cbar_ax)
        print("Saving Mutual Intensity Plots to: {}".format(pathJP+pol+'.png'))
        plt.savefig(pathJP+pol+'.png')
        plt.show()
        plt.clf()
        
plt.clf()
plt.close()
for pol, s0, s1, s2, s3 in zip(polarisation, S0, S1, S2, S3):
        plt.close()
        smin = np.min([s0,s1,s2,abs(s3)])
        smax = np.max([s0,s1,s2,abs(s3)])
        fig, axs = plt.subplots(2, 2)
        im = axs[0, 0].imshow(s0, vmin=smin, vmax=smax)
        axs[0, 0].set_title('S0')
        axs[0, 1].imshow(s1, vmin=smin, vmax=smax)
        axs[0, 1].set_title('S1')
        axs[1, 0].imshow(s2, vmin=smin, vmax=smax)
        axs[1, 0].set_title('S2')
        axs[1, 1].imshow(abs(s3), vmin=smin, vmax=smax)
        axs[1, 1].set_title('S3')

        for ax in axs.flat:
            ax.set(xlabel="x position [pixels]", ylabel="y position [pixels] ")
        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for ax in axs.flat:
            ax.label_outer()
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        fig.colorbar(im, cax=cbar_ax)
        print("Saving Stokes Plots to: {}".format(pathS+pol+'.png'))
        plt.savefig(pathS+pol+'.png')
        plt.show()
        plt.clf()
        
        
for sV, pol in zip(stokes, polarisation): 
        plt.close()
        print("-----Stokes Vector-----")
        print(sV)
        
        print("Polarisation: {}".format(pol))
        

for dP, pol in zip(P, polarisation):
        print("Degree of Polarisation: {}".format(dP))
        #plt.imshow(dP)
        #plt.title("Degree of Polarisation")
        #plt.colorbar()
        #print("Saving degree of polarisation plot to: {}".format(pathDP+pol+'.png'))
        #plt.savefig(pathDP+pol+'.png')
        #plt.show()
        #plt.clf()


""" Plotting Intensity Profiles - Total Polarisation """
plt.clf()
plt.close()
for xprof, yprof, p in zip(Xprofiles, Yprofiles, polarisation):
        plt.plot(xprof, label=p + "horizontal cut")
        plt.plot(yprof, label=p + "vertical cut")
        plt.title("Intensity profiles (total P)")
        plt.xlabel("Position [m]")
        plt.ylabel("Intensity")
print("Saving Intensity Profiles (tp) to {}".format(pathP))
plt.legend()
plt.savefig(pathP)
plt.show()

""" Plotting Intensity Profiles - Horizontal Polarisation """
plt.clf()
plt.close()
for xprof, yprof, p in zip(XprofilesH, YprofilesH, polarisation):
        plt.plot(xprof, label=p + "horizontal cut")
        plt.plot(yprof, label=p + "vertical cut")
        plt.title("Intensity profiles (horizontal P)")
        plt.xlabel("Position [m]")
        plt.ylabel("Intensity")
print("Saving Intensity Profiles (hp) to {}".format(pathPh))
plt.legend()
plt.savefig(pathPh)
plt.show()

""" Plotting Intensity Profiles - Vertical Polarisation """
plt.clf()
plt.close()
for xprof, yprof, p in zip(XprofilesV, YprofilesV, polarisation):
        plt.plot(xprof, label=p + "horizontal cut")
        plt.plot(yprof, label=p + "vertical cut")
        plt.title("Intensity profiles (vertical P)")
        plt.xlabel("Position [m]")
        plt.ylabel("Intensity")
print("Saving Horizontal Intensity Profiles (vp) to {}".format(pathPv))
plt.legend()
plt.savefig(pathPv)
plt.show()



""" Finding and Plotting Diffraction Efficiency """
for profile, pol in zip(Xprofiles, polarisation):
        
        print(pol)
        E0, E1, En1, rE0, rE1, rEn1 = utilMask.getEfficiency(incidentI, exitI, profile, m=1, g=1, resIN = resolutionXIN, resEX = resolutionXEX, resPR = resolutionX[0], pathI=pathI+str(pol)+'.png', pathM=pathM+str(pol)+'.png')
        e0.append(E0)
        e1.append(E1)
        en1.append(En1)
        re0.append(rE0)
        re1.append(rE1)
        ren1.append(rEn1)
        print(e0[-1])

#print("Shape of e0: {}".format(np.shape(e0)))
#print("Shape of e1: {}".format(np.shape(e1)))
#print("Shape of en1: {}".format(np.shape(en1)))


plt.clf()
plt.close()
plt.plot(polarisation, e0, label="m = 0")
plt.xlabel("Beam Polarisation")
plt.ylabel("Efficiency")
plt.legend()
print("Saving Efficiency Plot to {}".format(pathE0))
plt.savefig(pathE0)
plt.show()

plt.clf()
plt.close()
plt.plot(polarisation, e1, label="m = +1")
plt.plot(polarisation, en1, label="m = -1")
plt.xlabel("Beam Polarisation")
plt.ylabel("Efficiency")
plt.legend()
print("Saving Efficiency Plot to {}".format(pathE1))
plt.savefig(pathE1)
plt.show()
	
plt.clf()
plt.close()
plt.plot(polarisation, e0, label="m=0, abs")
plt.plot(polarisation, e1, label="m=+1, abs")
plt.plot(polarisation, en1, label="m=-1, abs")
plt.plot(polarisation, re0, label="m=0, rel")
plt.plot(polarisation, re1, label="m=+1, rel")
plt.plot(polarisation, ren1, label="m=-1, rel")
plt.xlabel("Beam Polarisation")
plt.ylabel("Efficiency")
plt.legend()
print("Saving Efficiency Plot to {}".format(pathE))
plt.savefig(pathE)
plt.show()

import numpy as np
e0minA = np.argmin(e0)
e0minR = np.argmin(re0)
e1maxA = np.argmax(e1)
e1maxR = np.argmax(re1)
print("Maximum absolute Efficiency (m=1): {}".format(max(e1)))
print("Beam Polarisation for maximum absolute efficiency (m=1): {}".format(polarisation[e1maxA]))
print("Minimum absolute Efficiency (m=0): {}".format(min(e0)))
print("Beam Polarisation for minimum absolute efficiency (m=0): {}".format(polarisation[e0minA]))
print("Maximum relative efficiency (m=1): {}".format(max(re1)))
print("Beam Polarisation for maximum relative efficiency (m=1): {}".format(polarisation[e1maxR]))
print("Minimum relative efficiency (m=0): {}".format(min(re0)))
print("Beam Polarisation for minimum relative efficiency (m=0): {}".format(polarisation[e0minR]))



""" Plotting Stokes parameters from SRWLStokes() """ 
#for pol, D, E, I in zip(polarisation, listValues(results,'stkDavg'), listValues(results,'stkEccentricity'), listValues(results, 'stkI')):
#       plt.plot(pol, 
#plt.clf()
#plt.close()
#plt.plot(polarisation, D)
#plt.title("average D")
#plt.xlabel("Polarisation")
#plt.ylabel("Degree of Polarisation")
#print("Saving degree of polarisation plot to: {}".format(pathdP))
#plt.savefig(pathdP)
#plt.show()

#plot(results, y='polarisation, 'stkDavg')

#plot(results,y='Intensity/Horizontal/Y/integratedOpticalDensity', x='op_Mask_Watchpoint_L')


#'stk0', 'stk1', 'stk2', 'stk3', 'stkNormS', 'stkDpol', 'stkDavg', 'stkEccentricity', 'stkI',
