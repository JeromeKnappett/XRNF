#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 14:51:24 2022

@author: jerome
"""

import phidl.geometry as pg
from phidl import Device, Layer, LayerSet
from phidl import quickplot as qp
import numpy as np
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

class FZP():
    def __init__(self, D, wl, delta_r):
        '''
        D: Lens diameter
        wl: wavelength
        delta_r: Outzone thickness
        '''
        self.D = D
        self.wl = wl
        self.delta_r = delta_r
        
        self.f = (self.D*self.delta_r)/self.wl #approx
        self.num_zones = self.D/(4*self.delta_r)
    def generate(self):
        n_raddii = np.zeros(int(self.num_zones))

        for n in range(1,int(self.num_zones)):
            n_raddii[-n] = np.sqrt(n*self.wl*self.f)
        
        D = pg.circle(radius = n_raddii[0], angle_resolution = 2.5, layer = 0)
        for r in range(1,int(self.num_zones)):
            if (r % 2) == 0:
                D.add_ref(pg.ring(radius = n_raddii[-r], width = n_raddii[-r]-n_raddii[-r-1] , angle_resolution = 2.5e-3, layer = 0))
        return D
            
def slowplot(items):  # noqa: C901
    """Takes a list of devices/references/polygons or single one of those, and
    plots them. Use `set_quickplot_options()` to modify the viewer behavior
    (e.g. displaying ports, creating new windows, etc)
    Parameters
    ----------
    items : PHIDL object or list of PHIDL objects
        The item(s) which are to be plotted
    Examples
    --------
    >>> R = pg.rectangle()
    >>> quickplot(R)
    >>> R = pg.rectangle()
    >>> E = pg.ellipse()
    >>> quickplot([R, E])
    """
    import sys
    import io
    import gdspy
    from matplotlib.lines import Line2D
    import matplotlib
    from matplotlib.collections import PolyCollection
    from matplotlib.widgets import RectangleSelector
    import phidl
    from phidl.device_layout import (
        CellArray,
        Device,
        DeviceReference,
        Layer,
        Path,
        Polygon,
        _rotate_points,
    )
    from phidl.quickplotter import _update_bbox, _get_layerprop, _draw_polygons,_draw_line


    fig, ax = plt.subplots()

    ax.axis("equal")
#     ax.grid(True, which="both", alpha=0.4)
#     ax.axhline(y=0, color="k", alpha=0.2, linewidth=1)
#     ax.axvline(x=0, color="k", alpha=0.2, linewidth=1)
    bbox = None

    # Iterate through each each Device/DeviceReference/Polygon
    if not isinstance(items, list):
        items = [items]
    for item in items:
        if isinstance(item, (Device, DeviceReference, CellArray)):
            polygons_spec = item.get_polygons(by_spec=True, depth=None)
            for key in sorted(polygons_spec):
                polygons = polygons_spec[key]
                layerprop = _get_layerprop(layer=key[0], datatype=key[1])
                new_bbox = _draw_polygons(
                    polygons,
                    ax,
                    facecolor="k",
                    edgecolor="k",
                    alpha=1,
                )
                bbox = _update_bbox(bbox, new_bbox)


        elif isinstance(item, Polygon):
            polygons = item.polygons
            layerprop = _get_layerprop(item.layers[0], item.datatypes[0])
            new_bbox = _draw_polygons(
                polygons,
                ax,
                facecolor="k",
                edgecolor="k",
                alpha=1,
            )
            bbox = _update_bbox(bbox, new_bbox)

#     if bbox is None:
#         bbox = [-1, -1, 1, 1]
    xmargin = 0#(bbox[2] - bbox[0]) * 0.01 + 1e-9
    ymargin = 0#(bbox[3] - bbox[1]) * 0.01 + 1e-9
    ax.set_xlim([bbox[0] - xmargin, bbox[2] + xmargin])
    ax.set_ylim([bbox[1] - ymargin, bbox[3] + ymargin])
    
    with io.BytesIO() as buff:
        plt.axis('off')
        fig.savefig(buff, format='raw')
        buff.seek(0)
        data = np.frombuffer(buff.getvalue(), dtype=np.uint8)
    w, h = fig.canvas.get_width_height()
    im = data.reshape((int(h), int(w), -1))


    return fig,ax,im

def test():    
    '''
    D: Lens diameter
    wl: wavelength
    delta_r: Outzone thickness
    '''
    D = 20.0e-6
    wl = 6.7e-9
    dr = 50.0e-9
    fzp = FZP(D,wl,dr)
    D = fzp.generate()
    
    #quick plot
    qp(D)
    
    #slow plot
    fig,ax,im = slowplot(D)
    plt.axis('off')
    plt.draw()
    plt.savefig('fzp.pdf')
    plt.show()
    
    import tifffile
    
    tifffile.imwrite(D,'/user/home/opt/xl/xl/FZP_200um.tif')
    
    # im
    
if __name__=='__main__':
    test()