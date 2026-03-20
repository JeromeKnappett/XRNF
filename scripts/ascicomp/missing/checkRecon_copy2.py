
import h5py
import matplotlib.pyplot as plt
plt.ion()
import numpy as np
# import propagators as props
from math import floor, log10
import tifffile
from matplotlib.colors import LogNorm
import ptypy

# %%
def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
            return x

def prop_free_nf(wavefield, wavelength, distance, psize=1.,padx=100,pady=100):
    """
    Syntax:
        prop_free_nf(wavefield, wavelength, distance [, psize])

    Python script to propagate a wavefields in the near field.
   
    Parameters:
        wavefield             (ndarray) : complex input wavefield
        wavelength              (float) : wavelength in meters
        distance                (float) : propagation distance in meters
       
    Optional parameters:
        psize                   (float) : pixel size in meters
                                        : [default = 1.0 (pixel units)]

    Returns:
        wavefield_out         (ndarray) : propagated wavefield
    """


    program = 'prop_free_nf'

    if padx or pady:
        wavefield = np.pad(wavefield, ((pady, pady), (padx, padx)), mode='constant')

    asize = np.shape(wavefield)
    print('asize:', asize)
    
    if np.size(psize) == 1:
        psize = np.array((psize, psize))
       
    if np.sqrt(np.sum(1.0/psize**2) * np.sum(1.0/(asize*psize)**2)) * \
            abs(distance) * wavelength > 1:
        print('{0}: warning: there could be some aliasing issues...'.
              format(program))
        print('{0}: (you could enlarge your array, or try a far field '
              'method)'.format(program))
        print(np.sqrt(np.sum(1.0/psize**2) * np.sum(1.0/(asize*psize)**2)) * \
                abs(distance) * wavelength)

    ind0 = np.arange(-asize[0]/2, asize[0]/2)
    ind1 = np.arange(-asize[1]/2, asize[1]/2)

    [x1,x2] = np.meshgrid(ind1/(asize[0]*psize[0]), ind0/(asize[1]*psize[1]))
    q2 = np.fft.fftshift(x1**2 + x2**2)
   
    wavefield_out = np.fft.ifft2( np.fft.fft2(wavefield) * \
            np.exp(2.0 * 1j * np.pi * (distance / wavelength) * \
                    (np.sqrt(1.0 - q2 * wavelength**2) - 1)),s=asize)#[int(asize[0]+pady),int(asize[1]+padx)])

    return wavefield_out

def Complex2HSV(z, rmin, rmax, hue_start=90):
    from matplotlib.colors import hsv_to_rgb
    # get amplidude of z and limit to [rmin, rmax]
    amp = np.abs(z)
    amp = np.where(amp < rmin, rmin, amp)
    amp = np.where(amp > rmax, rmax, amp)
    ph = np.angle(z, deg=1) + hue_start
    # HSV are values in range [0,1]
    h = (ph % 360) / 360
    s = 0.85 * np.ones_like(h)
    v = (amp -rmin) / (rmax - rmin)
    return hsv_to_rgb(np.dstack((h,s,v)))


def showRecon(f, prop=0, comp=False, rmphase=False, log=False,unwrap=False, scan_name = 'scan_00',n_pmodes=10):
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
    
    for ob in OB:
        if rmphase == 'probe':
            probeModes(pr,px,comp,rmphase=True,scan=scan_name,nmodes=n_pmodes)
            showObject(ob,px,comp,log=log,unwrap=unwrap,scan=scan_name)
            if prop:
                propESW(ob,px,prop,comp,log=log,unwrap=unwrap,scan=scan_name)
        elif rmphase == 'obj':
            probeModes(pr,px,comp,scan=scan_name,nmodes=n_pmodes)
            showObject(ob,px,comp,rmphase=True,log=log,unwrap=unwrap,scan=scan_name)
            if prop:
                propESW(ob,px,prop,comp,rmphase=True,log=log,unwrap=unwrap,scan=scan_name)
        elif rmphase == 'both':
            probeModes(pr,px,comp,rmphase=True,scan=scan_name,nmodes=n_pmodes)
            showObject(ob,px,comp,rmphase=True,log=log,unwrap=unwrap,scan=scan_name)
            if prop:
                propESW(ob,px,prop,comp,rmphase=True,log=log,unwrap=unwrap,scan=scan_name)
        else:
            probeModes(pr,px,comp,scan=scan_name,nmodes=n_pmodes)
            showObject(ob,px,comp,log=log,unwrap=unwrap,scan=scan_name)
            if prop:
                propESW(ob,px,prop,comp,log=log,unwrap=unwrap,scan=scan_name)
        

