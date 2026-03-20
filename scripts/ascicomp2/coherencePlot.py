#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 12:18:51 2023

@author: -
"""

import pickle
import os
import matplotlib.pyplot as plt
import numpy as np
from usefulWavefield import round_sig
import matplotlib as mpl

plt.rcParams["figure.figsize"] = (5,4)
FSIZE = 12


mpl.rcParams['mathtext.default'] = 'regular'


cLx = pickle.load(open('/user/home/optjk/xl/xl/experiments/correctedAngle_coherence/pickles/cXlength.pkl', 'rb')) #'/user/home/Downloads/cXlength.pkl', 'rb'))
cLy = pickle.load(open('/user/home/Downloads/cYlength.pkl', 'rb'))
Ix = pickle.load(open('/user/home/optjk/xl/xl/experiments/correctedAngle_coherence/pickles/totI.pkl', 'rb')) #'/user/home/Downloads/totIx.pkl', 'rb'))
Iy = pickle.load(open('/user/home/Downloads/totIy.pkl', 'rb'))
cLx100 = pickle.load(open('/user/home/Downloads/cXlength100.pkl', 'rb'))
cLy100 = pickle.load(open('/user/home/Downloads/cYlength100.pkl', 'rb'))
Ix100 = pickle.load(open('/user/home/Downloads/totIx100.pkl', 'rb'))
Iy100 = pickle.load(open('/user/home/Downloads/totIy100.pkl', 'rb'))

 
print([(2.0/3.0)*c*1e3 for c in cLx[0:10]])

sX = [25,50,75,100,125,150,200,250,300,350]
sY = [25,50,75,100,125,150,175,200]
sX100 = [25,50,75,100,125,150,175,200,225,250,275,300,325,350,375]
sY100 = [25,50,75,100,125,150,175,200,225,250,275,300,325,350]

sybw = [50,100,150,200,250,300,350]
BWy = [0.044783384,0.059903136,0.071764895,0.093915228,0.113844421,0.145226545,0.158851144]
# BWy = [(2.0/3.0)*(s*0.000396378) + 0.019051304 for s in sY]
BWx =  0.1 #(3.0/2.0)*(200*0.000396378) + 0.019051304
#[(2.0/3.0)*(s*0.000396378) + 0.019051304 for s in sX]
#(2.0/3.0)*(200*0.000396378) + 0.019051304

eff = 1.0 
#0.03935212451203237 # cff = 3, grating E = 10%
#0.03569853100423892 # cff = 2, grating E = 10%
#0.027501275406876923 # cff = 1.4, grating E = 10%
#0.027501275406876923 # 0.013750637703438462 #0.004297207161730262

# Create figure and subplot manually
# fig = plt.figure()
# host = fig.add_subplot(111)

print(Ix)

CC = [(2.0/3.0)*c*1e6 for c in cLx[0:10]]
print(CC)

print([i for i in range(len(CC)) if CC[i] > 0.3])

# print(sX[CC>0.3])

Imin,Imax = np.min([(BWx/0.1)*i*eff for i in Ix[0:10]])-0.05e10 ,np.max([(BWx/0.1)*i*eff for i in Ix[0:10]])+0.05e10
BWmin,BWmax = np.min([1/(b/100) for b in BWy])-75 ,np.max([1/(b/100) for b in BWy])+75

# More versatile wrapper
plt.clf()
plt.close()
fig, host = plt.subplots(figsize=(5,4), layout='constrained') # (width, height) in inches
# (see https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html and
# .. https://matplotlib.org/stable/tutorials/intermediate/constrainedlayout_guide.html)
    
ax2 = host.twinx()
ax3 = host.twinx()
    
# host.set_xlim(0, 400)
# host.set_ylim(0, )
# ax2.set_ylim(0, 4)
# ax3.set_ylim(1, 65)
    
host.set_xlabel("SSA size [microns]")
host.set_ylabel("Intensity [ph/s/cm$^2$]")
ax2.set_ylabel("Horizontal Coherence Length [mm]")
ax3.set_ylabel("Resolving Power")

color1, color2, color3 = ['black','red','blue']#plt.cm.viridis([0, .5, .9])

# p1x = host.plot(sX,[(b/0.1)*i for b,i in zip(BWx,Ix[0:10])], 'x:',   color=color1, label="Ix")
p1x = host.plot(sX,[(BWx/0.1)*i*eff for i in Ix[0:10]], 'o',   color=color1, label="Ix",markerfacecolor='none')
# p1y = host.plot(sY,[(b/0.1)*i for b,i in zip(BWy,Iy[0:8])], label="Iy")
# p1x = host.plot(sY,Iy[0:8],'x:',    color=color1, label="Ix")
# p1y = host.plot(sX,Ix[0:10],'x:',color=color1, label="Iy")
p2 = ax2.plot(sX,[(2.0/3.0)*c*1e3 for c in cLx[0:10]],'o',    color=color2, label="Cx",markerfacecolor='none')
# p2 = ax2.plot(sY,[(2.0/3.0)*c*1e3 for c in cLy[0:8]],'x:',    color=color2, label="Cx")
p3 = ax3.plot(sybw,[1/(b/100) for b in BWy],'o', color=color3, label="BW",markerfacecolor='none')

# host.legend(handles=p1x+p2+p3, loc='best')

ax2.vlines(200,ymin=-0.1,ymax=1.25,colors='gray',linestyles=':')
ax2.hlines(0.15,xmin=0,xmax=350,colors='gray',linestyles=':')

# host.text(230,2.1e13,str(round_sig(abs((BWx/0.1)*eff*Ix[6])*1e-13)) + 'x$10^{13}$',color='black',fontname='serif',size=15)
ax2.text(310,0.175,str(round_sig((2.0/3.0)*cLx[9]*1e3)) + ' mm',color='red',fontname='serif',size=15)
# ax3.text(210,1050,str(round_sig(1/(BWy[6]/100))),color='blue',fontname='serif',size=15)

# ax2.axvspan()

# right, left, top, bottom
ax3.spines['right'].set_position(('outward', 60))

# no x-ticks                 
# host.xaxis.set_ticks([])

# Alternatively (more verbose):
# host.tick_params(
#     axis='x',          # changes apply to the x-axis
#     which='both',      # both major and minor ticks are affected
#     bottom=False,      # ticks along the bottom edge are off)
#     labelbottom=False) # labels along the bottom edge are off
# sometimes handy:  direction='in'    

# Move "Velocity"-axis to the left
# ax3.spines['left'].set_position(('outward', 60))
# ax3.spines['left'].set_visible(True)
# ax3.spines['right'].set_visible(False)
# ax3.yaxis.set_label_position('left')
# ax3.yaxis.set_ticks_position('left')

host.yaxis.label.set_color(p1x[0].get_color())
# host.yaxis.label.set_color(p1y[0].get_color())
ax2.yaxis.label.set_color(p2[0].get_color())
ax3.yaxis.label.set_color(p3[0].get_color())
for a in [host,ax2,ax3]:
    # a.set_xlim([0,355])
    a.minorticks_on()
# host.set_ylim([Imin,Imax])
ax2.set_ylim([np.min(CC)-0.05,np.max(CC)+0.05])
ax3.set_ylim([BWmin,BWmax])

# host.set_ylim([np.min([(BWx/0.1)*i*0.004297207161730262 for i in Ix[0:10]])-0.05e13,np.max([(BWx/0.1)*i*0.004297207161730262 for i in Ix[0:10]])])+0.05e13
# ax2.set_ylim([np.min([(2.0/3.0)*c*1e3 for c in cLx[0:10]]),np.max([(2.0/3.0)*c*1e3 for c in cLx[0:10]])])#np.max([(2.0/3.0)*c*1e3 for c in cLx[0:10]])])
# ax3.set_ylim([np.min([1/(b/100) for b in BWy]),np.max([1/(b/100) for b in BWy])])
# For professional typesetting, e.g. LaTeX, use .pgf or .pdf
# For raster graphics use the dpi argument. E.g. '[...].png", dpi=300)'
# plt.savefig("pyplot_multiple_y-axis.pdf", bbox_inches='tight')
# bbox_inches='tight': Try to strip excess whitespace
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html

plt.show()


RP = [1918.3606352512863, 1635.1844314938915, 1295.2590777259088, 1013.7937550497033, 844.4056094871311, 668.8689116075233, 619.0788953044856]
RP_AE = [296.3750517868526, 250.6401341759244, 196.04319849020442, 151.38667654215803, 124.92481788893019, 95.5527016582176, 88.43984218635508]


print(np.shape(sX))
print(np.shape(Ix))

fig, ax = plt.subplots(2,1)
ax1 = ax[0]
ax2 = ax1.twinx()
ax1.plot(sX,[(BWx/0.1)*i*eff for i in Ix[0:10]],'o',color='red',markerfacecolor='none')#,label='intensity')
ax2.plot(sX,[(2.0/3.0)*c*1e6 for c in cLx[0:10]],'o',color='blue',markerfacecolor='none')#,label='coherence length')
ax1.set_xlabel('Slit width [$\mu$m]',fontsize=FSIZE)
ax1.set_ylabel("$\it{\Phi}$ [ph/s]",fontsize=FSIZE)#"Intensity [ph/s/cm$^2$]")
ax2.set_ylabel('$\it{l_c} (\it{x})$ [$\mu$m]',fontsize=FSIZE)
ax1.spines['left'].set_color('red')
ax1.spines['right'].set_color('blue')

ax1.yaxis.label.set_color('red')
ax1.tick_params(axis='y', colors='red')
ax2.yaxis.label.set_color('blue')
ax2.tick_params(axis='y', colors='blue')
# for a in [ax1,ax2,ax3]:
    # a.set_xlim([0,350])
    # a.minorticks_on()
# ax1.set_ylim([np.min([(BWx/0.1)*i*0.004297207161730262 for i in Ix[0:10]]),np.max([(BWx/0.1)*i*0.004297207161730262 for i in Ix[0:10]])])
# ax2.set_ylim([np.min([(2.0/3.0)*c*1e3 for c in cLx[0:10]]),1.2])#np.max([(2.0/3.0)*c*1e3 for c in cLx[0:10]])])
# ax3.set_ylim([np.min([1/(b/100) for b in BWy]),np.max([1/(b/100) for b in BWy])])
#ax1.set_title('Horizontal')

# ax[1].plot(sybw,[1/(b/100) for b in BWy],'o', color='black', label="BW",markerfacecolor='none')
ax[1].errorbar(sybw,RP,yerr=RP_AE,fmt='o',color='black',label='BW',markerfacecolor='none')
ax[1].set_ylabel("Resolving Power",fontsize=FSIZE)
ax[1].set_xlabel('Slit height [$\mu$m]',fontsize=FSIZE)

ax2.vlines(200,ymin=-0.1,ymax=1250,colors='gray',linestyles=':')
# ax2.hlines(0.17,xmin=0,xmax=350,colors='gray',linestyles=':')
ax[1].hlines(1000,xmin=0,xmax=350,colors='gray',linestyles=':')

ax1.arrow(200,2.665e10,-25,0,color='red',length_includes_head=True,head_width=2e9,head_length=10)
ax2.arrow(200,170,25,0,color='blue',shape='full',length_includes_head=False,head_width=50,head_length=10)
# ax[1].arrow(200,1000,25,0,color='black')

ax1.text(210,abs((BWx/0.1)*eff*Ix[6])-0.35e10,str(round_sig(abs((BWx/0.1)*eff*Ix[6])*1e-10)) + 'x$10^{10}$ ph/s',color='red',fontname='serif',size=12)
ax2.text(210,250,str(int(round_sig((2.0/3.0)*cLx[6]*1e6))) + ' $\mu$m',color='blue',fontname='serif',size=12)
# ax[1].text(210,1050,str(int(round_sig(1/(BWy[3]/100),1))),color='black',fontname='serif',size=12)

ax2.text(-70,1250,'(a)',color='black',size=12)
ax2.text(-70,-300,'(b)',color='black',size=12)

print('\n hereherehere')
print([1/(b/100) for b in BWy])
print([(2.0/3.0)*c*1e6 for c in cLx[0:10]])
for a in [ax1,ax2,ax[1]]:
    a.set_xlim([20,355])
    a.minorticks_on()
# ax1.set_ylim([Imin,Imax])
ax2.set_ylim([np.min(CC)-50,np.max(CC)+50])
ax[1].set_ylim([BWmin-40,BWmax])

fig.tight_layout()
#plt.savefig('CvIhorizontal.jpg',dpi=1000)
# plt.show


# M = (abs(((BWx/0.1)*eff*Ix[9])-((BWx/0.1)*eff*Ix[0]))) / (325)

# ax1.plot(sX,[M*s for s in sX])
# plt.show
plt.show()



# print("here it is")
# plt.plot(sX,Ix[0:10],'o',markerfacecolor='none')
# plt.xlabel('SSA width [\u03BCm]') #icrons]')
# plt.ylabel("$I_G$ [ph/s/cm$^2$]")
# plt.legend(['max($I_G$) =' + str(Ix[10]*1e-12) + 'x10$^{12} ph/s/cm$^2$'])
# plt.show()

# print(str((2.0/3.0)*cLx[10]*1e3) + ' mm')

# print("and here again")
# print('Intensity gradient (m): ', M)
# print('Intensity at SSAx = 500 um: ', (M*500)*1e-13)

# print(np.shape(sX))
# print(np.shape(Ix))

# fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()
# ax1.plot(sX100,Ix100,'x:',color='red')#,label='intensity')
# ax2.plot(sX100,[c*1e3 for c in cLx100],'x:',color='blue')#,label='coherence length')
# ax2.plot(sX,[c*1e3 for c in cLx[0:10]],'x:',color='blue')#,label='coherence length')
# ax1.set_xlabel('Slit separation [microns]')
# ax1.set_ylabel('Intensity')
# ax2.set_ylabel('Coherence Length [mm]')
# ax1.spines['left'].set_color('red')
# ax1.spines['right'].set_color('blue')

# ax1.yaxis.label.set_color('red')
# ax1.tick_params(axis='y', colors='red')
# ax2.yaxis.label.set_color('blue')
# ax2.tick_params(axis='y', colors='blue')
# ax1.set_title('Horizontal (100 um)')
# fig.tight_layout()
# plt.show


# fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()
# ax1.plot(sY,Iy[0:8],'x:',color='red')#,label='intensity')
# ax2.plot(sY,[c*1e3 for c in cLy[0:8]],'x:',color='blue')#,label='coherence length')
# ax1.set_xlabel('Slit separation [microns]')
# ax1.set_ylabel('Intensity')
# ax2.set_ylabel('Coherence Length [mm]')
# ax1.spines['left'].set_color('red')
# ax1.spines['right'].set_color('blue')

# ax1.yaxis.label.set_color('red')
# ax1.tick_params(axis='y', colors='red')
# ax2.yaxis.label.set_color('blue')
# ax2.tick_params(axis='y', colors='blue')
# ax1.set_title('Vertical')
# fig.tight_layout()
# #plt.savefig('CvIvertical.jpg',dpi=1000)
# plt.show

# fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()
# ax1.plot(sX,Ix[0:10],'x:',color='red',label='intensity')
# ax1.plot(sY,Iy[0:8],'o:',color='red',label='intensity')
# ax2.plot(sY[0:8],[c*1e3 for c in cLy[0:8]],'x:',color='blue',label='Vertical')
# ax2.plot(sX,[c*1e3 for c in cLx[0:10]],'o:',color='blue', label='Horizontal')#,label='coherence length')
# ax1.set_xlabel('Slit separation [microns]')
# ax1.set_ylabel('Intensity')
# ax2.set_ylabel('Coherence Length [mm]')
# ax1.spines['left'].set_color('red')
# ax1.spines['right'].set_color('blue')

# ax1.yaxis.label.set_color('red')
# ax1.tick_params(axis='y', colors='red')
# ax2.yaxis.label.set_color('blue')
# ax2.tick_params(axis='y', colors='blue')
# #ax1.set_title('Vertical (100 um)')
# ax1.legend()
# ax2.legend()
# fig.tight_layout()
# plt.show