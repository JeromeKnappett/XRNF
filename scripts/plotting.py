#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 14:27:21 2022

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
try:
    import imageio
    import tifffile
except ModuleNotFoundError:
    pass
import pickle
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
# from mpl_toolkits.axes_grid1.colorbar import colorbar
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
#from useful import round_sig, getLineProfile
from matplotlib import rcParams
from math import log10, floor

colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]


# %%
def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
            return x
        
def resample(a,fx,fy, midX=None, midY=None, debug=False, show=False):
    nx, ny = np.shape(a)[1], np.shape(a)[0]
    if midX == None:
        midX = nx/2
    if midY == None:
        midY = ny/2
    
    aNew = a[int(midY-fy*midY):int(midY+fy*midY), int(midX-fx*midX):int(midX+fx*midX)]
    if debug:
        print("original shape: ", np.shape(a))
        print("new shape: ", np.shape(aNew))
    else:
        pass
    if show:
        plt.imshow(a, aspect='auto')
        plt.title('original')
        plt.show()
        plt.imshow(aNew, aspect='auto')
        plt.title('new')
        plt.show()
    else:
        pass
    return aNew


def colorize(z):
    from colorsys import hls_to_rgb
    n,m = z.shape
    c = np.zeros((n,m,3))
    c[np.isinf(z)] = (1.0, 1.0, 1.0)
    c[np.isnan(z)] = (0.5, 0.5, 0.5)

    idx = ~(np.isinf(z) + np.isnan(z))
    A = (np.angle(z[idx]) + np.pi) / (2*np.pi)
    A = (A + 0.5) % 1.0
    B = 1.0 - 1.0/(1.0+abs(z[idx])**0.3)
    c[idx] = [hls_to_rgb(a, b, 0.8) for a,b in zip(A,B)]
    return c


