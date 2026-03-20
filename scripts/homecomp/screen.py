#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 11:29:05 2019

@author: G van Riessen

Adapted from WPG oeScreen class to provide convenient feedback during propagation through a beamline
Not maintained, not recommended for use



"""
     
class oeScreen(Empty):
    """
    class: Based on WPG Screen optical element

    Originally made to write intensity files to common format that is convenient for inspection
    
    
    """
    
    def __init__(self, filename=None, 
                       writeIntensity = True,
                       writePhase = False,
                       showIntensity = False,
                       showPhase = False,
                       calculateMetrics = True,
                       description = None,
                       ROI=None):
        """ Constructor for the Screen class.

        :param filename: Name of file to store wavefront data.
        :type filename: str
        :raise IOError: File exists.
        """
        
         # Initialize base class.
        super(oeScreen, self).__init__()
        self.description = description
        
        if filename is not None:
            self.extension = '.h5' #os.path.splitext(filename)[1]
            self.filename = os.path.splitext(filename)[0]
        else:
            self.filename = None
        
        self.writeIntensity = writeIntensity
        self.writePhase = writePhase
        
        self.showIntensity = showIntensity
        self.showPhase = showPhase
        
        self.calculateMetrics = calculateMetrics
        self.ROI = ROI
        
    def describe(self,wfr,ROI):
        ''' 
        print and return summary of wfr
        
        param ROI: tuple of tuples: [{roi_xmin,roi_xmax}, {roi_ymin,roi_ymax}] where each value is in pixels
        '''
              
        #mesh = wfr.params.Mesh           
        [nx, ny, xmin, xmax, ymin, ymax] = get_mesh(wfr)
        dx = (xmax-xmin)/nx
        dy = (ymax-ymin)/ny

        intensity = wfr.get_intensity(polarization='horizontal')
        intensityOnAxis = intensity[nx//2, ny//2] / intensity.max()
        
        if ROI is not None:    
            # Note that ROI valus are in units of pixels
            print ('Analysing ROI: [{},{}], [{},{}]'.format(ROI[0][0],ROI[0][1],ROI[1][0],ROI[1][1]))
            intensity = intensity[ROI[0][0]:ROI[0][1],ROI[1][0]:ROI[1][1]]
            xmin, xmax = ROI[0][0]*dx, ROI[0][1]*dx
            ymax, ymin = ROI[1][0]*dy, ROI[1][1]*dy
            nx,ny = np.abs(ROI[0][1]-ROI[0][0]), np.abs(ROI[1][0]-ROI[1][1])
            
        intensityTotal = intensity.sum()
        #intensityTotal = np.squeeze(intensity)
        intensityTotal = intensityTotal*dx*dy#*1e6*1e-9   # [GW] /  dx [mm]/ dy [mm], i.e. GW/mm^2
        
        energy = intensity*wfr.params.photonEnergy/J2EV#*1e3
        try:
            imax = np.max(energy)
        except:
            imax = 0
        
        x_center = intensity[nx//2, :]
        fwhm_x = len(x_center[x_center > x_center.max()/2])*dx

        y_center = intensity[:, ny//2]
        fwhm_y = len(y_center[y_center > y_center.max()/2])*dy
        
        intensityPeak = imax*1e-9*1e6*2*np.pi*(fwhm_x/2.35)*(fwhm_y/2.35)
        
        print('stepX, stepY [um]:', dx * 1e6, dy * 1e6, '\n')
        print('Total power: %g [GW]' % intensityTotal)
        print('Peak power calculated using FWHM:         %g [GW]' %(intensityPeak))
        print('Max irradiance: %g [GW/mm^2]'    %(imax*1e-9))
        
        #label4irradiance = 'Irradiance (W/$mm^2$)'

        summary = {'IntensitySum':intensityTotal,
                   'IntensityPeak':intensityPeak,
                   'dx':dx,
                   'dy':dy,
                   'fwhm_x':fwhm_x, 
                   'fwhm_y': fwhm_y}
        
        print(summary)
        
        return summary

    
    def show(self,wfr):
        
        if self.showIntensity:
            plotWavefront(wfr, self.description)
            #plot_intensity_map(wfr, save=self.description, range_x=None, range_y=None,im_aspect='equal')
            
        if self.showPhase:
            
            plotWavefront(wfr, self.description, phase=True)
            
        
        
    def write(self,wfr):
        
        if self.filename is not None:
            if self.extension == '.h5':
                wfr.store_hdf5(self.filename + self.extension)
                
            if self.writeIntensity == True:
                imageio.imwrite(self.filename + '_intensity.tif', wfr.get_intensity(polarization='horizontal'))
                
            if self.writePhase == True:
                imageio.imwrite(self.filename + '_phase.tif', wfr.get_phase(polarization='horizontal'))
        else:
            print('No filename.  Wavefield at screen will not be saved')
         
        
    def propagate(self, wfr):
        """ Overloaded propagation for this element. """

        #we could propagate to allow resizing etc, but then we need to manage preservation of original wavefield.
        # better to keep functinoality restricted to that of a screen, and manage its use outside class.
        ##super(oeScreen, self).propagate(wfr, propagation_parameters)
        
        if self.filename is not None:
            self.write(wfr)
        
        self.show(wfr)
        
        if self.calculateMetrics:
            metrics = self.describe(wfr, self.ROI)
            return metrics
        else:
            return None
                 
            
    def plotPhase(self, wfr, title, cuts=False, interactive=True):
    # adapted from WPG with minor modifications.
    #draw wavefront with common functions
        J2EV = 6.24150934e18
        
        wf_phase = wfr.get_phase(polarization='horizontal')
        ii = wf_phase
   
        ii = ii*wfr.params.photonEnergy/J2EV#*1e3
        imax = np.max(ii)
        [nx, ny, xmin, xmax, ymin, ymax] = get_mesh(wfr)
        dx = (xmax-xmin)/(nx-1); dy = (ymax-ymin)/(ny-1)
        print('stepX, stepY [um]:', dx * 1e6, dy * 1e6, '\n')

        if wfr.params.wEFieldUnit != 'arbitrary':
            print('Total power (integrated over full range): %g [GW]' %(ii.sum(axis=0).sum(axis=0)*dx*dy*1e6*1e-9))
            print('Max irradiance: %g [GW/mm^2]'    %(imax*1e-9))
            label4irradiance = 'Irradiance (W/$mm^2$)'
        else:
                ii = ii / imax
                label4irradiance = 'Irradiance (a.u.)'

        [x1, x2, y1, y2] = wfr.get_limits()
    
       
        pylab.figure(figsize=(21,6))
        pylab.imshow(ii, extent=[x1 * 1e3, x2 * 1e3, y1 * 1e3, y2 * 1e3])
        pylab.set_cmap('hot')
        pylab.axis('tight')
        #pylab.colorbar(orientation='horizontal')
        pylab.xlabel('x (mm)')
        pylab.ylabel('y (mm)')
        pylab.axes().set_aspect(0.5)
    
        pylab.title(title)
        pylab.show()

  