def probeModes(pr,px,comp=False, rmphase=False, scan = 'scan_00', nmodes=10):
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
    
    if comp:
        import c2image
        # obC = Complex2HSV(ob, np.min(abs(ob)), np.max(abs(ob)))
        prC = [Complex2HSV(n,np.min(abs(n)),np.max(abs(n))) for n in nplist]
        fig = plt.figure()
        
        for i in range(len(nplist)): #number of probe modes
            if nmodes > 5:
                plt.subplot(2,int(nmodes/2),i+1)
            else:
                plt.subplot(1,nmodes,i+1)
            plt.imshow(prC[i])
            if i == 0 or i == 5:
                plt.yticks([int((ny-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],
                           [round_sig(ny*px*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))])#,fontsize=fSize )            
                plt.ylabel('y [um]')
            else:
                plt.yticks([],[])
                pass
            plt.xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],
                       [round_sig(nx*px*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))])#,fontsize=fSize)
            plt.xlabel('x [um]')
            plt.title(amp[i])
        fig.suptitle(scan)
        fig.tight_layout()
        plt.show()
    else:
        fig = plt.figure()
        for i in range(len(nplist)): #number of probe modes
            if nmodes > 5:
                plt.subplot(2,int(nmodes/2),i+1)
            else:
                plt.subplot(1,nmodes,i+1)
            plt.imshow(np.abs(nplist[i]))
            if i == 0 or i == 5:
                plt.yticks([int((ny-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],
                           [round_sig(ny*px*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))])#,fontsize=fSize )            
                plt.ylabel('y [um]')
            else:
                plt.yticks([],[])
                pass
            plt.xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],
                       [round_sig(nx*px*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))])#,fontsize=fSize)
            plt.xlabel('x [um]')
            plt.title(amp[i])
        fig.suptitle(scan)
        fig.tight_layout()
        plt.show()

def showObject(ob,px,comp=False,rmphase=False,log=False,unwrap=False, scan='scan_00'):
    if rmphase:
        ob = ptypy.utils.rmphaseramp(np.squeeze(ob))
    else:
         pass# = [f['/content/obj/S' + scan + 'G00/data'][()]] #ptypy.utils.rmphaseramp(np.squeeze(f['/content/obj/S' + scan + 'G00/data'][()]))
    # px = f['/content/obj/S' + scan + 'G00/_psize'][()][0]
        
    print('Shape of object array: ', np.shape(ob))
    sF = 1e6 # convert from m to um
    numXticks = 15
    numYticks = 15
    (ny,nx) = np.shape(np.squeeze(ob)[50:-50, 50:-50])

    print('nx: ', nx)
    print('ny: ', ny)        
    print('px: ', px)    
    
    print(np.shape(ob))
    if comp:
        import c2image
        obC = Complex2HSV(np.squeeze(ob)[50:-50, 50:-50],np.min(abs(np.squeeze(ob)[50:-50, 50:-50])),np.max(abs(np.squeeze(ob)[50:-50, 50:-50])))
        
        print(np.shape(obC))
        
        plt.figure()
        plt.imshow(obC)
        plt.yticks([int((ny-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],
                    [round_sig(ny*px*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))])#,fontsize=fSize )
        plt.xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],
                    [round_sig(nx*px*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))])#,fontsize=fSize)
        plt.xlabel('x [um]')
        plt.ylabel('y [um]')
        plt.title(scan + ': ' + 'Complex Wavefield')
        # plt.colorbar()
        plt.show()
        
        # plt.figure()
        # plt.imshow(obCBar)
        # plt.title('color bar')
        # plt.show()
    else:
        plt.figure()
        if unwrap:
            plt.imshow(np.unwrap(np.angle(np.squeeze(ob)[50:-50, 50:-50])))
        else:
            plt.imshow(np.angle(np.squeeze(ob)[50:-50, 50:-50]))
        plt.yticks([int((ny-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],
                    [round_sig(ny*px*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))])#,fontsize=fSize )
        plt.xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],
                    [round_sig(nx*px*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))])#,fontsize=fSize)
        plt.xlabel('x [um]')
        plt.ylabel('y [um]')
        plt.title(scan + ': ' + 'Phase')
        plt.colorbar()
        plt.show()

        plt.figure()
        if log:
            plt.imshow(np.log(np.abs(np.squeeze(ob)[50:-50, 50:-50])**2))
            plt.title(scan + ': ' + 'Intensity (log)')
        else:
            plt.imshow(np.abs(np.squeeze(ob)[50:-50, 50:-50])**2)
            plt.title(scan + ': ' + 'Intensity')
        plt.yticks([int((ny-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],
                    [round_sig(ny*px*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))])#,fontsize=fSize )
        plt.xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],
                    [round_sig(nx*px*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))])#,fontsize=fSize)
        plt.xlabel('x [um]')
        plt.ylabel('y [um]')
        plt.colorbar()
        plt.show()
            

