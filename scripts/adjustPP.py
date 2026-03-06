#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 13:52:41 2024

@author: -
"""

def adjustPropParams(current_res,current_shape,new_res,new_shape,pp):
    
    dx,dy = current_res
    Nx,Ny = current_shape
    
    newdx, newdy = new_res
    newNx, newNy = new_shape
    
    a_dx = newdx / dx
    a_dy = newdy / dy
    
    a_nx = (newNx / Nx) # / a_dx
    a_ny = (newNy / Ny) # / a_dy
    
    new_pp = [p/a for p,a in zip(pp,[a_dx/a_nx,a_dx,a_dy/a_ny,a_dy])]
    
    return new_pp


def adjustRange(current_range,desired_range,pp):
    factor = desired_range / current_range
    new_pp = factor*pp
    return factor


def test():
    # at pinhole:
    nx,ny = 1600,1600
    dx,dy = 5.0e-8,4.98e-8
    rx,ry = dx*nx, dy*ny
    
    
    new_res = [75.0e-6,75.0e-6]#[10.0e-9,10.0e-9]
    new_shape = [2048,2048] #[rx/new_res[0]/2,ry/new_res[1]/2]
    
    print()
    
    current_pp = [2.5, 0.2, 2.5, 0.2]
    
    new_pp = adjustPropParams([dx,dy], [nx,ny], new_res, new_shape, current_pp)
    
    print(new_pp)
    
    # Dx, Dy  = 0.0001451164034208724,6.399557119087705e-05
    # Nx, Ny = 1782,1232
    
    # new_res = [75.0e-6,75.0e-6]
    # new_shape = [Nx,Ny]#[1028, 1060]
    
    # pp = [167.30363245666365, 0.0016621455778422186, 231.59584078085845, 0.0012514659048723403,]
    
    # new_pp = adjustPropParams([Dx,Dy], [Nx,Ny], new_res, new_shape, pp)
    
    # print(new_pp)
    
    
if __name__ == '__main__':
    test()