

import phidl.geometry as pg
from phidl import Device, Layer, LayerSet
from phidl import quickplot as qp
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def siemens_star(r,min_feature=2, num_spikes=128, unit=1,layer=0):
    """Produces a Siemens star
    Parameters
    ----------
    r : int or float
        radius of Siemens star
    cut : int or float
        min feature size
    num_spikes : int, 
        number of spikes in star
    layer : int, array-like[2], or set
        Specific layer(s) to put polygon geometry on.
    Returns
    -------
    D : Device
        A Device containing the grating
        geometry.
    """

    theta = np.arange(-np.pi,np.pi,2*np.pi/num_spikes)
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    D = Device()
    for k in range(0,int(num_spikes/2)):
        D.add_polygon([(0,0),(x[2*k -1],y[2*k -1]),(x[2*k ],y[2*k])], layer=layer)

    r2 = (num_spikes*min_feature*unit)/(2*np.pi)
    circ = pg.circle(radius = r2, angle_resolution = r2/10, layer = 0)
    C = pg.boolean(A = D, B = circ, operation = 'not', precision = 1e-6,
               num_divisions = [1,1], layer = 0)
    return C
    
def fit2wafer(wafer,die, diameter,diex,diey,spacing=0):
    """Packs die in regular spacing on a wafer.

    Parameters
    ----------
    die : Device
        The die to fit to a wafer.
    diameter : int or float
        Wafer diameter
    diex : int or float
        die width
    diey : int or float
        die height
    spacing: int or float
        dead space for dicing etc
    Returns
    -------
    D : Device
        A Device containing as many die as possible
    """
    D= Device()

    for x in np.arange(-diameter/2,diameter/2,diex+(spacing/2)):
        for y in np.arange(-diameter/2,diameter/2,diey+(spacing/2)):
            if x**2 + y**2 < (diameter/2)**2:
                D.add_ref(die).movex(x - ((diex/2)+(spacing/2))).movey(y -((diey/2)+(spacing/2)))
            else:
                pass
    wafer.add_ref(D)
    return wafer

def FZP( D, wl, delta_r,layer):

        '''
        Paramaters
        D: Lens diameter
        wl: wavelength
        delta_r: Outzone thickness
        ----------
        Returns 
        D: Device
        '''

        f = (D*delta_r)/wl #approx
        num_zones = D/(4*delta_r)

        n_raddii = np.zeros(int(num_zones))

        for n in range(1,int(num_zones)):
            n_raddii[-n] = np.sqrt(n*wl*f)
        
        D = pg.circle(radius = n_raddii[-1], angle_resolution = 2.5, layer = layer)
        for r in range(1,int(num_zones)):
            if (r % 2) == 0:
                D.add_ref(pg.ring(radius = n_raddii[-r], width = n_raddii[-r]-n_raddii[-r-1] , angle_resolution = 2.5e-3, layer = 0))
        return D

def gc(radius, initial_angle, final_angle, points=500):
    """
    This methods generates points in a circle shape at (0,0) with a specific radius and from a 
    starting angle to a final angle.
    Args:
        radius: radius of the circle in microns
        initial_angle: initial angle of the drawing in degrees
        final_angle: final angle of the drawing in degrees
        points: amount of points to be generated (default 199)
    Returns:
        Set of points that form the circle
    """
    theta = np.linspace(    np.deg2rad(initial_angle), 
                            np.deg2rad(final_angle), 
                            points)

    return  radius * np.cos(theta) , radius * np.sin(theta) 

def grating(size,pitch, duty_cycle=0.5, layer=0):
    """Produces a square grating
    Parameters
    ----------
    size : size of grating
    pitch : int or float
        pitch
    duty_cycle : int or float
        duty cycle
    layer : int, array-like[2], or set
        Specific layer(s) to put polygon geometry on.
    Returns
    -------
    D : Device
        A Device containing the grating
        geometry.
    """

    D = Device("grating")
    assert round(size % pitch) == 0, 'size must be multiple of pitch'
    num_lines = size/pitch

    for i in range(int(num_lines)):

        R = pg.rectangle(size=(pitch*duty_cycle, size), layer=layer)
        D.add_ref(R).movex(i*pitch)
    D.movex(-size/2).movey(-size/2)
    return D







