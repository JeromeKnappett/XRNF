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

dirPath = '/data/experiments/maskEfficiency19/data/'

batchOutputFile = dirPath + '11500/results.pickle'

ran= range(1, 20)

trialData = [dirPath + str(i) + '/' for i in ran]
pickles = ['mo' + str(i) + '.pkl' for i in ran]
expickles = ['mo' + str(i) + '-exit.pkl' for i in ran]

nX = []
resolutionX = []
nY = []
resolutionY = []
Xprofiles = []
Yprofiles = []
maskThickness = list(ran)

resolutionXEX = []
resolutionYEX = []
nXEX = []
nYEX = []
exitIx = []
exitIy = []

exitWave = False
propWave = True

for t, pk, xp in zip(trialData, pickles, expickles):
    print("")
    print("----- Analysing trial:" + pk[0:len(str(pk))-3] + " -----")
    """ Getting range, resolution, dimensions """
    if propWave == True:
        print("Loading propagated wavefield")
        with open(t + pk, 'rb') as f:
            r = pickle.load(f)
        nx = r['results']['params/Mesh/nx']
        xMax = r['results']['params/Mesh/xMax']
        xMin = r['results']['params/Mesh/xMin']
        rx = np.subtract(xMax,xMin)
        dx = np.divide(rx,nx)
        resolutionX.append(dx)
        nX.append(nx)
        ny = r['results']['params/Mesh/ny']
        yMax = r['results']['params/Mesh/yMax']
        yMin = r['results']['params/Mesh/yMin']
        ry = np.subtract(yMax,yMin)
        dy = np.divide(ry,ny)   
        resolutionY.append(dy)
        nY.append(ny)
        
        print("(xMin,xMax) [m]: {}".format((xMin,xMax)))
        print("x-Range [m]: {}".format(rx))
        print("(yMin,yMax) [m]: {}".format((yMin,yMax)))
        print("y-Range [m]: {}".format(ry))
        print("Dimensions (Nx,Ny) [pixels]: {}".format((nx,ny)))
        print("Resolution (dx,dy) [m]: {}".format((dx,dy)))
        
        Ix = r['results']['Intensity/Total/X/profile']
        Iy = r['results']['Intensity/Total/Y/profile']
    
    
        Xprofiles.append(Ix)
        Yprofiles.append(Iy)

        plt.clf()
        plt.close()
        plt.plot(Ix, label='x-cut')
        plt.title("Horizontal intensity"+ pk[0:len(str(pk))-4])
        print("Saving intensity plot to: " + dirPath + 'plots/exitIntensityX' + pk[0:len(str(pk))-4] + '.png')
        plt.savefig(dirPath + 'plots/IntensityX' + pk[0:len(str(pk))-4] + '.png')
        
        plt.clf()
        plt.close()    
        plt.plot(Iy, label='y-cut')
        plt.title("Vertical intensity"+ pk[0:len(str(pk))-4])
        print("Saving intensity plot to: " + dirPath + 'plots/IntensityY' + pk[0:len(str(pk))-4] + '.png')
        plt.savefig(dirPath + 'plots/IntensityY' + pk[0:len(str(pk))-4] + '.png')
    
    else:
        print("Ignoring propagated wavefield")
        pass
        
    if exitWave == True:
        print("Loading exit wavefield")
        with open(t + xp, 'rb') as g:
            s = pickle.load(g)
        Enx = s['results']['params/Mesh/nx']
        ExMax = s['results']['params/Mesh/xMax']
        ExMin = s['results']['params/Mesh/xMin']
        Erx = np.subtract(ExMax,ExMin)
        Edx = np.divide(Erx,Enx)
        resolutionXEX.append(Edx)
        nXEX.append(Enx)
        Eny = s['results']['params/Mesh/ny']
        EyMax = s['results']['params/Mesh/yMax']
        EyMin = s['results']['params/Mesh/yMin']
        Ery = np.subtract(EyMax,EyMin)
        Edy = np.divide(Ery,Eny)   
        resolutionYEX.append(Edy)
        nYEX.append(Eny)    
        EXIx = s['results']['Intensity/Total/X/profile']
        EXIy = s['results']['Intensity/Total/Y/profile']
    
        exitIx.append(EXIx)
        exitIy.append(EXIy)
        
        plt.clf()
        plt.close()
        plt.plot(EXIx, label='x-cut')
        plt.title("Horizontal exit intensity"+ xp[0:len(str(pk))-4])
        print("Saving exit intensity plot to: " + dirPath + 'plots/exitIntensityX' + xp[0:len(str(pk))-4] + '.png')
        plt.savefig(dirPath + 'plots/exitIntensityX' + xp[0:len(str(pk))-4] + '.png')
        
        plt.clf()
        plt.close()    
        plt.plot(EXIy, label='y-cut')
        plt.title("Vertical exit intensity"+ xp[0:len(str(pk))-4])
        print("Saving exit intensity plot to: " + dirPath + 'plots/exitIntensityY' + xp[0:len(str(pk))-4] + '.png')
        plt.savefig(dirPath + 'plots/exitIntensityY' + xp[0:len(str(pk))-4] + '.png')
    else:
        print("Ignoring exit wavefield")
        pass





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
    

        
#results = pickle.load( open(batchOutputFile, 'rb')  )


