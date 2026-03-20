
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from skimage import io,  exposure, img_as_uint, img_as_float
from tqdm import tqdm
import os
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable

from usefulWavefield import counts2photonsPsPcm2, intensity2power, findBeamCenter
from FWarbValue import getFWatValue

from image_processing import sumImages,cropImage,IoverGrating
from usefulGrating import lateralShift 
from usefulWavefield import EtoWL, round_sig
from fractions import Fraction
    
# Location of the images
imageFolder = '/user/home/data/HarmonicContam/Detector_Comission_August_2023/ProcessedImages/SLSmask_all/'
darkFolder =  '/user/home/data/HarmonicContam/Detector_Comission_August_2023/ProcessedImages/darkfield/sls/'
savePath_dark =  None #'/user/home/data/HarmonicContam/Detector_Comission_August_2023/ProcessedImages/darkfield/sls/'
savePath_images = '/user/home/data/HarmonicContam/Detector_Comission_August_2023/ProcessedImages/SLSmask_all/'

energy_range = [185,185,185,185]
# [91.84, 100, 110, 120, 130, 140, 150, 160, 170, 180, 185.05, 190, 200, 210, 220, 230, 240, 250, 260, 270, 3*91.84, 280, 290]
# [290] #  
tl=0 
tr=1
ml=2
mr=3
bl=4
br=5

process = False
verbose = True
show = 200
gratings = [200] #[88,120,160,200]
positions = [tl] #[tl,ml,mr,bl]
save = False

if process:
    print("Averaging Darkfield Images...")
    sumImages(darkFolder,name='a_1_',sumNum=5000,imgType=".tif",average=True,
              darkfield=None,savePath=savePath_dark,show=True,verbose=True)
    print("Summing/Averaging Images...")
    ims,iTot,er = sumImages(imageFolder,name='a_1_',sumNum=4000,imgType=".tif",average=True,
                            darkfield=savePath_dark + str(4999) + '.tif',
                            savePath=savePath_images,hist=True,show=True,verbose=True)
    
    pEr = [e/i for e,i in zip(er,iTot)] # percentage error for summed intensities
    
    plt.errorbar(energy_range,iTot,yerr=er)
    plt.xlabel('Photon Energy [eV]')
    plt.ylabel('Total Intensity [counts]')
    plt.show()

names = ['cff1.4offset2','cff2offset0','cff2offset0_circpol','cff2offset0_doubleSLV']
inames = [savePath_images + str(i) + '.tif' for i in names]

# print([savePath_images + str(i) + '.tif' for i in inames])
# ims = [io.imread(i for i in inames)]
# image = io.imread(path + str(name) + str(i) + str(imgType))

# defining coordinates for grating centers (same for every image) (y,x)
p88 = [(256,99),(118,117),(141,87),(141,116),(164,86),(164,115)]   # tl=0,tr=1,ml=2,mr=3,bl=4,br=5
p120 =  [(268,68),(129,79),(152,57),(152,79),(175,57),(175,78)]    # tl,tr,ml,mr,bl,br
p160 =  [(279,45),(140,51),(163,34),(163,50),(187,34),(187,50)]    # tl,tr,ml,mr,bl,br
p200 =  [(291,26),(151,30),(175,17),(174,30),(198,16),(199,29)]    # tl,tr,ml,mr,bl,br

# defining grating sizes in pixels (y,x)
s88 = (14,14) #
s120 = (14,14) # (12,10)
s160 = (14,14) # (12,8)
s200 = (14,14) # (12,8)

