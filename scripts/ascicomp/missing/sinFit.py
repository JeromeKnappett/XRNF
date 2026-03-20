#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 13:31:57 2025

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    mean = np.nanmean(yy)
    inds = np.where(np.isnan(yy))
    # print(inds)
    yy[inds] = np.take(mean,inds)
    
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    
    Fyy = abs(np.fft.fft(yy))
    
    # plt.plot(Fyy[1::])
    # plt.show()
    # print(ff[np.argmax(Fyy[1:])+1])
    # print(Fyy[-1])
    # print(Fyy[1])
    
    guess_freq1 = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_freq2 = abs(ff[np.argmax(Fyy[2:-2])+1])
    guess_amp1 = np.std(yy) * 2.**0.5
    guess_amp2 = np.std(yy) * 2.**0.5
    guess_offset1 = np.mean(yy)
    guess_offset2 = np.mean(yy)
    guess = np.array([guess_amp1, 2.*np.pi*guess_freq1, 0., guess_offset1,guess_amp2, 2.*np.pi*guess_freq2, 0., guess_offset2])

    def multiSinFunc(t, A1, w1, p1, c1, A2, w2, p2, c2):
        S = (A1 * np.sin(w1*t + p1) + c1) + (A2 * np.sin(w2*t + p2) + c2)
        return S
    popt, pcov = scipy.optimize.curve_fit(multiSinFunc, tt, yy, p0=guess)
    A1, w1, p1, c1, A2, w2, p2, c2 = popt
    f1 = w1/(2.*np.pi)
    f2 = w2/(2.*np.pi)
    fitfunc = lambda t:  (A1 * np.sin(w1*t + p1) + c1) + (A2 * np.sin(w2*t + p2) + c2)
    return {"amp1": A1, "omega1": w1, "phase1": p1, "offset1": c1, "freq1": f1, "period1": 1./f1,"amp2": A2, "omega2": w2, "phase2": p2, "offset2": c2, "freq2": f2, "period2": 1./f2, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}


def fitTriangle(tt,yy):
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    A=90;f=1/856; p=-np.pi-0.5; c=460    
    guess_freq = f#abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = A #np.std(yy) * 2.**0.5
    guess_offset = c#np.mean(yy)
    guess_phase = p#np.max(yy)
    
    
    guess = np.array([guess_amp, guess_freq, guess_phase, guess_offset])
    def triangleFunc(t,A,f,p,c):
        # Argument that goes through 2À each period
        arg = 2 * np.pi * f * t + p  # Radians
    
        # Map arg into [0, 2À), then scale to x in [0, 2)
        #   (arg % 2À) / À -> in [0, 2)
        x = (arg % (2 * np.pi)) / np.pi  # x in [0, 2)
    
        # For x in [0,1], ramp up; for x in [1,2], ramp down
        # This yields y in [0,1]
        y = np.where(x < 1, x, 2 - x)
    
        # Scale from [0,1] to [-1, +1], then apply amplitude and offset
        wave = A * (2 * y - 1) + c
        return wave
    popt, pcov = scipy.optimize.curve_fit(triangleFunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}
    
