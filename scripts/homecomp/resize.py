#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 10:31:31 2020

@author: gvanriessen
"""
import sys, argparse
sys.path.append('./wpg/')
sys.path.append('./extensions/')

from wfutils import  modifyDimensions,  getDimensions, check_sampling
from wavefront import Wavefront


def resize(args):
    
    w = Wavefront()
    w.load_hdf5(args.ifile)
    nx, ny, dx, dy, rx, ry = getDimensions(w)

    
    if args.px and args.py:
        resolution = (args.px, args.py)
    else:
        resolution = None
        
    if args.rx and args.ry:
        dimensions = (args.rx, args.ry)
    else:
        dimensions  = None
        
    
    modifyDimensions(w,  R=dimensions, D=resolution) 
    
    if args.check == True:
        check_sampling(w)

    w.store_hdf5(args.ofile)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--px', type=float, default=None,
                        help='Pixel width (x)')
    parser.add_argument('--py', type=float, default=None,
                        help='Pixel height (y')
    parser.add_argument('--rx', type=float, default=None,
                        help='Wavefront width (x)')
    parser.add_argument('--ry', type=float, default=None,
                        help='Wavefront height (y')
    parser.add_argument('--ifile', type=str, default=None,
                        help='Input wavefront (HDF5 file path)')
    parser.add_argument('--ofile', type=str, default=None,
                        help='Output wavefront (HDF5 file path)')
    parser.add_argument("-c","--check",action="store_true",help="Check sampling after resize")    
    args = parser.parse_args()
    resize(args)
    
    
if __name__ == '__main__':
    main()