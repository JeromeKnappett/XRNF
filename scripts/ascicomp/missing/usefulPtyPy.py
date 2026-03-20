#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 15:01:33 2023

@author: -
"""

def buildComplexProbe(path):
    import numpy as np
    import pickle
    
    pick = pickle.load(open(path, 'rb'))
    EhR, EhI, EvR, EvI = pick[0], pick[1], pick[2], pick[3]
    res = (pick[4],pick[5])
    
    Eh = EhR + EhI*1j
    Ev = EvR + EvI*1j
    cE = Eh + Ev
    
    print(np.shape(cE))
    
    P.probe = Container(P, 'Cprobe', data_type='complex')
    
    
    pr_shape = (1,)+ tuple(G.shape)
    pr = P.probe.new_storage(shape=pr_shape, psize=G.resolution)

    # Probe is loaded through the :py:meth:`~ptypy.core.classes.Storage.fill` method.
    pr.fill(moon_probe)
    fig = u.plot_storage(pr, 0)
    fig.savefig('%s_%d.png' % (scriptname, fig.number), dpi=300)
    
#     prC = P.probe.new_storage(shape=pr)
#     pr3 = P.probe.new_storage(shape=pr_shape, psize=G.resolution)
# y, x = pr3.grids()
# apert = u.smooth_step(fsize[0]/5-np.abs(x), 3e-5)*u.smooth_step(fsize[1]/5-np.abs(y), 3e-5)
# pr3.fill(apert)
# fig = u.plot_storage(pr3, 2)
# fig.savefig('%s_%d.png' % (scriptname, fig.number), dpi=300)
    
    return cE
    

def test():
    path = '/user/home/opt/xl/xl/experiments/correctedAngle_coherence3/data/sx100sy100/sx100sy100Efields.pkl'
    
    buildComplexProbe(path)
    
if __name__=='__main__':
    test()