def PEC_test(min_feature,layer=0):
    '''
    Copies the proximity effect test pattern found here 
    https://ebeam.wnf.uw.edu/ebeamweb/doc/patternprep/patternprep/proximity_main.html
    Parameters
    ----------
    min_feature: Minimum feature size
    
    Returns
    -------
    D : Device
        A Device containing the grating
        geometry.

    '''
    D = Device("PEC test")

    size = int(min_feature*5)
    

    i = -1

    for x in np.arange(0,size+1,min_feature/2):
        i +=1
        j = -1
        for y in np.arange(0,size+1,min_feature/2):
            j +=1
            if (i % 2) == 0:
                D.add_ref(pg.rectangle(size=(size, min_feature), layer=layer)).movey(x*2) #First set of horizontal lines
                if (j % 2) == 0:
                    D.add_ref(pg.rectangle(size=(min_feature, min_feature), layer=layer)).movex(size + 2*x).movey(2*(size-y)) # Even set of squares 
            elif (i % 2 and j % 2) == 1:  
                D.add_ref(pg.rectangle(size=(min_feature, min_feature), layer=layer)).movex(size + 2*x ).movey(2*(size-y))     # Odd Sqares
                D.add_ref(pg.rectangle(size=((3*size-2*x), min_feature), layer=layer)).movex((size*3) +min_feature).movey(2*x)    # Second (odd) set of lines
                D.add_ref(pg.rectangle(size=(min_feature,(3*size-2*x)), layer=layer)).movex((2*(3*size-x))+min_feature).movey(2*x)# Corresponding vertical lines
                if i > 1:
                    D.add_ref(pg.rectangle(size=(min_feature,2*size), layer=layer)).movex((2*(3*size-x))+2*min_feature).movey(3*size)

        
    D.add_ref(pg.rectangle(size=(min_feature,4*size), layer=layer)).movex(((7*size-2*x))+min_feature).movey(5*size)
    PEC =  pg.offset(D, distance = 0, join_first = True, precision = 1e-6,
        num_divisions = [1,1], layer = 0)
    return PEC



















        
# def sample_die(layer,idim, jdim,idx=0,jdx=0,side='front'):
#         '''
#     Creates Sample Die
#     Parameters
#     ----------
#     layer: Layer of Die
#     idim: Label for i-dimension. 
#     jdim: Label for j-dimension
#     side: front or back side of die
#     Returns
#     -------
#     D : Device
#         A Device containing the grating
#         geometry.

#     '''
#     D = Device('Sample Die')
#     R = pg.rectangle(size=(5e3, 5e3), layer=layer) #Die itself
#     BL = pg.rectangle(size=(250, 250), layer=layer-1) #Bottom Left, global alignment
#     LA = pg.cross(length = 100, width = 10, layer = layer+1) #Local ALignment
#     BRS = pg.rectangle(size=(10, 10), layer=layer+1)
#     D.add_ref(R)
#     D.add_ref(BL)
#     D.add_ref(LA).movex(5e3 -50).movey(50)
#     D.add_ref(BRS).movex(5e3+40 -50).movey(0)
    
#     D.add_ref(LA).movex(5e3 -50).movey(5e3 -50)
#     D.add_ref(BRS).movex(5e3+40 -50).movey(5e3-10)
    
    
#     D.add_ref(LA).movex(50).movey(5e3 -50)
#     D.add_ref(BRS).movex(0).movey(5e3-10)
#     if side == 'front':
#         x=0
#         y=1e3
#         D << grating(1e3,50, duty_cycle=0.5, layer=7).movex(x+1.5e3).movey(y+3e3)
#         D << grating(1e3,50, duty_cycle=0.5, layer=7).rotate(90).movex(x+2.5e3).movey(y+3e3)
#         D << pg.text(text = '1 mm / 50 um', size = 1e2,
#             justify = 'left', layer = 7).movex(x+1.5e3).movey(y+3.625e3)


#         D << grating(.5e3,5, duty_cycle=0.5, layer=7).movex(x+3.5e3).movey(y+3.25e3)
#         D << grating(.5e3,5, duty_cycle=0.5, layer=7).rotate(90).movex(x+3.5e3).movey(y+2.75e3)
#         D << pg.text(text = '500 / 5 um', size = 1e2,
#             justify = 'left', layer = 7).movex(x+3e3).movey(y+3.625e3)


#         D << grating(.25e3,1, duty_cycle=0.5, layer=7).movex(x+4.25e3).movey(y+3.25e3)
#         D << grating(.25e3,1, duty_cycle=0.5, layer=7).rotate(90).movex(x+4.25e3).movey(y+2.75e3)
#         D << pg.text(text = '250 / 1 um', size = 1e2,justify = 'left', layer = 7).movex(x+3.875e3).movey(y+3.625e3)

#         D << grating(1e2,.5, duty_cycle=0.5, layer=7).movex(x+1.25e3).movey(y+2.1e3)
#         D << grating(1e2,.5, duty_cycle=0.5, layer=7).rotate(90).movex(x+1.4e3).movey(y+2.1e3)
#         D << pg.text(text = '100 um / 500 nm', size = .5e2,
#             justify = 'left', layer = 7).movex(x+1e3).movey(y+2.25e3)

#         D << grating(50,.05, duty_cycle=0.5, layer=7).movex(x+1.75e3).movey(y+2.1e3)
#         D << grating(50,.05, duty_cycle=0.5, layer=7).rotate(90).movex(x+1.85e3).movey(y+2.1e3)
#         D << pg.text(text = '10 um / 50 nm', size = .5e2,
#             justify = 'left', layer = 7).movex(x+1.75e3).movey(y+2.25e3)

