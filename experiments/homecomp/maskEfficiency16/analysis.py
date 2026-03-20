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

dirPath = '/data/experiments/maskEfficiency16/data/'

batchOutputFile = dirPath + '11500/results.pickle'

ran= range(1000, 1500,5)

trialData = [dirPath + str(i) + '/' for i in ran]
pickles = ['mt' + str(i) + '.pkl' for i in ran]
expickles = ['mt-exit' + str(i) + '.pkl' for i in ran]

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

for t, pk, xp in zip(trialData, pickles, expickles):
    print("")
    print("----- Analysing trial:" + pk[0:len(str(pk))-3] + " -----")
    """ Getting range, resolution, dimensions """
    with open(t + pk, 'rb') as f:
        r = pickle.load(f)
    with open(t + xp, 'rb') as g:
        s = pickle.load(g)
        
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
    
    print("(xMin,xMax) [m]: {}".format((xMin,xMax)))
    print("x-Range [m]: {}".format(rx))
    print("(yMin,yMax) [m]: {}".format((yMin,yMax)))
    print("y-Range [m]: {}".format(ry))
    print("Dimensions (Nx,Ny) [pixels]: {}".format((nx,ny)))
    print("Resolution (dx,dy) [m]: {}".format((dx,dy)))
    
    Ix = r['results']['Intensity/Total/X/profile']
    Iy = r['results']['Intensity/Total/Y/profile']
    #mT = r['results']['op_Mask_thick']
    
    EXIx = s['results']['Intensity/Total/X/profile']
    EXIy = s['results']['Intensity/Total/Y/profile']
    
    Xprofiles.append(Ix)
    Yprofiles.append(Iy)
    exitIx.append(EXIx)
    exitIy.append(EXIy)
    #maskThickness.append(mT)




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
#resultsEX = pickle.load( open('/data/experiments/maskEfficiency3/data/' + 'exit/results.pickle', 'rb')  )

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

#nxEX = listValues(resultsEX,'params/Mesh/nx')[0]
#xMaxEX = listValues(resultsEX,'params/Mesh/xMax')[0]
#xMinEX = listValues(resultsEX, 'params/Mesh/xMin')[0]
#resolutionXEX  = np.divide(np.subtract(xMaxIN,xMinIN),nxIN)

incidentI = listValues(resultsIN, 'Intensity/Total/X/profile')[0]
#exitI = listValues(resultsEX, 'Intensity/Total/X/profile')[0]

pathI = dirPath + 'plots/IntensityTest'
pathM = dirPath + 'plots/orderIntensity'
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


for profile, mask, exitI in zip(Xprofiles, maskThickness, exitIx):
        
        print(mask)
        E0, E1, En1, rE0, rE1, rEn1 = utilMask.getEfficiency(incidentI, exitI, profile, m=1, g=1, resIN = resolutionXIN, resEX = resolutionXEX[0], resPR = resolutionX[0], pathI=pathI+str(mask)+'.png', pathM=pathM+str(mask)+'.png')
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

with open(dirPath + 'ZeroEfficiencyABS.pkl', 'wb') as s:
    pickle.dump(e0, s)
with open(dirPath + 'ZeroEfficiencyREL.pkl', 'wb') as t:
    pickle.dump(re0, t)
with open(dirPath + 'FirstEfficiencyABS.pkl', 'wb') as w:
    pickle.dump(e1, w)
with open(dirPath + 'FirstEfficiencyREL.pkl', 'wb') as x:
    pickle.dump(re1, x)
with open(dirPath + 'FirstEfficiencyABSneg.pkl', 'wb') as y:
    pickle.dump(en1, y)
with open(dirPath + 'FirstEfficiencyRELneg.pkl', 'wb') as p:
    pickle.dump(ren1, p)
#with open(dirPath + 'FourthEfficiencyABS.pkl', 'wb') as q:
#    pickle.dump(e4, q)
#with open(dirPath + 'SecondEfficiencyREL.pkl', 'wb') as r:
#    pickle.dump(re2, r)
#with open(dirPath + 'ThirdEfficiencyREL.pkl', 'wb') as z:
#    pickle.dump(re3, z)
#with open(dirPath + 'FourthEfficiencyREL.pkl', 'wb') as o:
#    pickle.dump(re4, o)

plt.clf()
plt.close()
plt.plot(maskThickness, e0, label="m = 0")
plt.xlabel("Mask Thickness [m]")
plt.ylabel("Absolute Efficiency")
plt.legend()
print("Saving Efficiency Plot to {}".format(pathE0))
plt.savefig(pathE0)
plt.show()

plt.clf()
plt.close()
plt.plot(maskThickness, e1, label="m = +1")
plt.plot(maskThickness, en1, label="m = -1")
plt.xlabel("Mask Thickness [m]")
plt.ylabel("Abslute Efficiency")
plt.legend()
print("Saving Efficiency Plot to {}".format(pathE1))
plt.savefig(pathE1)
plt.show()
	
plt.clf()
plt.close()
plt.plot(maskThickness, e1, label="m = +1")
plt.plot(maskThickness, en1, label="m = -1")
plt.xlim(1200,1300)
plt.xlabel("Mask Thickness [m]")
plt.ylabel("Efficiency")
plt.legend()
print("Saving Efficiency Plot (close-up) to {}".format(pathE1close))
plt.savefig(pathE1close)
plt.show()

plt.clf()
plt.close()
plt.plot(maskThickness, re1, label="m = +1")
plt.plot(maskThickness, ren1, label="m = -1")
plt.xlim(1200,1300)
plt.xlabel("Mask Thickness [m]")
plt.ylabel("Efficiency")
plt.legend()
print("Saving Relative Efficiency Plot (close-up) to {}".format(pathrE1close))
plt.savefig(pathrE1close)
plt.show()

plt.clf()
plt.close()
plt.plot(maskThickness, re0, label="m = 0")
plt.xlabel("Mask Thickness [m]")
plt.ylabel("Relative Efficiency")
plt.legend()
print("Saving Relative Efficiency Plot to {}".format(pathrE0))
plt.savefig(pathrE0)
plt.show()


plt.clf()
plt.close()
plt.plot(maskThickness, re1, label="m = +1")
plt.plot(maskThickness, ren1, label="m = -1")
plt.xlabel("Mask Thickness [m]")
plt.ylabel("Relative Efficiency")
plt.legend()
print("Saving Relative Efficiency Plot to {}".format(pathrE1))
plt.savefig(pathrE0)
plt.show()
	
plt.clf()
plt.close()
plt.plot(maskThickness, e0, label="m=0, abs")
plt.plot(maskThickness, e1, label="m=+1, abs")
plt.plot(maskThickness, en1, label="m=-1, abs")
plt.plot(maskThickness, re0, label="m=0, rel")
plt.plot(maskThickness, re1, label="m=+1, rel")
plt.plot(maskThickness, ren1, label="m=-1, rel")
plt.xlabel("Mask Thickness [m]")
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
print("Mask Thickness for maximum absolute efficiency (m=1): {}".format(maskThickness[e1maxA]))
print("Minimum absolute Efficiency (m=0): {}".format(min(e0)))
print("Mask Thickness for minimum absolute efficiency (m=0): {}".format(maskThickness[e0minA]))
print("Maximum relative efficiency (m=1): {}".format(max(re1)))
print("Mask Thickness for maximum relative efficiency (m=1): {}".format(maskThickness[e1maxR]))
print("Minimum relative efficiency (m=0): {}".format(min(re0)))
print("Mask Thickness for minimum relative efficiency (m=0): {}".format(maskThickness[e0minR]))