def plotTwoD(t, dx=1, dy=1, 
             sF=1, 
             describe=False, 
             title=None, 
             xLabel=None, 
             yLabel=None,
             numXticks= 7,
             numYticks= 7, 
             fSize=10, 
             colour=None, 
             cbar=True,
             cbarLabel=None, 
             aspct='auto', 
             rotate=False,
             dpi=200,
             savePath=None):
    
    rcParams['figure.dpi']=dpi
    
    nx, ny = np.shape(t)[1], np.shape(t)[0]
    midX, midY = nx/2, ny/2
    rx, ry = nx*dx, ny*dy
    
    if rotate:
        from scipy.ndimage import rotate
        t = rotate(t, 90)
        dx,dy = dy,dx
        nx,ny = ny,nx
        rx,ry = ry,rx
        midX,midY=midY,midX
    
    if describe:
        print(title)
        print("Shape of tif (x, ", (nx,ny))
        print("Range (x,y): {}".format((rx,ry)))
        print("Resolution (x,y): {}".format((dx,dy)))
    else:
        pass
    
    plt.imshow(t, cmap=colour, aspect=aspct)
    plt.yticks([int((ny-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],
               [round_sig(ny*dy*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=fSize )
    plt.xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],
               [round_sig(nx*dx*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=fSize)
    if cbar:
        plt.colorbar(label=cbarLabel).ax.tick_params(labelsize=10)
    plt.xlabel(xLabel,fontsize=15 )#[\u03bcm]')
    plt.ylabel(yLabel,fontsize=15 )#[\u03bcm]')
    if title:
        plt.title(label=title)
    plt.tight_layout()
    if savePath != None:
        print("Saving : ", savePath)
        plt.savefig(savePath)
    plt.show()


def plotMultiTwoD(T, 
                  dims, #(rows,columns)
                  dx=1, 
                  dy=1, 
                  sF=1, 
                  mid=None, 
                  ran=None,
                  describe=False, 
                  title=None, 
                  xLabel=None, 
                  yLabel=None, 
                  fSize=10, 
                  numXticks=7, 
                  numYticks=7,
                  onlyEdgeLabels=False, 
                  colour=None, 
                  cBar='side', 
                  cbarLabel=None, 
                  multiCBar=False, 
                  aspct='auto', 
                  savePath=None,
                  verbose=False):
    N = len(T)
    nx, ny = [np.shape(t)[1] for t in T], [np.shape(t)[0] for t in T] 

    if title is None or len(title) == 1:
        title = np.full(N, title)
    if xLabel is None or len(xLabel) == 1:
        xLabel = np.full(N, xLabel)
    if yLabel is None or len(yLabel) == 1:
        yLabel = np.full(N, yLabel)
    if isinstance(dx,int):
        dx = np.full(N,dx)
    if isinstance(dy,int):
        dy = np.full(N,dy)
    if ran is None:
        ran=[[np.min(t), np.max(t)] for t in T]
    elif len(ran) == 1:
        ran = np.tile(ran,[N,1])
    else:
        pass
    
    if mid == None:
        midX, midY = [x/2 for x in nx], [y/2 for y in ny]
    else:
        midX, midY = [m[1] for m in mid], [m[0] for m in mid]
    rx, ry = [x*dX for x,dX in zip(nx,dx)], [y*dY for y,dY in zip(ny,dy)]
    
    if describe:
        for i in range(0, N):
            print(title[i])
            print("Shape of tif (x,y): ", (nx[i],ny[i]))
            print("Range (x,y): {}".format((rx[i],ry[i])))
            print("Resolution (x,y): {}".format((dx[i],dy[i])))
    else:
        pass

    
    fig, ax = plt.subplots(dims[0],dims[1])
    for i, t in enumerate(T):
        if dims[0] > 1 and dims[1] > 1:
            if i <= dims[1]-1:
                im = ax[0,i].imshow(t, vmin=ran[i][0], vmax=ran[i][1], cmap=colour, aspect=aspct)
                if title[i] != None:
                    ax[0,i].set_title(title[i])          
                ax[0,i].set_yticks([int((ny[i]-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)])
                ax[0,i].set_xticks([int((nx[i]-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])
                if onlyEdgeLabels:
                    ax[0,i].set_xticklabels([])
                    if i == 0:
                        ax[0,i].set_ylabel(yLabel)
                        ax[0,i].set_yticklabels([round_sig(ny[i]*dy[i]*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2),int((numYticks/2 + 1)))],fontsize=fSize)
                    else:
                        ax[0,i].set_yticklabels([])
                else:
                    # print('labels everywhere')
                    ax[0,i].set_ylabel(yLabel)
                    ax[0,i].set_yticklabels([round_sig(ny[i]*dy[i]*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2),int((numYticks/2 + 1)))],fontsize=fSize)
                    ax[0,i].set_xlabel(xLabel)
                    ax[0,i].set_xticklabels([round_sig(nx[i]*dx[i]*(a/(numXticks-1.0))*sF) for a in range(-int((numXticks-1.0)/2),int((numXticks/2 + 1)))],fontsize=fSize)  
                if multiCBar:
                    divider = make_axes_locatable(ax[0,i])
                    cax = divider.append_axes("right", size="3%", pad=0.05)
                    plt.colorbar(im,cax=cax)
                else:
                    # print('not adding colorbar to every plot')
                    pass
                # if i == 0:
                #     ax[0,i].set_ylabel(yLabel)
                #     ax[0,i].set_yticklabels([round_sig(ny[i]*dy[i]*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2),int((numYticks/2 + 1)))],fontsize=fSize)
            elif 2*dims[1]-1>= i >=dims[1]-1:
                im2 = ax[1,abs(i-dims[1])].imshow(t, vmin=ran[i][0], vmax=ran[i][1], cmap=colour, aspect=aspct)
                if title[i] != None:
                    ax[1,abs(i-dims[1])].set_title(title[i])   
                ax[1,abs(i-dims[1])].set_yticks([int((ny[i]-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)])
                ax[1,abs(i-dims[1])].set_xticks([int((nx[i]-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])      
                if onlyEdgeLabels:
                    if i == dims[1]:
                        ax[1,abs(i-dims[1])].set_ylabel(yLabel)
                        ax[1,abs(i-dims[1])].set_yticklabels([round_sig(ny[i]*dy[i]*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2),int((numYticks/2 + 1)))],fontsize=fSize)
                        ax[1,abs(i-dims[1])].set_xticklabels([])
                    else:
                        ax[1,abs(i-dims[1])].set_yticklabels([])
                else:
                    ax[1,abs(i-dims[1])].set_ylabel(yLabel)
                    ax[1,abs(i-dims[1])].set_yticklabels([round_sig(ny[i]*dy[i]*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2),int((numYticks/2 + 1)))],fontsize=fSize)
                    ax[1,abs(i-dims[1])].set_xlabel(xLabel)
                    ax[1,abs(i-dims[1])].set_xticklabels([round_sig(nx[i]*dx[i]*(a/(numXticks-1.0))*sF) for a in range(-int((numXticks-1.0)/2),int((numXticks/2 + 1)))],fontsize=fSize)                
                if multiCBar:
                    divider = make_axes_locatable(ax[1,abs(i-dims[1])])
                    cax = divider.append_axes("right", size="3%", pad=0.05)
                    plt.colorbar(im2,cax=cax)
                else:
                    pass
                # if i == 2*dims[0]-1:
                #     ax[1,abs(i-dims[0])].set_ylabel(yLabel)
                #     ax[1,abs(i-dims[0])].set_yticklabels([round_sig(ny[i]*dy[i]*(a/(numYticks-1))*sF) for a in range(-int((numYticks-1)/2),int((numYticks/2 + 1)))],fontsize=fSize)
                # if i == dims[0]:
                #     ax[1,abs(i-dims[0])].set_ylabel(yLabel)
                #     ax[1,abs(i-dims[0])].set_yticklabels([round_sig(ny[i]*dy[i]*(a/(numYticks-1))*sF) for a in range(-int((numYticks-1)/2),int((numYticks/2 + 1)))],fontsize=fSize)
            elif 3*dims[1]-1>= i >= 2*(dims[1]-1):
                im3 = ax[2,abs(i-2*dims[1])].imshow(t, vmin=ran[i][0], vmax=ran[i][1], cmap=colour, aspect=aspct)
                if title[i] != None:
                    ax[2,abs(i-2*dims[1])].set_title(title[i])      
                ax[2,abs(i-2*dims[1])].set_yticks([int((ny[i]-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)])
                ax[2,abs(i-2*dims[1])].set_xticks([int((nx[i]-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])  
                if onlyEdgeLabels:
                    if i == 2*dims[1]:
                        ax[2,abs(i-2*dims[1])].set_ylabel(yLabel)
                        ax[2,abs(i-2*dims[1])].set_yticklabels([round_sig(ny[i]*dy[i]*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2),int((numYticks/2 + 1)))],fontsize=fSize)
                        ax[2,abs(i-2*dims[1])].set_xticklabels([])
                    else:
                        ax[2,abs(i-2*dims[1])].set_yticklabels([])
                else:
                    ax[2,abs(i-2*dims[1])].set_ylabel(yLabel)
                    ax[2,abs(i-2*dims[1])].set_yticklabels([round_sig(ny[i]*dy[i]*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2),int((numYticks/2 + 1)))],fontsize=fSize)
                    ax[2,abs(i-2*dims[1])].set_xlabel(xLabel)
                    ax[2,abs(i-2*dims[1])].set_xticklabels([round_sig(nx[i]*dx[i]*(a/(numXticks-1.0))*sF) for a in range(-int((numXticks-1.0)/2),int((numXticks/2 + 1)))],fontsize=fSize)
                if multiCBar:
                    divider = make_axes_locatable(ax[2,abs(i-2*dims[1])])
                    cax = divider.append_axes("right", size="3%", pad=0.05)
                    plt.colorbar(im3,cax=cax)
                else:
                    pass
                # if i == 3*dims[0]-1:
                #     ax[2,abs(i-2*dims[0])].set_ylabel(yLabel)
                #     ax[2,abs(i-2*dims[0])].set_yticklabels([round_sig(ny[i]*dy[i]*(a/(numYticks-1))*sF) for a in range(-int((numYticks-1)/2),int((numYticks/2 + 1)))],fontsize=fSize)
            else:
                pass
            if onlyEdgeLabels:
                if dims[0]*dims[1]-dims[1] <= i <= dims[0]*dims[1]-1:
                    ax[dims[0]-1,abs(i-dims[0]*dims[1])-1].set_xlabel(xLabel)
                    ax[dims[0]-1,abs(i-dims[0]*dims[1])-1].set_xticks([int((nx[i]-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])      
                    ax[dims[0]-1,abs(i-dims[0]*dims[1])-1].set_xticklabels([round_sig(nx[i]*dx[i]*(a/(numXticks-1.0))*sF) for a in range(-int((numXticks-1.0)/2),int((numXticks/2 + 1)))],fontsize=fSize)
                else:
                    pass
            
            fig.tight_layout()
            
            # if onlyEdgeLabels:
            #     if i == 0:
            #         ax[0,i].set_ylabel(yLabel)
            #         ax[0,i].set_yticklabels([round_sig(ny[i]*dy[i]*(a/(numYticks-1))*sF) for a in range(-int((numYticks-1)/2),int((numYticks/2 + 1)))],fontsize=fSize)
            #     elif i == dims[1]:
            #         ax[1,abs(i-dims[1])].set_ylabel(yLabel)
            #         ax[1,abs(i-dims[1])].set_yticklabels([round_sig(ny[i]*dy[i]*(a/(numYticks-1))*sF) for a in range(-int((numYticks-1)/2),int((numYticks/2 + 1)))],fontsize=fSize)
            #     elif i == 2*dims[1]:
            #         ax[2,abs(i-2*dims[1])].set_ylabel(yLabel)
            #         ax[2,abs(i-2*dims[1])].set_yticklabels([round_sig(ny[i]*dy[i]*(a/(numYticks-1))*sF) for a in range(-int((numYticks-1)/2),int((numYticks/2 + 1)))],fontsize=fSize)
                
            #     else:
            #         try:
            #             ax[0,i].set_yticklabels([])
            #         except:
            #             TypeError
            # else:
            #     pass
                # elif dims[0]*dims[1]-dims[1] <= i <= dims[0]*dims[1]-1:
            #     ax[dims[0]-1,abs(i-dims[0]*dims[1])].set_xlabel(xLabel)
            #     ax[dims[0]-1,abs(i-dims[0]*dims[1])].set_xticklabels([round_sig(nx[i]*dx[i]*(a/(numXticks-1))*sF) for a in range(-int((numXticks-1)/2),int((numXticks/2 + 1)))],fontsize=fSize)

        elif dims[0] or dims[1] == 1:
            im = ax[i].imshow(t, vmin=ran[i][0], vmax=ran[i][1], cmap=colour, aspect=aspct)
            if onlyEdgeLabels:
                if dims[0] == 1:
                    if i == 0:
                        ax[i].set_ylabel(yLabel)
                        ax[i].set_yticklabels([round_sig(ny[i]*dy[i]*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2),int((numYticks/2 + 1)))],fontsize=fSize)
                    elif i == int(len(T)/2.0 - 0.5):
                        ax[i].set_yticklabels([])
                        ax[i].set_xlabel(xLabel)
                    else:
                        ax[i].set_yticklabels([])
                    ax[i].set_yticks([int((ny[i]-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)])   
                    ax[i].set_xticks([int((nx[i]-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])
                    ax[i].set_xticklabels([round_sig(nx[i]*dx[i]*(a/(numXticks-1.0))*sF) for a in range(-int((numXticks-1.0)/2),int((numXticks/2 + 1)))],fontsize=fSize)            
                elif dims[1] == 1:
                    if i == len(T)-1:
                        ax[i].set_xlabel(xLabel)
                        ax[i].set_xticks([int((nx[i]-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])   
                        ax[i].set_xticklabels([round_sig(nx[i]*dx[i]*(a/(numXticks-1.0))*sF) for a in range(-int((numXticks-1.0)/2),int((numXticks/2 + 1)))],fontsize=fSize)
                    elif i == int(len(T)/2.0 - 0.5):
                        ax[i].set_xticklabels([])
                        ax[i].set_ylabel(yLabel)
                    else:
                        ax[i].set_xticklabels([])
                    ax[i].set_xticks([int((nx[i]-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])   
                    ax[i].set_yticks([int((ny[i]-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)])
                    ax[i].set_yticklabels([round_sig(ny[i]*dy[i]*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2),int((numYticks/2 + 1)))],fontsize=fSize)
            else:
                ax[i].set_ylabel(yLabel)
                ax[i].set_xlabel(xLabel)
                ax[i].set_yticks([int((ny[i]-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)])
                ax[i].set_xticks([int((nx[i]-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])   
                ax[i].set_yticklabels([round_sig(ny[i]*dy[i]*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2),int((numYticks/2 + 1)))],fontsize=fSize)
                ax[i].set_xticklabels([round_sig(nx[i]*dx[i]*(a/(numXticks-1.0))*sF) for a in range(-int((numXticks-1.0)/2),int((numXticks/2 + 1)))],fontsize=fSize)
            if title[i] != None:
                ax[i].set_title(title[i])
            if multiCBar:
                print("constructing multiple colorbars... ")
                # plt.colorbar(im, ax=ax[i])
                divider = make_axes_locatable(ax[i])
                cax = divider.append_axes("right", size="3%", pad=0.05)
                if onlyEdgeLabels:
                    fig.tight_layout()
                    if i == int(len(T)/2.0 - 0.5):
                        plt.colorbar(im, cax=cax, label=cbarLabel)
                    else:
                        plt.colorbar(im, cax=cax)
                else:
                    fig.tight_layout()
                    plt.colorbar(im, cax=cax, label=cbarLabel)
            # cbar_ax = fig.add_axes([0.85, 0.14, 0.03, 0.8])
        else:
            pass
    # print("... made it here ...")
    if cBar == 'side':
        if multiCBar == False:
            # plt.colorbar(im,label=cbarLabel).ax.tick_params(labelsize=10)
            fig.tight_layout()
            fig.subplots_adjust(right=1.2)
            cbar_ax = fig.add_axes([1.25, 0.13, 0.03, 0.8])#[0.85, 0.14, 0.03, 0.8])
            try:
                fig.colorbar(im, cax=cbar_ax, label=cbarLabel).ax.tick_params(labelsize=10)
            except UnicodeDecodeError:
                import sys
                reload(sys)
                sys.setdefaultencoding('utf-8')
                fig.colorbar(im, cax=cbar_ax, label=cbarLabel).ax.tick_params(labelsize=10)
                
    elif cBar == 'bottom':
        if multiCBar == False:
            axins = inset_axes(ax[len(T)-2],
                    width="100%",  
                    height="20%",
                    loc='lower center',
                    borderpad=-5
                    )
            try:
                fig.colorbar(im, cax=axins, orientation="horizontal", label=cbarLabel)
                
            except UnicodeDecodeError:
                import sys
                reload(sys)
                sys.setdefaultencoding('utf-8')
                fig.colorbar(im, cax=axins, orientation="horizontal", label=cbarLabel)
            # fig.tight_layout()
            
        pass
    # print(" ")
    # print("... even made it here ...")
    if savePath != None:
        print("Saving : ", savePath)
        plt.savefig(savePath)
    
    # print(" ")
    # print("... even made it here if you'd believe it ...")
    plt.show()
    # print("... ")

def plotOneD(p, 
             d=1, 
             sF=1, 
             xlim=None,
             ylim=None,
             describe=False, 
             split=None, 
             customX = None,
             title=None, 
             labels=None, 
             xLabel=None, 
             yLabel=None, 
             figSize=(10,12),
             aspct='auto',
             lStyle='-',
             lWidth=1,
             pStyle='',
             fSize=10,
             color= None,
             savePath=None):
    
    try:
        n, x = int(np.shape(p)[0]), int(np.shape(p[1])[0])
    except IndexError:
        n, x = 1, int(np.shape(p)[0])
    mid = x/2
    
    
    if title is None or len(title) == 1:
        title = np.full(n, title)
    if labels is None or len(labels) == 1:
        labels = np.full(n, labels)
    if xLabel is None or len(xLabel) == 1:
        xLabel = np.full(n, xLabel)
    if yLabel is None or len(yLabel) == 1:
        yLabel = np.full(n, yLabel)
    if len(lStyle) == 0 or 1:
        lStyle = np.full(n, lStyle)
    if len(pStyle) == 0 or 1:
        pStyle = np.full(n, pStyle)
    if isinstance(d,int):
        d = np.full(n,d)
    if color is None:
        color = range(0,len(p))
    if customX is None:
        customX = np.full(n, customX)
    elif len(customX) == 1 or None:
        customX = np.full(n, customX)
    else:
        pass
    
    r = [x*dx for dx in d]
    
    if describe:
        print('Title: ', title)
        print("Number of profiles (n): ", n)
        print("Length of profiles (x): ", x)
        print("Range [m]: {}".format(r))
        print("Resolution [m]: {}".format(d))
        print('len of lstyle: ', len(lStyle))
    else:
        pass
    
    # print(title)
    # print(labels)
    # print(xLabel)
    # print(yLabel)
    # plt.figure(figsize=figSize)
    if split != None:
        print("splitting plot....")
        if split == 'columns':
            fig, ax = plt.subplots(1,n,figsize=figSize)
        elif split == 'rows':
            fig, ax = plt.subplots(n,1,figsize=figSize)
        elif split == 'dual':
            fig, ax0 = plt.subplots(figsize=figSize)
            ax1 = ax0.twinx()
            if customX:
                print("custom x-axis....")
                ax0.plot(customX[0][0:len(p[0])], [c*sF for c in p[0]], linestyle=lStyle[0], marker=pStyle[0], color=colours[0], label=labels[0],lineWidth=lWidth)
                ax1.plot(customX[0][0:len(p[1])], [c*sF for c in p[1]], linestyle=lStyle[0], marker=pStyle[1], color=colours[1], label=labels[1],lineWidth=lWidth)
            else:
                ax0.plot([c*sF for c in p[0]], linestyle=lStyle[0], marker=pStyle[0], color=colours[0], label=labels[0],lineWidth=lWidth)
                ax1.plot([c*sF for c in p[1]], linestyle=lStyle[0], marker=pStyle[1], color=colours[1], label=labels[1],lineWidth=lWidth)
            ax0.set_aspect(aspct)
            ax1.set_aspect(aspct)
            ax0.set_ylabel(yLabel[0])
            ax1.set_ylabel(yLabel[1])
            ax1.spines['left'].set_color(colours[0])
            ax1.spines['right'].set_color(colours[1])
            ax0.yaxis.label.set_color(colours[0])
            ax0.tick_params(axis='y', colors=colours[0])
            ax1.yaxis.label.set_color(colours[1])
            ax1.tick_params(axis='y', colors=colours[1])
            ax0.set_xlabel(xLabel[0])
            fig.tight_layout()
        else:
            pass
        
        if split != 'dual':
            for i, l in enumerate(p):
                if customX != None:
                    ax[i].plot(customX[i][0:len(l)], [c*sF for c in l], linestyle=lStyle[i], marker=pStyle, color=colours[color[i]], label=labels[i],lineWidth=lWidth)
                else:
                    ax[i].plot(l, linestyle=lStyle[i], marker=pStyle, color=colours[color[i]], label=labels[i],lineWidth=lWidth)
                    ax[i].set_xticks([int(x*(b/6)) for b in range(0,7)])
                    ax[i].set_xticklabels([round_sig(x*d[i]*(a/6)*sF) for a in range(-3,4)],fontsize=fSize)
                ax[i].set_aspect(aspct)
                ax[i].set_title(label=title[i])
                ax[i].set_xlabel(xLabel, fontsize=fSize)
                ax[i].set_ylabel(yLabel, fontsize=fSize)
                ax[i].legend()
        
    else:
        for i, l in enumerate(p):
            print("HERE I AM")
            if customX[i] != None:
                print("custom x-axis....")
                # print(len(customX[i][i]))
                print(len(l)) # removed customX[i][0:len(l)], [c*sF for c in l]
                plt.plot(customX[i], l, linestyle=lStyle[i], marker=pStyle[i], color=colours[color[i]], label=labels[i],lineWidth=lWidth)
            else:
                print(np.shape(l))
                print(len(lStyle))
                print(len(pStyle))
                print(len(labels))
                plt.plot(l, linestyle=lStyle[i], marker=pStyle[i], color=colours[color[i]], label=labels[i],lineWidth=lWidth)
                plt.xticks([int(x*(b/8)) for b in range(0,9)],
                           [round_sig(x*d[i]*(a/8)*sF) for a in range(-4,5)],fontsize=fSize)
            plt.xlabel(xLabel[i],fontsize=fSize) #[\u03bcm]')
            plt.ylabel(yLabel[i],fontsize=fSize) #[\u03bcm]')
            plt.title(label=title[i])
            plt.tight_layout()
            if xlim != None:
                plt.xlim(xlim)
            if ylim != None:
                plt.ylim(ylim)
        
        plt.gca().set_aspect(aspct)
        plt.legend()
    plt.tight_layout()
    if savePath != None:
        print("Saving : ", savePath)
        plt.savefig(savePath)
    plt.show()

def plotMultiOneD(p, X, dims, d, split=None, describe=False, titles=None, 
                  legend=None, xLabel=None, yLabel=None, lineStyle='-', 
                  pointStyle='',fSize=10,aspct='auto', savePath=None):
    n, x = int(np.shape(p)[0]), int(np.shape(p)[1])
    mid = x/2
    r = x*d
#    
    if describe:
        print(titles)
        print("Number of profiles (n): ", n)
        print("Length of profiles (x): ", x)
        print("Range [m]: {}".format(r))
        print("Resolution [m]: {}".format(d))
    else:
        pass
    
    if titles == None:
        titles = np.full(n, None)
    elif legend == None:
        legend = np.full(n, None)
    elif xLabel == None:
        xLabel = np.full(n, None)
    elif yLabel == None:
        yLabel = np.full(n, None)
    else:
        pass
    
    if split:    
        P = []
#        P = np.reshape(p,[split[1],split[0],len(X)])
        for a in p:
            print(np.shape(a))
            print(np.shape(p))
            try:
                b = np.reshape(a,split)
            except ValueError:
                b = np.reshape(a,[split[0],split[1]])
            P.append(b)
            try:
                X = np.reshape(X,[split,split])
#                X = X[0]
            except TypeError:
                pass
            print("new shape of P: ", np.shape(P))
            print("new shape of X: ", np.shape(X))
            print(X)
        P = np.transpose(P,(1,0,2))
    else:
        P = p
    
    print(dims[0], dims[1])
    fig, ax = plt.subplots(dims[0],dims[1])
    plt.gca().set_aspect(aspct)
    for i, l in enumerate(P):
        print(i)
        if i == 0:
#            print(l)
#            print(i)
#            print('here')
            if split:
                for j in l:
                    print(j)
                    print(X)
                    try:
                        ax[0,i].plot(X,j, linestyle=lineStyle, marker=pointStyle)#, label=legend[i])
                        ax[0,i].set_ylabel(yLabel[i],fontsize=fSize) 
                        #                ax[0,i].legend()
                    except IndexError:
                        ax[i].plot(X,j, linestyle=lineStyle, marker=pointStyle)#, label=legend[i])
                        ax[i].set_ylabel(yLabel[i],fontsize=fSize)        
            else:
                try:
                    ax[0,i].plot(X,l, linestyle=lineStyle, marker=pointStyle)#, label=legend[i])
                    ax[0,i].set_ylabel(yLabel[i],fontsize=fSize) 
                except IndexError:
                    ax[i].plot(X,l, linestyle=lineStyle, marker=pointStyle)#, label=legend[i])
                    ax[i].set_ylabel(yLabel[i],fontsize=fSize) 
                
        elif 0<= i <= dims[1]-1:
            print('dims: ', dims[1]-1)
            print('index: ', i)
            if split:
                for j in l:
                    try:
                        ax[0,i].plot(X,j, linestyle=lineStyle, marker=pointStyle)
                        ax[0,i].set_ylabel(yLabel[i],fontsize=fSize) 
                    except IndexError:
                        ax[i].plot(X,j, linestyle=lineStyle, marker=pointStyle)
                        ax[i].set_ylabel(yLabel[i],fontsize=fSize) 
            else:
                try:
                    ax[0,i].plot(X,l, linestyle=lineStyle, marker=pointStyle)
                    ax[0,i].set_ylabel(yLabel[i],fontsize=fSize) 
                except IndexError:
                    ax[i].plot(X,l, linestyle=lineStyle, marker=pointStyle)
                    ax[i].set_ylabel(yLabel[i],fontsize=fSize) 
        elif 2*dims[1]-1>= i >=dims[1]-1:
            print('dims: ', 2*dims[1]-1)
            print('index: ', abs(i-dims[1]))
            if split:
                for j in l:
                    try:
                        ax[1,abs(i-dims[1])].plot(X,j, linestyle=lineStyle, marker=pointStyle)
                        ax[1,abs(i-dims[1])].set_ylabel(yLabel[i],fontsize=fSize) 
                    except IndexError:
                        ax[i].plot(X,j, linestyle=lineStyle, marker=pointStyle)
                        ax[i].set_ylabel(yLabel[i],fontsize=fSize) 
            else:
                try:
                    ax[1,abs(i-dims[1])].plot(X,l, linestyle=lineStyle, marker=pointStyle)
                    ax[1,abs(i-dims[1])].set_ylabel(yLabel[i],fontsize=fSize) 
                except IndexError:
                    ax[i].plot(X,l, linestyle=lineStyle, marker=pointStyle)
                    ax[i].set_ylabel(yLabel[i],fontsize=fSize)                     
        elif 3*dims[0]-1>= i >= 2*(dims[0]-1):
            print('dims: ', 3*dims[1]-1)
            print('index: ', abs(i-2*dims[1]))
            if split:
                for j in l:
                    try:
                        ax[2,abs(i-2*dims[1])].plot(X,j, linestyle=lineStyle, marker=pointStyle)
                        ax[2,abs(i-2*dims[1])].set_ylabel(yLabel[i],fontsize=fSize) 
                    except IndexError:
                        ax[i].plot(X,j, linestyle=lineStyle, marker=pointStyle)
                        ax[i].set_ylabel(yLabel[i],fontsize=fSize) 
            else:
                try:
                    ax[2,abs(i-2*dims[1])].plot(X,l, linestyle=lineStyle, marker=pointStyle)
                    ax[2,abs(i-2*dims[1])].set_ylabel(yLabel[i],fontsize=fSize) 
                except IndexError:
                    ax[i].plot(X,l, linestyle=lineStyle, marker=pointStyle)
                    ax[i].set_ylabel(yLabel[i],fontsize=fSize) 
    if dims[1]>1:
        for i in range(0,dims[1]):
            try:
                ax[dims[0]-1,i].set_xlabel(xLabel,fontsize=fSize) 
            except IndexError:
                ax[i].set_xlabel(xLabel,fontsize=fSize) 
    elif dims[0]>1:
        for i in range(0,dims[0]):
            try:
                ax[i,dims[1]-1].set_xlabel(xLabel,fontsize=fSize) 
            except IndexError:
                ax[dims[0]-1].set_xlabel(xLabel,fontsize=fSize) 
    fig.tight_layout()
    if legend !=None:
        fig.subplots_adjust(bottom=0.2)   ##  Need to play with this number.
        fig.legend(labels=legend, loc="lower center", ncol=split[0],fontsize=fSize) 
    if savePath !=None:
        plt.savefig(savePath)# dpi=2000)
    plt.show()

def plotCorrelationMap(DS, labels, colours='vlag', ran = [-1,1], labelSize = [10,10], labelRot=[0,0], annot=True, annotScale=1, savePath=None):
    import pandas as pd
    
    dataStructure = DS
    
    dF = pd.DataFrame(np.array(dataStructure).T,
                      columns= labels)
    
    print(labels)

    
    correlations = dF.corr()
    import seaborn as sns
    sns.set(font_scale=annotScale)
    plt.rcParams["figure.figsize"] = (8,6)
    res = sns.heatmap(abs(correlations).round(2),cmap=colours,vmin=ran[0],vmax=ran[1],annot=annot)
    res.set_xticklabels(res.get_xmajorticklabels(), fontsize = labelSize[0], rotation=labelRot[0])
    res.set_yticklabels(res.get_ymajorticklabels(), fontsize = labelSize[1], rotation=labelRot[1])
    if savePath !=None:
        plt.savefig(savePath + 'correlations.png')
    plt.show()
    
def plotComplex2D(t, dx=1, dy=1, 
             sF=1, 
             describe=False, 
             title=None, 
             xLabel=None, 
             yLabel=None,
             numXticks= 7,
             numYticks= 7, 
             fSize=10, 
             cbarLabel=None, 
             aspct='auto', 
             savePath=None):
    
    nx, ny = np.shape(t)[1], np.shape(t)[0]
    midX, midY = nx/2, ny/2
    rx, ry = nx*dx, ny*dy
    
    if describe:
        print(title)
        print("Shape of tif (x,y): ", (nx,ny))
        print("Range (x,y): {}".format((rx,ry)))
        print("Resolution (x,y): {}".format((dx,dy)))
    else:
        pass
    
    plt.imshow(colorize(t), aspect=aspct)
    plt.yticks([int((ny-1)*(b/(numYticks-1))) for b in range(0,numYticks)],
               [round_sig(ny*dy*(a/(numYticks-1))*sF) for a in range(-int((numYticks-1)/2),int((numYticks/2 + 1)))],fontsize=fSize )
    plt.xticks([int((nx-1)*(b/(numXticks-1))) for b in range(0,numXticks)],
               [round_sig(nx*dx*(a/(numXticks-1))*sF) for a in  range(-int((numXticks-1)/2),int((numXticks/2 + 1)))],fontsize=fSize)
    plt.colorbar(label=cbarLabel).ax.tick_params(labelsize=10)
    plt.xlabel(xLabel,fontsize=15 )#[\u03bcm]')
    plt.ylabel(yLabel,fontsize=15 )#[\u03bcm]')
    plt.title(label=title)
    plt.tight_layout()
    if savePath != None:
        print("Saving : ", savePath)
        plt.savefig(savePath)
    plt.show()

def testPlot2D():
    dirPath = '/home/jerome/dev/data/correctedCharacterisation/'
    #'/home/jerome/dev/data/aerialimages/' #'/home/jerome/dev/data/correctedCharacterisation/' #'/home/jerome/dev/experiments/beamPolarisation13/data/' #'/home/jerome/dev/data/sourceNdBeam/'
    
    files = ['intensityAfterMask.tif']
    #['farField.tif']    #['intensityATMask.tif', 'atBDA_200yintensity.tif'] # ['intensityAtExitAp.tif', 'intensityAtM3.tif', 'intensityAtExitSlits.tif']#, 'atBDA_200yintensity.tif'] #
    labels = None #['Exit Aperture Intensity', 'M3 Intensity', 'Exit Slits Intensity']
    res = [(11e-6,11e-6)]
    #[(3.3452615124385716e-07, 6.074644954894064e-06),(3.3452615124385716e-07, 6.074644954894064e-06)]
#     [(2.5011882651601634e-09, 2.426754806976689e-07),
#            (2.5011882651601634e-09, 2.426754806976689e-07)]
# #    [(2.5011765755127684e-09,2.426754715058574e-07)]
# #        [(1.3683879929232588e-05, 1.4105451618857176e-05),
# #           (1.3806530986264533e-05, 1.4150856529979121e-05),
# #           (1.5250285651236968e-05, 9.668362831086895e-06)]
#           (3.3452615124385716e-07, 6.074644954894064e-06)]

    fileType = 0      # 0 for tiff file, 1 for pickle file
    
    print(len(files))
    
    savepath = [dirPath + 'maskExit.eps']
    #[dirPath + 'farField.eps']#[None,None]# [dirPath + files[i][0:len(str(files[i])) - 4] + 'SE.png' for i in range(0,len(files))] 
    
    if fileType == 0:
        T = [tifffile.imread(dirPath + f) for f in files]
    elif fileType == 1:
        T = [pickle.load(open(dirPath + f, 'rb')) for f in files]
    else:
        pass
    
    Tnew = [resample(t, fx=1,fy=0.25) for t in T] #[resample(t, fx=0.024,fy=0.14) for t in T] 
    
    
    print(np.shape(T[0]))
    # print(np.shape(T[1]))
    print(np.shape(Tnew[0]))
    # print(np.shape(Tnew[1]))
    print(len(Tnew))
    
    
    for i, t in enumerate(Tnew):
        plotTwoD(t,
                dx = res[i][0],
                dy = res[i][1],
                sF = 1e3,
                describe = True,
                title= None, #labels[i],
                xLabel= 'x-position [mm]',#'x-position $[\mu m]$',
                yLabel= 'y-position [mm]',#'y-position $[\mu m]$',
                numXticks= 3,
                numYticks= 5,
                aspct = 0.0125,
#                colour = 'gray',
                cbar=False,
                cbarLabel= 'Intensity [ph/s/.1\%bw/mm²]',
                rotate=True,
                dpi=800,
                savePath = savepath[i] )#'Intensity [ph/s/.1%bw/mm²]')
        print(np.shape(t[int(np.shape(t)[0]/2),:]))
    
    # plotOneD([t[int(np.shape(t)[0]/2),:] for t in Tnew],
    #          d=[res[0][0]],
    #          sF=1e6)
    
    # print([(np.max(t[int(np.shape(t)[0]/2),:])-np.min(t[int(np.shape(t)[0]/2),:]))/np.max(t[int(np.shape(t)[0]/2),:]) for t in Tnew])

def testMultiTwoD():
    # rcParams['figure.dpi']=300
    dirPath = '/home/jerome/dev/data/correctedRoughness/'
    #'/home/jerome/dev/data/aerialImages/LER/'
    #'/home/jerome/dev/data/correctedRoughness/' #'/home/jerome/dev/experiments/beamPolarisation13/data/' #'/home/jerome/dev/data/sourceNdBeam/'
    
    files = [str(i) + 'intensity.tif' for i in [20,22,24]]
    #[str(i) + 'intensity.tif' for i in [20,22,24]] #LER
    #['rms' + str(n) + 'AerialImageNEW.pkl' for n in [10,20,30,40]] #SURFACE ROUGHNESS
    #['20NILS.pkl', '22NILS.pkl' , '24NILS.pkl']#['imagePlaneintensity.tif'] # ['intensityAtExitAp.tif', 'intensityAtM3.tif', 'intensityAtExitSlits.tif']#, 'atBDA_200yintensity.tif'] #
    labels = None
    #None #['Exit Aperture Intensity', 'M3 Intensity', 'Exit Slits Intensity']
    res = [(2.5011882651601634e-09, 2.426754806976689e-07),
            (2.5011882651601634e-09, 2.426754806976689e-07),
            (2.5011882651601634e-09, 2.426754806976689e-07)]

    fileType = 0      # 0 for tiff file, 1 for pickle file
    
    # print(len(files))
    
    savepath = dirPath + 'closeUpSurfaceRoughnessAerialImages.eps'
    # dirPath + 'closeUpLERAerialImages.eps'
    #dirPath + 'closeUpSurfaceRoughnessAerialImages.eps'
    #dirPath + 'LERimages.png' 
    #None 
    #dirPath + 'NILSnew.png'
    
    if fileType == 0:
        T = [tifffile.imread(dirPath + f) for f in files]
        mid = [196,12188]
    elif fileType == 1:
        picks = [pickle.load(open(dirPath + f, 'rb')) for f in files]
        T = [p[0].T for p in picks]
        res = [p[1] for p in picks]
        mid = [p[2] for p in picks]
        print(mid)
    else:
        pass
    print(np.shape(T))
    
    # mid = [196,12188]
    #mid[0] 
    # [196,12188]
    
    # print(mid[0])
    # print(mid[1])
    # T1 = np.array(resample(T[0], fx=1,fy=0.14, mid=mid))#, debug=True, show=True))
    # T2 = np.array(resample(T[0], fx=0.032,fy=0.14, mid=mid))
    # print(np.shape(T1))
    # print("HERE")
    # print(np.shape(T2))
    # Tnew = [T1,T2]

    Tnew = [np.array(resample(t, fx=0.00415, fy=0.085, midX=mid[1], midY=mid[0])).T for t in T]
    # [np.array(resample(t, fx=0.94, fy=0.05,show=False,debug=False)) for t in T] #LER
    # [np.array(resample(t, fx=0.00415, fy=0.085, midX=mid[1], midY=mid[0])).T for t in T]  # SURFACE ROUGHNESS
    # [np.array(resample(t, fx=0.05, fy=1.0,show=False,debug=False)) for t in T]
    # [np.array(resample(t, fx=0.0165, fy=0.085, mid=mid)) for t in T]
    
#    for t in Tnew:
#        plt.imshow(t,aspect='auto')
#        plt.show()
    
    
    plotMultiTwoD(Tnew,
            dims=[1,3],
            dx = [r[1] for r in res], #[r[0]*8.5 for r in res],
            dy = [r[0] for r in res],#[r[1]*1.02 for r in res],
            sF = 1e6,
            describe = True,
            title= None, #labels[i],
            xLabel= 'x-position $[\mu m]$',
            yLabel= 'y-position $[\mu m]$',
            fSize=15,
            numXticks= 3,
            numYticks= 5,
            onlyEdgeLabels= True,
            aspct ='auto',
#                colour = 'gray',
            cBar = None,#'bottom', # None,#'side', #'bottom',
            cbarLabel= None,#'Intensity [ph/s/.1\%bw/mm²]', #'NILS', #'Intensity [ph/s/.1\%bw/mm²]',
            # multiCBar= False,
            savePath = savepath)#'Intensity [ph/s/.1%bw/mm²]')

def testPlot1D():
    dirPath = '/home/jerome/dev/data/sourceNdBeam/'
    #'/home/jerome/dev/data/correctedCharacterisation/' #'/home/jerome/dev/experiments/beamPolarisation13/data/' #'/home/jerome/dev/data/sourceNdBeam/'
    electrons = [100,1000,2000,3000,4000,5000,10000]
    files = ['100umSSAintensity.tif','200umSSAintensity.tif','300umSSAintensity.tif']
    #['imagePlaneintensity.tif'] #[str(e) + '.pkl' for e in electrons]#['20_cy10.pkl','21_cy10.pkl','22_cy10.pkl','23_cy10.pkl','24_cy10.pkl'] #['100umSSAintensity.tif','200umSSAintensity.tif','300umSSAintensity.tif'] #'NormalisedIx.pkl','xProf.pkl']
    labels = None #['TE','TM'] # ['$100$ $\mu m$ $SSA$','$200$ $\mu m $ $SSA$','$300$ $\mu m$ $SSA$'] #['normalised intensity (y=0)', 'horizontal coherence']
    res = [2.5011882651601634e-09,2.5011882651601634e-09] #coherenceAE[2.4986984256410265e-09, 2.5011882651601634e-09, 2.5053583133791704e-09] #[3.3452615124385716e-07]
    
    mid = [(196,12189)]
#        [(196,12544-354),
#         (196,12544-356),
#         (196,12544-359)]
    
    fileType = 0      # 0 for tiff file, 1 for pickle file
    resnmidIncluded = False
    getContrast = True
    
    savePath = None #dirPath + 'cLengthsNEW.png' #'/home/jerome/Documents/MASTERS/Figures/plots/'
    
    if fileType == 0:
        t = [tifffile.imread(dirPath + f) for f in files]
        newt = [np.array(resample(T, fx=0.0165,fy=1, mid=m)) for T, m in zip(t, mid)]
        ps = [getLineProfile(T, axis=1, show=False) for T in newt]
        
    elif fileType == 1:
        if resnmidIncluded:
            ps = [pickle.load(open(dirPath + f, 'rb'))[0] for f in files]
            res = [pickle.load(open(dirPath + f, 'rb'))[1][0] for f in files]
            mid = [pickle.load(open(dirPath + f, 'rb'))[2][1] for f in files]
        else:
            ps = [pickle.load(open(dirPath + f, 'rb')) for f in files]
    
    import jerome.dev.scripts.interferenceGratingModelsJK as interferenceGratingModelsJK
    # ps = [[p for p in ps],IP]
    # ps = [[p*1e6 for p in ps[0][0:6]], [p*1e6 for p in ps[1][0:4]]]
    M = 200
    # # print("HERE")
    # # print(mid)
    # # print("shape of profiles (1,2): ", np.shape(ps[0]), np.shape(ps[1]))
    ps = [p[int(len(p)/2-M):int(len(p)/2+M)] for p in ps]
    # print("shape of ps: ", np.shape(ps))
    # ps = ps[0][int(len(ps)/2-M):int(len(ps)/2+M)]
    xP = [np.linspace(-M*r, M*r,2*M) for r in res]
    # print("shape of profiles (1,2): ", np.shape(ps[0]), np.shape(ps[1]))
    # print("shape of xP (1,2): ", np.shape(xP[0]), np.shape(xP[1]))
    
    
    # n = int(len(ps[0])/2)
    n = int(len(ps[0])/2)
    print(n)
    print(res)
    wl = 6.710553853647976e-9 # wavelength in m
    # xP = np.linspace(-n*res[0], n*res[0],n*2)
    A = 5.15e5 # Amplitude of both beams (assumed equal) this may be scaled to  match simulated intensity
    k = 2*np.pi/wl
    m = 1 # order of diffracted beams from each grating
    d = 100e-9 #24e-9 #100e-9 # grating spacing
    theta = np.arcsin(m*wl/d) # angle between the beams from each grating
    IP = interferenceGratingModelsJK.interferenceIntensity(xP[0],k,theta,A=A)
    
    # tiffAE = tifffile.imread(dirPath + 'idealintensity.tif')
    # # imageAE = tiffAE[mid[0]-1:mid[0]+1,mid[1]-M:mid[1]+M]
    # print("MID: ", mid[0], mid[1])
    # imageAE = tiffAE[196-1:196+1,mid[1]-M:mid[1]+M]#imageAE.mean(0)
    # profileAE = imageAE.mean(0)
    # xAE = np.linspace(-M*res[0], M*res[0],2*M)
    
    ps = [ps[0],IP]
    # xP = [xP, xP]
    # for i, p in enumerate(ps):
    #     print(np.shape(xP[i]))
    #     print(np.shape(p))
    #     plt.plot(xP[i],p)
    # plt.show()
    plotOneD(ps, 
             d=res, 
             sF = 1e6,
             xlim= [-500,500], #[0,len(ps[0])],
             ylim= None, #,[0,1.2e12],
             describe = True,
             split = None,
             customX = [x*1e9 for x in xP],
             title = None,
             labels = labels,
             xLabel= ['SSA Width [$\mu m$]'],#['Position [nm]'],
             yLabel= ['Coherence Length [$\mu m$]'],# ['Intensity [ph/s/.1\%bw/mm²]']],
             lStyle=['-',':'],
             lWidth= 1,
             pStyle='', #'',
             fSize=10,
             aspct = 'auto',
             savePath= savePath)
    
    if getContrast:
        Cm = [interferenceGratingModelsJK.gratingContrastMichelson(p) for p in ps]
        Crms = [interferenceGratingModelsJK.gratingContrastRMS(p) for p in ps]
        NILS = [interferenceGratingModelsJK.NILS(p, x, 50e-9) for p, x in zip(ps, xP)]
        print(Cm)
        print(Crms)
        print(NILS)
        
        # plt.gca().set_aspect(10)
        fig, ax = plt.subplots(1,2)
        ax[0].plot(electrons,Cm, 'x:')
        ax[0].set_title('Michelson', fontsize=15)
        ax[0].set_xlabel('$N_e$', fontsize=15)
        ax[0].set_ylabel('Contrast', fontsize=15)
        ax[1].plot(electrons,Crms, 'x:')
        ax[1].set_title('RMS', fontsize=15)
        ax[1].set_xlabel('$N_e$', fontsize=15)
        # ax[1].set_ylabel('Contrast', fontsize=15)
        # ax[0].set_yticklabels(labels=[round_sig(c,3) for c in Cm], fontsize=15)
        # ax[1].set_yticklabels(labels=[round_sig(c,3) for c in Crms], fontsize=15)
        ratio = 1.0
        for a in ax:
            # a.set_xticklabels(labels=electrons,fontsize=10)
            xleft, xright = a.get_xlim()
            ybottom, ytop = a.get_ylim()
            a.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)
        # plt.gca().set_aspect('equal')
        plt.tight_layout()
        
        plt.show()
        
        # print("TE contrast: ", C[0])
        # print("TM contrast: ", C[1])
        

def testCorrelationMap():
    dirPath = '/home/jerome/dev/data/BEUVcoherenceRoughness/'
#    '/home/jerome/dev/data/BEUVcoherenceLER/'
    # '/home/jerome/dev/data/BEUVcoherenceRoughness/'
    file = 'dataStructureNEW_50.pkl'
    labels =  ['$\sigma$', '$c_y$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$Fidelity$', '$NILS$', '$NILS_{\sigma_n}$', '$LWR$', '$\eta_{m=0}$', '$\eta_{m=\pm1}$']
     # ['$\sigma$','$c_y$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$Fidelity$', '$NILS$', '$NILS_{\sigma_n}$', '$LWR$','$Eff$']
    #['$\sigma$', '$c_y$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$Fidelity$', '$NILS$', '$NILS_{\sigma_n}$', '$LWR$']
    
    savePath = '/home/jerome/dev/data/BEUVcoherenceRoughness/50um_'
    pick = pickle.load(open(dirPath + file, 'rb'))
#    print(pick[1])
    
#    pick[1] = [10,10,10,10,10, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8]

    plotCorrelationMap(DS = pick, 
                       labels = labels, 
                       colours='Greys', 
                       ran = [0,1], 
                       labelSize = [8,8],
                       labelRot = [0,0],
                       annot=True, 
                       annotScale= 1,
                       savePath=savePath)
    
    
def testMultiCorrelationMap():
    dirPath = '/home/jerome/dev/data/BEUVcoherenceRoughness/'
#    '/home/jerome/dev/data/BEUVcoherenceLER/'
    # '/home/jerome/dev/data/BEUVcoherenceRoughness/'
    files = ['dataStructureNEW.pkl','dataStructureNEW_50.pkl']
    labels =  ['$\sigma$', '$c_y$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$Fidelity$', '$NILS$', '$NILS_{\sigma_n}$', '$LWR$', '$\eta_{m=\pm1}$','$D$']
#     ['$\sigma$', '$c_y$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$Fidelity$', '$NILS$', '$NILS_{\sigma_n}$', '$LWR$', '$\eta_{m=0}$', '$\eta_{m=\pm1}$']
    D = [27.5,27.5,27.5,27.5,27.5,
         27.5,27.5,27.5,27.5,27.5,
         27.5,27.5,27.5,27.5,27.5,
         27.5,27.5,27.5,27.5,27.5,
         27.5,27.5,27.5,27.5,27.5,
         50.0,50.0,50.0,50.0,50.0,
         50.0,50.0,50.0,50.0,50.0,
         50.0,50.0,50.0,50.0,50.0,
         50.0,50.0,50.0,50.0,50.0,
         50.0,50.0,50.0,50.0,50.0]
    
    savePath = '/home/jerome/dev/data/BEUVcoherenceRoughness/combined_'
    picks = [pickle.load(open(dirPath + f, 'rb')) for f in files]
    
#    print(np.shape(picks))
#    print(picks[1])
    P = []
    for p in picks[1]:
#        print(p)
        p = [p[5],p[6],p[7],p[8],p[9],
             p[10],p[11],p[12],p[13],p[14],
             p[15],p[16],p[17],p[18],p[19],
             p[20],p[21],p[22],p[23],p[24],
             p[0],p[1],p[2],p[3],p[4]]
#        print("NEW")
#        print(p)
        P.append(p)
#    print(picks[1])
#    picks[1][1] = []
    picks[1] = P
#    print("HERE")
#    print(picks[0])
#    print(picks[1])
    picks[1] = [picks[1][0],picks[1][1],picks[1][2],picks[1][3],picks[1][4],picks[1][5],picks[1][6],picks[1][7],picks[1][8],picks[1][9]]
    
    s = []
    c = []
    Cm = []
    Crms = []
    Cc = []
    F = []
    NILS = []
    NILSs = []
    LWR = []
    eta = []
    
    for p in picks:
#        print(np.shape(p))
        print(p[1])
        s.append(p[0])
        c.append(p[1])
        Cm.append(p[2])
        Crms.append(p[3])
        Cc.append(p[4])
        F.append(p[5])
        NILS.append(p[6])
        NILSs.append(p[7])
        LWR.append(p[8])
        eta.append(p[9])
        
    DS = [s,c,Cm,Crms,Cc,F,NILS,NILSs,LWR,eta,D]
    
#    print(np.shape(DS))
    for i,d in enumerate(DS):
#        print(np.array(DS[i]).flatten())
        DS[i] = np.array(DS[i]).flatten()
    
#    print("HERE")
#    print(np.shape(DS))
#    print(np.shape(s))
#    print(DS)
#    print(pick[1])
    
#    pick[1] = [10,10,10,10,10, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8]

    plotCorrelationMap(DS = DS, 
                       labels = labels, 
                       colours='Greys', 
                       ran = [0,1], 
                       labelSize = [8,8],
                       labelRot = [0,0],
                       annot=True, 
                       annotScale= 1,
                       savePath=savePath)

def testMultiOneD():
    
    # rcParams['figure.dpi']=300
    dirPath = '/home/jerome/dev/data/LER/'
    # '/home/jerome/dev/data/maskLER2/'
    # '/home/jerome/dev/data/BEUVcoherenceLER/'
    # '/home/jerome/dev/data/BEUVcoherenceRoughness/'
    # '/home/jerome/Downloads/'
    #'/Users/jknappett/Downloads/'
    #'/home/jerome/dev/data/aerialImages/'
    #'/home/jerome/dev/data/correctedRoughness/'
    
     #MULTIPLE
    files = ['dataStructuremaskLER2NEW.pkl','dataStructureEUVmaskLER1NEW.pkl']
    #['dataStructureNEW.pkl','dataStructure50NEW.pkl']
    #['dataStructuremaskLER2NEW.pkl','dataStructureEUVmaskLER1NEW.pkl']
     #[ 'contrastMetrics.pkl', 'contrastMetrics350.pkl']
    
#    # #SINGLE
#    file = 'dataStructure50NEW.pkl'
#    #'dataStructuremaskLER2NEW.pkl'
#    #'contrastMetrics350.pkl'
#    #'dataStructureLER1.pkl'
#    #'contrastMetrics.pkl'
#    #'dataStructureNEW.pkl'
    
    labelX = '$\sigma [nm]$'
    #'$d$'
    #'$\sigma [nm]$'
    #labelY = ['$1 - Fidelity$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$NILS_{mean}$', '$NILS_{\sigma_n}$', '$LWR$']
    #labelY = ['$1 - Fidelity$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$NILS_{mean}$', '$LWR$']
    labelY = ['$C_{Composite}$', '$Fidelity$', '$NILS$', '$LWR$', '$\eta_{\pm 1}$','$NILS_{\sigma_n}$']
#    ['$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$Fidelity$', '$NILS$', '$NILS_{\sigma_n}$', '$LWR$','$Eff$']
    #['$NILS_{mean}$', '$C_{Composite}$', '$NILS_{\sigma_n}$', '$LWR [nm]$']
    #['NILS', 'LWR  [nm]']
    #['$C_{M}$','$C_{RMS}$','$NILS_{mean}$', '$C_{Composite}$']
#    ['$NILS_{mean}$', '$C_{Composite}$', '$NILS_{\sigma_n}$', '$LWR [nm]$']
    legend = ['$6.7 \ nm$','$13.5 \ nm$']
#    ['$c_y  = 2$','$c_y = 4$','$c_y = 6$','$c_y = 8$','$c_y = 10$']
#    ['$D = 27 \mu m$','$D = 50 \mu m$']
#    ['$c_y  = 2$','$c_y = 4$','$c_y = 6$','$c_y = 8$','$c_y = 10$']
    #['$c_y = 10$','$c_y  = 2$','$c_y = 4$','$c_y = 6$','$c_y = 8$']
    #['$6.7 \ nm$','$13.5 \ nm$']
    #['$6.7 \ nm$','$13.5 \ nm$']
    #['dx = 2.50 nm', 'dx = 1.25 nm']
    #['$\Delta SSA_x = 350 \mu m$','$\Delta SSA_x = 50 \mu m$'] 
    #None #['$c_y  = 2$','$c_y = 4$','$c_y = 6$','$c_y = 8$','$c_y = 10$']
    
    savePath = '/home/jerome/Documents/OneDrive/Documents/PhD/Figures/forPapers/AImetricsLER.pdf'
    #'/home/jerome/onedriver/Documents/PhD/Figures/forPosters/contrastLERNILSLWR_4metrics.eps'
    #'/home/jerome/Documents/OneDrive/Documents/PhD/Figures/forPosters/contrastLERNILSLWR.eps'
    #'/home/jerome/Documents/OneDrive/Documents/PhD/Figures/forPosters/LERbothWlengthNILSLWR.png'
    # None
    #'/home/jerome/Documents/OneDrive/Documents/PhD/Figures/forPosters/CoherenceContrast.png'
    #'/home/jerome/dev/data/correctedRoughness/contrastWithoutLWR.png'
    
     # # #MULTIPLE
    picks = [pickle.load(open(dirPath + f, 'rb')) for f in files]
    
#    #SINGLE
#    pick = pickle.load(open(dirPath + file, 'rb'))
# #        
#     sigma = 0
#     cy = 1
#     michelson = 2#1#2
#     rms = 3#2#3
#     composite = 4#3#4
#     fidelity = 5
#     nils = 6
#     _nils = 7#4#7
#     lwr = 8
#     eff = 9
    
    sigma = 0
    michelson = 1
    rms = 2
    composite = 3
    fidelity = 4
    nils = 5
    _nils = 6
    lwr = 7
    eff = 8

    
    #['$\\sigma$', '$c_y$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$Fidelity$', '$NILS$', '$NILS_{\\sigma_n}$', '$LWR$']
    
    
    # # #MULTIPLE
    # A = [[p[composite][1:8],p[fidelity][1:8],p[nils][1:8],p[lwr][1:8],p[eff][1:8]/p[eff][0],p[_nils][1:8]] for p in picks]
    A = [[p[composite][1:8],p[fidelity][1:8],p[nils][1:8],p[lwr][1:8],p[eff][1:8],p[_nils][1:8]] for p in picks]
#    A = [[p[composite][1::],p[fidelity][1::],p[nils][1::],p[lwr][1::],p[_nils][1::]] for p in picks]
    # A = [[p[composite-1],p[fidelity-1],p[nils-1],p[lwr-1],p[eff-1],p[_nils-1]] for p in picks]
#    A = [[p[composite][0:5],p[fidelity][0:5],p[nils][0:5],p[lwr][0:5],p[eff][0:5],p[_nils][0:5]] for p in picks]
#    A = [[p[nils],p[composite],p[_nils],p[lwr]] for p in picks]
#    A = [A[0][0][1::] + A[1][0][1::],A[0][1][1::] + A[1][1][1::], A[0][2][1::] + A[1][2][1::], [a*1e9 for a in A[0][3][1::] + A[1][3][1::]]]
    #[A[0][0][1::] + A[1][0][1::],[a*1e9 for a in A[0][1][1::] + A[1][1][1::]]] #A[0][1][1::] + A[1][1][1::]]
    # #[[p[michelson],p[rms],p[nils],p[composite]] for p in picks]
    
#    #SINGLE
#    #A = [[1 - p for p in pick[5]], pick[2], pick[3], pick[4], pick[6], pick[7], pick[8]]
#    #A = [[1 - p for p in pick[5]], pick[2], pick[3], pick[4], pick[6], pick[8]]
##    A = [pick[nils],[p*1e9 for p in pick[lwr]]]
#    # A = [pick[michelson],pick[rms],pick[nils], pick[composite]]
#    # A = [pick[michelson-1],pick[rms-1],pick[composite-1],pick[fidelity-1],pick[nils-1],pick[_nils-1],pick[lwr-1],pick[eff-1]]
##    A = [pick[michelson],pick[rms],pick[composite],pick[fidelity],pick[nils],pick[_nils],pick[lwr],pick[eff]]
#    A = [pick[composite],pick[fidelity],pick[nils],pick[lwr],pick[eff],pick[_nils]]
    
     # # #MULTIPLE
    X = [p[0][1:8] for p in picks]
    X = X[0]#[1::]
    
#    # SINGLE
#    X = pick[0][0:5]
#    pick[0] 
##    [50,75,100,125,150,175,200,300]#pick[0]
    
#    print(np.shape(A))
#    
#    for a in A:
#        print(a)
##        b = np.reshape(a,[5,5])
###        print(np.shape(b))
#    print(X)
##    
    plt.plot(X,A[0][0],'x:')
    plt.plot(X,A[1][0],'x:')
    plt.show()
#    
#    # print(A)
    
    plotMultiOneD(p=A, 
                  X=X,
                  dims = [2,3], 
                  d=1, 
                  split=[6,7], #[5,5] 
                  describe=True,
                  titles=None,
                  legend=legend, 
                  xLabel=labelX, 
                  yLabel=labelY, 
                  lineStyle=':',
                  pointStyle='x',
                  fSize=12,
                  aspct='auto', 
                  savePath=savePath)
    
def testComplex():
    import c2image
    dirPath = '/user/home/opt/xl/xl/experiments/correctedAngle_coherence4/data/sx100sy100/'
    # '/home/jerome/Downloads/' 
    #'/home/jerome/dev/data/Efields/'
    # '/home/jerome/Downloads/' 
    #'/home/jerome/dev/experiments/beamPolarisation13/data/' 
    #'/home/jerome/dev/data/sourceNdBeam/'
    
    files = ['sx100sy100EfieldsNEW.pkl']
    #['aerialImageEfieldEfields.pkl']
    #['sx100sy100Efields.pkl']
    #['aerialImageEfieldEfieldsNEW.pkl']
    #['farFieldEfieldEfieldsNEW.pkl']
    #['aerialImageEfieldEfieldsNEW.pkl','beforeBDA_efield_sx200sy200_10000eEfieldsNEW.pkl','maskExitEfieldEfieldsNEW.pkl']
    # ['beforeBDA_efield_sx200sy200EfieldsNEW.pkl','beforeBDA_efield_sx200sy200_10000eEfieldsNEW.pkl']#,'maskExitEfieldEfieldsNEW.pkl','aerialImageEfieldEfieldsNEW.pkl']
    #['Vgrad25000EfieldsNEW.pkl']
    #['atM1EfieldsNEW.pkl'] # ['intensityAtExitAp.tif', 'intensityAtM3.tif', 'intensityAtExitSlits.tif']#, 'atBDA_200yintensity.tif'] #
    labels = None #['Exit Aperture Intensity', 'M3 Intensity', 'Exit Slits Intensity']

    fileType = 1      # 0 for tiff file, 1 for pickle file
    savepathImage =None# dirPath + 'atMask100x100Complex.eps'
    savepathIntensity = None#dirPath + 'atMask100x100Intensity.eps'
    #dirPath + 'farFieldComplex.eps'
    #None
    #[dirPath + s for s in['aerialImageComplex.eps','atMaskComplex.eps','maskExitComplex.eps']]
    savepathCbar = None
    #dirPath + 'aerialImageCloseCbar.eps'
    #dirPath + 'farFieldCbar.eps'
    #None
    #[dirPath + s for s in['aerialImageCbar.eps','atMaskCbar.eps','maskExitCbar.eps']]
    
    if fileType == 0:
        T = [tifffile.imread(dirPath + f) for f in files]
    elif fileType == 1:
        T = [pickle.load(open(dirPath + f, 'rb')) for f in files]
        EhR = [p[0] for p in T]
        EhI = [p[1] for p in T]
        EvR = [p[2] for p in T]
        EvI = [p[3] for p in T]
        res = [(p[4],p[5]) for p in T]
        Eh = [eR + eI*1j for eR,eI in zip(EhR,EhI)]
        Ev = [eR + eI*1j for eR,eI in zip(EvR,EvI)]
        # E = [np.sqrt((h**2) + (v**2)) for h,v in zip(Eh,Ev)]
        E = [eh + ev for eh,ev in zip(Eh,Ev)]
    else:
        pass
    
    print(res)
    
    for i, e in enumerate(E):
        
#         plotComplex2D(e,
#                 dx = res[i][0],
#                 dy = res[i][1],
#                 sF = 1e6,
#                 describe = True,
#                 title= None, #labels[i],
#                 xLabel= 'x-position $[\mu m]$',
#                 yLabel= 'y-position $[\mu m]$',
#                 numXticks= 5,
#                 numYticks= 5,
#                 aspct = 'auto',
# #                colour = 'gray',
#                 cbarLabel= 'Intensity [ph/s/.1\%bw/mm²]',
#                 savePath = savepath[i] )#'Intensity [ph/s/.1%bw/mm²]')
# #        print(np.shape(t[int(np.shape(t)[0]/2),:]))
        
        # e = resample(e,fx=0.033,fy=0.125,midX=12188)
    
        cIm = c2image.c2image(e)
        cBar,di,dP,dA = c2image.complexCbar(e,1000)
        
        plotTwoD(cIm,
                 dx=res[i][0],
                 dy=res[i][1],
                 sF=1e6,
                 xLabel='x-position $[\mu m]$',#'x-position [nm]', #'x-position $[\mu m]$',
                 yLabel='y-position $[\mu m]$',#'y-position [nm]', #'y-position $[\mu m]$',
                 cbar=False,
                 aspct=5.0,#'auto',
                 savePath=savepathImage)#[i])
        
        plotTwoD(cBar,
                 dx=dA,
                 dy=dP,
                 xLabel='Amplitude  $[|A|]$',
                 yLabel='Phase [rad]',
                 numXticks=3,
                 numYticks=5,
                 cbar=False,
                 aspct=3,
                 savePath=savepathCbar)#[i])
        
        
        plotTwoD(np.abs(e)**2,
                 dx=res[i][0],
                 dy=res[i][1],
                 sF=1e6,
                 xLabel='x-position $[\mu m]$',#'x-position [nm]', #'x-position $[\mu m]$',
                 yLabel='y-position $[\mu m]$',#'y-position [nm]', #'y-position $[\mu m]$',
                 cbar=True,
                 aspct='auto',
                 savePath=savepathIntensity)#[i])
        
        # cIm = resample(cIm,fx=0.01,fy=0.125)
        
        plt.imshow(cIm,aspect='auto')
        # plt.colorbar()
        # plt.savefig('const_chroma.jpeg')
        plt.show()
        
        # c2image.complexCbar(e)
        
        plt.imshow(np.angle(e),aspect='auto')
        plt.colorbar()
        plt.show()
        plt.imshow(np.abs(e)**2,aspect='auto')
        plt.colorbar()
        # plt.savefig(dirPath + 'atMask100x100Intensity.eps')
        plt.show()

if __name__ == "__main__":
    # testPlot2D()
    # testPlot1D()
#     testCorrelationMap()
#     testMultiCorrelationMap()
    # testMultiOneD()
#     testMultiTwoD()
    testComplex()
    
