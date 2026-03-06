#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 09:44:12 2020

@author: gvanriessen

test/demonstrate the use of Experiment class in runner.py

"""

from xl.runner import experiment, makeDirs, csvParams, listOfNumbers


def main():

    # Experiment will execute experiment for each value in a list
    
    runModule = 'blE90'
    parametersFile = '/user/home/opt/xl/xl/experiments/E90/params.csv'
    
    ''' Define/override parameters '''
    options = [     
        
        ['op_nested', 'i', 0, 'Nested loop over experiment parameters if true, else multiple parameters are changed for each event in the experiment'],
        
        #Single-Electron Wavefront Propagation
        ['ws', 'i', 1, 'calculate single-electron (/ fully coherent) wavefront propagation'],
             
        # HDF output     
        ['wfr_file', 's', 'wf_final.hdf', 'Name of file to write final wavefront to (uses wfSave plugin)'],
        
        # or?
        ['wfFileOut', 's', 'wf.h5', 'file name for wavefront after propagation.'],
        
        #disable some plots for testing
        ['ws_pl', 's', '1', 'plot the resulting intensity distributions in graph(s): ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],
        
        #enable plots from actions (plugins)
        ['ws_pli', 's', 'xy', 'plot intensity and phase distributions, borrowing other parameters si_*: ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],
        ['ws_plp', 's', 'xy', 'plot intensity and phase distributions, borrowing other parameters si_*: ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],
               
        # Specify the directory where action modules are located. Default is wfactions [Should this actually be a package name?]
        ['actionsDir','s', 'xl.wfactions', 'directory where action scripts are located'],
        
        # disable actions:  (yes, it is silly that the default is enabled)
        ['wfInterferencePatternProperties1DWide','',False,'Enable/Disable Action (True/False) '],
        ['showWavefront','',                        False,'Enable/Disable Action (True/False) '],
        ['wfInterferencePatternProperties2D','',    False,'Enable/Disable Action (True/False) '],
        ['wfFWHM','',                               False,'Enable/Disable Action (True/False) '],
        ['template','',                             False,'Enable/Disable Action (True/False) '],
        ['wfSave','',                               False,'Enable/Disable Action (True/False) '],
        ['wfInterferencePatternProperties1D','',    False,'Enable/Disable Action (True/False) '],
        ['wfLineProfiles','',                       False,'Enable/Disable Action (True/False)'],
        ['wfSaveIntensity','',                      True,'Enable/Disable Action (True/False)'], 
        ['describeWavefront','',                    False,'Enable/Disable Action (True/False)'], 
        ['sumIntensity','',                         False,'Enable/Disable Action (True/False)'], 
        ['pickleWavefront','',                      False,'Enable/Disable Action (True/False)'], 

        ]

    ''' We can load variables into a list of dict from csv file:
        This is especially useful if the column names match parameter names expected
        by srwl_bl.  All variables will be stored with the experiment output, which 
        is useful for record keeping. 
        '''
    p  = csvParams(parametersFile)
    for k,v in p.items():
        if listOfNumbers(v):
            v = [float(i) for i in v]
        options.append([k, '', list(v), ''])
        
    
    # we assume that the csv file included a column for the output directory, i.e. fdir
    makeDirs(p['fdir'])
    
    multiE = True
    if multiE == True:
        options.append(['wm', '', '1', 'calculate multi-electron (/ partially coherent) wavefront propagation', 'store_true'])
        options.append(['si_type', 'i', 1, 'type of a characteristic to be extracted after calculation of intensity distribution: 0- Single-Electron Intensity, 1- Multi-Electron Intensity, 2- Single-Electron Flux, 3- Multi-Electron Flux, 4- Single-Electron Radiation Phase, 5- Re(E): Real part of Single-Electron Electric Field, 6- Im(E): Imaginary part of Single-Electron Electric Field, 7- Single-Electron Intensity, integrated over Time or Photon Energy'],)
        # options.append(['wm_ch', 'i', 0, 'type of a characteristic to be extracted after calculation of multi-electron wavefront propagation: #0- intensity (s0); 1- four Stokes components; 2- mutual intensity cut vs x; 3- mutual intensity cut vs y; 40- intensity(s0), mutual intensity cuts and degree of coherence vs X & Y'],)
    elif multiE == False:
        options.append(['wm', '', '', 'calculate multi-electron (/ partially coherent) wavefront propagation', 'store_true'])
        options.append(['si_type', 'i', 0, 'type of a characteristic to be extracted after calculation of intensity distribution: 0- Single-Electron Intensity, 1- Multi-Electron Intensity, 2- Single-Electron Flux, 3- Multi-Electron Flux, 4- Single-Electron Radiation Phase, 5- Re(E): Real part of Single-Electron Electric Field, 6- Im(E): Imaginary part of Single-Electron Electric Field, 7- Single-Electron Intensity, integrated over Time or Photon Energy'],)
        # options.append(['wm_ch', 'i', 0, 'type of a characteristic to be extracted after calculation of multi-electron wavefront propagation: #0- intensity (s0); 1- four Stokes components; 2- mutual intensity cut vs x; 3- mutual intensity cut vs y; 40- intensity(s0), mutual intensity cuts and degree of coherence vs X & Y'],)

    exp = experiment(options=options, # options to customise experiment (optional)
                     moduleName=runModule  #specify name of run module, default 'run' if not specified
                     )
    exp.run()
    
    
    # You can now list the paramaters and 'results', which are dependent variables:
    #exp.printParameters() 
    #exp.printResults()
    
    # You can also list the values of a variable:
    #print(exp.listValues('intensitySum'))
    
    ''' Finally, you can plot any pair of parameters or variables, including ones 
    loaded from the csv file e.g.
    '''
    #exp.plot(y='Intensity/Horizontal/meanDynamicRangeC', x='heightRMS')

if __name__ == '__main__':
    main()