def propESW(ob,px,prop,comp=False,rmphase=False, dx = 0, dy=0,log=False,unwrap=False, scan = 'scan00'):
    if rmphase:
        ob = ptypy.utils.rmphaseramp(np.squeeze(ob))
    else:
        pass
        # ob = f['/content/obj/S' + scan + 'G00/data'][()] #ptypy.utils.rmphaseramp(np.squeeze(f['/content/obj/S' + scan + 'G00/data'][()]))
    # px = f['/content/obj/S' + scan + 'G00/_psize'][()][0]
    sF = 1e6 # convert from m to um
    numXticks = 15
    numYticks = 15
    pad = [int(dx/px), int(dy/px)]
    print(f"Propagating {prop} m ...")
    print('Shape of ob:', np.shape(ob))
    ESW = prop_free_nf(np.squeeze(ob), wavelength=0.148307e-9, distance=prop, psize=px ,padx=pad[0],pady=pad[1]) 
    print('Shape of ESW: ', np.shape(ESW))
    
    if comp:
        ESWC = Complex2HSV(np.squeeze(ESW)[50:-50, 50:-50],np.min(abs(np.squeeze(ESW)[50:-50, 50:-50])),np.max(abs(np.squeeze(ESW)[50:-50, 50:-50])))
        print(np.shape(ESWC))
        print(int(dx / px))
        (ny,nx,nc) = np.shape(ESWC)
    
        plt.figure()
        plt.imshow(ESWC)
        plt.yticks([int((ny-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],
                    [round_sig(ny*px*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))])#,fontsize=fSize )
        plt.xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],
                    [round_sig(nx*px*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))])#,fontsize=fSize)
        plt.xlabel('x [um]')
        plt.ylabel('y [um]')
        plt.title(scan + ': ' + f"Complex Wavefield (z = {prop} m)")
        # plt.colorbar()
        plt.show()
    else:
        (ny,nx) = np.shape(np.squeeze(ESW)[50:-50, 50:-50])
        plt.figure()
        if unwrap:
            plt.imshow(np.unwrap(np.angle(np.squeeze(ESW)[50:-50, 50:-50])))
        else:
            plt.imshow(np.angle(np.squeeze(ESW)[50:-50, 50:-50]))
        plt.yticks([int((ny-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],
                   [round_sig(ny*px*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))])#,fontsize=fSize )
        plt.xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],
                   [round_sig(nx*px*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))])#,fontsize=fSize)
        plt.xlabel('x [um]')
        plt.ylabel('y [um]')
        plt.title(scan + ': ' + f"Phase (z = {prop} m)")
        plt.show()
    
        plt.figure()
        if log:
            plt.imshow(np.log(np.abs(np.squeeze(ESW)[50:-50, 50:-50])))
            plt.title(scan + ': ' + f"Amplitude (log) (z = {prop} m)")
        else:
            plt.imshow(np.abs(np.squeeze(ESW)[50:-50, 50:-50]))
            plt.title(scan + ': ' + f"Amplitude (z = {prop} m)")
        plt.yticks([int((ny-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],
                   [round_sig(ny*px*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))])#,fontsize=fSize )
        plt.xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],
                   [round_sig(nx*px*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))])#,fontsize=fSize)
        plt.xlabel('x [um]')
        plt.ylabel('y [um]')
        plt.show()

