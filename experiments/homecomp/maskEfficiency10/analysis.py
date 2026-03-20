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

dirPath = '/data/experiments/maskEfficiency6/data/'

batchOutputFile = dirPath + '115/results.pickle'


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


key = 'intensitySum'
values = listValues(results, key)

print(resultsKeys(results))
     

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

print(" ")
print("Results Key")
print(resultsKeys(results))

Yprofiles = listValues(results, 'Intensity/Total/Y/profile')
Xprofiles = listValues(results, 'Intensity/Total/X/profile')
maskThickness = listValues(results, 'op_Mask_thick')

import utilMask

resultsIN = pickle.load( open('/data/experiments/maskEfficiency4/data/incident/results.pickle', 'rb')  )
resultsEX = pickle.load( open('/data/experiments/maskEfficiency4/data/exit/results.pickle', 'rb')  )

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

nxEX = listValues(resultsEX,'params/Mesh/nx')[0]
xMaxEX = listValues(resultsEX,'params/Mesh/xMax')[0]
xMinEX = listValues(resultsEX, 'params/Mesh/xMin')[0]
resolutionXEX  = np.divide(np.subtract(xMaxIN,xMinIN),nxIN)

incidentI = listValues(resultsIN, 'Intensity/Total/X/profile')[0]
exitI = listValues(resultsEX, 'Intensity/Total/X/profile')[0]

propDist = listValues(results, 'op_Farfield_Propagation_L')

pathI = dirPath + 'IntensityTest'
pathM = dirPath + 'orderIntensity'
pathE = dirPath + 'efficiencyPlot.png'
pathE0 = dirPath + 'efficiencyPlotM0.png'
pathE1 = dirPath + 'efficiencyPlotM1.png'
pathP = dirPath + 'Profiles'
pathEAE = dirPath + 'efficiencyPlotAE.png'
pathAE = dirPath + 'efficiencyABSOLUTE.png'
pathRE = dirPath + 'efficiencyRELATIVE.png'


e0 = [] #zero order efficiency (single grating)
e1 = [] #+1 order efficiency
en1 = [] #-1 order efficiency
re0 = [] #zero order relative efficiency (single grating) 
re1 = [] #+1 order relative efficiency
ren1 = [] #-1 order relative efficiency

eAE = [] # aerial image absolute efficiency (binary grating)
e0r = [] # zero order absolute efficiency (right grating - binary)
e0l = [] # zero order absolute efficiency (left grating - binary)
reAE = [] # aerial image relative efficiency (binary grating)
re0r = [] # zero order relative efficiency (right grating - binary)
re0l = [] # zero order relative efficiency (left grating - binary)


plt.clf()
plt.close()
#for profile, z in zip(Xprofiles, propDist):
#        Z = str(z)
#        plt.clf()
#        plt.close()
#        plt.plot(profile)
#        plt.title("horizontal intensity profiles")
#        plt.xlabel("x [m]")
#        plt.ylabel("Intensity")
#        print("Saving Intensity Profiles to {}".format(pathP + str(z)))
#        plt.savefig(pathP + str(z) + '.png')

#plt.plot([a for a in Xprofiles])
#listValues(results, 'x'),[a for a in zip(Xprofiles)])
#print("Saving Intensity Profiles to {}".format(pathP))
#plt.savefig(pathP)
#plt.show()


for profile, mask in zip(Xprofiles, maskThickness):
        
        print(mask)
        #E0, E1, En1, rE0, rE1, rEn1 = 
        EAE, E0r, E0l, E1, En1, rEAE, rE0r, rE0l, rE1, rEn1 = utilMask.getEfficiency(incidentI, exitI, profile, m=1, g=2, resIN = resolutionXIN, resEX = resolutionXEX, resPR = resolutionX[0], pathI=pathI+str(mask)+'.png', pathM=pathM+str(mask)+'.png')
        #e0.append(E0)
        eAE.append(EAE)
        e0r.append(E0r)
        e0l.append(E0l)
        e1.append(E1)
        en1.append(En1)
        reAE.append(rEAE)
        re0r.append(rE0r)
        re0l.append(rE0l)
        #re0.append(rE0)
        re1.append(rE1)
        ren1.append(rEn1)
        #print(e0[-1])

#print("Shape of e0: {}".format(np.shape(e0)))
#print("Shape of e1: {}".format(np.shape(e1)))
#print("Shape of en1: {}".format(np.shape(en1)))


plt.clf()
plt.close()
plt.plot(maskThickness, eAE, label="Aerial Image")
plt.xlabel("Mask Thickness [m]")
plt.ylabel("Efficiency")
plt.legend()
print("Saving Efficiency Plot to {}".format(pathEAE))
plt.savefig(pathEAE)
plt.show()

plt.clf()
plt.close()
plt.plot(maskThickness, e0r, label="m=0 (right)")
plt.plot(maskThickness, e0l, label="m=0 (left)")
plt.xlabel("Mask Thickness [m]")
plt.ylabel("Efficiency")
plt.legend()
print("Saving Efficiency Plot to {}".format(pathE0))
plt.savefig(pathE0)
plt.show()

plt.clf()
plt.close()
plt.plot(maskThickness, e1, label="m = +1")
plt.plot(maskThickness, en1, label="m = -1")
plt.xlabel("Mask Thickness [m]")
plt.ylabel("Efficiency")
plt.legend()
print("Saving Efficiency Plot to {}".format(pathE1))
plt.savefig(pathE1)
plt.show()
	
plt.clf()
plt.close()
plt.plot(maskThickness, e0r, label="m=0 (right)")
plt.plot(maskThickness, e0l, label="m=0 (left)")
plt.plot(maskThickness, eAE, label="Aerial Image")
plt.plot(maskThickness, e1, label="m=+1")
plt.plot(maskThickness, en1, label="m=-1")
plt.title("Absolute Efficiency")
plt.xlabel("Mask Thickness [m]")
plt.ylabel("Efficiency")
plt.legend()
print("Saving Absolute efficiency plot to: {}".format(pathAE))
plt.savefig(pathAE)
plt.show()
plt.clf()
plt.close()

plt.plot(maskThickness, re0r, label="m=0 (right)")
plt.plot(maskThickness, re0l, label="m=0 (left)")
plt.plot(maskThickness, reAE, label="Aerial Image")
plt.plot(maskThickness, re1, label="m=+1")
plt.plot(maskThickness, ren1, label="m=-1")
plt.title("Relative Efficiency")
plt.xlabel("Mask Thickness [m]")
plt.ylabel("Efficiency")
plt.legend()
print("Saving Efficiency Plot to {}".format(pathRE))
plt.savefig(pathRE)
plt.show()

import numpy as np
e0minA = np.argmin(e0r)
e0minR = np.argmin(re0r)
e1maxA = np.argmax(eAE)
e1maxR = np.argmax(reAE)
print("Maximum absolute Efficiency (Aerial Image): {}".format(max(eAE)))
print("Mask Thickness for maximum absolute efficiency (Aerial Image): {}".format(maskThickness[e1maxA]))
print("Minimum absolute Efficiency (m=0): {}".format(min(e0r)))
print("Mask Thickness for minimum absolute efficiency (m=0): {}".format(maskThickness[e0minA]))
print("Maximum relative efficiency (Aerial Image): {}".format(max(reAE)))
print("Mask Thickness for maximum relative efficiency (Aerial Image): {}".format(maskThickness[e1maxR]))
print("Minimum relative efficiency (m=0): {}".format(min(re0r)))
print("Mask Thickness for minimum relative efficiency (m=0): {}".format(maskThickness[e0minR]))

