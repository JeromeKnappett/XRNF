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
    
    runModule = 'blBeamPolarisation17'
    parametersFile = '/user/home/opt/xl/xl/experiments/beamPolarisation17ME/params0.csv'
    
    ''' Define/override parameters '''
    options = [     
        
        ['op_nested', 'i', 0, 'Nested loop over experiment parameters if true, else multiple parameters are changed for each event in the experiment'],
        
        #Single-Electron Wavefront Propagation
        ['ws', 'i', 1, 'calculate single-electron (/ fully coherent) wavefront propagation'],
        
        #Multi-electron wavefront propagation
        ['wm', '', '', 'calculate multi-electron (/ partially coherent) wavefront propagation', 'store_true'],
        ['wm_ch', 'i', 0, 'type of a characteristic to be extracted after calculation of multi-electron wavefront propagation: #0- intensity (s0); 1- four Stokes components; 2- mutual intensity cut vs x; 3- mutual intensity cut vs y; 40- intensity(s0), mutual intensity cuts and degree of coherence vs X & Y'],
        ['wm_fbk', '', 1, 'create backup file(s) with propagated multi-e intensity distribution vs horizontal and vertical position and other radiation characteristics', 'store_true'],
        ['stokes_fname','s','stokes',''],
        ['res_ipm','','','container for results of multi-electron wavefront propagation.'],
        ['wm_nm', 'i', 5000, 'number of macro-electrons (coherent wavefronts) for calculation of multi-electron wavefront propagation'],
        ['wm_na', 'i', 10, 'number of macro-electrons (coherent wavefronts) to average on each node for parallel (MPI-based) calculation of multi-electron wavefront propagation'],
        ['wm_ns', 'i', 10, 'saving periodicity (in terms of macro-electrons / coherent wavefronts) for intermediate intensity at multi-electron wavefront propagation calculation'],

             
        # HDF output     
        ['wfr_file', 's', 'wf_final.hdf', 'Name of file to write final wavefront to (uses wfSave plugin)'],
        
        # or?
        ['wfFileOut', 's', 'wf.h5', 'file name for wavefront after propagation.'],
        
        #disable some plots for testing
        ['ws_pl', 's', '', 'plot the resulting intensity distributions in graph(s): ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],
        
        #enable plots from actions (plugins)
        ['ws_pli', 's', 'xy', 'plot intensity and phase distributions, borrowing other parameters si_*: ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],
        ['ws_plp', 's', 'xy', 'plot intensity and phase distributions, borrowing other parameters si_*: ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],
               
        # Specify the directory where action modules are located. Default is wfactions [Should this actually be a package name?]
        ['actionsDir','s', 'xl.wfactions', 'directory where action scripts are located'],
        
        # disable actions:  (yes, it is silly that the default is enabled)
        ['wfInterferencePatternProperties1DWide','',False,'Enable/Disable Action (True/False) '],
        ['showWavefront','',True,'Enable/Disable Action (True/False) '],
        ['wfInterferencePatternProperties2D','',False,'Enable/Disable Action (True/False) '],
        ['wfFWHM','',False,'Enable/Disable Action (True/False) '],
        ['template','',False,'Enable/Disable Action (True/False) '],
        ['wfSave','',True,'Enable/Disable Action (True/False) '],
        ['wfSaveIntensity','',True,'Enable/Disable Action (True/False) '],
        ['wfInterferencePatternProperties1D','',True,'Enable/Disable Action (True/False) '],
        #['wfPolarisation','',True,'Enable/Disable Action (True/False) '],
        ['wfMutualIntensity','',False,'Enable/Disable Action (True/False) '],
        ['wfComplexProfile','',False,'Enable/Disable Action (True/False) '],
        ['wfStokes','',True,'Enable/Disable Action (True/False) '],
        ['wfStokes1D','',True,'Enable/Disable Action (True/False) '],
        ['wfCheckSampling','',False,'Enable/Disable Action (True/False) '],

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