def multiProp(ob,px,zi,zf,dz,dx=0,savePath=None,show=False, scan = 'scan00'):
    # plt.close('all')
    # ob = f['/content/obj/S' + scan + 'G00/data'][()]
    # px = f['/content/obj/S' + scan + 'G00/_psize'][()][0]
    
    N = abs(int((zf-zi)/dz))
    zR = zi - zf
    print(f"Propagating wavefield from {zi} m to {zf} m, in {N} steps of {dz} m ...")
    Z = np.linspace(zi,zf,N)
    # print(Z)
    I, P = [], []
    for z in Z:
        ESW = prop_free_nf(np.squeeze(ob)[50:-50, 50:-50], wavelength=0.148307e-9, distance=z, psize=px,padx=int(dx / px)+200,pady=200)
        
        i = np.abs(np.squeeze(ESW))
        p = np.angle(np.squeeze(ESW))
        i_min = np.min(i)
        i_max = np.max(i)
        p_min = np.min(p)
        p_max = np.max(p)

        if i_max > i_min:
            i = ((i - i_min) / (i_max - i_min)) * 255
        i.astype(np.uint8)

        if p_max > p_min:
            p = ((p - p_min) / (p_max - p_min)) * 255
        p.astype(np.uint8)

        I.append(i)
        P.append(p)
    
    if savePath:
        saveTiffStack(savePath + '_intensity.tif', I)
        saveTiffStack(savePath + '_phase.tif', P)
    if show:
        showTiffStack(savePath + '_intensity.tif',zi,zR,N,px,zPlot=True)
        showTiffStack(savePath + '_phase.tif',zi,zR,N,px,zPlot=True)
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

    arrays = [(a/np.max(a))*255 for a in arrays]
    for i,a in enumerate(arrays):
        a_min = np.min(a)
        a_max = np.max(a)
        if a_max > a_min:
            a = ((a - a_min) / (a_max - a_min)) * 255
        a = a.astype(np.uint8)
        arrays[i] = a

    # Stack along the first axis (creates a 3D array: (num_images, height, width))
    stack = np.stack(arrays, axis=0)
    
    # Save as a multi-page TIFF
    tifffile.imwrite(filename, stack, photometric='minisblack')#, dtype=)
    print(f"Saved {len(arrays)} images to {filename}")


def showTiffStack(filename,zi,zR,N,px=1,zPlot=False,comp=False):
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
    stack = np.squeeze(tifffile.imread(filename))
    num_slices = stack.shape[0]
    print('shape of stack:', np.shape(stack))
    # Set up figure and show the first slice
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)  # Leave space at the bottom for the slider
    current_slice = 0

    # Display the first slice
    im = ax.imshow(stack[current_slice], cmap='gray')
    ax.set_title(f"Slice: {current_slice}")
    ax.axis('off')

    # Define slider axis and create the slider
    # (left, bottom, width, height) in figure coordinates
    slider_ax = plt.axes([0.1, 0.1, 0.8, 0.03])
    slice_slider = Slider(
        ax=slider_ax,
        label='Slice',
        valmin=0,
        valmax=num_slices - 1,
        valinit=current_slice,
        valstep=1  # Only move in integer steps
    )

    # Callback to update image when slider is moved
    def update(val):
        slice_index = int(slice_slider.val)
        im.set_data(stack[slice_index])
        ax.set_title(f"Slice: {slice_index}")
        # Redraw canvas
        fig.canvas.draw_idle()

    # Register the update function with each slider move
    slice_slider.on_changed(update)

    # Show the interactive figure
    plt.show()
    
    if zPlot:
        propPlot(stack,zi,zR,N,res=px)

# %%
def getLineProfile(a,axis=0, mid=None, show=False):
    nx, ny = np.shape(a)[1], np.shape(a)[0]
    if mid == None:
        midX, midY = int(nx/2), int(ny/2)
    else:
        midX, midY = int(mid[1]), int(mid[0])    
    # print(midX)
    
    if axis == 0:
        p = a[:,midX]
        title = 'vertical profile'
    elif axis == 1:
        p = a[midY,:]
        title = 'horizontal profile'
    
    if show:
        plt.plot(p)
        plt.title(title)
        plt.show()
    
    return p

def propPlot(I,zi,zRange,zPlanes,res=1,axis='hor',log=False,lMin=1,savePath=False,plotProfiles=False,verbose=True):
    cmap='viridis'
    p=[]
    for e,i in enumerate(I):
        if verbose:
            print(f'Getting profile #{e+1} out of {len(I)}')
        if axis=='hor':
            profile = getLineProfile(i,axis=1)
        elif axis=='ver':
            profile = getLineProfile(i,axis=0)
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
#    print(np.shape(p))
    nx,ny = np.shape(p)[0],np.shape(p)[1]
    dx = zRange/zPlanes