#         D << pg.gridsweep(
#             function = pg.circle,
#             param_x = {'radius' : [10,20,40,60,80,100]},
#             param_y = {'layer'  : [0,6,3,9]},
#             param_defaults = {},
#             param_override = {},
#             spacing = (30,10),
#             separation = True,
#             align_x = 'x',
#             align_y = 'y',
#             edge_x = 'x',
#             edge_y = 'ymax',
#             label_layer = None).movex(3.5e3).movey(2.25e3)

#         #Window topside
#         D << pg.rectangle(size = (1e3, 1e3), layer = 8).movex((5e3 - 1e3)/2).movey((5e3 - 1e3)/2)


#         D << siemens_star(200,num_spikes=64).movex(1.25e3).movey(y+1.75e3)


#         D << siemens_star(200,num_spikes=64).movex(1.25e3).movey(y+1.3e3)


#         D << siemens_star(400,num_spikes=64).movex(1.25e3).movey(y+0.6e3)


#         for x in range(1,5):
#             for y in range(1,5):
#                 D << PEC_test(int(100/x),layer=6).movex(4.25e3).movey(0.75e3+(2e2*x))


#     #     fzp = FZP(100,6.7e-3,500e-3,7)
#     #     D << fzp.generate().movex(x+3e3).movey(y+2e3)

#     #     fzp = FZP(200,6.7e-3,500e-3,7)
#     #     D << fzp.generate().movex(x+3e3).movey(y+1.75e3)

#     #     fzp = FZP(500,6.7e-3,500e-3,7)
#     #     D << fzp.generate().movex(x+3e3).movey(y+1.275e3)
#         D << pg.text(text = f'{idim[idx]}{jdim[jdx]}', size = 1e3,
#         justify = 'left', layer = 2).movex(2e3).movey(0)
#         return D.movex(-5e3/2).movey(-5e3/2) 
#     elif side == 'rear':
#                 #Window Bottom side
#         etch_depth = 0.5e3
#         offset = 2*np.tan(np.deg2rad(54.74))*etch_depth
#         D << pg.rectangle(size = (1e3+offset, 1e3+offset), layer = 9).movex((1e3+offset)/2).movey((1e3+offset)/2)
#         D.mirror(p1=(0, D.ymax), p2=(0, D.ymin))
#         D << pg.text(text = f'{idim[-idx]}{jdim[-jdx]}', size = 1e3,
#             justify = 'right', layer = 2).movex(-2e3).movey(0)
#         return D.movex(5e3/2).movey(5e3/2)

# def label(D,idx=0,jdx=0,side='front'):

#     if side == 'front':
#         D << pg.text(text = f'{idim[idx]}{jdim[jdx]}', size = 1e3,
#         justify = 'left', layer = 2).movex(2e3).movey(0)
#         return D.movex(-5e3/2).movey(-5e3/2) 


if __name__ == "__main__":
    # D = Device() #Inititate Device
    # ls = LayerSet() # Create a blank LayerSet

    D = siemens_star(100,2, num_spikes=64, layer=0)
    qp(D)
    # D = PEC_test(10)


    # qp(D)
    # plt.show()
    # D.write_gds(filename = r'C:\Users\blair\PhD\Mask Fabrication\CAD_Files\test_siemens_star.gds', # Output GDS file name
    #         unit = 1e-6,                  # Base unit (1e-6 = microns)
    #         precision = 1e-9,             # Precision / resolution (1e-9 = nanometers)
    #         auto_rename = True,           # Automatically rename cells to avoid collisions
    #         max_cellname_length = 28,     # Max length of cell names
    #         cellname = 'toplevel'         # Name of output top-level cell
    #        )
    
    # jdim = np.arange(0,20,1)
    # idim = ['A','B','C','D','E','F','G','H','I', 'J','K','L','M','N','O','P']

    # jdx = 0

    # D = sample_die(4,side='rear')
    # radius = 35e3
    # for x in tqdm(np.arange(-radius,radius,5e3)):
    #     idx = 0
    #     for y in np.arange(-radius,radius,5e3):
    #         if x**2 + y**2 < radius**2:

    #             D << label(D.copy('die'),idx=0,jdx=0,side='rear')
    #         else:
    #             pass
    #         idx +=1
    #     jdx +=1
    # plt.ion()
    # fig = qp(D)  
    # test = Device()
    # test.add_polygon([gc((100e3/2),
    #         0 - 71.03,
    #         180 + 71.03)], layer = 1) 
    # test << pg.circle()
    # fw = fit2wafer(test,pg.rectangle(size = (5e3,5e3), layer = 2), 80e3,5e3,5e3,spacing=10000)

    # qp(fw)


    # PEC = PEC_test(105,layer=0)
    # qp(PEC)
    plt.show()