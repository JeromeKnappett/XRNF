#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 11:03:50 2017

@author: gvanriessen
"""
#uncomment for Jupyter notebook
#%matplotlib notebook

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

#Importing necessary modules:
import os
import sys
sys.path.insert(0,os.path.join('..','..'))

import time
import copy
import numpy as np
import matplotlib.pyplot as plt
import itertools

import numexpr as ne


try:
    from wpg import srwlpy as srwl
except ImportError:
    import srwlpy as srwl  #  Hack for read the docs


#import SRW core functions
from wpg.srwlib import SRWLOptD,SRWLOptA,SRWLOptC,SRWLOptT,SRWLOptL,SRWLOptMirEl, SRWLOptZP

#import SRW helpers functions
#from wpg.useful_code.srwutils import AuxTransmAddSurfHeightProfileScaled


from wpg.useful_code.wfrutils import calculate_fwhm_x, plot_wfront, calculate_fwhm_y, print_beamline, get_mesh, plot_1d, plot_2d
from wpg.useful_code.wfrutils import propagate_wavefront

from wpg import wavefront, beamline #Wavefront, Beamline
from wpg.generators import build_gauss_wavefront_xy #Gaussian beam generator
from wpg.optical_elements import Empty, Use_PP
from wpg.wpg_uti_wf import *

from beautifultable import BeautifulTable


J2EV = 6.24150934e18




def timeit(method):
    # implements @timeit decorator:
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()        
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r  %2.2f ms' %   (method.__name__, (te - ts) * 1000))
        return result    
    
    return timed
    
    
def mkdir_p(path):
    """
    Create directory tree, if not exists (mkdir -p)

    :param path: Path to be created
    """
    if path == '':
        return
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def calculate_fwhm(wfr):
    """
    Calculate FWHM of the beam calculating number of point bigger then max/2 throuhgt center of the image

    :param wfr:  wavefront
    :return: {'fwhm_x':fwhm_x, 'fwhm_y': fwhm_y} in [m]
    """
    intens = wfr.get_intensity(polarization='total').sum(axis=-1);


    mesh = wfr.params.Mesh
    dx = (mesh.xMax-mesh.xMin)/mesh.nx
    dy = (mesh.yMax-mesh.yMin)/mesh.ny

    x_center = intens[intens.shape[0]//2,:]
    fwhm_x = len(x_center[x_center>x_center.max()/2])*dx

    y_center = intens[:,intens.shape[1]//2]
    fwhm_y = len(y_center[y_center>y_center.max()/2])*dy
    return {'fwhm_x':fwhm_x, 'fwhm_y': fwhm_y}

def get_intensity_on_axis(wfr):
    """
    Calculate intensity (spectrum in frequency domain) along z-axis (x=y=0)

    :param wfr:  wavefront
    :return: [z,s0] in [a.u.] if frequency domain
    """

    wf_intensity = wfr.get_intensity(polarization='horizontal')
    mesh = wfr.params.Mesh;
    zmin = mesh.sliceMin;
    zmax = mesh.sliceMax;
    sz = numpy.zeros((mesh.nSlices, 2), dtype='float64')
    sz[:,0] = numpy.linspace(zmin, zmax, mesh.nSlices);
    sz[:,1] = wf_intensity[mesh.nx/2, mesh.ny/2, :] / wf_intensity.max()

    return sz

def objOpt(obj):
    # wrapper function for  cleaning up code  a little bit - replace with custom class later.
    from wpg.srwl_uti_smp import srwl_opt_setup_transm_from_file

    opt =  srwl_opt_setup_transm_from_file(
                        obj.file_path,
                        obj.resolution,
                        obj.thickness,
                        obj.delta,
                        obj.atten_len,
                        xc=obj.xc if obj.contains('xc') else 0.0,
                        yc=obj.yc if obj.contains('yc') else 0.0,
                        area=obj.area  if obj.contains('area') else None,
                        rotate_angle=obj.rotate_angle  if obj.contains('rotate_angle') else None,
                        rotate_reshape=obj.rotate_reshape  if obj.contains('rotate_reshape') else None,
                        cutoff_background_noise=obj.cutoff_background_noise  if obj.contains('cutoff_background_Noise') else 0,
                        background_color=obj.background_color if obj.contains('background_color') else 0,
                        tile=obj.tile if obj.contains('tile') else None,
                        shift_x = obj.shift_x if obj.contains('shift_x') else None,
                        shift_y = obj.shift_y if obj.contains('shift_y') else None,
                        invert = obj.invert if obj.contains('invert') else None,
                        is_save_images = obj.is_save_images if obj.contains('is_save_images') else None,
                        prefix=obj.prefix if obj.contains('prefix') else None,
                        output_image_format=obj.output_image_format if obj.contains('output_image_format') else None
                        )

    return opt


class Struct:
    "A structure that can have any fields defined."
    def __init__(self, **entries): self.__dict__.update(entries)

    def contains(self,attrName):
        return (hasattr(self,attrName))


def get_transmissionFunctionCplx(tr):

    """
    Extract complex transmission function of  transmission object

    :param transmission: SRWLOptT struct, see srwlib.h
    :return: mag, phase tuple map of transmission object
    """

    mesh = tr.mesh
    nx = mesh.nx
    ny = mesh.ny
    phase = np.array(tr.arTr[1::2]).reshape((ny, nx))
    amplitude = np.array(tr.arTr[::2]).reshape((ny, nx))

    cplx = ne.evaluate("complex(phase, amplitude)")

    return cplx

def add_transmissionFunctions(trA,trB):

    return ne.evaluate("trA + trB")

def show_transmissionFunctionCplx(trCplx):
    from husl import complex_to_rgb
    rgb = complex_to_rgb(z=trCplx,amin=None,amax=None,mode='special',phstart=0.,sat=1.0,as_image=True)

    #make colour wheel:
    colorWheel = complex_to_rgb(z=None,amin=None,amax=None,mode='special',phstart=0.,sat=1.0,as_image=True)

    plt.figure(figsize=(10, 7))
    plt.subplot(121)
    plt.imshow(rgb)
    plt.title('Transmission Function');plt.xlabel('mm');plt.ylabel('mm')
    plt.subplot(122)
    plt.imshow(colorWheel)
    plt.title('Colorwheel (TODO: proper labelling');plt.xlabel('');plt.ylabel('')
    plt.show()


@timeit
def plotWavefront(wf, title, slice_numbers=False, cuts=False, interactive=False, phase = False):
    #draw wavefront with common functions
    #if phase = True, plot phase only

    print('Displaying wavefront...')

    if slice_numbers is None:
        slice_numbers = range(wf_intensity.shape[-1])

    if isinstance(slice_numbers, int):
        slice_numbers = [slice_numbers, ]


    [nx, ny, xmin, xmax, ymin, ymax] = get_mesh(wf)
    dx = (xmax-xmin)/(nx-1); dy = (ymax-ymin)/(ny-1)
    print('stepX, stepY [um]:', dx * 1e6, dy * 1e6, '\n')
    
    if phase == True:
        A = wf.get_phase(slice_number=0, polarization='horizontal')
        label = 'Phase (rad.)'
    else:
        ii = wf.get_intensity(slice_number=0, polarization='horizontal')
        ii = ii*wf.params.photonEnergy/J2EV#*1e3
        imax = numpy.max(ii)

        if wf.params.wEFieldUnit != 'arbitrary':
            #print('Total power (integrated over full range): %g [GW]' %(ii.sum(axis=0).sum(axis=0)*dx*dy*1e6*1e-9))
            #print('Peak power calculated using FWHM:         %g [GW]' %(imax*1e-9*1e6*2*numpy.pi*(calculate_fwhm_x(wf)/2.35)*(calculate_fwhm_y(wf)/2.35)))
            #print('Max irradiance: %g [GW/mm^2]'    %(imax*1e-9))
            label = 'Irradiance (W/$mm^2$)'
        else:
            ii = ii / imax
            label = 'Irradiance (a.u.)'
            
        A = ii    

        

    [x1, x2, y1, y2] = wf.get_limits()
    
    if (interactive == True):
        import mpld3
        from mpld3 import plugins              
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        im = ax.imshow(ii, extent=[x1 * 1e3, x2 * 1e3, y1 * 1e3, y2 * 1e3])
        fig.colorbar(im, ax=ax)
        
        fig = plt.figure()     
        ax.set_title(title, size=20)
        plugins.connect(fig, plugins.MousePosition(fontsize=14))
        mpld3.show()                
        #mpld3.display(fig)
        
    else: 
        pylab.figure(figsize=(21,6))
        pylab.imshow(A, extent=[x1 * 1e3, x2 * 1e3, y1 * 1e3, y2 * 1e3])
        pylab.set_cmap('hot')
        pylab.axis('tight')
        pylab.colorbar(orientation='horizontal')
        pylab.xlabel('x (mm)')
        pylab.ylabel('y (mm)')
        pylab.axes().set_aspect(0.5)
    
        pylab.title(title)
        pylab.show()

#
#
#    if wf.params.Mesh.nSlices==1:
#        dt = 1  # added because alternative results in in div by zero where only 1 slice exists
#    else:
#        dt = (wf.params.Mesh.sliceMax - wf.params.Mesh.sliceMin) / (wf.params.Mesh.nSlices - 1)
#
#    for sn in slice_numbers:
#        data = wf_intensity[:, :, sn]
#        data = data*dt
#        phase = wf_phase[:, :, sn]
#
#        plt.subplot(1,2,1)
#        plt.imshow(data)
#        plt.subplot(1,2,2)
#        plt.imshow(phase)
#        plt.show()
#
#    #draw wavefront with cuts
#    if cuts:
#        plot_wfront2(wf, title_fig=title,
#                    isHlog=False, isVlog=False,
#                    orient='x', onePlot=True,
#                    i_x_min=None, i_y_min=None)
#
#        plt.set_cmap('jet') #set color map, 'bone', 'hot', 'jet', etc
#        plt.show()




# function to allow more convenient use of default propgation parameters)
# all instances of this should be replaced with class Use_PP(object) in opticalElements.py:
def propagationParameters (
            AutoResizeBeforeProp = 0, # 0
            AutoResizeAfterProp  = 0, # 1
            RelPrecAutoresize = 1.0,  # 2
            SemiAnalyt = 0,           # 3
            ResizeFourierSide = 0,    # 4
            RangeX = 1.0,             # 5
            ResolutionX = 1.0,        # 6
            RangeY = 1.0,             # 7
            ResolutionY = 1.0,        # 8
            ShiftType = 0,            # 9
            ShiftX = 0,               # 10
            ShiftY = 0 ):             # 11


    # propagation parameter list & description:
    #[0]:  Auto-Resize (1) or not (0) Before propagation
    #[1]:  Auto-Resize (1) or not (0) After propagation
    #[2]:  Relative Precision for propagation with Auto-Resizing (1. is nominal)
    #[3]:  Allow (1) or not (0) for semi-analytical treatment of quadratic phase terms at propagation
    #[4]:  Do any Resizing on Fourier side, using FFT, (1) or not (0)
    #[5]:  Horizontal Range modification factor at Resizing (1. means no modification)
    #[6]:  Horizontal Resolution modification factor at Resizing
    #[7]:  Vertical Range modification factor at Resizing
    #[8]:  Vertical Resolution modification factor at Resizing
    #[9]:  Type of wavefront Shift before Resizing (not yet implemented)
    #[10]: New Horizontal wavefront Center position after Shift (not yet implemented)
    #[11]: New Vertical wavefront Center position after Shift (not yet implemented)



    pp  = [ AutoResizeBeforeProp, AutoResizeAfterProp, RelPrecAutoresize,
            SemiAnalyt,  ResizeFourierSide,
            RangeX,  ResolutionX ,
            RangeY,  ResolutionY,
            ShiftType, ShiftX, ShiftY]



    return pp


def pixelScale (lengthInMeters,metersPerPixel):
    return lengthInMeters/metersPerPixel

def joinContainers (opticalContainerList):
# concatenates list of SRWLOptC objects
# note that the beamline.append method could can be used instead of this
    oe = []
    pp = []
    for ocl in opticalContainerList:
        if ocl != None:
            oe.append(ocl.getOpticalElements())
            pp.append(ocl.getPropagationParameters())

    container = SRWLOptC(_arOpt=oe,_arProp=pp)

    return container




def meshDim(wf):
    """
    return wavefront mesh dimensions
    """
    wf_mesh = wf.params.Mesh
    return  wf_mesh.nx,  wf_mesh.ny



def modes2D(m,N):
    """
    return N pairs of Transverse Gauss-Hermite Mode Order pairs with order up to m.

    """
    A=list()
    for i in range(1,m+1):
       A.append ( list(itertools.product([0,i],repeat=2)))

    # combine
    A=list(itertools.chain.from_iterable(A))

    # remove duplicates
    temp = []
    for a,b in A:
        if (a,b) not in temp: #to check for the duplicate tuples
            temp.append((a,b))

    return temp[0:N]


def eigenvaluePartCoh(p_I, p_mu, n):
    """
    GVR

    return eigenvalue normalised to eigenvalue of fundamental

    definitions follow Starikov and Wolf, 1982:


    p_mu and p_I are the rms widths of the degree of coherence and of the intensity of the source.

    beta =  p_mu/p_I is a measure of the "degree of global coherence" of the source.

    When beta >> 1, the source is effectively spatially coherent in the global sense and is then
    found to be well represented by a single mode.
    When beta << 1, the source is effectively spatially incoherent in the global
    sense, and the number of modes needed to describe its behavior is of the order of beta/3

    """

    a = 1/(2*p_I**2)
    b = 1/(2*p_mu**2)
    c = (a**2 + 2*a*b)**(1/2)
    l_0=1.0

    l_n = l_0*(b/(a+b+c))**n

    return l_n

def plotEigenValues(e,_threshold):

    plt.plot(e,'bo')
    plt.plot(e[e>_threshold],'r+')
    plt.title('Eigenvalues')
    plt.xlabel('Mode')
    plt.ylabel('$\lambda/\lambda_0$')
    plt.legend(loc=2)
    plt.show()


def ZPf (D, drn, E, _n=1):

    """
    D is outer diamter [m]
    drn is width  of outer zone [m]
    E is energy [eV]
    _n is diffraction order (default 1])
    """

    w =  1.2398 / E   # use swrlib swrl_uti_ph_en_conv in future!
    f = ( D*(drn*1.0e6) ) / ( _n*w )
    return f


def writeCSV(wf, fn, _comment=''):

    np.savetxt(fn, wf, delimiter=',',comments=_comment)


def animateWF(wf,_filename=''):
    """
    wf should be a wf with multiple slices... For now (Testing) it is a list of image arrays
    if filename given a movie file will be saved
    """

    import matplotlib.animation as animation

    fig = plt.figure()

    ims = []

    for i in range(0,len(wf)-1):
        print(i)

        im = plt.imshow(wf[i], animated=True)
        ims.append([im])


    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=500)
    plt.show()

    if _filename != '':
        ani.save(_filename)



def constructWavefield(ekeV,
                       qnC,
                       z1,
                       range_xy,
                       strOutputDataFolder = None,
                       dimension=2,
                       beta = 0.7, # 'tunable' parameter — sets global degree of coherence
                       threshold = 0.8, # ignore modes with eigenvalue < this value
                       npoints=512,
                       nslices=10, display = True):
    """
    Define Transverse Optical Modes
    """
    k = 2*np.sqrt(2*np.log(2))
    wlambda = 12.4*1e-10/ekeV       # wavelength
    theta_fwhm = calculate_theta_fwhm_cdr(ekeV,qnC)
    sigX = 12.4e-10*k/(ekeV*4*np.pi*theta_fwhm)

    # coherence width:
    widthCoherence = beta * sigX

    # get first n eigenvalues for transverse modes
    n=99
    e0=eigenvaluePartCoh(sigX, widthCoherence, range(0,n))

    # keep only modes for which eigenvalue > threshold
    e = e0[e0>threshold]

    if display:
      plotEigenValues(e0,threshold)

    # generate mode indices
    modes = modes2D(9,N=len(e))


    dimension = 2  # value should be 3 for 3D wavefront, 2 for 2D wavefront
    wf=[]
    for mx,my in modes:

            #define unique filename for storing results
            ip = np.floor(ekeV)
            frac = np.floor((ekeV - ip)*1e3)

            #build initial gaussian wavefront
            if dimension==2:
                wfr0=build_gauss_wavefront_xy(nx=npoints, ny=npoints, ekev=ekeV,
                                              xMin=-range_xy/2 ,xMax=range_xy/2,
                                              yMin=-range_xy/2, yMax=range_xy/2,
                                              sigX=sigX, sigY=sigX,
                                              d2waist=z1,
                                              _mx=mx, _my=my
                                              )

            else:
                # build initial 3d gaussian beam
                tau =1 ; # not sure if this parameter is even used - check meaning.
                wfr0 = build_gauss_wavefront(nx=npoints, ny=npoints, nz=nslices, ekev=ekev,
                                             xMin=-range_xy/2 ,xMax=range_xy/2,
                                             yMin=-range_xy/2, yMax=range_xy/2,
                                             tau=tau,
                                             sigX=sigX, sigY=sigX,
                                             d2waist=z1,
                                            _mx=mx, _my=my)
                if display==True:
                    print( 'dy {:.1f} um'.format((mwf.params.Mesh.yMax-mwf.params.Mesh.yMin)*1e6/(mwf.params.Mesh.ny-1.)))
                    print( 'dx {:.1f} um'.format((mwf.params.Mesh.xMax-mwf.params.Mesh.xMin)*1e6/(mwf.params.Mesh.nx-1.)))
                    plot_t_wf(mwf)
                    look_at_q_space(mwf)

            #init WPG Wavefront helper class
            mwf = Wavefront(wfr0)

            #store wavefront to HDF5 file
            if strOutputDataFolder:
                fname0 = 'g' + str(int(ip))+'_'+str(int(frac)) +'kev' + '_tm' +str(mx) + str(my)
                ifname = os.path.join(strOutputDataFolder,fname0+'.h5')
                mwf.store_hdf5(ifname)
                print('Saved wavefront to HDF5 file: {}'.format(ifname))
            else:
                ifname = None

            wf.append( [mx,my,ifname,mwf] )

            #plotWavefront(mwf, 'at '+str(z1)+' m')
            #look_at_q_space(mwf)

            fwhm_x = calculate_fwhm_x(mwf)
            print('FWHMx [mm], theta_fwhm [urad]: {}, {}'.format(fwhm_x*1e3,fwhm_x/z1*1e6))

            #show_slices_hsv(mwf, slice_numbers=None, pretitle='SLICETYSLICE')



            return wf, modes, e



def writeIntensity(wavefield,label,path='./out',polarization='horizontal',imgType='tif'):

    from slugify import slugify
    import imageio
    import os


    #imageio.imwrite(os.path.join(path, slugify(label)+'.'+imgType),
    #                wavefield.get_intensity(polarization=polarization))
    
    imageio.imwrite(os.path.join(path, label +'.'+imgType),
                    wavefield.get_intensity(polarization=polarization))

