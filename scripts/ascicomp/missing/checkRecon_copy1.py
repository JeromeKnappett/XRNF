
import h5py
import matplotlib.pyplot as plt
plt.ion()
import numpy as np
# import propagators as props
from math import floor, log10
import tifffile
from matplotlib.colors import LogNorm
try:
    import ptypy
except:
    pass
from scipy.signal import windows as wins
import inspect
from plot_complex_colourbar import plotComplexWithColorbar
# print(inspect.getsource(plotComplexWithColorbar))
# print(plotComplexWithColorbar.__code__.co_filename)
#from FWarbValue import getFWatValue
import pickle
# from tqdm import tqdm
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap

# %%
def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
            return x

def rotate_cyclic_cmap(cmap, offset, N=256):
    vals = cmap(np.linspace(0, 1, N))
    k = int(offset * N) % N
    vals2 = np.vstack([vals[k:], vals[:k]])
    return mpl.colors.LinearSegmentedColormap.from_list(
        cmap.name + "_rotated", vals2)

def rotate_complex_array(arr, angle_deg, order=3):
    """
    Rotate a 2D complex-valued array by any angle (in degrees).
    Uses spline interpolation.

    Parameters
    ----------
    arr : 2D numpy array of complex numbers
    angle_deg : float
        Rotation angle in degrees (counter-clockwise)
    order : int (05)
        Interpolation order (3 = cubic, good compromise)

    Returns
    -------
    2D complex numpy array (rotated)
    """
    from scipy.ndimage import rotate
    real_rotated = rotate(arr.real, angle_deg, reshape=True, order=order)
    imag_rotated = rotate(arr.imag, angle_deg, reshape=True, order=order)
    return real_rotated + 1j * imag_rotated

# def prop_free_nf(wavefield, wavelength, distance, psize=1.,padx=100,pady=100, show=True):
#     """
#     Syntax:
#         prop_free_nf(wavefield, wavelength, distance [, psize])

#     Python script to propagate a wavefields in the near field.
   
#     Parameters:
#         wavefield             (ndarray) : complex input wavefield
#         wavelength              (float) : wavelength in meters
#         distance                (float) : propagation distance in meters
       
#     Optional parameters:
#         psize                   (float) : pixel size in meters
#                                         : [default = 1.0 (pixel units)]

#     Returns:
#         wavefield_out         (ndarray) : propagated wavefield
#     """


#     program = 'prop_free_nf'
#     #check if padding is sufficient
#     pad_min = abs(distance) * wavelength / (psize*2)  
#     print(f"minnimum padding: {pad_min*1e6} microns")
#     pad_pixels = int(np.ceil(pad_min / psize))  # assuming square pixels
#     # print(f"Minimum padding for propagation of {wavelength} m wavelength, {distance} m distance, with {psize} m pixels:      {pad_pixels}")
    
#     if padx < pad_pixels:
#         print("WARNING! x padding is lower than minimum padding for this propagation!")
#     if pady < pad_pixels:
#         print("WARNING! y padding is lower than minimum padding for this propagation!")
#     else:
#         print("... padding is acceptable")

#     if show:
#         # fig = plt.figure()
#         fig, ax = plt.subplots(2,2)
#         ax[0,0].imshow(np.abs(wavefield))
#         ax[0,0].set_title('original')
#         ax[1,0].imshow(np.angle(wavefield))
#         ax[1,0].set_title('original')
#     else:
#         pass
    
#     if padx or pady:
#         wavefield = np.pad(wavefield, ((pady, pady), (padx, padx)), mode='constant')
#     else:
#         pass
    
#     if show:
#         ax[0,1].imshow(np.abs(wavefield))
#         ax[0,1].set_title('padded wavefield')
#         ax[1,1].imshow(np.angle(wavefield))
#         ax[1,1].set_title('padded wavefield')
#         plt.tight_layout()
#         plt.show()
#     else:
#         pass

#     asize = np.shape(wavefield)
    
#     print(f"pixel size:  {psize} m")
#     print(f"asize:       {asize}")
#     print(f"distance:    {distance} m")
#     print(f"wavelength:  {wavelength} m")
    
#     if np.size(psize) == 1:
#         psize = np.array((psize, psize))
       
#     if np.sqrt(np.sum(1.0/psize**2) * np.sum(1.0/(asize*psize)**2)) * \
#             abs(distance) * wavelength > 1:
#         print('{0}: warning: there could be some aliasing issues...'.
#               format(program))
#         print('{0}: (you could enlarge your array, or try a far field '
#               'method)'.format(program))
#         print('y', np.sqrt(np.sum(1.0/psize**2) * np.sum(1.0/(asize[0]*psize)**2)) * \
#                 abs(distance) * wavelength)
#         print('x', np.sqrt(np.sum(1.0/psize**2) * np.sum(1.0/(asize[1]*psize)**2)) * \
#                 abs(distance) * wavelength)

#     ind0 = np.arange(-asize[0]/2, asize[0]/2)
#     ind1 = np.arange(-asize[1]/2, asize[1]/2)

#     [x1,x2] = np.meshgrid(ind1/(asize[0]*psize[0]), ind0/(asize[1]*psize[1]))
#     q2 = np.fft.fftshift(x1**2 + x2**2)
   
#     wavefield_out = np.fft.ifft2( np.fft.fft2(wavefield) * \
#             np.exp(2.0 * 1j * np.pi * (distance / wavelength) * \
#                     (np.sqrt(1.0 - q2 * wavelength**2) - 1)),s=asize)#[int(asize[0]+pady),int(asize[1]+padx)])

#     return wavefield_out

