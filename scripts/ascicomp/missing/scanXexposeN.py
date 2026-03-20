
import time
import epics
import numpy as np
import pandas as pd


delay = 0.18 #s
#exposures = 4000 #Used for scan of grating
exposures = 1000 #Used for Whitefield 
print 'Enter Outfile name'

fname = raw_input()
outFileName = '/sxri_data/detectorCom/'+ str(fname) + '.csv'
#E1 = 90.
#E2 = 290
#Estep = 20.
EChangeSleepTime = 10.

pvPhotoDiodeCurrent = epics.PV('SR14ID01AMP05:CURR_MONITOR')
pvScanStatus = epics.PV('SR14ID01IOC70:scan1.EXSC')
pvRingCurrent = epics.PV('SR11BCM01:CURRENT_MONITOR')
pvPhotonEnergy = epics.PV('SR14ID01PGM_ENERGY_SP')
pvHLV = epics.PV('SR14ID01SLH02:XSIZE')

print 'Handling multiple exposure scan...\n'
print 'YOU MUST SET EXPOSURE TIME!\N'


#r = np.arange(E1,E2+Estep,Estep)
r =   [91.84, 100., 110., 120., 130., 140.,  150.,  160., 170.,  180., 185.05,190., 200., 210., 220., 230., 240., 250., 260., 270., 3*91.84,280.,290.]

#hlv = [144.,  136., 136., 128., 124., 122.,  118.,  116., 116.,  114., 114.,  114., 113., 112., 111., 111,  110., 110., 109., 108., 108.,   108., 109.] #Used for scans of gratings

hlv = [144.,  136., 136., 128., 124., 122.,  118.,  116., 116.,  114., 114.,  114., 113., 112., 111., 111,  110., 110., 109., 108., 108.,   108., 109.] # Used for white field
#SLV fixed to 30 um


time.sleep(EChangeSleepTime)

print ('Starting Scan...')


N = np.size(r)
df =  pd.DataFrame(columns = ['Energy','Ip','Ir'],index=range((N)*exposures))

print 'Set number of exposures in MOSAIC to ' + str(N*exposures) + '\n'



print 'setting first energy, E1...\n'
pvPhotonEnergy.put(r[0])

i = 0
for E, H in zip(r,hlv):
    print 'changing HLV...'
    pvHLV.put(H)   

    print 'Changing energy...'
    pvPhotonEnergy.put(E)
    time.sleep(EChangeSleepTime)

    
    for ei in range(exposures):

        # start scan        
	#pvScanStatus.put(1)
        epics.caput('SR14ID01IOC70:scan1.EXSC',1)

	# wait for scan to complete
	done = False
	while not done:

	    #done = pvScanStatus.get()==0
            done = epics.caget('SR14ID01IOC70:scan1.EXSC') ==0
            time.sleep(delay/5.)
            #print pvScanStatus

        df.loc[i].Ip = pvPhotoDiodeCurrent.get()
        df.loc[i].Ir = pvRingCurrent.get()
        df.loc[i].Energy = pvPhotonEnergy.get()
        i = i+1
	    
df.to_csv(outFileName)
print  'Wrote ' + outFileName

