#!/usr/bin/env python
#
# Name: prop_free_nf.py
# Author: Cameron M. Kewish
#
# Description:
# Near field propagation, propagates <wavefield> by <distance>,
# using <wavelength>, and the dimension of one pixel is <psize>.
#
# Dependencies: numpy
#
# To do:
#
# History:
#
# 2018-04-28: Cameron M. Kewish, first version forked from cSAXS matlab
# program prop_free_nf.m


def prop_free_nf(wavefield, wavelength, distance, psize=1.):
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

    import numpy as np
    import matplotlib.pyplot as plt

    program = 'prop_free_nf'

    asize = np.squeeze(np.shape(wavefield))

    if np.size(psize) == 1:
        psize = np.array((psize, psize))
    
    
    # print(psize)
    # print(asize)
    # print(distance)
    # print(wavelength)
    
    if np.sqrt(np.sum(1.0/psize**2) * np.sum(1.0/(asize*psize)**2)) * \
            abs(distance) * wavelength > 1:
        print('{0}: warning: there could be some aliasing issues...'.
              format(program))
        print('{0}: (you could enlarge your array, or try a far field '
              'method)'.format(program))

    ind0 = np.arange(-asize[0]/2, asize[0]/2)
    ind1 = np.arange(-asize[1]/2, asize[1]/2)

    [x1,x2] = np.meshgrid(ind1/(asize[0]*psize[0]), ind0/(asize[1]*psize[1]))
    q2 = np.fft.fftshift(x1**2 + x2**2)
   
    wavefield_out = np.fft.ifft2( np.fft.fft2(wavefield) * \
            np.exp(2.0 * 1j * np.pi * (distance / wavelength) * \
                    (np.sqrt(1.0 - q2 * wavelength**2) - 1)))

    return wavefield_out

def test():
    import numpy as np
    import matplotlib.pyplot as plt
    import pickle
    
    path = '/user/home/opt/xl/xl/experiments/correctedWBS_beamCharacterisation/data/'
    names = ['maskExitEfield']
    #['24nmTMincident','24nmTMexit','24nmTEincident','24nmTEexit']
    files = [path + str(n) + '/' + str(n) + 'Efields.pkl' for n in names]
    
#    picks = [pickle.load(open(f, 'rb')) for f in files]
#    N = [(int(p[2]),int(p[3])) for p in picks]
#    nTot = [n[0]*n[1] for n in N]
#    res = [(p[4],p[5]) for p in picks]
#    Ex = [p[0] for p in picks]
#    Ey = [p[1] for p in picks]
    
    T = [pickle.load(open(f, 'rb')) for f in files]
    EhR = [p[0] for p in T]
    EhI = [p[1] for p in T]
    EvR = [p[2] for p in T]
    EvI = [p[3] for p in T]
    res = [(p[4],p[5]) for p in T]
    Eh = [eR + eI*1j for eR,eI in zip(EhR,EhI)]
    Ev = [eR + eI*1j for eR,eI in zip(EvR,EvI)]
    # E = [np.sqrt((h**2) + (v**2)) for h,v in zip(Eh,Ev)]
    E = [eh + ev for eh,ev in zip(Eh,Ev)]
    
    
    plt.imshow(abs(np.array(E[0])),aspect='auto')
    plt.show()
    
    D = [2e-6*r for r in range(10,200,10)]#,10)]
    for d in D:
        Wout = prop_free_nf(E[0],6.7e-9,d,psize=np.array((res[0][1],res[0][0])))
        
        plt.imshow(abs(np.array(Wout)),aspect='auto')
        plt.title('d = {} m'.format(d))
        plt.show()
        
        
        
#    Wout = prop_free_nf(E[0],6.7e-9,1,psize=np.array((res[0][1],res[0][0])))
#    
#    plt.imshow(abs(np.array(E[0])),aspect='auto')
#    plt.show()
#    
#    plt.imshow(abs(np.array(Wout)),aspect='auto')
#    plt.show()
    
        
        
if __name__=='__main__':
    test()
        
    