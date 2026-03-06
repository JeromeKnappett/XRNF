#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 16:03:36 2022

@author: -
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable

def getFWatValue(I,dx,dy,frac=0.5,cuts='xy',centered=True,averaging=None,smoothing=None,sparams=0,verbose=True,show=True,title=None):
    """
    Calculate FW of the beam at arbitrary fraction of maximum,
    calculating number of point bigger than max/value through center of the image

    :param 
        I:  intensity
        dx,dy: resolution in x and y
        frac: Fraction of maximum to find with at. Default is 0.5
        cuts: 1D cuts to display, if show=True. Can be 'x','y', or 'xy'. Default is 'xy'.
        centered: Is the data centered. Default is True.
        averaging: Number of central pixels to take average over for line profile. Default is None.
        smoothing: Speficy whether to smooth the data before finding width of curve. Smoothing can be 'savgol' or 'gauss'. Default is None.
        sparams: Parameters for fitting. If savgol, params is an int that determines the number of polynomials in the fit. If gaussian, sparams is an int that specifies the number of central pixels to ignore.
    :return: fw_x, fw_y in [m]
    """
    
    if centered:
        # print(' ')
        # print('Centered')
        centerIndex = (I.shape[0]//2,I.shape[1]//2)
        if averaging != None:
            # print('Averaging 1')
            x_center = np.mean(I[I.shape[0]//2 - int(averaging/2):I.shape[0]//2 + int(averaging/2),:],axis=0)
            y_center = np.mean(I[:,I.shape[1]//2 - int(averaging/2):I.shape[1]//2 + int(averaging/2)],axis=1)
        else:
            # print('Not Averaging 1')
            x_center = I[I.shape[0]//2,:]
            y_center = I[:,I.shape[1]//2]
#        print(centerIndex)
    else:
        # print(' ')
        # print('Not centered')
        centerIndex = np.unravel_index(I.argmax(), I.shape)
        if averaging != None:
            # print('Averaging 2')
            x_center = np.mean(I[I.shape[0]//2 - int(averaging/2):I.shape[0]//2 + int(averaging/2),:],axis=0)
            y_center = np.mean(I[:,I.shape[1]//2 - int(averaging/2):I.shape[1]//2 + int(averaging/2)],axis=1)
        else:
            # print('No averaging 2')
            x_center = I[centerIndex[0],:]
            y_center = I[:,centerIndex[1]]

    if smoothing != None:
        # print(' ')
        # print('Smoothing')
        from scipy.signal import savgol_filter
        from scipy.optimize import curve_fit
        if smoothing == 'savgol':
            # print('savgol')
            x_center_s = savgol_filter(x_center,window_length=len(x_center)-1,polyorder=sparams)
            y_center_s = savgol_filter(y_center,window_length=len(y_center)-1,polyorder=sparams)
        
        elif smoothing == 'gauss':
            # print('Gauss')
            # print(np.sqrt(np.sqrt(np.std(x_center))))
            p0x = [np.max(x_center), centerIndex[1], np.sqrt(np.sqrt(np.std(x_center)))] #100.0] #np.std(x_center)
            p0y = [np.max(y_center), centerIndex[0], np.sqrt(np.sqrt(np.std(y_center)))] #100.0]# centerIndex[0], 100.0] #np.std(y_center)
            
            x,y = np.linspace(0,len(x_center),len(x_center)), np.linspace(0,len(y_center),len(y_center))
            sigX = np.ones_like(x)
            sigY = np.ones_like(y)
            sigX[centerIndex[1]-sparams:centerIndex[1]+sparams] = 100
            sigY[centerIndex[0]-sparams:centerIndex[0]+sparams] = 100
            # plt.plot(sigX)
            # plt.show()
            
            # try:
            coeffX, covX = curve_fit(gauss,x,x_center,p0=p0x,sigma=sigX)
            coeffY, covY = curve_fit(gauss,y,y_center,p0=p0y,sigma=sigY)
            # except:
                # print('HERE FOR REAL')
                # coeffX, covX = curve_fit(gauss,x,x_center[:,0],p0=p0x,sigma=sigX)
                # coeffY, covY = curve_fit(gauss,y,y_center[:,0],p0=p0y,sigma=sigY)
            
            x_center_s = gauss(x,coeffX[0],coeffX[1],coeffX[2])
            y_center_s = gauss(y,coeffY[0],coeffY[1],coeffY[2])
            
        elif smoothing == 'multigauss':
            # print('Gauss')
            # print(np.sqrt(np.sqrt(np.std(x_center))))
            p0x = [np.max(x_center)/4,
                   np.max(x_center)/2,
                   centerIndex[1], 
                   np.sqrt(np.sqrt(np.std(x_center)))/4,
                   np.sqrt(np.sqrt(np.std(x_center)))/12] 
            p0y = [np.max(y_center)/15,
                   np.max(y_center)/2, 
                   centerIndex[0], 
                   np.sqrt(np.sqrt(np.std(y_center)))/15,
                   np.sqrt(np.sqrt(np.std(y_center)))/25] 
            
            x,y = np.linspace(0,len(x_center),len(x_center)), np.linspace(0,len(y_center),len(y_center))
            sigX = np.ones_like(x)
            sigY = np.ones_like(y)
            sigX[centerIndex[1]-sparams:centerIndex[1]+sparams] = 100
            sigY[centerIndex[0]-sparams:centerIndex[0]+sparams] = 100
            # plt.plot(sigX)
            # plt.show()
            
            try:
                coeffX, covX = curve_fit(multiGauss,x,x_center,p0=p0x)#,sigma=sigX)
                coeffY, covY = curve_fit(multiGauss,y,y_center,p0=p0y)#,sigma=sigY)
            except:
                print('HERE')
                coeffX, covX = curve_fit(multiGauss,x,x_center[:,0],p0=p0x)#,sigma=sigX)
                coeffY, covY = curve_fit(multiGauss,y,y_center[:,0],p0=p0y)#,sigma=sigY)
            
            x_center_s = multiGauss(x,coeffX[0],coeffX[1],coeffX[2],coeffX[3],coeffX[4],plot=True)
            y_center_s = multiGauss(y,coeffY[0],coeffY[1],coeffY[2],coeffX[3],coeffX[4],plot=True)
        
        fw_x = len(x_center_s[x_center_s>(x_center_s.max()*frac)])*dx
        fw_y = len(y_center_s[y_center_s>(y_center_s.max()*frac)])*dy
    else:
        fw_x = len(x_center[x_center>(x_center.max()*frac)])*dx
        fw_y = len(y_center[y_center>(y_center.max()*frac)])*dy
    
    if verbose:
        print(f'Full width at {frac} maximum:')
        print(f'horizontal:      {fw_x} [m]')
        print(f'vertical:        {fw_y} [m]')
    
    if show:
        import matplotlib.patches as patches
        try:
            from usefulWavefield import round_sig
        except ModuleNotFoundError:
            from usefulWavefield_old import round_sig
        if smoothing:
            xmaxpos = np.argmax(x_center_s)
            ymaxpos = np.argmax(y_center_s)
        else:
            xmaxpos = np.argmax(x_center)
            ymaxpos = np.argmax(y_center)
        
        if centered:
            xmaxpos = centerIndex[1]
            ymaxpos = centerIndex[0]
            
        x0,y0 = xmaxpos - ((fw_x/dx)/2), ymaxpos - ((fw_y/dy)/2)
#        x0,y0 = centerIndex[0] - ((fw_x/dx)/2), centerIndex[1] - ((fw_y/dy)/2)
        xl,yl = fw_x/dx, fw_y/dy
        
        numYticks = 5
        numXticks = 3
        nx,ny = np.shape(I)[1], np.shape(I)[0]
        if cuts=='xy':
            fig, ax = plt.subplots(1,3)
            xax,iax,yax = 0,1,2
        elif cuts=='x':
            fig, ax = plt.subplots(1,2)
            xax,iax,yax = 0,1,2
        elif cuts=='y':
            fig, ax = plt.subplots(1,2)
            xax,iax,yax = 2,1,0
        elif cuts=='none':
            fig, ax = plt.subplots(1,1)
            xax,iax,yax = 1,0,2
        rect_0 = patches.Rectangle((x0,y0),xl,yl, edgecolor='r', facecolor="none")
        if cuts == 'xy' or cuts == 'x':
            ax[xax].plot(x_center,label='raw')
            ax[xax].vlines(x=[x0, x0 + xl],ymin=0, ymax=np.max(x_center), colors='red', ls='--', lw=2)
            # ax[xax].axvline(x=xmaxpos,color='blue')
            ax[xax].set_ylabel('Intensity [$ph/s/cm^2$]')
            ax[xax].set_xlabel('x-position (y=0) [mm]')
            ax[xax].set_xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])
            ax[xax].set_xticklabels([round_sig(nx*dx*(a/(numXticks-1.0))*1e3) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=10)
        
        if cuts == 'xy' or cuts == 'y':
            ax[yax].plot(y_center,label='raw')
            ax[yax].vlines(x=[y0, y0 + yl],ymin=0, ymax=np.max(y_center), colors='red', ls='--', lw=2)
            ax[yax].set_ylabel('Intensity [$ph/s/cm^2$]')
            ax[yax].set_xlabel('y-position (x=0) [mm]')
            ax[yax].set_xticks([int((ny-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])
            ax[yax].set_xticklabels([round_sig(ny*dy*(a/(numXticks-1.0))*1e3) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=10)
        # ax[2].axvline(x=ymaxpos,color='blue')
        I = ax[iax].imshow(np.squeeze(I),aspect='auto')
        # ax[iax].axhline(y=ymaxpos,color='blue')
        # ax[iax].axvline(x=xmaxpos,color='blue')
        ax[iax].add_patch(rect_0)
        ax[iax].set_ylabel('y-position [mm]')
        ax[iax].set_xlabel('x-position [mm]')
        ax[iax].set_yticks([int((ny-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)])
        ax[iax].set_yticklabels([round_sig(ny*dy*(a/(numYticks-1.0))*1e3) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=10)
        ax[iax].set_xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])
        ax[iax].set_xticklabels([round_sig(nx*dx*(a/(numXticks-1.0))*1e3) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=10)
        divider = make_axes_locatable(ax[iax])
        cax = divider.append_axes("right",size="3%",pad=0.05)
        plt.colorbar(I,cax=cax,label='Intensity [$ph/s/cm^2$]')
        
        if smoothing:
            if cuts == 'xy' or 'x':
                ax[xax].plot(x_center_s,label='smoothed')
            if cuts == 'xy' or 'y':
                ax[yax].plot(y_center_s,label='smoothed')
            ax[0].legend()
            # ax[yax].legend()
        if title:
            ax[iax].set_title(title)
        plt.tight_layout()
        plt.show()
    return fw_x, fw_y
# %%
def gauss(x,A,mu,sigma,plot=False):
    # G = H + A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))
    # A,mu,sigma = p
    G = A*np.exp(-1*((x-mu)**2) / (2.0*(sigma**2)))
    
    if plot:
        plt.plot(x,G)
        plt.show()
    return G
# %%
def multiGauss(x,A1,A2,mu,sigma1,sigma2,plot=False):
    # G = H + A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))
    # A,mu,sigma = p
    G1 = A1*np.exp(-1*((x-mu)**2) / (2.0*(sigma1**2)))
    G2 = A2*np.exp(-1*((x-mu)**2) / (2.0*(sigma2**2)))
    G = G1 + G2
    if plot:
        plt.plot(x,G1,label='G1')
        plt.plot(x,G2,label='G2')
        plt.plot(x,G,label='G')
        plt.legend()
        plt.show()
    return G

def test():
    import numpy as np
    import tifffile
    path = '/user/home/opt/xl/xl/experiments/focusedOffAxis2/data/atFZPuf375x200/driftVol/intensity/'
    files = ['000000.tif','000004.tif']
    
    I = [tifffile.imread(path + f) for f in files]
    
    dx,dy = 9.57713358e-7, 7.253495748e-7
    z = 9.5
    
    fwx = []
    fwy = []
    for i in I:
        fx,fy = getFWatValue(i,dx,dy,frac=1/2,smoothing='multigauss',sparams=200)
        fwx.append(fx)
        fwy.append(fy)
    
    dX = fwx[1]-fwx[0]
    dY = fwy[1]-fwy[0]
    
    divx = 2*np.arctan((0.5*dX)/z)
    divy = 2*np.arctan((0.5*dY)/z)
    
    print(f"Div x:    {divx*1e6:.5g} urad")
    print(f"Div y:    {divy*1e6:.5g} urad")
        
if __name__ == '__main__':
    test()