#    print('Here')
    p = np.squeeze(np.transpose(p))
    #p = [[i if i>1.0e5 else 0.0 for i in row] for row in p]
    plt.figure()
#    maxp = np.
    if log:
        print(lMin)
        print(abs(np.max(p)))
        im = plt.imshow(p, aspect='auto',norm=LogNorm(vmin=lMin,vmax=abs(np.nanmax(p))),cmap=cmap)
    else:
        im = plt.imshow(p, aspect='auto',cmap=cmap)
    plt.yticks([int((ny-1)*(b/(9-1))) for b in range(0,9)],
               [round_sig(ny*res*(a/(9-1))) for a in range(-int((9-1)/2),int((9/2 + 1)))],fontsize=10 )
    # plt.xticks([int((nx-1)*(b/(9-1))) for b in range(0,9)],
    #            [round_sig(nx*dx*(a/(9-1))) for a in  range(0,int((9 + 1)))],fontsize=10)
#    plt.xticks([int((nx-1)*(b/(9-1))) for b in range(0,9)],
#               [round_sig(nx*dx*(a/(9-1))) for a in  range(-int((9-1)/2),int((9/2 + 1)))],fontsize=10)
    plt.colorbar(label='intensity [a.u]').ax.tick_params(labelsize=10)
    plt.xlabel('Propagation Distance [m]',fontsize=15 )#[\u03bcm]')
    if axis == 'hor':
        plt.ylabel('x [m]',fontsize=15 )#[\u03bcm]')
    if axis == 'ver':
        plt.ylabel('y [m]',fontsize=15 )#[\u03bcm]')
    plt.title(label='Propagation Plot')
    plt.tight_layout()
    if savePath:
        print(f'Saving propagation plot to: {savePath}')
        plt.savefig(savePath + '.eps', dpi=300)
        import pickle
        with open(savePath + '.pkl', "wb") as f:
            pickle.dump(im, f)
    plt.show()
    
    #Cm = [contrastMichelson(_p) for _p in p]
    #Crms = [contrastRMS(_p) for _p in p]
    #Cm2d = [contrastMichelson(i) for i in I]
    #Crms2d = [contrastRMS(i) for i in I]
    
    # print(Cm)
    # print(Crms)
    
    #plt.figure()
    #plt.plot(np.linspace(-zi,-zi-zRange,len(Cm)),Cm,label='Michelson 1D')
    #plt.plot(np.linspace(-zi,-zi-zRange,len(Crms)),Crms,label='RMS 1D')
    #plt.plot(np.linspace(-zi,-zi-zRange,len(Cm2d)),Cm2d,label='Michelson 2D')
    #plt.plot(np.linspace(-zi,-zi-zRange,len(Crms2d)),Crms2d,label='RMS 2D')
    #plt.xlabel('z [m]')
    #plt.ylabel('Contrast')
    #plt.legend()
    #plt.show()
    
    
# def contrastMichelson(A):
#     '''
#     Return Michelson contrast: $\frac{\max(I) - \min(I)}{\max(I) + \min(I)}$
    
#     Michelson contrast is highly sensitive to noise. Since it is calculated only from extrema, i.e., at two pixels
    
#     In the case where the optical fringe period is comparable to pixel size, Michelson contrast is also sensitive to the phase difference,between pixel grid and optical fringe signal. 
#     '''
#     maxA = np.max(A)
#     minA = np.min(A)
#     C = (maxA-minA) / (maxA+minA)
#     return C


# def contrastRMS(A):
#     '''
#     Return root mean squared contrast. 
            
#     RMS contrast does not depend on the angular frequency content or the spatial distribution of contrast in the image.
#     '''    
#     # normalise it first  ---  wrong to do this
#     #A = (A-np.min(A))/(np.max(A)-np.min(A))    
#     A = (A)/ np.max(A) 

#     N = np.size(A)
#     mean = np.mean(A)    
#     C = np.sqrt( 1/N * np.sum(  np.square((A - mean)/mean)) )
    
#     # fro comparison to Michelson Contrast:
#     C = C * np.sqrt(2)
    
#     return C

def test():
	f = h5py.File('/data/xfm/22353/analysis/eiger/SXDM/tele_fzp/173674_46/dumps/ptypy_173674_46_256_roi_9999_gpu/ptypy_173674_46_256_roi_9999_gpu_ML_0360.ptyr', 'r')
	
	showRecon(f)
	
	#props.