try:
    x0_88,y0_88 = p88[positions[0]][1] - (s88[1]//2),  p88[positions[0]][0] - (s88[0]//2)
    x0_120,y0_120 = p120[positions[1]][1] - (s120[1]//2),  p120[positions[1]][0] - (s120[0]//2)
    x0_160,y0_160 = p160[positions[2]][1] - (s160[1]//2),  p160[positions[2]][0] - (s160[0]//2)
    x0_200,y0_200 = p200[positions[3]][1] - (s200[1]//2),  p200[positions[3]][0] - (s200[0]//2)
except:
    x0_88,y0_88 = p88[positions[0]][1] - (s88[1]//2),  p88[positions[0]][0] - (s88[0]//2)
    x0_120,y0_120 = p120[positions[0]][1] - (s120[1]//2),  p120[positions[0]][0] - (s120[0]//2)
    x0_160,y0_160 = p160[positions[0]][1] - (s160[1]//2),  p160[positions[0]][0] - (s160[0]//2)
    x0_200,y0_200 = p200[positions[0]][1] - (s200[1]//2),  p200[positions[0]][0] - (s200[0]//2)
    pass

# parameters that work for 1st harmonic
z = 0.655#366                   # propagation distance from grating in m
theta = 1.552                # correction factor for angle of grating
phi = 0.0000001

# # parameters that word for 5th harmonic
# z = 0.421                   # propagation distance from grating in m
# theta = np.deg2rad(90-1.1) #1.552                # correction factor for angle of grating
# phi = 0.0000001

N = [1,2,3,4,5]
M = [1,2,3,4,5]

Eff88 = [ [] for _ in range(np.max(N)*np.max(M))]
Er88 = [ [] for _ in range(np.max(N)*np.max(M))]
Eff120 = [ [] for _ in range(np.max(N)*np.max(M))]
Er120 = [ [] for _ in range(np.max(N)*np.max(M))]
Eff160 = [ [] for _ in range(np.max(N)*np.max(M))]
Er160 = [ [] for _ in range(np.max(N)*np.max(M))]
Eff200 = [ [] for _ in range(np.max(N)*np.max(M))]
Er200 = [ [] for _ in range(np.max(N)*np.max(M))]

NM = [ [] for _ in range(np.max(N)*np.max(M))]

for e,i in enumerate(inames):
    im = io.imread(i)
    rx,ry = np.shape(im)[1],np.shape(im)[0]
    wl = EtoWL(energy_range[e])
    print(" ")
    print(f"Energy:      {energy_range[e]}")
    print(f"Wavelength = {wl}")
    
    
    # Defining area of 0 order beam
    # 88 nm pitch grating
    I0_88 = im[y0_88:y0_88 + s88[0],x0_88:x0_88 + s88[1]]
    rect88_0 = patches.Rectangle((x0_88,y0_88),s88[1],s88[0], edgecolor='r', facecolor="none")
    I0sum88 = np.sum(I0_88)
    er0_88 = np.sqrt(I0sum88)/I0sum88  #1/(np.sqrt(I0sum88)*I0sum88)  
    
    # 120 nm pitch grating
    I0_120 = im[y0_120:y0_120 + s120[0],x0_120:x0_120 + s120[1]]
    rect120_0 = patches.Rectangle((x0_120,y0_120),s120[1],s120[0], edgecolor='b', facecolor="none")
    I0sum120 = np.sum(I0_120)
    er0_120 = np.sqrt(I0sum120)/I0sum120  #1/(np.sqrt(I0sum88)*I0sum88)
    
    # 160 nm pitch grating
    I0_160 = im[y0_160:y0_160 + s160[0],x0_160:x0_160 + s160[1]]
    rect160_0 = patches.Rectangle((x0_160,y0_160),s160[1],s160[0], edgecolor='g', facecolor="none")
    I0sum160 = np.sum(I0_160)
    er0_160 = np.sqrt(I0sum160)/I0sum160  #1/(np.sqrt(I0sum88)*I0sum88)
    
    # 200 nm pitch grating
    I0_200 = im[y0_200:y0_200 + s200[0],x0_200:x0_200 + s200[1]]
    rect200_0 = patches.Rectangle((x0_200,y0_200),s200[1],s200[0], edgecolor='y', facecolor="none")
    I0sum200 = np.sum(I0_200)
    er0_200 = np.sqrt(I0sum200)/I0sum200  #1/(np.sqrt(I0sum88)*I0sum88)
    
    
    numXticks = 5
    numYticks = 5
    dx = 11.0e-6
    dy = 11.0e-6
    ny, nx = np.shape(im)[0], np.shape(im)[1]
    sF = 1e3
    if energy_range[e] == 185.05:
        # plt.imshow(im[:,::250],vmin=0,vmax=np.max(im[:,::250]),aspect='auto')
        
        im0 = im[100:220,0:150]
        im1 = im[100:220,250::]
        ny0, nx0 = np.shape(im0)[0], np.shape(im0)[1]
        ny1, nx1 = np.shape(im1)[0], np.shape(im1)[1]
        
        plt.imshow(im0,aspect='auto')
        plt.yticks([int((ny0-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],[round_sig(ny0*dy*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=10)
        plt.xticks([int((nx0-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],[round_sig(nx0*dx*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=10)
        plt.xlabel("x [mm]")
        plt.ylabel("y [mm]")
        plt.colorbar()
        plt.show()
        
        plt.imshow(im1,vmin=0,vmax=np.max(im[:,250::]),aspect='auto')
        plt.yticks([int((ny1-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],[round_sig(ny1*dy*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=10)
        plt.xticks([int((nx1-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],[round_sig(nx1*dx*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=10)
        plt.xlabel("x [mm]")
        plt.ylabel("y [mm]")
        plt.colorbar()
        plt.show()
        plt.imshow(im,vmin=0,vmax=np.max(im[:,250::]),aspect='auto')
        plt.yticks([int((ny-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],[round_sig(ny*dy*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=10)
        plt.xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],[round_sig(nx*dx*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=10)
        plt.xlabel("x [mm]")
        plt.ylabel("y [mm]")
        plt.colorbar()
        plt.show()
    
    if show:
        # Setting up plot
        fig, ax = plt.subplot_mosaic("ABCDE;FGHIJ;KLMNO;PQRST;UVWXY;ZZZZZ;ZZZZZ;ZZZZZ",figsize=(8,8))#STUVWX;YZabcd;eeeeee;eeeeee;eeeeee")
        axl = ["A","B","C","D","E",
               "F","G","H","I","J",
               "K","L","M","N","O",
               "P","Q","R","S","T",
               "U","V","W","X","Y"
               ]
               # "S","T","Z","V","W","X",
               # "Y","Z","a","b","c","d"]
        # i1 = ax["A"].imshow(I0_88)
        i4 = ax["Z"].imshow(im,vmin=0,vmax=np.max(im[:,250::]),aspect=2)
        # ax["Z"].set_xlim(250,rx)
        # ax["Z"].set_ylim(250,100)
        ax["Z"].set_title(f"E = {energy_range[e]} eV, {names[e]}")        
        ax["Z"].set_yticks([int((ny-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)])
        ax["Z"].set_yticklabels([round_sig(ny*dy*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=10)
        ax["Z"].set_xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])
        ax["Z"].set_xticklabels([round_sig(nx*dx*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=10)
        ax["Z"].set_xlabel("x [mm]")
        ax["Z"].set_ylabel("y [mm]")
        ax["Z"].add_patch(rect88_0)
        ax["Z"].add_patch(rect120_0)
        ax["Z"].add_patch(rect160_0)
        ax["Z"].add_patch(rect200_0)
    
    # Finding positions of diffracted orders
    nm = 0
    for n in N:
        for m in M:
            if e ==0:
                NM[nm].append([n,m])
            # 88 nm pitch grating
            x_88_m = lateralShift(wl/n,p=88e-9,m=m,z=z,theta_i=phi)
            x_88 = x_88_m/11.0e-6
            y_88 = x_88/np.tan(theta)
            
            # 120 nm pitch grating
            x_120_m = lateralShift(wl/n,p=120e-9,m=m,z=z,theta_i=phi)
            x_120 = x_120_m/11.0e-6
            y_120 = x_120/np.tan(theta)
            
            # 160 nm pitch grating
            x_160_m = lateralShift(wl/n,p=160e-9,m=m,z=z,theta_i=phi)
            x_160 = x_160_m/11.0e-6
            y_160 = x_160/np.tan(theta)
            
            # 200 nm pitch grating
            x_200_m = lateralShift(wl/n,p=200e-9,m=m,z=z,theta_i=phi)
            x_200 = x_200_m/11.0e-6
            y_200 = x_200/np.tan(theta)
            
            if int(x_88+x0_88) <= rx and int(x_88+x0_88) >= 235:
                good88 = True
            else:
                good88 = False
                
            if int(x_120+x0_120) <= rx and int(x_120+x0_120) >= 235:
                good120 = True
            else:
                good120 = False
                
            if int(x_160+x0_160) <= rx and int(x_160+x0_160) >= 235:
                good160 = True
            else:
                good160 = False
                
            if int(x_200+x0_200) <= rx and int(x_200+x0_200) >= 235:
                good200 = True
            else:
                good200 = False
            
            if verbose:
                if 88 in gratings:
                    if good88:
                        print(" --------  p = 88 nm  ----------")
                        print(f"Lateral shift of {m} order beam from {n} harmonic [m]:              {x_88_m}")
                        print(f"Lateral shift of {m} order beam from {n} harmonic [pixels]:         {x_88}")
                        print(f"Position of {m} order beam from {n} harmonic ((x0,x1),(y0,y1)):     {((int(x_88+x0_88),int(x_88+x0_88+s88[1])),(int(y0_88+y_88),int(y0_88+y_88+s88[0])))}")
                
                if 120 in gratings:
                    if good120:
                        print(" --------  p = 120 nm  ----------")
                        print(f"Lateral shift of {m} order beam from {n} harmonic [m]:              {x_120_m}")
                        print(f"Lateral shift of {m} order beam from {n} harmonic [pixels]:         {x_120}")
                        print(f"Position of {m} order beam from {n} harmonic ((x0,x1),(y0,y1)):     {((int(x_120+x0_120),int(x_120+x0_120+s120[1])),(int(y0_120+y_120),int(y0_120+y_120+s120[0])))}")
                    
                if 160 in gratings:
                    if good160:
                        print(" --------  p = 160 nm  ----------")
                        print(f"Lateral shift of {m} order beam from {n} harmonic [m]:              {x_160_m}")
                        print(f"Lateral shift of {m} order beam from {n} harmonic [pixels]:         {x_160}")
                        print(f"Position of {m} order beam from {n} harmonic ((x0,x1),(y0,y1)):     {((int(x_160+x0_160),int(x_160+x0_160+s160[1])),(int(y0_160+y_160),int(y0_160+y_160+s160[0])))}")
            
                if 200 in gratings:
                    if good200:
                        print(" --------  p = 200 nm  ----------")
                        print(f"Lateral shift of {m} order beam from {n} harmonic [m]:              {x_200_m}")
                        print(f"Lateral shift of {m} order beam from {n} harmonic [pixels]:         {x_200}")
                        print(f"Position of {m} order beam from {n} harmonic ((x0,x1),(y0,y1)):     {((int(x_200+x0_200),int(x_200+x0_200+s200[1])),(int(y0_200+y_200),int(y0_200+y_200+s200[0])))}")
            
            # Defining area of diffracted beam
            I_88 = im[int(y0_88 + y_88):int(y0_88 + y_88 + s88[0]),int(x0_88 + x_88):int(x0_88 + x_88 + s88[1])]
            I_120 = im[int(y0_120 + y_120):int(y0_120 + y_120 + s120[0]),int(x0_120 + x_120):int(x0_120 + x_120 + s120[1])]
            I_160 = im[int(y0_160 + y_160):int(y0_160 + y_160 + s160[0]),int(x0_160 + x_160):int(x0_160 + x_160 + s160[1])]
            I_200 = im[int(y0_200 + y_200):int(y0_200 + y_200 + s200[0]),int(x0_200 + x_200):int(x0_200 + x_200 + s200[1])]
            # Defining area for background intensity subtraction
            Ib_88 = im[325:int(325+s88[0]),int(x0_88 + x_88):int(x0_88 + x_88 + s88[1])]
            Ib_120 = im[325:int(325+s120[0]),int(x0_120 + x_120):int(x0_120 + x_120 + s120[1])]
            Ib_160 = im[325:int(325+s160[0]),int(x0_160 + x_160):int(x0_160 + x_160 + s160[1])]
            Ib_200 = im[325:int(325+s200[0]),int(x0_200 + x_200):int(x0_200 + x_200 + s200[1])]
            
            rect_88 = patches.Rectangle((int(x0_88+x_88),int(y0_88+y_88)),s88[1],s88[0], edgecolor='r', facecolor="none")
            rect_120 = patches.Rectangle((int(x0_120+x_120),int(y0_120+y_120)),s120[1],s120[0], edgecolor='b', facecolor="none")
            rect_160 = patches.Rectangle((int(x0_160+x_160),int(y0_160+y_160)),s160[1],s160[0], edgecolor='g', facecolor="none")
            rect_200 = patches.Rectangle((int(x0_200+x_200),int(y0_200+y_200)),s200[1],s200[0], edgecolor='y', facecolor="none")
            # print(" ")
            # print(f"\"{axl[nm]}\"")
            # print(nm)
            # print(" ")
            
            # divider = make_axes_locatable(ax[axl[nm]])
            # cax = divider.append_axes("right",size="3%",pad=0.05)
            # plt.colorbar(imI,cax=cax)
            if show:
                if 88 in gratings:
                    if good88 and n == Fraction(n,m).numerator:
                        ax["Z"].add_patch(rect_88)
                        ax["Z"].text(int(x_88+x0_88),int(y0_88+y_88),f'{(n,m)}',color='r',fontsize=8)
                if 120 in gratings:
                    if good120 and n == Fraction(n,m).numerator:
                        ax["Z"].add_patch(rect_120)
                        ax["Z"].text(int(x_120+x0_120),int(y0_120+y_120),f'{(n,m)}',color='b',fontsize=8)
                if 160 in gratings:
                    if good160 and n == Fraction(n,m).numerator:
                        ax["Z"].add_patch(rect_160)
                        ax["Z"].text(int(x_160+x0_160),int(y0_160+y_160),f'{(n,m)}',color='g',fontsize=8)
                if 200 in gratings:
                    if  good200 and n == Fraction(n,m).numerator:
                        ax["Z"].add_patch(rect_200)
                        ax["Z"].text(int(x_200+x0_200),int(y0_200+y_200),f'{(n,m)}',color='y',fontsize=8)
                    
                if show == 88:
                    if good88 == False or n != Fraction(n,m).numerator:
                        fig.delaxes(ax[axl[nm]])
                        ax[axl[nm]].set_axis_off()
                        ax[axl[nm]].set_visible(False)
                    else:
                        imI = ax[axl[nm]].imshow(I_88)
                        ax[axl[nm]].set_title(f"$I_{n,m}$",fontsize=8)
                        ax[axl[nm]].get_xaxis().set_visible(False)
                        ax[axl[nm]].get_yaxis().set_visible(False)
                elif show == 120:
                    if good120 == False or n != Fraction(n,m).numerator:
                        fig.delaxes(ax[axl[nm]])
                        ax[axl[nm]].set_axis_off()
                        ax[axl[nm]].set_visible(False)
                    else:
                        imI = ax[axl[nm]].imshow(I_120)
                        ax[axl[nm]].set_title(f"$I_{n,m}$",fontsize=8)
                        ax[axl[nm]].get_xaxis().set_visible(False)
                        ax[axl[nm]].get_yaxis().set_visible(False)
                elif show == 160:
                    if good160 == False or n != Fraction(n,m).numerator:
                        fig.delaxes(ax[axl[nm]])
                        ax[axl[nm]].set_axis_off()
                        ax[axl[nm]].set_visible(False)
                    else:
                        imI = ax[axl[nm]].imshow(I_160)
                        ax[axl[nm]].set_title(f"$I_{n,m}$",fontsize=8)
                        ax[axl[nm]].get_xaxis().set_visible(False)
                        ax[axl[nm]].get_yaxis().set_visible(False)
                elif show == 200:
                    if good200 == False or n != Fraction(n,m).numerator:
                        fig.delaxes(ax[axl[nm]])
                        ax[axl[nm]].set_axis_off()
                        ax[axl[nm]].set_visible(False)
                    else:
                        imI = ax[axl[nm]].imshow(I_200)
                        ax[axl[nm]].set_title(f"I_{n,m}",fontsize=8)
                        ax[axl[nm]].get_xaxis().set_visible(False)
                        ax[axl[nm]].get_yaxis().set_visible(False)
                
            
            Isum88 = (np.sum(I_88) - np.sum(Ib_88))
            Isum120 = (np.sum(I_120) - np.sum(Ib_120))
            Isum160 = (np.sum(I_160) - np.sum(Ib_160))
            Isum200 = (np.sum(I_200) - np.sum(Ib_200))
            
            E_88 = Isum88/I0sum88
            erI_88 = np.sqrt(Isum88)/Isum88
            erE_88 = np.sqrt((er0_88**2) + (erI_88**2)) * E_88
            E_120 = Isum120/I0sum120
            erI_120 = np.sqrt(Isum120)/Isum120
            erE_120 = np.sqrt((er0_120**2) + (erI_120**2)) * E_120
            E_160 = Isum160/I0sum160
            erI_160 = np.sqrt(Isum160)/Isum160
            erE_160 = np.sqrt((er0_160**2) + (erI_160**2)) * E_160
            E_200 = Isum200/I0sum200
            erI_200 = np.sqrt(Isum200)/Isum200
            erE_200 = np.sqrt((er0_200**2) + (erI_200**2)) * E_200
            
            if E_88 == 0:
                Eff88[nm].append(np.nan)
                Er88[nm].append(np.nan)
            elif E_88 >= 1:
                Eff88[nm].append(np.nan)
                Er88[nm].append(np.nan)
            elif good88:
                Eff88[nm].append(E_88)
                Er88[nm].append(erE_88)
            else:
                Eff88[nm].append(np.nan)
                Er88[nm].append(np.nan)
                
            if E_120 == 0:
                Eff120[nm].append(np.nan)
                Er120[nm].append(np.nan)
            elif E_120 >= 1:
                Eff120[nm].append(np.nan)
                Er120[nm].append(np.nan)
            elif good120:
                Eff120[nm].append(E_120)
                Er120[nm].append(erE_120)
            else:
                Eff120[nm].append(np.nan)
                Er120[nm].append(np.nan)
                
                
            if E_160 == 0:
                Eff160[nm].append(np.nan)
                Er160[nm].append(np.nan)
            elif E_160 >= 1:
                Eff160[nm].append(np.nan)
                Er160[nm].append(np.nan)
            elif good160:
                Eff160[nm].append(E_160)
                Er160[nm].append(erE_160)
            else:
                Eff160[nm].append(np.nan)
                Er160[nm].append(np.nan)
                
                
            if E_200 == 0:
                Eff200[nm].append(np.nan)
                Er200[nm].append(np.nan)
            elif E_200 >= 1:
                Eff200[nm].append(np.nan)
                Er200[nm].append(np.nan)
            elif good200:
                Eff200[nm].append(E_200)
                Er200[nm].append(erE_200)
            else:
                Eff200[nm].append(np.nan)
                Er200[nm].append(np.nan)
                
            
                
            # NM[nm].append((n,m))
            # print(nm)
            # print(n,m)
            nm+=1
    if show:
        fig.tight_layout()
        plt.show()
        
        
# Plotting efficiency for 88 nm pitch grating
for i88,e88,nm in zip(Eff88,Er88,NM):
    if np.isnan(i88).all():
        pass
    elif nm[0][0] != Fraction(nm[0][0],nm[0][1]).numerator:
        pass
    else:
        plt.errorbar(names,[_i*100 for _i in i88],yerr=[_e*100 for _e in e88],fmt='.:', 
                     label="$\eta^{88}$" + str((nm[0][0],nm[0][1])))

# plt.xlabel("Photon Energy [eV]")
plt.ylabel("$\eta_{n,m}$ [%]")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3),
           ncol=4, fancybox=True, shadow=True)
if save:
    plt.savefig('/user/home/data/DE_processed/plots/p88_' + str(positions[0]) + '.png')
plt.show()

# Plotting efficiency for 120 nm pitch grating
for i120,e120,nm in zip(Eff120,Er120,NM):
    if np.isnan(i120).all():
        pass
    elif nm[0][0] != Fraction(nm[0][0],nm[0][1]).numerator:
        pass
    else:
        plt.errorbar(names,[_i*100 for _i in i120],yerr=[_e*100 for _e in e120],fmt='.:', 
                     label="$\eta^{120}$" + str((nm[0][0],nm[0][1])))

# plt.xlabel("Photon Energy [eV]")
plt.ylabel("$\eta_{n,m}$ [%]")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3),
           ncol=4, fancybox=True, shadow=True)
if save:
    plt.savefig('/user/home/data/DE_processed/plots/p120_' + str(positions[0]) + '.png')
plt.show()


# Plotting efficiency for 160 nm pitch grating
for i160,e160,nm in zip(Eff160,Er160,NM):
    if np.isnan(i160).all():
        pass
    elif nm[0][0] != Fraction(nm[0][0],nm[0][1]).numerator:
        pass
    else:
        plt.errorbar(names,[_i*100 for _i in i160],yerr=[_e*100 for _e in e160],fmt='.:', 
                     label="$\eta^{160}$" + str((nm[0][0],nm[0][1])))

# plt.xlabel("Photon Energy [eV]")
plt.ylabel("$\eta_{n,m}$ [%]")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3),
           ncol=4, fancybox=True, shadow=True)
if save:
    plt.savefig('/user/home/data/DE_processed/plots/p160_' + str(positions[0]) + '.png')
plt.show()


# Plotting efficiency for 120 nm pitch grating
for i200,e200,nm in zip(Eff200,Er200,NM):
    if np.isnan(i200).all():
        pass
    elif nm[0][0] != Fraction(nm[0][0],nm[0][1]).numerator:
        pass
    else:
        plt.errorbar(names,[_i*100 for _i in i200],yerr=[_e*100 for _e in e200],fmt='.:', 
                     label="$\eta^{200}$" + str((nm[0][0],nm[0][1])))

# plt.xlabel("Photon Energy [eV]")
plt.ylabel("$\eta_{n,m}$ [%]")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3),
           ncol=4, fancybox=True, shadow=True)
if save:
    plt.savefig('/user/home/data/DE_processed/plots/p200_' + str(positions[0]) + '.png')
plt.show()
            
    # x1_88_m = lateralShift(wl,p=88e-9,m=1,z=z)
    # x1_88 = x1_88_m/11e-6
    # y1_88 = x1_88/np.tan(theta)
    
    # x31_88_m = lateralShift(wl/3,p=88e-9,m=1,z=z)
    # x31_88 = x31_88_m/11e-6
    # y31_88 = x31_88/np.tan(theta)
    
    # print(f"Lateral shift of 1st order beam (fundamental) from 88 nm pitch grating [m]:       {x1_88_m}")
    # print(f"Lateral shift of 1st order beam (fundamental) from 88 nm pitch grating [pixels]:  {x1_88}")
    # print(f"Position of 1st order beam (fundamental) ((x0,x1),(y0,y1)):                       {((int(x1_88+x0_88),int(x1_88+x0_88+s88[1])),(int(y0_88+y1_88),int(y0_88+y1_88+s88[0])))}")
    # print(f"Lateral shift of 1st order beam (n=3) from 88 nm pitch grating [m]:       {x31_88_m}")
    # print(f"Lateral shift of 1st order beam (n=3) from 88 nm pitch grating [pixels]:  {x31_88}")
    # print(f"Position of 1st order beam (n=3) ((x0,x1),(y0,y1)):                       {((int(x31_88+x0_88),int(x31_88+x0_88+s88[1])),(int(y0_88+y31_88),int(y0_88+y31_88+s88[0])))}")
    
    # # Defining area of diffracted >0 order beams
    # I1_88 = im[int(y0_88 + y1_88):int(y0_88 + y1_88 + s88[0]),int(x0_88 + x1_88):int(x0_88 + x1_88 + s88[1])]
    # I31_88 = im[int(y0_88 + y31_88):int(y0_88 + y31_88 + s88[0]),int(x0_88 + x31_88):int(x0_88 + x31_88 + s88[1])]
    # # Defining area for background intensity subtraction and subtracting from >0 order beam intensity
    # Ib1_88 = im[325:int(325+s88[0]),int(x0_88 + x1_88):int(x0_88 + x1_88 + s88[1])]
    # Ib31_88 = im[325:int(325+s88[0]),int(x0_88 + x31_88):int(x0_88 + x31_88 + s88[1])]
    
    # I1_88 = I1_88 - Ib1_88
    # I1_88[I1_88 < 1] = 0
    # I31_88 = I31_88 - Ib31_88
    # I31_88[I31_88 < 1] = 0
    
    # rect_0 = patches.Rectangle((x0_88,y0_88),s88[1],s88[0], edgecolor='r', facecolor="none")
    # rect_1 = patches.Rectangle((int(x0_88+x1_88),int(y0_88+y1_88)),s88[1],s88[0], edgecolor='r', facecolor="none")
    # rect_2 = patches.Rectangle((int(x0_88+x31_88),int(y0_88+y31_88)),s88[1],s88[0], edgecolor='r', facecolor="none")
    # fig, ax = plt.subplot_mosaic("ABC;DDD")
    # i1 = ax["A"].imshow(I0_88)
    # ax["A"].set_title('$I_0$')
    # i2 = ax["B"].imshow(I1_88)
    # ax["B"].set_title('$I_1$')
    # i3 = ax["C"].imshow(I31_88)
    # ax["C"].set_title('I_{3,1}')
    # i4 = ax["D"].imshow(im)
    # ax["D"].set_title(f"E = {energy_range[e]} eV")
    # ax["D"].add_patch(rect_0)
    # ax["D"].add_patch(rect_1)
    # ax["D"].add_patch(rect_2)
    
    # ims = [i1,i2,i3,i4]
    # axl = ["A","B","C","D"]
    # for en, m in enumerate(ims):
    #     divider = make_axes_locatable(ax[axl[en]])
    #     cax = divider.append_axes("right", size="3%",pad=0.05)
    #     plt.colorbar(m,cax=cax)
    # fig.tight_layout()
    # plt.show()
    
    # # Calculating efficiency of each diffracted order (with background subtraction)
    # I0sum88 = np.sum(I0_88)
    # I1sum88 = (np.sum(I1_88) - np.sum(Ib1_88)) # np.sum(I1_88) #(np.sum(I1_88) - np.sum(Ib1_88))
    # I31sum88 = (np.sum(I31_88) - np.sum(Ib31_88)) # np.sum(I31_88) #(np.sum(I31_88) - np.sum(Ib31_88))
    
    # E1_88 = (I1sum88) / I0sum88
    # E31_88 = (I31sum88) / I0sum88
    # er0_88 = np.sqrt(I0sum88)/I0sum88  #1/(np.sqrt(I0sum88)*I0sum88)  
    # er1_88 = np.sqrt(I1sum88)/np.sum(I1sum88)  #1/(np.sqrt(I1sum88)*np.sum(I1sum88)) #
    # er31_88 = np.sqrt(I31sum88)/np.sum(I31sum88)  #1/(np.sqrt(I31sum88)*np.sum(I31sum88)) #
    # erE1_88 = np.sqrt((er0_88**2) + (er1_88**2)) * E1_88
    # erE31_88 = np.sqrt((er0_88**2) + (er31_88**2)) * E31_88
    
    # print(f"Total intensity (0):                                    {I0sum88}")
    # print(f"Total intensity (1) (before background sub):            {np.sum(I1_88)}")
    # print(f"Total intensity (1) (after backgroubd sub):             {I1sum88}")
    # print(f"Total intensity (b1):                                   {np.sum(Ib1_88)}")
    # print(f"Total intensity (3,1) (before backgrounf sub):          {np.sum(I31_88)}")
    # print(f"Total intensity (3,1) (after background sub):           {I31sum88}")
    # print(f"Total intensity (b31):                                  {np.sum(Ib31_88)}")
    # print(f"Efficiency (1,1):               {E1_88}")
    # print(f"Efficiency (3,1):               {E31_88}")
    
    # if E1_88 == 0:
    #     Eff1.append(np.nan)
    #     Er1.append(np.nan)
    # else:
    #     Eff1.append(E1_88)
    #     Er1.append(erE1_88)
        
    # if E31_88 == 0:
    #     Eff31.append(np.nan)
    #     Er31.append(np.nan)
    # elif E31_88 >= 1:
    #     Eff31.append(np.nan)
    #     Er31.append(np.nan)
    # else:
    #     Eff31.append(E31_88)
    #     Er31.append(erE31_88)
    
    
    # fig, ax = plt.subplots(1,2)
    # ax[0].imshow(I0_88)
    # ax[0].set_title('$I_0$')
    # ax[1].imshow(I1_88)
    # ax[1].set_title('$I_1$')
    # plt.show()

# # Eff = [np.nan 
# # Er[ Eff==np.nan ] = np.nan
# # print(Eff)
# plt.errorbar(energy_range,Eff1,yerr=Er1,fmt='.:', label="$\eta_1$")
# plt.errorbar(energy_range,Eff31,yerr=Er31,fmt='.:', label="$\eta_{3,1}$")
# plt.xlabel("Photon Energy [eV]")
# plt.ylabel("$\eta_n$")
# plt.legend()
# plt.show()

# x0,y0 = 450,614
# xL,yL = 650,650 #520, 380

# # cropping images to assist with finding the beam center
# ims = [cropImage(i, x0, y0, xL, yL) for i in ims]

# print(" ")
# print("Finding Beam Center...")
# # finding beam center for each image
# cX,cY = [],[]
# for i in tqdm(ims):
#     cx,cy = findBeamCenter(i,show=False)
#     # print(cx,cy)
#     cX.append(int(cx))
#     cY.append(int(cy))
# # print(energy_range)
# # print(len(cX))
# plt.plot(energy_range,[abs(c-cX[0])*11.0e-3 for c in cX],label='x')
# plt.plot(energy_range,[abs(c-cY[0])*11.0e-3 for c in cY],label='y')
# plt.ylabel('Beam center drift [mm]')
# plt.xlabel('Photon energy [eV]')
# # plt.yscale('log')
# plt.legend()
# plt.show()


# for xc,yc in zip(cX,cY):
#     if xc-(xL-25) <= 0:
#         print('ERROR!! LENGTH OF NEW CROPPED IMAGE IS TOO LARGE! REDUCE IN X')
#     if yc-(yL-25) <= 0:
#         print('ERROR!! LENGTH OF NEW CROPPED IMAGE IS TOO LARGE! REDUCE IN Y')
        
# # cropping images again to center them with the calculated beam center
# ims = [cropImage(i,xc,yc,xL-25,yL-25) for i,xc,yc in zip(ims,cX,cY)]

# for e,i in enumerate(ims):
#     IN = (i/np.max(i))*65535
#     io.imsave(savePath_images + '/normalised/' + str(e) + '.tif',  IN.astype(np.uint16))
#     io.imsave(savePath_images + '/averaged/' + str(e) + '.tif',  i.astype(np.uint16))

# # converting cropped images from detector counts to ph/s/cm^2
# ims = [counts2photonsPsPcm2(i, e, t=60.0e-3, res=(11.0e-6,11.0e-6), conversion=1.27) for i,e in zip(ims,energy_range)]
# # comverting from ph/s/cm^2 to mJ/s/cm^2
# Pims = [intensity2power(i, e) for i,e in zip(ims,energy_range)]

# # finding new total intensity (in ph/s/cm^2)
# iTot = [np.sum(i) for i in ims]
# er = [p*i for p,i in zip(pEr,iTot)]
# # finding total power (in mJ/s/cm^2)
# pTot = [np.sum(p) for p in Pims]
# erP = [p*i for p,i in zip(pEr,pTot)]

# # finding total intensity and intensity slope over grating area
# # finding FWHM of intensity profile
# gsums, csums, S = [],[],[]
# fwhmX,fwhmY = [],[]
# fwXs,fwYs = [],[]
# print(" ")
# print(" ")
# for e,i in enumerate(tqdm(ims)):
#     print(f"number {e}")
#     gs,cs,s = IoverGrating(i, GA=100.0e-6, dx=11.0e-6, dy=11.0e-6,show=True)
#     gsums.append(gs)
#     csums.append(cs)
#     S.append(s)
    
#     FWHMx,FWHMy = getFWatValue(i, dx=11.0e-6, dy=11.0e-6,averaging=10,show=False)
#     fwhmX.append(FWHMx)
#     fwhmY.append(FWHMy)
#     if e <= 20:
#         FWHMx_sm, FWHMy_sm = getFWatValue(i, dx=11.0e-6, dy=11.0e-6,averaging=10,smoothing='multigauss',sparams=100,show=False)
#     else:
#         FWHMx_sm, FWHMy_sm = getFWatValue(i, dx=11.0e-6, dy=11.0e-6,averaging=10,smoothing='multigauss',show=False)
#     fwXs.append(FWHMx_sm)
#     fwYs.append(FWHMy_sm)
# # gsums,csums = [IoverGrating(i, GA=100.0e-6, dx=11.0e-6, dy=11.0e-6,show=True) for i in ims]

# plt.plot(energy_range,[abs(c-cX[0])*11.0e-3 for c in cX],label='x')
# plt.plot(energy_range,[abs(c-cY[0])*11.0e-3 for c in cY],label='y')
# plt.ylabel('Beam center drift [mm]')
# plt.xlabel('Photon energy [eV]')
# # plt.yscale('log')
# plt.legend()
# plt.show()

# plt.errorbar(energy_range[0:60], iTot[0:60], yerr=er[0:60], fmt='.')
# plt.xlabel("Photon Energy [eV]")
# plt.ylabel("Total Intensity [$ph/s/cm^2$]")
# plt.show()

# plt.errorbar(energy_range[0:60], pTot[0:60], yerr=erP[0:60], fmt='.')
# plt.xlabel("Photon Energy [eV]")
# plt.ylabel("Total Power [$mJ/s/cm^2$]")
# plt.show()


# plt.plot(energy_range[0:60],gsums[0:60],'.')
# plt.xlabel("Photon Energy [eV]")
# plt.ylabel("Total Intensity over Grating [$ph/s/cm^2$]")
# plt.show()

# plt.plot(energy_range[0:60],csums[0:60],'.')
# plt.xlabel("Photon Energy [eV]")
# plt.ylabel("Total Intensity over Central 100x100 um [$ph/s/cm^2$]")
# plt.show()

# plt.plot(energy_range[0:60],S[0:60],'.')
# plt.xlabel("Photon Energy [eV]")
# plt.ylabel("Intensity Slope over Grating")
# plt.show()

# plt.plot(energy_range[0:60],fwhmX[0:60],'.:',label='x')
# plt.plot(energy_range[0:60],fwhmY[0:60],'.:',label='y')
# plt.plot(energy_range[0:60],fwXs[0:60], '.:',label='x - smoothed')
# plt.plot(energy_range[0:60],fwYs[0:60], '.:',label='y - smoothed')
# plt.xlabel("Photon Energy [eV]")
# plt.ylabel("Intensity FWHM [m]")
# plt.legend()
# plt.show()