#key = 'intensitySum'
#values = listValues(results, key)

#print(resultsKeys(results))
     

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

##number of pixels, range, resolution
#ny = listValues(results,'params/Mesh/ny')
#yMax = listValues(results,'params/Mesh/yMax')
#yMin = listValues(results, 'params/Mesh/yMin')
#resolutionY  = np.divide(np.subtract(yMax,yMin),ny)

#y = listValues(results, 'y')
 

##number of pixels, range, resolution
#nx = listValues(results,'params/Mesh/nx')
#xMax = listValues(results,'params/Mesh/xMax')
#xMin = listValues(results, 'params/Mesh/xMin')
#resolutionX  = np.divide(np.subtract(xMax,xMin),nx)

#x = listValues(results, 'x')


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

#Yprofiles = listValues(results, 'Intensity/Total/Y/profile')
#Xprofiles = listValues(results, 'Intensity/Total/X/profile')
#maskThickness = listValues(results, 'op_Mask_thick')

import utilMask

resultsIN = pickle.load( open('/data/experiments/maskEfficiency3/data/' + 'incident/results.pickle', 'rb')  )
resultsEX = pickle.load( open('/data/experiments/maskEfficiency3/data/' + 'exit/results.pickle', 'rb')  )

#print(" ")
#print("Incident results Key")
#print(resultsKeys(resultsIN))
#print(" ")
#print("Exit results Key")
#print(resultsKeys(resultsEX))


nxIN = listValues(resultsIN,'params/Mesh/nx')[0]
xMaxIN = listValues(resultsIN,'params/Mesh/xMax')[0]
xMinIN = listValues(resultsIN, 'params/Mesh/xMin')[0]
resolutionXIN  = np.divide(np.subtract(xMaxIN,xMinIN),nxIN)

#with open('/data/experiments/maskEfficiency7/data/exit_05/exit-f0-5.pkl', 'rb') as g:
#    rEX = pickle.load(g)

#nxEX = rEX['results']['params/Mesh/nx']
#xMaxEX = rEX['results']['params/Mesh/xMax']
#xMinEX = rEX['results']['params/Mesh/xMin']
#resolutionXEX  = np.divide(np.subtract(xMaxEX,xMinEX),nxEX)
#exitI = rEX['results']['Intensity/Total/X/profile']

nxEX = listValues(resultsEX,'params/Mesh/nx')[0]
xMaxEX = listValues(resultsEX,'params/Mesh/xMax')[0]
xMinEX = listValues(resultsEX, 'params/Mesh/xMin')[0]
resolutionXEX  = np.divide(np.subtract(xMaxIN,xMinIN),nxIN)

incidentI = listValues(resultsIN, 'Intensity/Total/X/profile')[0]
exitI = listValues(resultsEX, 'Intensity/Total/X/profile')[0]

pathI = dirPath + 'plots/IntensityTest'
pathM = dirPath + 'plots/orderIntensity'
pathexitI = dirPath + 'plots/exitIntensity.png'
pathE = dirPath + 'plots/efficiencyPlot.png'
pathE0 = dirPath + 'plots/efficiencyPlotM0.png'
pathE1 = dirPath + 'plots/efficiencyPlotM1.png'
pathE1close = dirPath + 'plots/efficiencyPlotM1close.png'
pathrE0 = dirPath + 'plots/efficiencyRELPlotM0.png'
pathrE1 = dirPath + 'plots/efficiencyRELPlotM1.png'
pathrE1close = dirPath + 'plots/efficiencyRELPlotM1close.png'
pathP = dirPath + 'plots/Profiles.png'

e0 = [] #zero order efficiency (single grating)
e1 = [] #+1 order efficiency
en1 = [] #-1 order efficiency
re0 = [] #zero order relative efficiency (single grating) 
re1 = [] #+1 order relative efficiency
ren1 = [] #-1 order relative efficiency