def prop_free_nf(wavefield, wavelength, distance,
                        psize=1.0, padx=100, pady=100, show=False, verbose=False):
    """
    Angular Spectrum Near-Field Propagation

    Parameters
    ----------
    wavefield : ndarray (complex)
        Input complex wavefield (2D).
    wavelength : float
        Wavelength in meters.
    distance : float
        Propagation distance in meters.
    psize : float or (float, float)
        Pixel size in meters. Default = 1.0.
    padx, pady : float
        Padding size in pixels on x and y sides.
    show : bool
        If True, displays diagnostic images.

    Returns
    -------
    wavefield_out : ndarray (complex)
        Propagated wavefield (same padded size).
    """
    
    # -------------------------------------------------------------------------
    # 0. Standardize psize to a numpy array if scalar
    # -------------------------------------------------------------------------
    if np.isscalar(psize):
        psize = np.array([psize, psize])
    else:
        psize = np.array(psize)

    Ny, Nx = wavefield.shape

    # -------------------------------------------------------------------------
    # 1. Check minimum padding required based on propagation distance
    # -------------------------------------------------------------------------
    pad_min = abs(distance) * wavelength / (psize[0] * 2)
    if verbose:
        print(f"Minimum padding required: {pad_min * 1e6:.2f} microns")

    pad_pixels_x = int(np.ceil(pad_min / psize[1]))
    pad_pixels_y = int(np.ceil(pad_min / psize[0]))

    if padx < pad_pixels_x:
        print(f"WARNING! x padding is lower than minimum required!")
    if pady < pad_pixels_y:
        print(f"WARNING! y padding is lower than minimum required!")

    # Apply padding if necessary
    if padx > 0 or pady > 0:
        wavefield = np.pad(wavefield, ((pady, pady), (padx, padx)), mode='constant')

    Ny, Nx = wavefield.shape  # Recalculate size after padding

    # -------------------------------------------------------------------------
    # 2. Spatial frequency grid (corrected)
    # -------------------------------------------------------------------------
    fx = np.fft.fftfreq(Nx, d=psize[1])  # x spatial frequencies
    fy = np.fft.fftfreq(Ny, d=psize[0])  # y spatial frequencies
    FX, FY = np.meshgrid(fx, fy)

    k = 2 * np.pi / wavelength

    # squared transverse spatial frequency
    f2 = FX**2 + FY**2

    # -------------------------------------------------------------------------
    # 3. Aliasing check
    # -------------------------------------------------------------------------
    aliasing_check = np.sqrt(np.sum(1.0 / psize**2) * np.sum(1.0 / (np.array([Ny, Nx]) * psize)**2)) * abs(distance) * wavelength
    if verbose:
        if aliasing_check > 1:
            print("WARNING! Possible aliasing issues detected!")
            print(f"Aliasing parameter value: {aliasing_check:.2e}")
            
            # -------------------------------------------------------------------------
            # 1. Check if far-field condition is satisfied
            # -------------------------------------------------------------------------
            field_size_x = Nx * psize[1]  # field size in x (meters)
            field_size_y = Ny * psize[0]  # field size in y (meters)
    
            farfield_condition = distance > (field_size_x**2 + field_size_y**2) / wavelength
    
            if farfield_condition:
                print("Far-field condition satisfied. Reccomend using Fraunhofer approximation.")
            

    # -------------------------------------------------------------------------
    # 4. Angular spectrum transfer function (standard form)
    # -------------------------------------------------------------------------
    # Avoid evanescent wave sqrt of negative number:
    inside = (1 / wavelength**2) - f2
    inside = np.maximum(inside, 0)  # ensures no negative values

    # Transfer function H
    H = np.exp(1j * distance * 2 * np.pi * np.sqrt(inside))

    # -------------------------------------------------------------------------
    # 5. Apply propagation
    # -------------------------------------------------------------------------
    WF = np.fft.fft2(wavefield)  # Fourier transform of the wavefield
    wavefield_out = np.fft.ifft2(WF * H)  # Apply transfer function

    # -------------------------------------------------------------------------
    # 6. Optional visualization
    # -------------------------------------------------------------------------
    if show:
        fig, ax = plt.subplots(2, 2, figsize=(9, 8))

        ax[0, 0].imshow(np.abs(wavefield), cmap='gray')
        ax[0, 0].set_title("Input amplitude")

        ax[1, 0].imshow(np.angle(wavefield), cmap='twilight')
        ax[1, 0].set_title("Input phase")

        ax[0, 1].imshow(np.abs(wavefield_out), cmap='gray')
        ax[0, 1].set_title("Propagated amplitude")

        ax[1, 1].imshow(np.angle(wavefield_out), cmap='twilight')
        ax[1, 1].set_title("Propagated phase")

        plt.tight_layout()
        plt.show()

    return wavefield_out


def prop_free_ff(wavefield, wavelength, distance,
                       psize=1.0, show=False):
    """
    Fraunhofer Far-Field Propagation

    Parameters
    ----------
    wavefield : ndarray (complex)
        Input complex wavefield (2D).
    wavelength : float
        Wavelength in meters.
    distance : float
        Propagation distance in meters.
    psize : float or (float, float)
        Pixel size in meters. Default = 1.0.
    show : bool
        If True, displays diagnostic images.

    Returns
    -------
    wavefield_out : ndarray (complex)
        Propagated wavefield (same size).
    """

    Ny, Nx = wavefield.shape

    # -------------------------------------------------------------------------
    # 0. Standardize psize to a numpy array if scalar
    # -------------------------------------------------------------------------
    if np.isscalar(psize):
        psize = np.array([psize, psize])
    else:
        psize = np.array(psize)

    # -------------------------------------------------------------------------
    # 1. Spatial frequency grid for far-field (Fraunhofer)
    # -------------------------------------------------------------------------
    fx = np.fft.fftfreq(Nx, d=psize[1])  # x spatial frequencies
    fy = np.fft.fftfreq(Ny, d=psize[0])  # y spatial frequencies
    FX, FY = np.meshgrid(fx, fy)

    k = 2 * np.pi / wavelength

    # squared transverse spatial frequency
    f2 = FX**2 + FY**2

    # -------------------------------------------------------------------------
    # 2. Far-field transfer function (Fraunhofer approximation)
    # -------------------------------------------------------------------------
    H_farfield = np.exp(1j * k * distance) * np.exp(-1j * np.pi * wavelength * distance * f2)

    # -------------------------------------------------------------------------
    # 3. Apply far-field propagation
    # -------------------------------------------------------------------------
    WF = np.fft.fft2(wavefield)  # Fourier transform of the wavefield
    wavefield_out = np.fft.ifft2(WF * H_farfield)  # Apply transfer function

    # -------------------------------------------------------------------------
    # 4. Optional visualization
    # -------------------------------------------------------------------------
    if show:
        fig, ax = plt.subplots(2, 2, figsize=(9, 8))

        ax[0, 0].imshow(np.abs(wavefield), cmap='gray')
        ax[0, 0].set_title("Input amplitude")

        ax[1, 0].imshow(np.angle(wavefield), cmap='twilight')
        ax[1, 0].set_title("Input phase")

        ax[0, 1].imshow(np.abs(wavefield_out), cmap='gray')
        ax[0, 1].set_title("Propagated amplitude")

        ax[1, 1].imshow(np.angle(wavefield_out), cmap='twilight')
        ax[1, 1].set_title("Propagated phase")

        plt.tight_layout()
        plt.show()

    return wavefield_out

