#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 14:39:23 2021

@author: jerome
"""
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib.font_manager import FontProperties
import plt_style

colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]

#import xl.runner as runner
experimentName = 'maskEfficiency18' #'maskEfficiency16' 'maskEfficiency20' 'maskEfficiency21'  'maskEfficiency18'
ran= range(1000, 1505,5)
numGratings = 1
independantV = 'Duty Cycle' #'Thickness' #'Duty Cycle'

dirPath = '/home/jerome/dev/experiments/' + experimentName + '/newdata/' #'/data/experiments/maskEfficiency21/data/'

save = False
saveBlair = False

# For efficiency vs duty cycle plots
dutyCycle = np.array([0.825, 0.75, 0.625, 0.6, 0.4, 0.5, 0.375, 0.25, 0.175])
idx = [0,     1,    2,     3,   5,   4,   6,    7,     8] #8,7,6,5,3,4,2,1,0
newDCycle = dutyCycle[idx]

# For efficiency vs mask thickness plots
maskThickness = list([t*1e-1 for t in ran])

if numGratings == 1:
        
    with open(dirPath + 'ZeroEfficiencyABS.pkl', 'rb') as s:
        e0 = pickle.load(s)
    with open(dirPath + 'ZeroEfficiencyREL.pkl', 'rb') as t:
        re0 = pickle.load(t)
    with open(dirPath + 'FirstEfficiencyABS.pkl', 'rb') as w:
        e1 = pickle.load(w)
    with open(dirPath + 'FirstEfficiencyREL.pkl', 'rb') as x:
        re1 = pickle.load(x)
        
    if independantV == 'Thickness':
        with open(dirPath + 'FirstEfficiencyABSneg.pkl', 'rb') as n:
            en1 = pickle.load(n)
        with open(dirPath + 'FirstEfficiencyRELneg.pkl', 'rb') as m:
            ren1 = pickle.load(m)
        with open(dirPath + '1g_diff1_Ni3Al_0.0067nm.pkl', 'rb') as bH:
            eBH = pickle.load(bH)
        with open(dirPath + '1g_diff1_1st_order_Ni_3Al_6.7nm_wl_thick_range_0.1_to299.0nm.pkl', 'rb') as bH1:
            eBH1 = pickle.load(bH1)
        with open(dirPath + '1g_diff1_1st_order_Ni3Al_nexafs_no_anneal_6.7nm_wl_thick_range_0.1_to299.0nm.pkl', 'rb') as bH2:
            eBH2 = pickle.load(bH2)
        with open(dirPath + '1g_diff1_1st_order_Ni3Al_nexafs_annealed_6.7nm_wl_thick_range_0.1_to299.0nm.pkl', 'rb') as bH3:
            eBH3 = pickle.load(bH3)
        with open(dirPath + '1g_diff1_0th_order_order_Ni_3Al_6.7nm_wl_thick_range_0.1_to299.0nm.pkl', 'rb') as bH4:
            eBH4 = pickle.load(bH4)
        with open(dirPath + '1g_diff1_0th_order_Ni3Al_nexafs_no_anneal_6.7nm_wl_thick_range_0.1_to299.0nm.pkl', 'rb') as bH5:
            eBH5 = pickle.load(bH5)
        with open(dirPath + '1g_diff1_0th_order_Ni3Al_nexafs_annealed_6.7nm_wl_thick_range_0.1_to299.0nm.pkl', 'rb') as bH6:
            eBH6 = pickle.load(bH6)
        
        
        xB = np.linspace(0,250,np.shape(eBH1)[0])
        xJ = np.linspace(100,150,len(ran))
        
        curves1, curves0 = [eBH1,eBH2,eBH3], [eBH4,eBH5,eBH6]
        curves=curves1 + curves0
        
        print("Shape of blair data: ", np.shape(eBH1))
        print("Shape of blair x: ", np.shape(xB))
        print("Shape of jerome data: ", np.shape(e1))
        print("Shape of jerome x: ", np.shape(xJ))
        
        # Plotting with Blairs data
        fig, ax = plt.subplots()
        thickRCWA = np.linspace(1, 300,len(eBH1))
    
        from scipy.signal import find_peaks
        # peakB, peakJ = find_peaks(eBH, height=(max(eBH))),find_peaks(e1, height=(max(e1)))
        # heightyB, heightyJ = peakB[1]['peak_heights'], peakJ[1]['peak_heights']#list of the heights of the peaks
        # peak_posB, peak_posJ = thickRCWA[int(peakB[0])], maskThickness[int(peakJ[0])] #list of the peaks positions
        peakPositions = []
        peakHeights = []
        zeroPositions = []
        zeroHeights= []
        for b in curves1:
            pB = find_peaks(b, height=max(b))
            print("")
            print("DEBUG: pB - ", pB)
            print("DEBUG: pB - ", pB[0])
            print("DEBUG: pB - ", pB[1])
            hB = pB[1]['peak_heights']
            pP = thickRCWA[int(pB[0])]
            
            peakPositions.append(pP)
            peakHeights.append(hB)
            
        for b0 in curves0:
            peakPositions.append(thickRCWA[np.argmin(b0[0:len(b0)-10])])
            peakHeights.append(min(b0[0:len(b0)-10]))
        
        peakJ = find_peaks(e1, height=max(e1))
        peakHeightsJ = peakJ[1]['peak_heights']
        peakPositionsJ = maskThickness[int(peakJ[0])]
        
        # peakB = [find_peaks(b, height=(max(b))) for b in curves]
        print("")
        print("peakPositions: ", peakPositions)
        # heightyB = [p[1]['peak_heights'] for p in peakB]
        print("")
        print("peakHeights: ", peakHeights)
        # peak_posB = [thickRCWA[int(p[0])] for p in peakB]
        print("")
        # print("peak_posB: ", peak_posB)`1`
        
        for sample,thick, name, color, pPos, pHeight in zip(curves1,
                                                            [thickRCWA,thickRCWA,thickRCWA],#thickRCWA,thickRCWA,thickRCWA,xJ],
                                                            ['m=1 (RCWA) - database','m=1 (RCWA) - NEXAFS (annealed)','m=1 (RCWA) - NEXAFS (no anneal)'],#'m=0 (RCWA) - database','m=0 (RCWA) - NEXAFS (annealed)','m=0 (RCWA) - NEXAFS (no anneal)'],
                                                            plt.rcParams['axes.prop_cycle'].by_key()['color'],
                                                            peakPositions[0:len(curves1)], peakHeights[0:len(curves1)]):#peakPositions[int(len(curves)/2)::],peakHeights[int(len(curves)/2)::]): #peakPositions[0:len(curves1)], peakHeights[0:len(curves1)]):
            ax.plot(thick,sample,color=color,label=name)
            ax.scatter(pPos,pHeight,color = color, s = 15, marker = 'D')

        plt.plot(maskThickness, e1, 'o', markersize=0.75, label="m=1 (SRW)",color=colours[3])
        ax.scatter(peakPositionsJ,peakHeightsJ,color=colours[3], s = 15, marker = 'D')
        # plt.plot(maskThickness, e0, 'o', markersize=0.75, label="m=0 (SRW)",color=colours[0])
        # ax.scatter(maskThickness[np.argmin(e0)],min(e0),color=colours[0], s = 15, marker = 'D')
        
        ax.set_xlabel('Thickness (nm)')
        ax.set_ylabel(r'$\mathcal{D}_1$') #'$\u03B7_m$') #r'$\mathcal{D}_1$')
        ax.set_xlim(90,160)#0,250) #90,160)#50,200)
        ax.set_ylim(0,0.2)
        ax.legend(title=r'Ni$_3$Al', fontsize=6)
        if saveBlair:
            fig.savefig(dirPath + 'RCWA_vs_SRWsingle_grating_m1CLOSE.png',dpi=2000)
            fig.savefig(dirPath + 'RCWA_vs_SRWsingle_grating_m1CLOSE.pdf')
        else:
            pass
        plt.show()
        
        # plt.clf()
        # plt.close()
        # plt.plot(xB,eBH, label='Blair data')
        # plt.plot(xJ,e1, label='Jerome data')
        # plt.legend()
        # plt.xlabel('Thickness [nm]')
        # plt.ylabel('$\u03B7_m$')
        # # plt.title("Blair Data")
        # plt.show()
            
        # plt.clf()
        # plt.close()
        # plt.plot(maskThickness, e0, label="m = 0")
        # plt.xlabel("Mask Thickness [m]")
        # plt.ylabel("Absolute Efficiency")
        # plt.legend()
        # # print("Saving Efficiency Plot to {}".format(pathE0))
        # # plt.savefig(pathE0)
        # plt.show()
        
        # plt.clf()
        # plt.close()
        # plt.plot(maskThickness, e1, label="m = +1")
        # plt.plot(maskThickness, en1, label="m = -1")
        # plt.xlabel("Mask Thickness [m]")
        # plt.ylabel("Abslute Efficiency")
        # plt.legend()
        # # print("Saving Efficiency Plot to {}".format(pathE1))
        # # plt.savefig(pathE1)
        # plt.show()
        
        plt.clf()
        plt.close()
        plt.plot(maskThickness, e1, label="m = +1")
        plt.plot(maskThickness, en1, label="m = -1")
        # plt.xlim(1200,1300)
        plt.xlabel("Mask Thickness [m]")
        plt.ylabel("Efficiency")
        plt.legend()
        # print("Saving Efficiency Plot (close-up) to {}".format(pathE1close))
        # plt.savefig(pathE1close)
        plt.show()
        
        # plt.clf()
        # plt.close()
        # plt.plot(maskThickness, re0, label="m = 0")
        # plt.xlabel("Mask Thickness [m]")
        # plt.ylabel("Relative Efficiency")
        # plt.legend()
        # # print("Saving Relative Efficiency Plot to {}".format(pathrE0))
        # # plt.savefig(pathrE0)
        # plt.show()
        
        
        plt.clf()
        plt.close()
        plt.plot(maskThickness, re1, label="m = +1")
        plt.plot(maskThickness, ren1, label="m = -1")
        plt.xlabel("Mask Thickness [m]")
        plt.ylabel("Relative Efficiency")
        plt.legend()
        # print("Saving Relative Efficiency Plot to {}".format(pathrE1))
        # plt.savefig(pathrE0)
        plt.show()
          
        import numpy as np
        e0minA = np.argmin(e0)
        e0minR = np.argmin(re0)
        e1maxA = np.argmax(e1)
        e1maxR = np.argmax(re1)
        
        
        plt.clf()
        plt.close()    
        fig,ax = plt.subplots() #Initiates plots
        color = next(ax._get_lines.prop_cycler)['color'] #gets colour so line and peak are the same colour
    
        # plt_style.findpeaks(maskThickness,re0,str('m=0'),ax,color)
    
        from scipy.signal import find_peaks
        peaks, peaksN = find_peaks(e1, height=(max(e1))), find_peaks(en1, height=(max(en1)))
        print(peaks[0])
        heighty, heightyN = peaks[1]['peak_heights'], peaksN[1]['peak_heights'] #list of the heights of the peaks
        print(heighty)
        print(maskThickness[int(peaks[0])])
        peak_pos, peak_posN = maskThickness[int(peaks[0])], maskThickness[int(peaksN[0])] #list of the peaks positions
    
        # ax.plot(maskThickness,e1, 'o', markersize=0.75, label="m=1",color = color)
        # ax.scatter(peak_pos,heighty,color = colours[1], s = 15, marker = 'D')
        
        ax.set_xlabel('Thickness [nm]')
        ax.set_ylabel('$\u03B7_m$')
        plt.plot(maskThickness, e0, 'o', markersize=2.75, linewidth=0.0, markerfacecolor='none', color=colours[0], label="m = 0")
        # plt.plot(maskThickness, e1, 'o', markersize=2.75, linewidth=0.0, markerfacecolor='none', color=colours[1], label="m = 1")
        plt.plot(maskThickness, en1, 'o', markersize=2.75, linewidth=0.0, markerfacecolor='none', color=colours[3], label="m = 1")
        ax.scatter(peak_posN,heightyN,color = colours[3], s = 15, marker = 'D')
        # # ax.plot(maskThickness, re0, label="m=0", color='b')
        # ax.scatter(maskThickness[e0minA],min(e0),color=colours[0], s = 15, marker = 'D')
        
        # plt.plot(maskThickness, re1, label="m=+1, rel")
        # ax.plot(maskThickness, ren1, label="m=-1, rel")
        # plt.xlabel("Mask Thickness [m]")
        # plt.ylabel(r'$\mathcal{D}_1$')
        # plt.ylabel("Efficiency")
        ax.legend()
        if save:
            plt.savefig(dirPath + 'SingleGrating_m0m1.pdf')
            plt.savefig(dirPath + 'SingleGrating_m0m1.png', dpi=2000)
        else:
            pass
        plt.show()
        

        eBmaxD = np.argmax(eBH1)
        eBmaxNn = np.argmax(eBH2)
        eBmaxNa = np.argmax(eBH3)
          
        print("Maximum absolute Efficiency (m=1): {}".format(max(e1)))
        print("Mask Thickness for maximum absolute efficiency (m=1): {}".format(maskThickness[e1maxA]))
        print("Minimum absolute Efficiency (m=0): {}".format(min(e0)))
        print("Mask Thickness for minimum absolute efficiency (m=0): {}".format(maskThickness[e0minA]))
        print("")
        print("Maximum RCWA efficiency (database): {}".format(max(eBH1)))
        print("Mask Thickness for maximum RCWA efficiency (database): {}".format(thickRCWA[eBmaxD]))
        print("Maximum RCWA efficiency (anneal): {}".format(max(eBH2)))
        print("Mask Thickness for maximum RCWA efficiency (anneal): {}".format(thickRCWA[eBmaxNa]))
        print("Maximum RCWA efficiency (no anneal): {}".format(max(eBH3)))
        print("Mask Thickness for maximum RCWA efficiency (no anneal): {}".format(thickRCWA[eBmaxNn]))



    
    if independantV == 'Duty Cycle':
        with open(dirPath + 'SecondEfficiencyABS.pkl', 'rb') as y:
            e2 = pickle.load(y)
        with open(dirPath + 'ThirdEfficiencyABS.pkl', 'rb') as p:
            e3 = pickle.load(p)
        with open(dirPath + 'FourthEfficiencyABS.pkl', 'rb') as q:
            e4 = pickle.load(q)
        with open(dirPath + 'SecondEfficiencyREL.pkl', 'rb') as r:
            re2 = pickle.load(r)
        with open(dirPath + 'ThirdEfficiencyREL.pkl', 'rb') as z:
            re3 = pickle.load(z)
        with open(dirPath + 'FourthEfficiencyREL.pkl', 'rb') as o:
            re4 = pickle.load(o)
            
        # with open(dirPath + 'diff1_Ni3Al_0th_order_thick_0.127_nm.pkl', 'rb') as bH0:
        #     eBH0 = pickle.load(bH0)
        with open(dirPath + 'diff1_Ni3Al_1th_order_thick_0.127_nm.pkl', 'rb') as bH1:
            eBH1 = pickle.load(bH1)
        with open(dirPath + 'diff1_Ni3Al_2th_order_thick_0.127_nm.pkl', 'rb') as bH2:
            eBH2 = pickle.load(bH2)
        with open(dirPath + 'diff1_Ni3Al_3th_order_thick_0.127_nm.pkl', 'rb') as bH3:
            eBH3 = pickle.load(bH3)
        with open(dirPath + 'diff1_Ni3Al_4th_order_thick_0.127_nm.pkl', 'rb') as bH4:
            eBH4 = pickle.load(bH4)
        
        
        
        
        xB = np.arange(0.001, 1, 0.001) 
        curvesB = [np.array(b) for b in [eBH1,eBH2,eBH3,eBH4]]
        # print(curvesB)
        curvesJ = [np.array(j)[idx] for j in [e1,e2,e3,e4]]
        
        labels = ['m=1','m=2','m=3','m=4']
        labelsB = ['m=1 (RCWA)','m=2 (RCWA)','m=3 (RCWA)','m=4 (RCWA)']
        labelsJ = ['m=1 (SRW)','m=2 (SRW)','m=3 (SRW)','m=4 (SRW)']
        
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        # for i, b in enumerate(curvesB):
        #     ax1.plot(xB,b, color=colours[i], label=labels[i])
        # for i, j in enumerate(curvesJ):
        #     ax2.plot(newDCycle,j, 'x', color=colours[i], label=labels[i])
        
        # for i in range(0,len(curvesB)-1):
        ax1.plot(xB,curvesB[0], color=colours[0], label=labels[0])
        ax1.plot(xB,curvesB[1], color=colours[1], label=labels[1])
        ax1.plot(xB,curvesB[2], color=colours[2], label=labels[2])
        ax2.plot(newDCycle,np.array(e1)[idx], 'x', color=colours[0], label=labels[0])
        ax2.plot(newDCycle,np.array(e2)[idx], 'x', color=colours[1], label=labels[1])
        ax2.plot(newDCycle,np.array(e3)[idx], 'x', color=colours[2], label=labels[2])
        ax2.plot(newDCycle,np.array(e4)[idx], 'x', color='white', label=None)
        
        ax1.set_xlabel("Duty Cycle (f)")
        ax1.set_ylabel(r'$\mathcal{D}_m$')#r'$\mathcal{D}_m$') #"$\u03B7_m$")
        ax1.set_yscale("log")
        ax2.set_yscale("log")
        ax1.set_ylim(1e-3,2e-1)
        ax1.legend(loc='upper left',title='RCWA', fontsize=8)
        ax2.legend(loc='upper right',title='SRW', fontsize=8)
        ax2.axes.get_yaxis().set_visible(False)
        if saveBlair:
            fig.savefig(dirPath + 'RCWA_vs_SRW_dutyCycle_m3CLOSE.png',dpi=2000)
            fig.savefig(dirPath + 'RCWA_vs_SRWs_dutyCycle_m3CLOSE.pdf')
        else:
            pass
        plt.show()
        
        # Eff_0 = []
        # Eff_1 = []
        # Eff_2 = []
        # Eff_3 = []
        # Eff_4 = []
        
        # oEff = []
        
        
        # period = np.array(range(1,200))
        # # print("period: {}".format(period))
        # slit = np.array(range(1,200))
        # order = range(1,5)
        # from utilMask import gratingEfficiencyHARV
        # for s in slit:
        #     E0 = [gratingEfficiencyHARV(0,1e-9*s,1e-9*p,G=0) for p in period]
        #     Eff_0.append(E0)
        #     E1 = [gratingEfficiencyHARV(1,1e-9*s,1e-9*p,G=0) for p in period]
        #     Eff_1.append(E1)
        #     E2 = [gratingEfficiencyHARV(2,1e-9*s,1e-9*p,G=0) for p in period]
        #     Eff_2.append(E2)
        #     E3 = [gratingEfficiencyHARV(3,1e-9*s,1e-9*p,G=0) for p in period]
        #     Eff_3.append(E3)
        #     E4 = [gratingEfficiencyHARV(4,1e-9*s,1e-9*p,G=0) for p in period]
        #     Eff_4.append(E4)
            
        # plt.plot(slit*0.005,Eff_0, label="m=0", color='b')
        # plt.plot(slit*0.005,Eff_1, label="m=1", color='g')
        # plt.plot(slit*0.005,Eff_2, label="m=2", color='y')
        # plt.plot(slit*0.005,Eff_3, label="m=3", color='r')
        # plt.plot(slit*0.005,Eff_4, label="m=4", color='m')
        # for i, j in enumerate(curvesJ):
        #     plt.plot(newDCycle,j, 'x', color=colours[i], label=labels[i])
        # # plt.title("\u03B7\u2098 vs W\u209B/W\u209A")
        # plt.yscale("log")
        # plt.ylim(1e-4,1)
        # plt.xlim(0.175,0.825)
        # plt.xlabel('Duty Cycle (f)')#"W\u209B/W\u209A")
        # plt.ylabel("\u03B7\u2098")
        # plt.legend()
        # plt.show()
        
        # plt.clf()
        # plt.close()
        # plt.plot(newDCycle, np.array(e0)[idx], label="m = 0", color='b')
        # plt.xlabel("Duty Cycle (f)")
        # plt.ylabel("Absolute Efficiency")
        # plt.legend()
        # # print("Saving Absolute Efficiency Plot to {}".format(pathE0))
        # # plt.savefig(pathE0)
        # plt.show()
        
        # plt.clf()
        # plt.close()
        # plt.plot(newDCycle, np.array(e1)[idx], label="m = +1", color='g')
        # # plt.plot(newDCycle, np.array(en1)[idx],'.', color='g')
        # plt.xlabel("Duty Cycle (f)")
        # plt.ylabel("Absolute Efficiency")
        # plt.legend()
        # # print("Saving Absolute Efficiency Plot to {}".format(pathE1))
        # # plt.savefig(pathE1)
        # plt.show()
        
        # plt.clf()
        # plt.close()
        # plt.plot(newDCycle, np.array(e2)[idx], label="m = +2", color='y')
        # # plt.plot(newDCycle, np.array(en2)[idx],'.', color='y')
        # plt.xlabel("Duty Cycle (f)")
        # plt.ylabel("Absolute Efficiency")
        # plt.legend()
        # # print("Saving Absolute Efficiency Plot to {}".format(pathE2))
        # # plt.savefig(pathE2)
        # plt.show()
        
        # plt.clf()
        # plt.close()
        # plt.plot(newDCycle, np.array(e3)[idx], label="m = +3", color='r')
        # # plt.plot(newDCycle, np.array(en3)[idx], '.', color='r')
        # plt.xlabel("Duty Cycle (f)")
        # plt.ylabel("Absolute Efficiency")
        # plt.legend()
        # # print("Saving Absolute Efficiency Plot to {}".format(pathE3))
        # # plt.savefig(pathE3)
        # plt.show()
        	
        # plt.clf()
        # plt.close()
        # plt.plot(newDCycle, np.array(e4)[idx], label="m = +4", color='m')
        # # plt.plot(newDCycle, np.array(en4)[idx], '.', color='m')
        # plt.xlabel("Duty Cycle (f)")
        # plt.ylabel("Absolute Efficiency")
        # plt.legend()
        # # print("Saving Absolute Efficiency Plot to {}".format(pathE4))
        # # plt.savefig(pathE4)
        # plt.show()
        	
        plt.clf()
        plt.close()
        plt.plot(newDCycle, np.array(e0)[idx], label="m=0", color='b')
        plt.plot(newDCycle, np.array(e0)[idx], '.', color='b')
        plt.plot(newDCycle, np.array(e1)[idx], label="m=1", color='g')
        plt.plot(newDCycle, np.array(e1)[idx], '.', color='g')
        #plt.plot(dutyCycle, en1, label="m=-1")
        plt.plot(newDCycle, np.array(e2)[idx], label="m=2", color='y')
        plt.plot(newDCycle, np.array(e2)[idx], '.', color='y')
        #plt.plot(newDCycle, en2[idx], label="m=-2")
        plt.plot(newDCycle, np.array(e3)[idx], label="m=3", color='r')
        plt.plot(newDCycle, np.array(e3)[idx], '.', color='r')
        #plt.plot(newDCycle, en3[idx], label="m=-3")
        plt.plot(newDCycle, np.array(e4)[idx], label="m=4", color='m')
        plt.plot(newDCycle, np.array(e4)[idx], '.', color='m')
        #plt.plot(newDCycle, en4[idx], label="m=-4")
        plt.xlabel("Duty Cycle (f)")
        plt.ylabel("$\u03B7_m$")
        plt.yscale("log")
        plt.ylim(1e-4,1e0)
        # plt.ylim(min(np.array(e4)[idx])-1e-4,1)
        plt.legend(loc='upper left')
        # print("Saving Absolute Efficiency Plot to {}".format(pathE))
        if save:
            plt.savefig(dirPath + 'DutyCycle_Efficiency.pdf')
            plt.savefig(dirPath + 'DutyCycle_Efficiency.png', dpi=2000)
        else:
            pass
        plt.show()
        
        # plt.clf()
        # plt.close()
        # plt.plot(newDCycle, np.array(re0)[idx], label="m = 0", color='b')
        # plt.xlabel("Duty Cycle (f)")
        # plt.ylabel("$\u03B7_m$")
        # plt.legend()
        # # print("Saving Relative Efficiency Plot to {}".format(pathrE0))
        # # plt.savefig(pathrE0)
        # plt.show()
        
        # plt.clf()
        # plt.close()
        # plt.plot(newDCycle, np.array(re1)[idx], label="m = +1", color='g')
        # # plt.plot(newDCycle, np.array(ren1)[idx],'.', color='g')
        # plt.xlabel("Duty Cycle (f)")
        # plt.ylabel("$\u03B7_m$")
        # plt.legend()
        # # print("Saving Relative Efficiency Plot to {}".format(pathrE1))
        # # plt.savefig(pathrE1)
        # plt.show()
        
        # plt.clf()
        # plt.close()
        # plt.plot(newDCycle, np.array(re2)[idx], label="m = +2", color='y')
        # # plt.plot(newDCycle, np.array(ren2)[idx],'.', color='y')
        # plt.xlabel("Duty Cycle (f)")
        # plt.ylabel("$\u03B7_m$")
        # plt.legend()
        # # print("Saving Relative Efficiency Plot to {}".format(pathrE2))
        # # plt.savefig(pathrE2)
        # plt.show()
        
        # plt.clf()
        # plt.close()
        # plt.plot(newDCycle, np.array(re3)[idx], label="m = +3", color='r')
        # # plt.plot(newDCycle, np.array(ren3)[idx], '.', color='r')
        # plt.xlabel("Duty Cycle (f)")
        # plt.ylabel("$\u03B7_m$")
        # plt.legend()
        # # print("Saving Relative Efficiency Plot to {}".format(pathrE3))
        # # plt.savefig(pathrE3)
        # plt.show()
        	
        # plt.clf()
        # plt.close()
        # plt.plot(newDCycle, np.array(re4)[idx], label="m = +4", color='m')
        # # plt.plot(newDCycle, np.array(ren4)[idx], '.', color='m')
        # plt.xlabel("Duty Cycle (f)")
        # plt.ylabel("$\u03B7_m$")
        # plt.legend()
        # # print("Saving Relative Efficiency Plot to {}".format(pathrE4))
        # # plt.savefig(pathrE4)
        # plt.show()
        	
        # plt.clf()
        # plt.close()
        # plt.plot(newDCycle, np.array(re0)[idx], label="m=0", color='b')
        # plt.plot(newDCycle, np.array(re0)[idx], '.', color='b')
        # plt.plot(newDCycle, np.array(re1)[idx], label="m=+1", color='g')
        # plt.plot(newDCycle, np.array(re1)[idx], '.', color='g')
        # plt.plot(newDCycle, np.array(re2)[idx], label="m=+2", color='y')
        # plt.plot(newDCycle, np.array(re2)[idx], '.', color='y')
        # plt.plot(newDCycle, np.array(re3)[idx], label="m=+3", color='r')
        # plt.plot(newDCycle, np.array(re3)[idx], '.', color='r')
        # plt.plot(newDCycle, np.array(re4)[idx], label="m=+4", color='m')
        # plt.plot(newDCycle, np.array(re4)[idx], '.', color='m')
        # plt.xlabel("Duty Cycle (f)")
        # plt.ylabel("$\u03B7_m$")
        # plt.yscale("log")
        # plt.ylim(1e-4,1e0)#min(np.array(re4)[idx])-1e-4,1)
        # plt.legend()
        # # print("Saving Relative Efficiency Plot to {}".format(pathrE))
        # # plt.savefig(pathrE)
        # plt.show()


elif numGratings == 2:    
    # Pickling results
    with open(dirPath + 'AIefficiencyABS.pkl', 'rb') as p:
        eAE = pickle.load(p)
    with open(dirPath + 'AIefficiencyREL.pkl', 'rb') as q:
        reAE = pickle.load(q)
    # with open(dirPath + 'AIefficiencyP.pkl', 'rb') as r:
    #     peAE = pickle.load(r)
    with open(dirPath + 'ZeroEfficiencyABSR.pkl', 'rb') as s:
        e0r = pickle.load(s)
    with open(dirPath + 'ZeroEfficiencyABSL.pkl', 'rb') as t:
        e0l = pickle.load(t)
    with open(dirPath + 'ZeroEfficiencyRELR.pkl', 'rb') as u:
        re0r = pickle.load(u)
    with open(dirPath + 'ZeroEfficiencyRELL.pkl', 'rb') as v:
        re0l = pickle.load(v)
    with open(dirPath + 'FirstEfficiencyABSR.pkl', 'rb') as w:
        e1 = pickle.load(w)
    with open(dirPath + 'FirstEfficiencyABSL.pkl', 'rb') as x:
        en1 = pickle.load(x)
    # with open(dirPath + 'FirstEfficiencyRELR.pkl', 'rb') as y:
    #     re1 = pickle.load(y)
    # with open(dirPath + 'FirstEfficiencyRELL.pkl', 'rb') as z:
    #     ren1 = pickle.load(z)
    with open(dirPath + '2g_diff1_1st_order_Ni_3Al_6.7nm_wl_thick_range_0.1_to299.0nm.pkl', 'rb') as bH1:
        eBH1 = pickle.load(bH1)
    with open(dirPath + '2g_diff1_1st_order_Ni3Al_nexafs_no_anneal_6.7nm_wl_thick_range_0.1_to299.0nm.pkl', 'rb') as bH2:
        eBH2 = pickle.load(bH2)
    with open(dirPath + '2g_diff1_1st_order_Ni3Al_nexafs_annealed_6.7nm_wl_thick_range_0.1_to299.0nm.pkl', 'rb') as bH3:
        eBH3 = pickle.load(bH3)
    with open(dirPath + '2g_diff1_0th_order_order_Ni_3Al_6.7nm_wl_thick_range_0.1_to299.0nm.pkl', 'rb') as bH4:
        eBH4 = pickle.load(bH4)
    with open(dirPath + '2g_diff1_0th_order_Ni3Al_nexafs_no_anneal_6.7nm_wl_thick_range_0.1_to299.0nm.pkl', 'rb') as bH5:
        eBH5 = pickle.load(bH5)
    with open(dirPath + '2g_diff1_0th_order_Ni3Al_nexafs_annealed_6.7nm_wl_thick_range_0.1_to299.0nm.pkl', 'rb') as bH6:
        eBH6 = pickle.load(bH6)   
    
    
    xB = np.linspace(0,250,np.shape(eBH1)[0])
    xJ = np.linspace(100,150,len(ran))
    
    _e1 = [2*a for a in e1]
    _e0l = [2*a for a in e0l]
    
    curves1, curves0 = [eBH1,eBH2,eBH3], [eBH4,eBH5,eBH6]
    curves=curves1 + curves0
    
    print("Shape of blair data: ", np.shape(eBH1))
    print("Shape of blair x: ", np.shape(xB))
    print("Shape of jerome data: ", np.shape(eAE))
    print("Shape of jerome x: ", np.shape(xJ))
    
    # Plotting with Blairs data
    fig, ax = plt.subplots()
    thickRCWA = np.linspace(1, 300,len(eBH1))

    from scipy.signal import find_peaks
    # peakB, peakJ = find_peaks(eBH, height=(max(eBH))),find_peaks(e1, height=(max(e1)))
    # heightyB, heightyJ = peakB[1]['peak_heights'], peakJ[1]['peak_heights']#list of the heights of the peaks
    # peak_posB, peak_posJ = thickRCWA[int(peakB[0])], maskThickness[int(peakJ[0])] #list of the peaks positions
    peakPositions = []
    peakHeights = []
    zeroPositions = []
    zeroHeights= []
    for b in curves1:
        pB = find_peaks(b, height=max(b))
        print("")
        print("DEBUG: pB - ", pB)
        print("DEBUG: pB - ", pB[0])
        print("DEBUG: pB - ", pB[1])
        hB = pB[1]['peak_heights']
        pP = thickRCWA[int(pB[0])]
        
        peakPositions.append(pP)
        peakHeights.append(hB)
        
    for b0 in curves0:
        peakPositions.append(thickRCWA[np.argmin(b0[0:len(b0)-10])])
        peakHeights.append(min(b0[0:len(b0)-10]))
    
    peakJ, peakJAE = find_peaks(_e1, height=max(_e1)),find_peaks(eAE, height=max(eAE))
    peakHeightsJ, peakHeightsJAE = peakJ[1]['peak_heights'],peakJAE[1]['peak_heights']
    peakPositionsJ, peakPositionsJAE = maskThickness[int(peakJ[0])],maskThickness[int(peakJAE[0])]
    
    # peakB = [find_peaks(b, height=(max(b))) for b in curves]
    print("")
    print("peakPositions: ", peakPositions)
    # heightyB = [p[1]['peak_heights'] for p in peakB]
    print("")
    print("peakHeights: ", peakHeights)
    # peak_posB = [thickRCWA[int(p[0])] for p in peakB]
    print("")
    # print("peak_posB: ", peak_posB)`1`
    
    for sample,thick, name, color, pPos, pHeight in zip(curves1,
                                                        [thickRCWA,thickRCWA,thickRCWA],#thickRCWA,thickRCWA,thickRCWA,xJ],
                                                        ['(RCWA) - database','(RCWA) - measurement ','m=1 (RCWA) - NEXAFS (no anneal)'],#'m=0 (RCWA) - database','m=0 (RCWA) - NEXAFS (annealed)','m=0 (RCWA) - NEXAFS (no anneal)'],
                                                        plt.rcParams['axes.prop_cycle'].by_key()['color'],
                                                        peakPositions[0:len(curves1)], peakHeights[0:len(curves1)]):#peakPositions, peakHeights):#peakPositions[int(len(curves)/2)::],peakHeights[int(len(curves)/2)::]): #peakPositions[0:len(curves1)], peakHeights[0:len(curves1)]):
        ax.plot(thick,sample/(33.75/13.75) ,color=color,label=name)
        ax.scatter(pPos,pHeight/(33.75/13.75) ,color = color, s = 15, marker = 'D')

    plt.plot(maskThickness, _e1, 'o', markersize=2.75, linewidth=0.0, markerfacecolor='none', label="(SRW) - Single Grating",color=colours[3])
    ax.scatter(peakPositionsJ,peakHeightsJ,color=colours[3], s = 15, marker = 'D')
    # plt.plot(maskThickness, eAE, 'o', markersize=2.75, linewidth=0.0, markerfacecolor='none', label="(SRW) - Aerial Image",color=colours[4])
    # ax.scatter(peakPositionsJAE,peakHeightsJAE,color=colours[4], s = 15, marker = 'D')
    # plt.plot(maskThickness, _e0l, 'o', markersize=0.75, label="m=0 (SRW)",color=colours[0])
    # ax.scatter(maskThickness[np.argmin(_e0l)],min(_e0l),color=colours[0], s = 15, marker = 'D')
    
    ax.set_xlabel('Thickness (nm)')
    ax.set_ylabel('$\u03B7_1$') #'$\u03B7_m$') #r'$\mathcal{D}_1$')
    ax.set_xlim(90,160)#0,250) #90,160)#50,200)
    # ax.set_ylim(0,0.3)
    ax.legend(title=r'Ni$_3$Al', fontsize=6)
    if saveBlair:
        fig.savefig(dirPath + 'RCWA_vs_SRWdouble_grating_m1CLOSE.png',dpi=2000)
        fig.savefig(dirPath + 'RCWA_vs_SRWdouble_grating_m1CLOSE.pdf')
    else:
        pass
    plt.show()
    
    # plt.clf()
    # plt.close()
    # plt.plot(maskThickness, eAE, label="Aerial Image")
    # plt.xlabel("Mask Thickness [m]")
    # plt.ylabel("Absolute Efficiency")
    # plt.legend()
    # # print("Saving Absolute Efficiency Plot to {}".format(pathEAE))
    # # plt.savefig(pathEAE)
    # plt.show()
    
    # plt.clf()
    # plt.close()
    # plt.plot(maskThickness, reAE, label="Aerial Image")
    # plt.xlabel("Mask Thickness [m]") 
    # plt.ylabel("$\u03B7_m$")
    # plt.legend()
    # # print("Saving Relative Efficiency Plot to {}".format(pathrEAE))
    # # plt.savefig(pathrEAE)
    # plt.show()
    
    # plt.clf()
    # plt.close()
    # plt.plot(maskThickness, peAE, label="Aerial Image")
    # plt.xlabel("Mask Thickness [m]") 
    # plt.ylabel("Self Efficiency")
    # plt.legend()
    # # print("Saving Self Efficiency Plot to {}".format(pathpEAE))
    # # plt.savefig(pathpEAE)
    # plt.show()
    
    # plt.clf()
    # plt.close()
    # plt.plot(maskThickness, e0r, label="m=0 (right)")
    # plt.plot(maskThickness, e0l, label="m=0 (left)")
    # plt.xlabel("Mask Thickness [m]")
    # plt.ylabel("Absolute Efficiency")
    # plt.legend()
    # # print("Saving Absolute Efficiency Plot to {}".format(pathE0))
    # # plt.savefig(pathE0)
    # plt.show()
    
    # plt.clf()  
    # plt.close()
    # plt.plot(maskThickness, re0r, label="m=0 (right)")
    # plt.plot(maskThickness, re0l, label="m=0 (left)")
    # plt.xlabel("Mask Thickness [m]")
    # plt.ylabel("$\u03B7_m$")
    # plt.legend()
    # # print("Saving Relative Efficiency Plot to {}".format(pathrE0))
    # # plt.savefig(pathrE0)
    # plt.show()
    
    
    plt.clf()
    plt.close()
    plt.plot(maskThickness, e1, label="m = +1")
    plt.plot(maskThickness, en1, label="m = -1")
    plt.xlabel("Mask Thickness [m]")
    plt.ylabel("$\u03B7_m$")
    plt.legend()
    # print("Saving Absolute Efficiency Plot to {}".format(pathE1))
    # plt.savefig(pathE1)
    plt.show()
    
    # plt.clf() 
    # plt.close()
    # plt.plot(maskThickness, re1, label="m = +1")
    # plt.plot(maskThickness, ren1, label="m = -1")
    # plt.xlabel("Mask Thickness [m]")
    # plt.ylabel("Relative Efficiency")
    # plt.legend()
    # # print("Saving Relative Efficiency Plot to {}".format(pathrE1))
    # # plt.savefig(pathrE1)
    # plt.show()
    	
    plt.clf()
    plt.close()
    # plt.plot(maskThickness, e0r, label="m=0 (right)")
    from scipy.signal import find_peaks
    peaksAE, peaks1 = find_peaks(eAE, height=(max(eAE))),find_peaks(_e1, height=(max(_e1)))
    heightyAE, heighty1 = peaksAE[1]['peak_heights'], peaks1[1]['peak_heights']#list of the heights of the peaks
    peak_posAE, peak_pos1 = maskThickness[int(peaksAE[0])], maskThickness[int(peaks1[0])] #list of the peaks positions

    plt.plot(maskThickness, eAE, 'o', markersize=2.75, linewidth=0.0, markerfacecolor='none', label="Aerial Image (m = 1)", color=colours[0])
    plt.scatter(peak_posAE,heightyAE,color = colours[0], s = 15, marker = 'D')
    plt.plot(maskThickness, _e0l, 'o', markersize=2.75, linewidth=0.0, markerfacecolor='none', label="m = 0", color=colours[1])
    plt.scatter(maskThickness[np.argmin(_e0l)],min(_e0l),color = colours[1], s = 15, marker = 'D')
    plt.plot(maskThickness, _e1, 'o', markersize=2.75, linewidth=0.0, markerfacecolor='none', label="m = 1", color=colours[3])
    plt.scatter(peak_pos1,heighty1,color = colours[3], s = 15, marker = 'D')
    # plt.plot(maskThickness, en1, label="m=-1")
    # plt.title("\u03B7")
    plt.xlabel("Mask Thickness [nm]")
    plt.ylabel("$\u03B7_m$")
    plt.legend()
    # print("Saving Absolute efficiency plot to: {}".format(pathAE))
    # plt.savefig(pathAE)
    if save:
        plt.savefig(dirPath + 'DoubleGrating_Efficiencym0m1AE.pdf')
        plt.savefig(dirPath + 'DoubleGrating_Efficiencym0m1AE.png', dpi=2000)
    else:
        pass
    plt.show()
    plt.clf()
    plt.close()
    
    plt.plot(maskThickness, re0r, label="m=0 (right)")
    plt.plot(maskThickness, re0l, label="m=0 (left)")
    plt.plot(maskThickness, reAE, label="Aerial Image")
    # plt.plot(maskThickness, re1, label="m=+1")
    # plt.plot(maskThickness, ren1, label="m=-1")
    plt.title("Relative Efficiency")
    plt.xlabel("Mask Thickness [m]")
    plt.ylabel("Efficiency")
    plt.legend()
    # print("Saving Relative Efficiency Plot to {}".format(pathRE))
    # plt.savefig(pathRE)
    plt.show()
    
    
    import numpy as np
    e0minA = np.argmin(e0r)
    e0minR = np.argmin(re0r)
    # e0minS = np.argmin(pe0r)
    em1maxA = np.argmax(e1)
    # em1maxR = np.argmax(re1)
    # em1maxS = np.argmax(pe1)
    e1maxA = np.argmax(eAE)
    e1maxR = np.argmax(reAE)
    # e1maxS = np.argmax(peAE)
    from scipy.signal import find_peaks
    peaks = find_peaks(eAE, height=(max(eAE)))
    print(peaks[0])
    heighty = peaks[1]['peak_heights'] #list of the heights of the peaks
    print(heighty)
    print(maskThickness[int(peaks[0])])
    peak_pos = maskThickness[int(peaks[0])] #list of the peaks positions
    
    plt.clf()
    plt.close()    
    fig,ax = plt.subplots() #Initiates plots
    color = next(ax._get_lines.prop_cycler)['color'] #gets colour so line and peak are the same colour
    ax.plot(maskThickness,eAE, 'o', markersize=0.75, label="Aerial Image",color = color)
    ax.scatter(peak_pos,heighty,color = color, s = 15, marker = 'D')
    
    ax.set_xlabel('Mask Thickness [nm]')
    ax.set_ylabel('$\u03B7_m$') #$\u03B7_m$
    
    # ax.plot(maskThickness, e0l, 'o', markersize=0.75, label="m=0", color='b')
    # ax.plot(maskThickness, e1, 'o', markersize=0.75, label="m=1", color= 'g') #color)#'g')    
    
    # peaks1 = find_peaks(e0l, height=(max(e0l)))
    
    # ax.scatter(maskThickness[e0minA],min(e0l),color = 'b', s = 15, marker = 'D')
    
    # peaks2 = find_peaks(e1, height=(max(e1)))
    # heighty2 = peaks2[1]['peak_heights'] #list of the heights of the peaks
    # peak_pos2 = maskThickness[int(peaks2[0])]
    # ax.scatter(peak_pos2,heighty2,color = 'g', s = 15, marker = 'D')
    # # plt.plot(maskThickness, e0, label="m=0, abs")
    # # plt.plot(maskThickness, e1, label="m=+1, abs")
    # # plt.plot(maskThickness, en1, label="m=-1, abs")
    # # ax.plot(maskThickness, re0, label="m=0", color=color)
    # # ax.scatter(maskThickness[e0minR],min(re0),color = color, s = 15, marker = 'D')
    
    # plt.plot(maskThickness, re1, label="m=+1, rel")
    # ax.plot(maskThickness, ren1, label="m=-1, rel")
    # plt.xlabel("Mask Thickness [m]")
    # plt.ylabel(r'$\mathcal{D}_1$')
    # plt.ylabel("Efficiency")
    ax.legend()
    if save:
        plt.savefig(dirPath + 'DoubleGrating_AerialImage.pdf')
        plt.savefig(dirPath + 'DoubleGrating_AerialImage.png', dpi=2000)
    else:
        pass
    plt.show()
    
    eBmaxD = np.argmax(eBH1)
    eBmaxNn = np.argmax(eBH2)
    eBmaxNa = np.argmax(eBH3)
    eBminD = np.argmin(eBH4[0:len(eBH4)-500])
    eBminNn = np.argmin(eBH5[0:len(eBH5)-500])
    eBminNa = np.argmin(eBH6[0:len(eBH6)-500])
    
    print(" ")
    print("Maximum absolute Efficiency (Aerial Image): {}".format(max(eAE)))
    print("Mask Thickness for maximum absolute efficiency (Aerial Image): {}".format(maskThickness[e1maxA]))
    print("Maximum absolute Efficiency (m=1): {}".format(max(e1)))
    print("Mask Thickness for maximum absolute efficiency (m=1): {}".format(maskThickness[em1maxA]))
    print("Minimum absolute Efficiency (m=0): {}".format(min(e0r)))
    print("Mask Thickness for minimum absolute efficiency (m=0): {}".format(maskThickness[e0minA]))
    print(" ")
    print("")
    print("Maximum RCWA efficiency (database): {}".format(max(eBH1)/(33.75/13.75)))
    print("Mask Thickness for maximum RCWA efficiency (database): {}".format(thickRCWA[eBmaxD]))
    print("Maximum RCWA efficiency (anneal): {}".format(max(eBH2)/(33.75/13.75)))
    print("Mask Thickness for maximum RCWA efficiency (anneal): {}".format(thickRCWA[eBmaxNa]))
    print("Maximum RCWA efficiency (no anneal): {}".format(max(eBH3)/(33.75/13.75)))
    print("Mask Thickness for maximum RCWA efficiency (no anneal): {}".format(thickRCWA[eBmaxNn]))
    print("")
    print("Minimum RCWA Efficiency (database): {}".format(min(eBH4)))
    print("Mask Thickness for minimum RCWA efficiency (database): {}".format(thickRCWA[eBminD]))
    print("Minimum RCWA Efficiency (anneal): {}".format(min(eBH6)))
    print("Mask Thickness for minimum RCWA efficiency (database): {}".format(thickRCWA[eBminNa]))
    print("Minimum RCWA Efficiency (no anneal): {}".format(min(eBH5)))
    print("Mask Thickness for minimum RCWA efficiency (database): {}".format(thickRCWA[eBminNn]))
    
    
    