if propWave == True:
    plt.clf()
    plt.close()
    for profile in Xprofiles:
            plt.plot(profile)
            plt.title("horizontal intensity profiles")
            plt.xlabel("x [m]")
            plt.ylabel("Intensity")
    #plt.plot([a for a in Xprofiles])
    #listValues(results, 'x'),[a for a in zip(Xprofiles)])
    print("Saving Intensity Profiles to {}".format(pathP))
    plt.savefig(pathP)
    plt.show()
else:
    pass

if exitWave == True:
    plt.clf()
    plt.close()
    for profile in exitIx:
            plt.plot(profile)
            plt.title("horizontal exit intensity profiles")
            plt.xlabel("x [m]")
            plt.ylabel("Intensity")
    #plt.plot([a for a in Xprofiles])
    #listValues(results, 'x'),[a for a in zip(Xprofiles)])
    print("Saving Exit Intensity Profiles to {}".format(pathexitI))
    plt.savefig(pathexitI)
    plt.show()
else:
    pass

offSet = [int((i*1e-6)/resolutionX[0]) for i in ran]

if propWave and exitWave:
    for profile, exitI, off in zip(Xprofiles, exitIx, offSet):
            
            print("offset: {}".format(off))
            E0, E1, En1, rE0, rE1, rEn1 = utilMask.getEfficiency(incidentI, exitI, profile, m=1, g=1, offset=off, resIN = resolutionXIN, resEX = resolutionXEX[0], resPR = resolutionX[0], pathI=pathI+str(off)+'.png', pathM=pathM+str(off)+'.png')
            e0.append(E0)
            e1.append(E1)
            en1.append(En1)
            re0.append(rE0)
            re1.append(rE1)
            ren1.append(rEn1)
            print(e0[-1])

if propWave and not exitWave:
    for profile, off in zip(Xprofiles, offSet):
            
            print("offset: {}".format(off))
            E0, E1, En1, rE0, rE1, rEn1 = utilMask.getEfficiency(incidentI, exitI, profile, m=1, g=1, offset=off, resIN = resolutionXIN, resEX = resolutionXEX, resPR = resolutionX[0], pathI=pathI+str(off)+'.png', pathM=pathM+str(off)+'.png')
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
plt.plot(offSet, e0, label="m = 0")
plt.xlabel("Grating offset [pix]")
plt.ylabel("Absolute Efficiency")
plt.legend()
print("Saving Efficiency Plot to {}".format(pathE0))
plt.savefig(pathE0)
plt.show()

plt.clf()
plt.close()
plt.plot(offSet, e1, label="m = +1")
plt.plot(offSet, en1, label="m = -1")
plt.xlabel("Grating offset [pix]")
plt.ylabel("Abslute Efficiency")
plt.legend()
print("Saving Efficiency Plot to {}".format(pathE1))
plt.savefig(pathE1)
plt.show()


plt.clf()
plt.close()
plt.plot(offSet, re0, label="m = 0")
plt.xlabel("Grating offset [pix]")
plt.ylabel("Relative Efficiency")
plt.legend()
print("Saving Relative Efficiency Plot to {}".format(pathrE0))
plt.savefig(pathrE0)
plt.show()


plt.clf()
plt.close()
plt.plot(offSet, re1, label="m = +1")
plt.plot(offSet, ren1, label="m = -1")
plt.xlabel("Mask Thickness [m]")
plt.ylabel("Relative Efficiency")
plt.legend()
print("Saving Relative Efficiency Plot to {}".format(pathrE1))
plt.savefig(pathrE0)
plt.show()
	
plt.clf()
plt.close()
plt.plot(offSet, e0, label="m=0, abs")
plt.plot(offSet, e1, label="m=+1, abs")
plt.plot(offSet, en1, label="m=-1, abs")
plt.plot(offSet, re0, label="m=0, rel")
plt.plot(offSet, re1, label="m=+1, rel")
plt.plot(offSet, ren1, label="m=-1, rel")
plt.xlabel("Grating offset [pix]")
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
print("offSet for maximum absolute efficiency (m=1): {}".format(offSet[e1maxA]))
print("Minimum absolute Efficiency (m=0): {}".format(min(e0)))
print("offSet for minimum absolute efficiency (m=0): {}".format(offSet[e0minA]))
print("Maximum relative efficiency (m=1): {}".format(max(re1)))
print("offSet for maximum relative efficiency (m=1): {}".format(offSet[e1maxR]))
print("Minimum relative efficiency (m=0): {}".format(min(re0)))
print("offSet for minimum relative efficiency (m=0): {}".format(offSet[e0minR]))

