#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 10:15:22 2021

@author: jerome
"""
import matplotlib.pyplot as plt
import numpy as np

DEGREEOFPOLARISATION  = [ 1.0, 0.9848076105117798, 0.939692497253418, 0.8660255074501038, 0.7660453915596008, 0.6427902579307556, 0.5000068545341492, 0.34203675389289856, 0.17369496822357178, 
                         0.004141990561038256, 0.1737147569656372, 0.3420543968677521, 0.5000208616256714, 0.6427999138832092, 0.7660503387451172, 
                         0.8660264611244202, 0.9396902322769165, 0.9848031997680664, 0.9999946355819702]
INCLINATION =           [ -4.7438268666155636e-05, 0.08728336542844772, 0.1746065616607666, 0.26198551058769226, 0.349445641040802, 0.4367794990539551, 0.5244755148887634, 0.6125873923301697, 0.7022992968559265, 
                         -0.014217056334018707, -0.7032666206359863, -0.6135092377662659, -0.525324821472168, -0.4375307261943817, -0.3499094843864441, 
                         -0.2623744606971741, -0.17488303780555725, -0.08742642402648926, 1.0733492566972203e-10]                     #[6.672828021692112e-05,7.139140507206321e-05, 7.586363790323958e-05, 0.10642404109239578, 0.11162425577640533, 8.7341497419402e-05]
INCREMENTS = np.linspace(0,180,19)
print(INCREMENTS)

save = True
savePath = '/home/jerome/Documents/MASTERS/Figures/plots/'

plt.plot(INCREMENTS, DEGREEOFPOLARISATION, 'o', label='P')#, markersize=10,linewidth=4)
plt.plot(INCREMENTS, abs(np.cos(np.deg2rad(INCREMENTS))), ':',label='|cos(\u0394\u03B8)|')
# plt.xticks(size=20)
# plt.yticks(size=20)
plt.xlabel('Angular Separation (\u0394\u03B8) [degrees]')#, fontsize=20)
plt.ylabel("Degree of Polarisation (P)")#, fontsize=20)
plt.legend()
if save:
    plt.savefig(savePath + 'degreePolarisation_angle.pdf')
    plt.savefig(savePath + 'degreePolarisation_angle.png', dpi=2000)
plt.show()
# plt.show()

fig, axs = plt.subplots(1,2)
axs[0].plot(INCREMENTS, DEGREEOFPOLARISATION, ':o')
axs[0].set_xlabel('Angular Separation [degrees]')
axs[0].set_ylabel("Degree of Polarisation")
axs[1].plot(INCREMENTS, abs(np.cos(np.deg2rad(INCREMENTS))))
axs[1].set_xlabel('Angular Separation [degrees]')
axs[1].set_ylabel('Inclination')
plt.show()


# electrons = [100,            1000,            2000,             3000,             4000,             5000,              10000]

# realTime = [1194.554,        152*60 + 16.56,  301*60 + 7.885,   458*60 + 17.129,  604*60 + 2.948,   745*60 + 35.449,   1505*60 + 43.718]
# userTime = [278*60 + 47.984, 2334*60 + 28.13, 4637*60 + 23.542, 7071*60 + 14.848, 9342*60 + 58.443, 11605*60 + 45.142, 23267*60 + 33.516]
# sysTime =  [32*60 + 10.116,  151*60 + 39.398, 228*60 + 2.226,   434*60 + 10.914,  571*60 + 23.125,  672*60 + 22.106,   1457*60 + 51.441]

# #1000 electrons
# # real 152m16.560s
# # user 2334m28.130s
# # sys 151m39.398s
# # real    173m58.839s
# # user    2539m6.062s
# # sys    172m4.882s


# # Coherence

# # real	4250m45.550s
# # user	64896m31.077s
# # sys	4463m25.430s


# fig, axs = plt.subplots(1,4)
# axs[0].plot(electrons, [(r/60)/60 for r in realTime], ':o')
# axs[0].set_ylabel("Real time [hours]")
# axs[1].plot(electrons, [(u/60)/60 for u in userTime], ':o')
# axs[1].set_ylabel("User time [hours]")
# axs[2].plot(electrons, [(s/60)/60 for s in sysTime], ':o')
# axs[2].set_ylabel("System Time [hours]")
# axs[3].plot(electrons, [(u)/((r)) for u, r in zip(userTime, realTime)], ':o')
# for ax in axs:
#     ax.set_xlabel("Electrons")
# fig.tight_layout()
# plt.show()