def Complex2HSV(z, rmin, rmax, hue_start=0,log=False):
    from matplotlib.colors import hsv_to_rgb
    # get amplidude of z and limit to [rmin, rmax]
    if log:
        amp = np.log(np.abs(z))
    else:
        amp = np.abs(z)
    amp = np.where(amp < rmin, rmin, amp)
    amp = np.where(amp > rmax, rmax, amp)
    # ph = np.angle(z, deg=1) + hue_start
    ph = np.angle(z, deg=1) + hue_start
    ph[ph<np.mean(ph[np.shape(ph)[0]//2-10:np.shape(ph)[0]//2+10,np.shape(ph)[1]//2-10:np.shape(ph)[1]//2+10])] += 360
    ph = ph - np.mean(ph)
    # HSV are values in range [0,1]
    h = (ph % 360) / 360
    s = 0.85 * np.ones_like(h)
    v = (amp -rmin) / (rmax - rmin)
    return hsv_to_rgb(np.dstack((h,s,v)))


def showRecon(f, prop=0, comp=False, rmphase=False, log='probe',unwrap=False,
              scan_name='scan_00',n_pmodes=10,wavelength=6.7e-9,lineprof=False,
              dx=0,dy=0,crop=50,taper_edge='cosine',savePath=None,name='_',saveType='.png',
              ROTATE=False,smooth=False):
    # plt.close('all')
    # if type(scan_name) == str:
    #     scan = [scan_name]
    # for scan in scan_name:
    print('scan_name: ', scan_name)
    OB = f['/content/obj/S' + scan_name + 'G00/data'][()]
    pr = f['/content/probe/S' + scan_name + 'G00/data'][()]
    px = f['/content/obj/S' + scan_name + 'G00/_psize'][()][0]
    if np.shape(OB)[0] > 10:
        print(np.shape(OB))
        ob = [OB]
    else:
        pass
    
    if log == 'probe':
        logp=True
        logo=False
    elif log == 'obj':
        logp=False
        logo=True
    elif log == 'both':
        logp=True
        logo=True
    else:
        logp=False
        logo=False
        
    
    for ob in OB:
        if rmphase == 'probe':
            probeModes(pr,px,comp,rmphase=True,scan=scan_name,nmodes=n_pmodes,save_path=savePath,name=name,savetype=saveType,log=logp)
            showObject(ob,px,comp,log=logo,unwrap=unwrap,scan=scan_name,lineprof=lineprof,crop=crop,save_path=savePath,name=name,savetype=saveType,ROTATE=ROTATE,smooth=smooth)
            if prop:
                propESW(ob,px,prop,comp,dx=dx,dy=dy,log=logo,unwrap=unwrap,scan=scan_name,wavelength=wavelength,
                        lineprof=lineprof,taper_edge=taper_edge,crop=crop)
        elif rmphase == 'obj':
            probeModes(pr,px,comp,scan=scan_name,nmodes=n_pmodes,save_path=savePath,name=name,savetype=saveType,log=logp)
            showObject(ob,px,comp,rmphase=True,log=logo,unwrap=unwrap,scan=scan_name,lineprof=lineprof,crop=crop,save_path=savePath,name=name,savetype=saveType,ROTATE=ROTATE,smooth=smooth)
            if prop:
                propESW(ob,px,prop,comp,dx=dx,dy=dy,rmphase=True,log=logo,unwrap=unwrap,scan=scan_name,wavelength=wavelength,
                        lineprof=lineprof,taper_edge=taper_edge,crop=crop)
        elif rmphase == 'both':
            probeModes(pr,px,comp,rmphase=True,scan=scan_name,nmodes=n_pmodes,save_path=savePath,name=name,savetype=saveType,log=logp)
            showObject(ob,px,comp,rmphase=True,log=logo,unwrap=unwrap,scan=scan_name,lineprof=lineprof,crop=crop,save_path=savePath,name=name,savetype=saveType,ROTATE=ROTATE,smooth=smooth)
            if prop:
                propESW(ob,px,prop,comp,dx=dx,dy=dy,rmphase=True,log=logo,unwrap=unwrap,scan=scan_name,wavelength=wavelength,
                        lineprof=lineprof,taper_edge=taper_edge,crop=crop)
        else:
            probeModes(pr,px,comp,scan=scan_name,nmodes=n_pmodes,save_path=savePath,name=name,savetype=saveType,log=logp)
            showObject(ob,px,comp,log=logo,unwrap=unwrap,scan=scan_name,lineprof=lineprof,crop=crop,save_path=savePath,name=name,savetype=saveType,ROTATE=ROTATE,smooth=smooth)
            if prop:
                propESW(ob,px,prop,comp,dx=dx,dy=dy,log=logo,unwrap=unwrap,scan=scan_name,wavelength=wavelength,
                        lineprof=lineprof,taper_edge=taper_edge,crop=crop)
        
        

def probeModes(pr,px,comp=False, rmphase=False, scan = 'scan_00', nmodes=10,save_path=None,log=True,name='_',savetype='.png'):
    # pr = f['/content/probe/S' + scan + 'G00/data'][()]
    # px = f['/content/obj/S' + scan + 'G00/_psize'][()]
    # px = f['/content/obj/S' + scan + 'G00/_psize'][()][0]
        
    sF = 1e6 # convert from m to um
    amp, nplist = ptypy.utils.ortho(pr)
    if rmphase:
        nplist = [ptypy.utils.rmphaseramp(n) for n in nplist]
    numXticks = 15
    numYticks = 15
    (ny,nx) = np.shape(pr[0])
    
    # Coordinate extents in um
    y_extent = (-(ny/2) * px, (ny/2) * px)
    x_extent = (-(nx/2) * px, (nx/2) * px)
    extent = [x_extent[0]*1e6, x_extent[1]*1e6, y_extent[0]*1e6, y_extent[1]*1e6]
    if comp:
        import c2image
        # obC = Complex2HSV(ob, np.min(abs(ob)), np.max(abs(ob)))
        if log:
            prC = [Complex2HSV(n,0.0,np.max(np.log(abs(n))),log=True) for n in nplist]
        else:
            prC = [Complex2HSV(n,np.min(abs(n)),np.max(abs(n))) for n in nplist]
        fig = plt.figure()
        
        for i in range(len(nplist)): #number of probe modes
            if nmodes > 5:
                plt.subplot(2,int(nmodes/2),i+1)
            else:
                plt.subplot(1,nmodes,i+1)
            plt.imshow(prC[i],extent=extent)
            if i == 0 or i == 5:       
                plt.ylabel('y [µm]')
            else:
                plt.yticks([],[])
                pass
            plt.xlabel('x [µm]')
            plt.title(amp[i])
        fig.suptitle(scan)
        fig.tight_layout()
        if save_path:
            plt.savefig(f"{save_path}probe_probe{name}{savetype}")
        else:
            pass
        plt.show()
        # plotComplexWithColorbar(prC[0],px,title='first probe mode',log=log)
    else:
        fig = plt.figure()
        for i in range(len(nplist)): #number of probe modes
            if nmodes > 5:
                plt.subplot(2,int(nmodes/2),i+1)
            else:
                plt.subplot(1,nmodes,i+1)
            if log:
                if i == 0:
                    im = plt.imshow(np.log(np.abs(nplist[i])),extent=extent,cmap='gray')
                else:
                    plt.imshow(np.log(np.abs(nplist[i])),extent=extent,cmap='gray')
            else:
                if i == 0:
                    im = plt.imshow(np.abs(nplist[i]),extent=extent,cmap='gray')
                else:
                    plt.imshow(np.abs(nplist[i]),extent=extent,cmap='gray')
            if i == 0 or i == 5:     
                plt.ylabel('y [µm]')
            else:
                plt.yticks([],[])
                pass
            plt.xlabel('x [µm]')
            plt.title(amp[i])
        fig.suptitle(scan)
        # plt.colorbar(im)
        fig.tight_layout()
        if save_path:
            plt.savefig(f"{save_path}probe_amp{name}{savetype}")
        else:
            pass
            # plotComplexWithColorbar(ob,px=px,title=scan,save_path=f"{save_path}object_comp{name}{savetype}")
        plt.show()
        
        #weighted_probes = [np.abs(nplist[i])*amp[i] for i in range(len(nplist))]
        #print('weighted probe shape')
        #print(np.shape(weighted_probes))
        psum = np.sum([abs(nplist[i]**2) for i in range(len(nplist))],axis=0)#np.sum(weighted_probes,axis=0)
        psum = psum/np.max(psum)
        print(np.shape(psum))
        
        plt.figure()
        plt.imshow(psum,extent=extent,cmap='gray')
        plt.ylabel('y [µm]')
        plt.xlabel('x [µm]')
        plt.colorbar()
        plt.show()
        
        
        if log:
            M1 = np.log(psum)#np.log(np.abs(nplist[0])**2)
        else:
            M1 = psum #np.abs(nplist[0])**2
        M1x = np.sum(M1,axis=0)#[M1.shape[0]//2 - int(AV/2):M1.shape[0]//2 + int(AV/2),:],axis=0)
        M1y = np.sum(M1,axis=1)#[:,M1.shape[1]//2 - int(AV/2):M1.shape[1]//2 + int(AV/2)],axis=1)
        # M1x = M1[ny//2,:]
        # M1y = M1[:,nx//2]
        M1x = M1x - np.min(M1x)
        M1y = M1y - np.min(M1y)
        M1x = M1x/np.max(M1x)
        M1y = M1y/np.max(M1y)
        X = np.linspace(-(nx/2)*px,(nx/2)*px,nx)
        #FWx,FWy = getFWatValue(M1, px, px, frac=frac,centered=True,averaging=AV)#,smoothing='savgol',sparams=10)
        fwtm = len(M1x[M1x>(M1x[nx//2]*0.1)])*px, len(M1y[M1y>(M1y[ny//2]*0.1)])*px
        fwhm = len(M1x[M1x>(M1x[nx//2]*0.5)])*px, len(M1y[M1y>(M1y[ny//2]*0.5)])*px
        fig = plt.figure()
        plt.plot(X*1e6,M1x,color='blue', label='x-profile')
        plt.plot(X*1e6,M1y,color='red', label='y-profile')
        plt.hlines(np.max(M1x)*(0.5), -fwhm[0]*1e6/2, fwhm[0]*1e6/2, linestyle='--', color='blue')
        plt.hlines(np.max(M1y)*(0.5), -fwhm[1]*1e6/2, fwhm[1]*1e6/2, linestyle='--', color='red')
        plt.text(-31,np.max(M1x),f"FWHM (x,y) = ({round_sig(fwhm[0]*1e6,3)},{round_sig(fwhm[1]*1e6,3)}) um")
        plt.hlines(np.max(M1x)*(0.1), -fwtm[0]*1e6/2, fwtm[0]*1e6/2, linestyle=':', color='blue')
        plt.hlines(np.max(M1y)*(0.1), -fwtm[1]*1e6/2, fwtm[1]*1e6/2, linestyle=':', color='red')
        plt.text(-31,np.max(M1x)*0.75,f"FWTM (x,y) = ({round_sig(fwtm[0]*1e6,3)},{round_sig(fwtm[1]*1e6,3)}) um")
        plt.xlabel('Position [µm]')
        plt.legend()
        plt.show()
        
        
        # centered=True,averaging=None,smoothing=None,sparams=0,verbose=True,show=True,title=None):
            # """
        print(f"FWHM of summed probe modes (x,y):       {fwhm}")
        print(f"FWTM of summed probe modes (x,y):       {fwtm}")
        
def showObject(ob,px,comp=False,rmphase=False,log=False,unwrap=False, scan='scan_00',
               lineprof=False,crop=50,save_path=None,name='_',savetype='.svg',
               ROTATE=False,smooth=False):
    import numpy as np
    
    ob = np.squeeze(ob)
    NY,NX = np.shape(ob) 
    ex = 50
    if rmphase:
        ob,PR = ptypy.utils.rmphaseramp(ob[NY//2 - crop//2 - ex: NY//2 + crop//2 + ex,
                                        NX//2 - crop//2 - ex: NX//2 + crop//2 + ex], return_phaseramp=True)#, weight = 'abs')
        # print(PR)
            # ob[crop+ex:-(crop+ex),crop+ex:-(crop+ex)],weight = 'abs')
        # ob = ptypy.utils.rmphaseramp(ob)
        # ob = ptypy.utils.rmphaseramp(ob)
    else:
        ob = ob[NY//2 - crop//2 - ex: NY//2 + crop//2 + ex, NX//2 - crop//2 - ex: NX//2 + crop//2 + ex]
        # ob[crop+ex:-(crop+ex),crop+ex:-(crop+ex)]
        # = [f['/content/obj/S' + scan + 'G00/data'][()]] #ptypy.utils.rmphaseramp(np.squeeze(f['/content/obj/S' + scan + 'G00/data'][()]))
    # px = f['/content/obj/S' + scan + 'G00/_psize'][()][0]
    
    print('Shape of object array: ', np.shape(ob))
    sF = 1e6 # convert from m to um
    numXticks = 15
    numYticks = 15
    (ny,nx) = np.shape(np.squeeze(ob))

    print(np.shape(ob))
    
    if ROTATE:
        print("Rotating... ")
        ob = rotate_complex_array(ob, ROTATE)
        # print(np.shape(ob))
        ob = np.squeeze(ob)[ex:ny-ex,ex:nx-ex]
    else:
        ob = np.squeeze(ob)[ex:ny-ex,ex:nx-ex]
    
    if unwrap:
        P = np.angle(ob)
        # meanP = np.angle(np.mean(np.exp(1j * P)))
        # P[P<np.mean(P[np.shape(P)[0]//2-10:np.shape(P)[0]//2+10,np.shape(P)[1]//2-10:np.shape(P)[1]//2+10])] += 2*np.pi 
        # print(f"Mean phase angle: {np.angle(np.mean(np.exp(1j * P)))}")
        
        
        P -= P.mean()
        P[P<-np.pi]+=2*np.pi
        P[P>np.pi]-=2*np.pi
        
        P -= P.mean()
        
        offset = 0
        
        # # P[P>np.mean(P)] -= 2*np.pi
        # P[P<0] += 2*np.pi
        # # P[P<-2.0] += 2*np.pi
        # # P[P<-0.7] += 2*np.pi
        # # P = -1*(P - np.mean(P) + 0.5)
        # # P = (P - np.mean(P) + 0.3)
        # # P = (P - meanP + np.pi - 1.2)
        # # Center phase so circular mean is zero
        # # P -= np.angle(np.mean(np.exp(1j * P)))
        # P -= P.mean()
        # # P[P>np.mean(P)] -= 2*np.pi
        # # P -= P.mean()
        # # P[P>3] -= 2*np.pi
        # # P[P<-3] += 2*np.pi
        # # P[P>2]-=2*np.pi
        # # P -= P.mean()
        
        # # P[P<-2.7] += 2*np.pi
        # # P[P>2.7] -= 2*np.pi
        # P = -P
        # if P[ny//2,0] <= 0:
        #     print(P[ny//2,0])
        #     print('cycling by pi')
        #     offset = 180
        # else:
        #     print(P[ny//2,0]) 
        #     offset = 0
        #     pass
        # print(f"Mean phase angle: {np.angle(np.mean(np.exp(1j * P)))}")
        
        
        
        
        ob = np.abs(ob) * np.exp(1j * P)
    else:
        offset = 0
        
    if smooth:
        from scipy.ndimage import gaussian_filter
        import numpy as np

        # Smooth real and imaginary parts separately
        ob = (
            gaussian_filter(np.real(ob), sigma=smooth)
            # np.real(ob)
            + 1j * gaussian_filter(np.imag(ob), sigma=smooth)
        )
        
        P = np.angle(ob)
    # print(np.shape(ob))
    (ny,nx) = np.shape(np.squeeze(ob))
    print('nx: ', nx)
    print('ny: ', ny)        
    print('px: ', px)    
    # Coordinate extents in um
    y_extent = (-(ny/2) * px, (ny/2) * px)
    x_extent = (-(nx/2) * px, (nx/2) * px)
    extent = [x_extent[0]*1e6, x_extent[1]*1e6, y_extent[0]*1e6, y_extent[1]*1e6]

    I = np.abs(ob)**2
    I = I / np.max(I)
    print('checking normalisation...')
    print(f"max I = {np.max(I)}")
    
    if comp:
        # import c2image
        print(np.min(abs(np.squeeze(ob))),np.max(abs(np.squeeze(ob))))
        obC = Complex2HSV(np.squeeze(ob),np.min(abs(np.squeeze(ob))),np.max(abs(np.squeeze(ob))))
        
        print(np.shape(obC))
        
        # plt.figure()
        if save_path:            
            plotComplexWithColorbar(ob,px=[px,px],title=scan,save_path=f"{save_path}object_comp{name}{savetype}", offset=offset)
        else:
            plotComplexWithColorbar(ob,px=[px,px],title=scan,save_path=None, offset=offset)
        
        # plt.figure()
        # plt.imshow(obC,extent=extent)
        # plt.xlabel('x [µm]')
        # plt.ylabel('y [µm]')
        # plt.title(scan + ': ' + 'Complex Wavefield')
        # # plt.colorbar()
        # plt.show()
        
        # obCBar = Complex2HSV()
        # plt.figure()
        # plt.imshow(obCBar)
        # plt.title('color bar')
        # plt.show()
    else:
        print('shape of object:', np.shape(ob))
        print(np.shape(np.angle(ob)))
        print(np.shape(abs(ob)**2))
        print(extent)
        plt.figure()
        if unwrap:
            
            # plt.imshow(P,extent=extent,cmap='gist_rainbow')#,norm=norm)#,vmin=-np.pi,vmax=np.pi)
            cmap = plt.cm.twilight
            # pink = [1.0, 0.0, 1.0]  # magenta/pink
            # cmap_aligned, offset = align_cmap_to_color(cmap, pink)

            # cmap_rot = rotate_cyclic_cmap(cmap, offset)


            # print("Offset =", offset)

            # plt.imshow(P, cmap=cmap_aligned)
            plt.imshow(P,extent=extent,cmap=cmap,vmin=-np.pi,vmax=np.pi)
            # plt.colorbar()
            # plt.show()

            
            
        else:
            # print('here')
            cmap = plt.cm.twilight
            plt.imshow(np.angle(ob),extent=extent,cmap=cmap,vmin=-np.pi,vmax=np.pi)
            print(np.angle(ob))
        plt.xlabel('x [µm]')
        plt.ylabel('y [µm]')
        plt.title(scan + ': ' + 'Phase')
        plt.colorbar()
        plt.show()
        
        plt.figure()
        if log:
            plt.imshow(np.log(I),extent=extent,cmap='gray')
            plt.title(scan + ': ' + 'Intensity (log)')
        else:
            plt.imshow(I,extent=extent,cmap='gray')
            plt.title(scan + ': ' + 'Intensity')
        plt.xlabel('x [µm]')
        plt.ylabel('y [µm]')
        plt.colorbar()
        plt.show()
    if lineprof:
        getLineProfile(I,axis=1,px=px,norm=True,show=True)
        if unwrap:
            getLineProfile(P,axis=1,px=px,show=True)
        else:
            getLineProfile(np.angle(ob),axis=1,px=px,show=True)
            

def propESW(ob,px,prop,comp=False,rmphase=False,dx=0,dy=0,crop=50,
            log=False,unwrap=False,scan='scan_00',wavelength=6.7e-9,
            lineprof=True,taper_edge=None,taper_width=100,ROTATE=None,savePath=None):
    if rmphase:
        ob = ptypy.utils.rmphaseramp(np.squeeze(ob))
    else:
        pass
        # ob = f['/content/obj/S' + scan + 'G00/data'][()] #ptypy.utils.rmphaseramp(np.squeeze(f['/content/obj/S' + scan + 'G00/data'][()]))
    # px = f['/content/obj/S' + scan + 'G00/_psize'][()][0]
    sF = 1e6 # convert from m to um
    # numXticks = 15
    # numYticks = 15
    pad = [int(dx/px), int(dy/px)]
    print(f"Pixel size:             {px*1e9} nm")
    print(f"Wavelength:             {wavelength*1e9} nm")
    print(f"padding array by (x,y): {pad}")
    ob = np.squeeze(ob)
    NY, NX = np.shape(ob)
    ob = ob[
            NY//2 - crop//2 : NY//2 + crop//2,
            NX//2 - crop//2 : NX//2 + crop//2
            ]

    if np.shape(ob)[0] != np.shape(ob)[1]:
        print('Array is not square.... cropping further')
        N = np.min(np.shape(ob))
        ob = ob[0:N,0:N]
    if taper_edge:
        ob = apply_edge_taper(ob,taper_width=taper_width,window_type=taper_edge)
    else:
        pass
        
    print(f"Shape of ob (pix):     {np.shape(ob)}")
    print(f"Shape of ob (µm):      {(np.shape(ob)[0]*px*sF, np.shape(ob)[1]*px*sF)}")
    
    
    if np.shape(ob)[0] != np.shape(ob)[1]:
        print('Array is not square.... cropping further')
        N = np.min(np.shape(ob))
        ob = ob[0:N,0:N]
    
    print(f"Propagating {prop} m ...")
    ESW = prop_free_nf(ob, wavelength=wavelength, distance=prop, psize=px ,padx=pad[0],pady=pad[1]) 
    print('Shape of ESW: ', np.shape(ESW))
    
    if savePath:    
        # Write to HDF5 file
        with h5py.File(savePath, "w") as f:
            f.create_dataset("data", data=ESW)
        print(f"saved wavefield to: {savePath}")
    
    (ny,nx) = np.shape(ESW)
    # Coordinate extents in µm
    y_extent = (-(ny/2) * px, (ny/2) * px)
    x_extent = (-(nx/2) * px, (nx/2) * px)
    extent = [x_extent[0]*1e6, x_extent[1]*1e6, y_extent[0]*1e6, y_extent[1]*1e6]
    if comp:
        ESWC = Complex2HSV(ESW,np.min(abs(ESW)),np.max(abs(ESW)))
        print(np.shape(ESWC))
        print(int(dx / px))
    
        phase = np.angle(ESW)
        # phase[np.abs(ESW) < 0.02] = 0  # hide unreliable phase
        from plot_complex_colourbar import plotComplexWithColorbar
        
        plotComplexWithColorbar(ESW,[px,px],title=f"scan: {scan} (z = {prop} m) ")
        # plt.figure()
        # plt.imshow(ESWC,extent=extent)
        # plt.xlabel('x [µm]')
        # plt.ylabel('y [µm]')
        # plt.title(scan + ': ' + f"Complex Wavefield (z = {prop} m)")
        # plt.colorbar()
        # plt.show()
    else:
        plt.figure()
        phase = np.angle(ESW)
        phase[np.abs(ESW) < 0.02] = 0  # hide unreliable phase

        if unwrap:
            plt.imshow(np.unwrap(phase,axis=0),extent=extent)
        else:
            plt.imshow(phase,extent=extent)
        plt.xlabel('x [µm]')
        plt.ylabel('y [µm]')
        plt.title(scan + ': ' + f"Phase (z = {prop} m)")
        plt.show()
    
        plt.figure()
        if log:
            plt.imshow(np.log(np.abs(ESW)**2),extent=extent)
            plt.title(scan + ': ' + f"Intensity (log) (z = {prop} m)")
        else:
            plt.imshow(np.abs(ESW)**2,extent=extent)
            plt.title(scan + ': ' + f"Intensity (z = {prop} m)")
        plt.xlabel('x [µm]')
        plt.ylabel('y [µm]')
        plt.show()
        
    if lineprof:
        if ROTATE:
            profileI, XS,YS, sc,ec = angled_profile_with_coords(np.abs(ESW)**2, angle_deg=ROTATE,show=True)
            profileP, XS,YS, sc,ec = angled_profile_with_coords(phase, angle_deg=ROTATE,show=True)
        else:
            getLineProfile(np.abs(ESW)**2,axis=1,px=px,show=True)
            getLineProfile(phase,axis=1,px=px,show=True)

def apply_edge_taper(wavefield, taper_width=50, window_type='cosine',show=True):
    """
    Applies a soft edge taper to a 2D complex wavefield to reduce edge artifacts.

    Parameters:
        wavefield     (ndarray): 2D complex input wavefield
        taper_width     (int): Width (in pixels) of the tapering region
        window_type     (str): Type of tapering window ('cosine', 'hanning', or 'tukey')

    Returns:
        tapered_wavefield (ndarray): Wavefield after applying edge taper
    """
    ny, nx = wavefield.shape

    # Create 1D taper windows
    def cosine_window(n, width):
        taper = np.ones(n)
        ramp = (1 - np.cos(np.linspace(0, np.pi, width))) / 2
        # plt.plot(ramp)
        # plt.show()
        taper[:width] *= ramp
        taper[-width:] *= ramp[::-1]
        return taper

    def tukey_window(n, width):
        alpha = 2 * width / n
        return np.tukey(n, alpha)
    
    
    def tukey_square(length, alpha=0.125) -> np.ndarray:    
        """ Creates a square Tukey window mask of length x length of width
        alpha. """
        tukey = wins.tukey(length, alpha=alpha)
        return np.ones((length, length)) * tukey.reshape((length, 1)) * tukey.reshape((1, length))
    
    def apply_tukey(n,width) -> np.ndarray:
        """ Apply a Tukey window to a 2D, square input image. """
        main_size = n.shape[0]
        alpha = 2 * width / n
        if n.ndim == 2 and main_size == np.ma.size(n, axis=1):
            return tukey_square(main_size, alpha) * n
        else:
            raise ValueError("Image not 2D or not square.")

    if window_type == 'cosine':
        win_x = cosine_window(nx, taper_width)
        win_y = cosine_window(ny, taper_width)
    elif window_type == 'hanning':
        win_x = np.hanning(nx)
        win_y = np.hanning(ny)
    elif window_type == 'tukey':
        pass
        # win_x = tukey_window(nx, taper_width)
        # win_y = tukey_window(ny, taper_width)
    else:
        raise ValueError("Unsupported window_type. Choose 'cosine', 'hanning', or 'tukey'.")
    
    if window_type == 'tukey':        
        tapered_wavefield = apply_tukey(wavefield,taper_width) 
        #wavefield * window_2d
    else:
        window_2d = np.outer(win_y, win_x)
        tapered_wavefield = wavefield * window_2d
    
    if show:
        # fig = plt.figure()
        fig, ax = plt.subplots(2,3)
        ax[0,0].imshow(np.abs(wavefield))
        ax[0,0].set_title('original')
        ax[0,1].imshow(window_2d)
        ax[0,1].set_title('taper window')
        ax[0,2].imshow(np.abs(tapered_wavefield))
        ax[0,2].set_title('tapered wavefield')
        ax[1,0].imshow(np.angle(wavefield))
        ax[1,0].set_title('original')
        ax[1,1].imshow(window_2d)
        ax[1,1].set_title('taper window')
        ax[1,2].imshow(np.angle(tapered_wavefield))
        ax[1,2].set_title('tapered wavefield')
        plt.tight_layout()
        plt.show()
    
    return tapered_wavefield


def multiProp(f,zi,zf,dz,dx=0,crop=50,savePath=None,show=False, scan = 'scan_00',comp=False,
              wavelength=6.7e-9,padx=0,pady=0,taper_edge=None,taper_width=100, ROTATE=0, force_z0=True):
    # plt.close('all')
    ob = f['/content/obj/S' + scan + 'G00/data'][()]
    px = f['/content/obj/S' + scan + 'G00/_psize'][()][0]
    
    if force_z0:
         # ensure Z range includes 0:
         zi = int(zi/dz)*dz
         zf = int(zf/dz)*dz
         if zi<=0:
             Z = np.concatenate((np.arange(zi,0,dz),np.arange(0,zf+dz,dz)))
         else:
             Z = np.arange(zi,zf+dz,dz)
         N = len(Z)
         # pos = 
    else:    
         # N = abs(int((zf-zi)/dz))
         N = int(np.floor((zf-zi)/dz)) + 1
         Z = np.linspace(zi,zf,N)
    
    zR = zi - zf
    print(f"Propagating wavefield from {zi} m to {zf} m, in {N} steps of {dz} m ...")
    # print(Z)
    pad = [int(padx/px), int(pady/px)]
    print(f"padding array by (x,y): {pad}")
    ob = np.squeeze(ob)
    NY,NX = np.shape(ob)
    ob = ob[NY//2 - crop//2: NY//2 + crop//2, NX//2 - crop//2: NX//2 + crop//2]
    if np.shape(ob)[0] != np.shape(ob)[1]:
        print('Array is not square.... cropping further')
        n = np.min(np.shape(ob))
        ob = ob[0:n,0:n]
    if taper_edge:
        ob = apply_edge_taper(ob,taper_width=taper_width,window_type=taper_edge,show=True)
    else:
        pass
    print('Shape of ob:', np.shape(ob))
    
    I, P = [], []
    Il,Pl= [], []
    W = []
    # for e,z in enumerate(tqdm(Z, desc="Propagating wavefield", unit="distances")):
    for e,z in enumerate(Z):
        print(f"Performing propagation #{e+1} of {N}...")
        ESW = prop_free_nf(ob, wavelength=wavelength, distance=z, psize=px,padx=pad[0],pady=pad[1],show=False)
        
        i = np.abs(np.squeeze(ESW))
        p = np.angle(np.squeeze(ESW))
        # i.astype(np.float16)
        # p.astype(np.float16)
        i_min = np.min(i)
        i_max = np.max(i)
        p_min = np.min(p)
        p_max = np.max(p)

        if i_max > i_min:
            i = ((i - i_min) / (i_max - i_min)) * 255
        i = i.astype(np.uint8)

        if p_max > p_min:
            p = ((p - p_min) / (p_max - p_min)) * 255
        p = p.astype(np.uint8)

        # I.append(i)
        # P.append(p)
        Il.append([i_min,i_max])
        Pl.append([p_min,p_max])
        I.append(i)
        P.append(p)
        # print(f"i_min: {i_min}")
        # print(f"i_max: {i_max}")
        # ESW = [create_wavefield(p, i)]# for p, i in zip(stackI,stackP)]
        # W.append(ESW)#.astype(np.float16))
        
        # W = [create_wavefield(p, i)]# for p, i in zip(stackI,stackP)]
        # E16 = np.stack([
        #                 ESW.real.astype(np.float16),
        #                 ESW.imag.astype(np.float16)
        #                 ], axis=-1)

    # I_max = np.max(I)
    # I_min = np.min(I)
    
    # I = [((i - I_min) / (I_max - I_min)) * 255 for i in I]
    
    if savePath:
        # print("Saving tiff stack...")
        # saveTiffStack(savePath + '_intensity.tif', I)
        # saveTiffStack(savePath + '_phase.tif', P)
        print(f"Saving pickle file to: {savePath}_comp.pkl")
        with open(savePath + '_comp.pkl', "wb") as g:
            pickle.dump([I,P,Il,Pl], g)
    if show:
        print("Plotting tiff stack...")
        if comp:
            showTiffStack(savePath,zi,zR,N,px,zPlot=True,comp=comp,loadFrom='pkl',ROTATE=ROTATE)
        else:
            showTiffStack(savePath + '_intensity.tif',zi,zR,N,px,zPlot=True,comp=comp,ROTATE=ROTATE)
            showTiffStack(savePath + '_phase.tif',zi,zR,N,px,zPlot=True,comp=comp,ROTATE=ROTATE)
    # return ESWs

def saveTiffStack(filename, *arrays):
    """
    Saves multiple 2D arrays as a stacked TIFF file.
    
    Parameters
    ----------
    filename : str
        Name (and path if needed) of the output TIFF file.
    *arrays : tuple of numpy.ndarray
        One or more 2D NumPy arrays to be stacked into the TIFF.
    """
    # Ensure all arrays have the same shape
    shapes = [np.shape(arr) for arr in arrays]
    if not all(shape == shapes[0] for shape in shapes):
        raise ValueError("All arrays must have the same shape.")

    # arrays = [(a/np.max(a))*255 for a in arrays]
    # for i,a in enumerate(arrays):
    #     # a_min = np.min(a)
    #     # a_max = np.max(a)
    #     # if a_max > a_min:
    #     #     a = ((a - a_min) / (a_max - a_min)) * 255
    #     a = a.astype(np.uint8)
    #     arrays[i] = a

    # Stack along the first axis (creates a 3D array: (num_images, height, width))
    stack = np.stack(arrays, axis=0)
    
    # Save as a multi-page TIFF
    # tifffile.imwrite(filename, stack, photometric='minisblack')#, dtype=)
    # print(f"Saved {len(arrays)} images to {filename}")


def showTiffStack(filename,zi,zR,N,px=1,zPlot=False,comp=False,savePath=None,loadFrom='pkl',
                  ROTATE=0):
    """
    Reads a TIFF stack from 'filename' and displays it in an interactive
    window with a slider. Suitable for use in an IPython or standard
    Python terminal (non-Jupyter environment).

    Requirements:
      - matplotlib with an interactive backend (e.g. TkAgg, Qt5Agg, etc.)
      - tifffile installed
    """    
    from matplotlib.widgets import Slider
    # Load the stack (shape: (num_slices, height, width))
    if comp:
        print("Loading intensity and phase stacks and building complex stack... ")
        if loadFrom == 'tif':
            stackI = np.squeeze(tifffile.imread(filename + '_intensity.tif'))
            stackP = np.squeeze(tifffile.imread(filename + '_phase.tif'))
            stack = [stackI,stackP]
        elif loadFrom == 'pkl':      
            pick = pickle.load(open(filename + '_comp.pkl','rb'))
            I = pick[0]
            P = pick[1]
            stack = [I,P]#[create_wavefield(p, i) for p,i in zip(P,I)]
            Il = pick[2]
            Pl = pick[3]
            
        # stack = [create_wavefield(p, i) for p, i in zip(stackI,stackP)]
        # stack = np.stack([Complex2HSV(s,np.min(abs(s)),np.max(abs(s))) for s in stack])
    else:
        if loadFrom == 'tif':
            stack = np.squeeze(tifffile.imread(filename))
        elif loadFrom == 'pkl':            
            pick = pickle.load(open(filename + '_comp.pkl','rb'))
            I = pick[0]
            P = pick[1]
            Il = pick[2]
            Pl = pick[3]
            
        # stack = [s/255 for s in stack]
    # num_slices = stack.shape[0]
    # print('shape of stack:', np.shape(stack))
    # Set up figure and show the first slice
    # fig, ax = plt.subplots()
    # plt.subplots_adjust(bottom=0.25)  # Leave space at the bottom for the slider
    # current_slice = 0

    # # Display the first slice
    # im = ax.imshow(stack[current_slice], cmap='gray')
    # ax.set_title(f"Slice: {current_slice}")
    # ax.axis('off')

    # # Define slider axis and create the slider
    # # (left, bottom, width, height) in figure coordinates
    # slider_ax = plt.axes([0.1, 0.1, 0.8, 0.03])
    # slice_slider = Slider(
    #     ax=slider_ax,
    #     label='Slice',
    #     valmin=0,
    #     valmax=num_slices - 1,
    #     valinit=current_slice,
    #     valstep=1  # Only move in integer steps
    # )

    # # Callback to update image when slider is moved
    # def update(val):
    #     slice_index = int(slice_slider.val)
    #     im.set_data(stack[slice_index])
    #     ax.set_title(f"Slice: {slice_index}")
    #     # Redraw canvas
    #     fig.canvas.draw_idle()

    # # Register the update function with each slider move
    # slice_slider.on_changed(update)

    # # Show the interactive figure
    # plt.show()
    
    if loadFrom == 'pkl':
        limits = [Il,Pl]
        norm = True
    else:
        limits = None
        norm = False
    
    if zPlot:
        if comp:
            propPlot(stack,zi,zR,N,res=px,comp=comp,savePath=savePath,norm=norm,limits=limits,ROTATE=ROTATE)
        else:
            propPlot(I,zi,zR,N,res=px,comp=comp,savePath=savePath,norm=norm,limits=Il,cmap='gray',ROTATE=ROTATE)
            propPlot(P,zi,zR,N,res=px,comp=comp,savePath=savePath,norm='phase',limits=Pl,cmap='gist_rainbow',ROTATE=ROTATE)
            

# %%
def getLineProfile(a,axis=0, px=1.0, mid=None, norm=False, show=False):
    nx, ny = np.shape(a)[1], np.shape(a)[0]
    if mid == None:
        midX, midY = int(nx/2), int(ny/2)
    else:
        midX, midY = int(mid[1]), int(mid[0])    
    # print('Getting line profile...')
    # print(f"(nx,ny):       {(nx,ny)}")
    # print(f"(midX,midY):   {(midX,midY)}")
    # print(f"pixel size:    {px}")
    # print(midX)
    
    if axis == 0:
        p = a[:,midX]
        # x = np.linspace(-(len(a)/2)*px*1e6, (len(a)/2)*px*1e6, ny)
        x = np.linspace(-(ny/2)*px*1e6, (ny/2)*px*1e6, ny)
        title = 'vertical profile'
        label='y [µm]'
    elif axis == 1:
        p = a[midY,:]
        # x = np.linspace(-(len(a)/2)*px*1e6, (len(a)/2)*px*1e6, nx)
        x = np.linspace(-(nx/2)*px*1e6, (nx/2)*px*1e6, nx)
        title = 'horizontal profile'
        label = 'x [µm]'
    
    if norm:
        p = p/np.max(p)
        
    print(f"... Shape of line profile: {np.shape(p)}")
    
    if show:
        plt.figure()
        plt.plot(x,p,':o',color='black',mfc='none')
        plt.xlabel(label)
        plt.ylabel('Amplitude')
        plt.title(title)
        plt.show()
    
    return p

def create_wavefield(phase, magnitude):
    # Ensure phase is in radians (if it's in degrees, convert it)
    # phase = np.deg2rad(phase) if np.max(phase) > 2.1 * np.pi else phase
    
    # Create the complex wavefield
    # magnitude = intensity ##np.sqrt(intensity)
    complex_wavefield = magnitude * np.exp(1j * phase)
    
    return complex_wavefield

def propPlot(I,zi,zRange,zPlanes,res=1,axis='hor',log=False,comp=False,lMin=1,
             savePath=False,plotProfiles=False,verbose=False,norm=False,limits=None,
             pick=True,cmap='viridis',ROTATE=0):
    p=[]
    
    if comp:
        P = np.squeeze(I[1])
        I = np.squeeze(I[0])
        # dx = I.shape[1] * np.cos(np.deg2rad(ROTATE))
        # dy = I.shape[0] * np.sin(np.deg2rad(ROTATE))
        # center = np.array(I.shape) / 2
        # start = (center[0] - dy, center[1] - dx)
        # end = (center[0] + dy, center[1] + dx)
        
        # for e,i in enumerate(tqdm(I, desc="Extracting profiles", unit="profiles")):
        for e,i in enumerate(I):
            if e == len(I): #0:
                show=True
            else:
                show=False
            i = np.squeeze(i)
            if verbose:
                print(f'Getting profile #{e+1} out of {len(I)}')
            profileI, XS,YS, sc,ec = angled_profile_with_coords(i/255, angle_deg=ROTATE,show=show)
            profileP, XS,YS, sc,ec = angled_profile_with_coords((P[e]/255)*2*np.pi - np.pi, angle_deg=ROTATE)
            # if axis=='hor':
            #     profileI = getLineProfile(i/255,axis=1)
            #     profileP = getLineProfile((P[e]/255)*2*np.pi - np.pi,axis=1)
            # elif axis=='ver':
            #     profileI = getLineProfile(i/255,axis=0)
            #     profileP = getLineProfile((P[e]/255)*2*np.pi - np.pi,axis=0)
            # if verbose:
            #     print(f'Getting profile #{e+1} out of {len(I)}')
            # if axis=='hor':
            #     profile = getLineProfile(i,axis=1)
            # elif axis=='ver':
            #     profile = getLineProfile(i,axis=0)
            if show:
                plotComplexWithColorbar(create_wavefield(P,I),[res,res],title="test")
            else:
                pass
            if norm:
                
                # P = np.angle(profile)
                # I = np.abs(profile)
                imin,imax = limits[0][e][0], limits[0][e][1]
                pmin,pmax = limits[1][e][0], limits[1][e][1]
                
                profileI = ((profileI)*(imax - imin)) + imin
                # I = ((I/255.0)*(imax - imin)) + imin
                # P = ((P/255.0)*(pmax - pmin)) + pmin

                if log:
                    profileI = np.log(profileI)
                
            profile = create_wavefield(profileP, profileI)
                # profile = create_wavefield(P, I)

            p.append(profile)
    #        print(f'max p: {np.max(profile)}')
    #     pI, pP = [],[]
    #     I,P = I
    #     for e,i in enumerate(I):
    #         if verbose:
    #             print(f'Getting profile #{e+1} out of {len(I)}')
    #         if axis=='hor':
    #             profileI = getLineProfile(i/255,axis=1)
    #             profileP = getLineProfile((P[e]/255)*2*np.pi,axis=1)
    #         elif axis=='ver':
    #             profileI = getLineProfile(i,axis=0)
    #             profileP = getLineProfile((P[e]/255)*2*np.pi,axis=0)
    #         pI.append(profileI)
    #         pP.append(profileP)
    # #        print(f'max p: {np.max(profile)}')
    #         if plotProfiles:
    #             plt.figure()
    #             plt.plot(profileI, label=f'#{e}')
    #         else:
    #             pass
    else:
        for e,i in enumerate(I):
            if e == 0:
                show=True
            else:
                show=False
            if verbose:
                print(f'Getting profile #{e+1} out of {len(I)}')
            # if axis=='hor':
            #     profile = getLineProfile((i/255),axis=1)
            # elif axis=='ver':
            #     profile = getLineProfile((i/255),axis=0)
            
            
            profile, XS,YS, sc,ec = angled_profile_with_coords(i/255, angle_deg=ROTATE,show=show)
            
            if norm:
                imin,imax = limits[e][0], limits[e][1]
                
                if norm=='phase':
                    profile = profile*2*np.pi - np.pi #(((profile)*(imax - imin)) + imin)
                else:
                    profile = (((profile)*(imax - imin)) + imin)
                # I = ((I/255.0)*(imax - imin)) + imin
                # P = ((P/255.0)*(pmax - pmin)) + pmin
    
                if log:
                    profile = np.log(profile)
                
            p.append(profile)
    #        print(f'max p: {np.max(profile)}')
            if plotProfiles:
                plt.figure()
                plt.plot(profile, label=f'#{e}')
            else:
                pass
    if plotProfiles:
        plt.legend()
        plt.show()

    if pick:
        # try:
        if savePath:
            import pickle
            with open(savePath + '_profilestack.pkl', "wb") as f:
                pickle.dump(np.transpose(p), f)
        # except:
        #     pass

    # if log:
    #     p = np.log(p)
    
    if comp:
        # print("Combining intensity and phase profiles and building complex propagation plot... ")
        # pI = np.squeeze(np.transpose(pI))
        # pP = np.squeeze(np.transpose(pP))
        # p = create_wavefield(pP,pI)
        # p = Complex2HSV(np.transpose(p), np.mean(abs(np.array(p))), np.max(abs(np.array(p))))
        # p = Complex2HSV(np.transpose(p), np.min(abs(np.array(p))), np.max(abs(np.array(p))))
        p = np.squeeze(np.transpose(p))
    else:
        p = np.squeeze(np.transpose(p))
#    print(np.shape(p))
    nx,ny = np.shape(p)[1],np.shape(p)[0]
    dx = abs(zRange/zPlanes)
    NY = np.sqrt( ( (ec[0] - sc[0]) )**2  + ( (ec[1] - sc[1]) )**2 )
#    print('Here')
    #p = [[i if i>1.0e5 else 0.0 for i in row] for row in p]
    
    y_extent = (-(NY/2) * res, (NY/2) * res)
    x_extent = (zi,zi+abs(zRange))
    extent = [x_extent[0]*1e6, x_extent[1]*1e6, y_extent[0]*1e6, y_extent[1]*1e6]
    
    print(f"z-range:                    {zRange}")
    print(f"dx:                         {dx}")
    print(f"z-planes:                   {zPlanes}")
    print(f"extent used for plotting:   {extent}")
    print(f"length of angled profile {np.sqrt( ( (ec[0] - sc[0]) )**2  + ( (ec[1] - sc[1]) )**2 )}")
    print(f"{res*NY}")

#    maxp = np.
    if log:
        plt.figure()
        print(lMin)
        print(abs(np.max(p)))
        im = plt.imshow(p, aspect='auto', extent=extent) #norm=LogNorm(vmin=lMin,vmax=abs(np.nanmax(p))),cmap=cmap, extent=extent)
    else:
        if comp:
            import plot_complex_colourbar
            if savePath:
                savePath = savePath + 'compplot.svg'
            else:
                pass
            im = plot_complex_colourbar.plotComplexWithColorbar(p,save_path=savePath,px=[dx,res],extent=extent)
        else:
            plt.figure()
            im = plt.imshow(p, aspect='auto', extent=extent,cmap=cmap)##cmap='gist_rainbow')# cmap='gray')
    # plt.yticks([int((ny-1)*(b/(9-1))) for b in range(0,9)],
    #            [round_sig(ny*res*(a/(9-1))) for a in range(-int((9-1)/2),int((9/2 + 1)))],fontsize=10 )
    # plt.xticks([int((nx-1)*(b/(9-1))) for b in range(0,9)],
    #            [round_sig(nx*dx*(a/(9-1))) for a in  range(0,int((9 + 1)))],fontsize=10)
#    plt.xticks([int((nx-1)*(b/(9-1))) for b in range(0,9)],
#               [round_sig(nx*dx*(a/(9-1))) for a in  range(-int((9-1)/2),int((9/2 + 1)))],fontsize=10)
    if comp == False:
        plt.colorbar(label='intensity [a.u]').ax.tick_params(labelsize=10)
    plt.xlabel('Propagation Distance [m]',fontsize=15 )#[\u03bcm]')
    if axis == 'hor':
        plt.ylabel('x [µm]',fontsize=15 )#[\u03bcm]')
    if axis == 'ver':
        plt.ylabel('y [µm]',fontsize=15 )#[\u03bcm]')
    # plt.title(label='Propagation Plot')
    plt.tight_layout()
    if savePath:
        print(f'Saving propagation plot to: {savePath}')
        plt.savefig(savePath + '.svg')#, dpi=300)
        import pickle
        try:
            with open(savePath + '.pkl', "wb") as f:
                pickle.dump(im, f)
        except:
            print('... pickling failed')
    plt.show()
    

def angled_profile_with_coords(img, angle_deg, order=1, show=False):
    """
    Take a full-length line profile through the center of a 2D array at a given angle.
    Returns the profile and the x/y coordinates along the line.
    """
    from skimage.measure import profile_line
    h, w = img.shape
    center = np.array([h/2, w/2])

    # Convert angle to radians
    theta = np.deg2rad(angle_deg)

    # Maximum half-length (center to farthest corner)
    half_length = np.sqrt((h/2)**2 + (w/2)**2)

    # Direction vector
    dx = half_length * np.cos(theta)
    dy = half_length * np.sin(theta)

    # Start and end in (row, col) = (y, x)
    start = (center[0] - dy, center[1] - dx)
    end   = (center[0] + dy, center[1] + dx)

    # Profile and coordinates
    profile = profile_line(img, start, end, order=order, reduce_func=None)

    # Create coordinate arrays (skimage returns N samples)
    num_points = len(profile)
    ys = np.linspace(start[0], end[0], num_points)
    xs = np.linspace(start[1], end[1], num_points)
    
    if show:
        plt.figure()
        plt.imshow(abs(img),aspect='auto')
        plt.plot([start[1],end[1]], [start[0],end[0]], color='red', linewidth = 2)
        plt.axis('off')
        plt.show()

    return profile, xs, ys, start, end

def test():
	f = h5py.File('/data/xfm/22353/analysis/eiger/SXDM/tele_fzp/173674_46/dumps/ptypy_173674_46_256_roi_9999_gpu/ptypy_173674_46_256_roi_9999_gpu_ML_0360.ptyr', 'r')
	
	showRecon(f)
	
# 	#props.
# if __name__=='__main__':
#     test()

