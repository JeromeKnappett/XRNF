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

dirPath = '/data/experiments/maskEfficiency7/data/'

batchOutputFile = dirPath + '0175/results.pickle'


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

resultsIN = pickle.load( open('/data/experiments/maskEfficiency3/data/incident/results.pickle', 'rb')  )
resultsEX = pickle.load( open(dirPath + 'exit_0175/results.pickle', 'rb')  )

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
exitI = listValues(resultsEX, 'Intensity/Total/X/profile')

pathI = dirPath + 'IntensityTest'
pathM = dirPath + 'orderIntensity'
pathE = dirPath + 'efficiencyPlot.png'
pathE0 = dirPath + 'efficiencyPlotM0.png'
pathE1 = dirPath + 'efficiencyPlotM1.png'
pathE2 = dirPath + 'efficiencyPlotM2.png'
pathE3 = dirPath + 'efficiencyPlotM3.png'
pathE4 = dirPath + 'efficiencyPlotM4.png'
pathP = dirPath + 'Profiles.png'

e0 = []
e1 = []
en1 = []
e2 = []
en2 = []
e3 = []
en3 = []
e4 = []
en4 = []
re0 = []
re1 = []
ren1 = []
re2 = []
ren2 = []
re3 = []
ren3 = []
re4 = []
ren4 = []

dutyCycle = [0.5, 0.375, 0.25, 0.175]

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


for profile, f, ex in zip(Xprofiles, dutyCycle, exitI):
        
        print("Duty Cycle (f): {}.".format(f))
        E0, E1, En1, E2, En2, E3, En3, E4, En4, rE0, rE1, rEn1, rE2, rEn2, rE3, rEn3, rE4, rEn4 = utilMask.getEfficiency(incidentI, ex, profile, m=5, g=1, resIN = resolutionXIN, resEX = resolutionXEX, resPR = resolutionX[0], pathI=pathI+str(f)+'.png', pathM=pathM+str(f)+'.png')
        e0.append(E0)
        e1.append(E1)
        en1.append(En1)
        e2.append(E2)
        en2.append(En2)
        e3.append(E3)
        en3.append(En3)
        e4.append(E4)
        en4.append(En4)
        re0.append(rE0)
        re1.append(rE1)
        ren1.append(rEn1)
        re2.append(rE2)
        ren2.append(rEn2)
        re3.append(rE3)
        ren3.append(rEn3)
        re4.append(rE4)
        ren4.append(rEn4)
        print(e0[-1])

#print("Shape of e0: {}".format(np.shape(e0)))
#print("Shape of e1: {}".format(np.shape(e1)))
#print("Shape of en1: {}".format(np.shape(en1)))


plt.clf()
plt.close()
plt.plot(dutyCycle, e0, label="m = 0")
plt.xlabel("Duty Cycle (f)")
plt.ylabel("Efficiency")
plt.legend()
print("Saving Efficiency Plot to {}".format(pathE0))
plt.savefig(pathE0)
plt.show()

plt.clf()
plt.close()
plt.plot(dutyCycle, e1, label="m = +1")
plt.plot(dutyCycle, en1,label="m = -1")
plt.xlabel("Duty Cycle (f)")
plt.ylabel("Efficiency")
plt.legend()
print("Saving Efficiency Plot to {}".format(pathE1))
plt.savefig(pathE1)
plt.show()

plt.clf()
plt.close()
plt.plot(dutyCycle, e2, label="m = +2")
plt.plot(dutyCycle, en2, label="m = -2")
plt.xlabel("Duty Cycle (f)")
plt.ylabel("Efficiency")
plt.legend()
print("Saving Efficiency Plot to {}".format(pathE2))
plt.savefig(pathE2)
plt.show()

plt.clf()
plt.close()
plt.plot(dutyCycle, e3, label="m = +3")
plt.plot(dutyCycle, en3, label="m = -3")
plt.xlabel("Duty Cycle (f)")
plt.ylabel("Efficiency")
plt.legend()
print("Saving Efficiency Plot to {}".format(pathE3))
plt.savefig(pathE3)
plt.show()
	
plt.clf()
plt.close()
plt.plot(dutyCycle, e4, label="m = +4")
plt.plot(dutyCycle, en4, label="m = -4")
plt.xlabel("Duty Cycle (f)")
plt.ylabel("Efficiency")
plt.legend()
print("Saving Efficiency Plot to {}".format(pathE4))
plt.savefig(pathE4)
plt.show()
	
plt.clf()
plt.close()
plt.plot(dutyCycle, e0, '.', label="m=0", color='b')
plt.plot(dutyCycle, e1, '.', label="m=+1", color='g')
#plt.plot(dutyCycle, en1, label="m=-1")
plt.plot(dutyCycle, e2, '.', label="m=+2", color='y')
#plt.plot(dutyCycle, en2, label="m=-2")
plt.plot(dutyCycle, e3, '.', label="m=+3", color='r')
#plt.plot(dutyCycle, en3, label="m=-3")
plt.plot(dutyCycle, e4, '.', label="m=+4", color='m')
#plt.plot(dutyCycle, en4, label="m=-4")
plt.xlabel("Duty Cycle (f)")
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
e2maxA = np.argmax(e2)

e3maxA = np.argmax(e3)

e4maxA = np.argmax(e4)

print("Maximum absolute Efficiency (m=1): {}".format(max(e1)))
print("Duty Cycle (f) for maximum absolute efficiency (m=1): {}".format(dutyCycle[e1maxA]))
print("Minimum absolute Efficiency (m=0): {}".format(min(e0)))
print("Duty Cycle (f) for minimum absolute efficiency (m=0): {}".format(dutyCycle[e0minA]))
print("Maximum relative efficiency (m=1): {}".format(max(re1)))
print("Duty Cycle (f) for maximum relative efficiency (m=1): {}".format(dutyCycle[e1maxR]))
print("Minimum relative efficiency (m=0): {}".format(min(re0)))
print("Duty Cycle (f) for minimum relative efficiency (m=0): {}".format(dutyCycle[e0minR]))
print("Maximum absolute Efficiency (m=2): {}".format(max(e2)))
print("Duty Cycle (f) for maximum absolute efficiency (m=2): {}".format(dutyCycle[e2maxA]))
print("Maximum absolute Efficiency (m=3): {}".format(max(e3)))
print("Duty Cycle (f) for maximum absolute efficiency (m=3): {}".format(dutyCycle[e3maxA]))
print("Maximum absolute Efficiency (m=4): {}".format(max(e4)))
print("Duty Cycle (f) for maximum absolute efficiency (m=4): {}".format(dutyCycle[e4maxA]))

