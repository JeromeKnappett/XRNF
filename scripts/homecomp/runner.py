#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 10:47:04 2020

@author: gvanriessen
"""

import errno, os, copy

from xl.action import ActionCollection
from wpg.wavefront import Wavefront
from xl.srwl_blx import beamline  # this wraps original srwl_bl
from srwl_bl import srwl_uti_merge_options, srwl_uti_parse_options
#from diskcache import Cache
import pickle as pkl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import collections
import csv
from slugify import slugify

from prettyprinter import pprint

def csvParams(filename):
    ''' 
    Returns a dictionary with keys equal to column names and a values equal to 
    a list of values in the corresponding column of a csv file identified by filename
    '''
    with open(filename, "r") as infile:
       reader = csv.reader(infile)
       headers = next(reader, None)  # returns the headers or `None` if the input is empty
       lists = [i for i in zip(*reader)]
    d = {}
    for h, l in zip(headers, lists):
        d.update({h:l})
    return d

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def listOfNumbers(l):
    nums = True
    for item in l:
        nums = nums and isNumber(item)
    return nums
    
def makeDirs(dirList):
    
    for path in dirList:
        print('Creating {}'.format(path))
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
                
def makehash():
    return collections.defaultdict(makehash)

def merge(dict1, dict2):
    ''' Immutable dictionary merge.
        Return a new dictionary by merging two dictionaries recursively. 
    '''
    result = copy.deepcopy(dict1)

    for key, value in dict2.items():
        if isinstance(value, collections.Mapping):
            result[key] = merge(result.get(key, {}), value)
        else:
            result[key] = copy.deepcopy(dict2[key])

    return result







class experiment():
    '''
    Manage experiment with beamline, where an experiment is a series (optionally
     nested) of events.  An event is:
        1. generation of a wavefront from a source model or loading wavefront from file
        2. propagation of wavefront through a beamline.
     The wavefront generation, beamline and propation parameters may be different for
     each event.  Each event is defined by a common set of single-valued parmaeters 
     and the nth value in parameters provided as lists.
     
     Output is aggregated in a dictionary  [more on definition??]
        
        
    '''
    
    def __init__(self,moduleName=None,options=None):
        '''
        options: list of parameters in the form expected by srwl_bl.srwl_uti_ext_options
        
        module is a external module. 
        This kind of dependency injection is a bit clumsy, but it preserves compatibility
        with SIREPO/SRW simulations while effectively separating beamline-specific 
        implementation concerns.  An alternative to expecting a default module (run.py) 
        should be implemented in future.
        
        '''
        try:
            if moduleName:
                self._run = __import__(moduleName) 
                print('Loaded module: {}'.format(moduleName))
            else:
                import run as _run   
                self._run = _run
        except ImportError as e: print(e)
        except Exception as e: print(e)
            
        self.set_optics = self._run.set_optics
        self.varParam   = self._run.varParam
        self.options = options
        self.parseParameters()
        
        # locate and load actions (plugins)
        try:
            self.v.actionDir
        except AttributeError:
            self.v.actionDir = 'wfactions'  # default, assumed location
        
        self.v.actionDir = 'xl.wfactions'
        
        print('DEBUG: actionDir is ', self.v.actionDir)
        
        actions = ActionCollection(self.v.actionDir)
        
        # detault to execute all actions (plugins) unless overridden by value in self.v.actions
        try:
            self.v.actions
        except AttributeError:
            self.v.actions = actions.performAll
        
        self.v0 = copy.deepcopy(self.v)

        #initialise diskcache instance for storing the output from all actions
        #  Note that Set an item, get a value, and delete a key using the usual dictionary operators
        #  can also use add, incr, iterkeys,  etc
#        try:
#            self.v.cachePath
#        except AttributeError:
#            self.v.cachePath = os.path.join(os.getcwd(), 'cache_'+str(uuid.uuid4()))  
#            print("cachePath parameter missing, initialising cache in " + self.v.cachePath)
#        self.cache = Cache(directory=self.v.cachePath)
#        #cache.clear()
#        self.cache.reset('cull_limit', 0)       # Disable automatic evictions. necessary?
#    
        #...while diskcache implementation is incomplete...
        # initialise output dictionary
        self.results = makehash()
    
    def cacheVolume(self):
        return self.cache.volume()
    
    def parseParameters(self):
        if self.options:
            self.mergeOptions(self.options)  
        #self.v = srwl_bl.srwl_uti_parse_options(self.varParam, use_sys_argv=True)
        self.v = srwl_uti_parse_options(self.varParam, use_sys_argv=False)
    
    def mergeOptions(self,options):
        if self.options:
            self.varParam = srwl_uti_merge_options(self.varParam, self.options)
        
    def run(self):
        self.trialCount = 0
        options = vars(self.v)
        optionsRef = vars(self.v0)  #input, unchanged
    
        # find items where value is a list, ignoring propagation parameters and optimization variables:
        ExpVariables = [k for k, v in optionsRef.items() if (type(v) is list and not (k.endswith('_pp') or k.startswith('om_') or k == 'opList'))]    
        
        if not ExpVariables:
            self.trial(self.v)
        else:
            # expand/loop
            if self.v.op_nested == 1:
                for e in ExpVariables:
                    params = [p for p in optionsRef[e]]
                    for p in params:
                        # substitute a single value from list
                        options[e] = p    # this updates v            
                        self.trial(self.v)
            
            if self.v.op_nested == 0:
                # check that parameter lists are the same length
                #assert all(np.size(e)==n for e in ExpVariables) is True
                n = np.size(optionsRef[ExpVariables[0]])
                print('Parameter list length: {}'.format(n))
                for e in ExpVariables:
                    print ('Parameter: {}, Number of values: {}'.format(e,np.size(optionsRef[e])))
    
                for i in range(n):
                    for e in ExpVariables:
                        params = [p for p in optionsRef[e]]
                        options[e]  =  params[i]  # note that this changes the value the namescape self.v
                    print('Running trial {}: {}'.format(self.trialCount, options['name']))
                    self.trial(self.v)
        
        self.saveAll()
                    
    
    def trial(self,v):        
        op = self.set_optics(v)
        
        if(len(v.ws_fnei) == 0):
            #wf = srwl_bl.SRWLBeamline(_name=v.name).calc_all(v, op)
            #wf = beamline(_name=v.name).calc_all(v,op)
            
            #if v.wm_ch == 20:
            #        v.wm = True
            #        v.wm_pl = 'xy'
            #        v.wm_ns = v.sm_ns = 5
            #else:
            #        v.ws = True
            #        v.ws_pl = 'xy'
            
            BL = beamline(v, _op=op)
            BL.printOE()
            #wf = BL.calc_all(v)
            BL.calc_all(v)
            wf = v.w_res

            self.processOutput(Wavefront(srwl_wavefront=wf), vars(v))
            
        else:
            '''
            Propagate through beamline using an initial wavefront.
            In this case, we can use a simplified method for improved 
            performance.  The wavefront is loaded into memory at this point
            and only reloaded on subsequent trials if ws_fnei changes.
            
            currently limited to se propagation only!!!! - THIS SHOULD be changed
            or made conditional on  matching parameters.
            '''
            # functionality could be moved into srwl_blx!!
            
            
            #fnWfr = os.path.join(v.fdir, v.ws_fnei)
            #hack... temporary use:
            root,sub = os.path.split(v.fdir)    
            root,sub = os.path.split(root)    
            fnWfr = os.path.join(root, v.ws_fnei)
            #fnWfr = v.ws_fnei
            
            try: self.last_fnWfr
            except: self.last_fnWfr = None
             
            if fnWfr != self.last_fnWfr:
                print('Loading wavefront from file {}'.format(fnWfr))
                self.w0 = Wavefront()
                self.w0.load_hdf5(fnWfr)      
            self.last_fnWfr = fnWfr
        
            BL = beamline(v, _op=op)
            BL.printOE()
            
            wf = copy.deepcopy(self.w0)  # calc_part modifies wavefront in place, so copy it first
            BL.calc_part(v, wfr=wf._srwl_wf)
                          
            self.processOutput(Wavefront(srwl_wavefront=wf._srwl_wf),  vars(v))
            
        self.trialCount += 1

    def processOutput(self,wf,v):
        # actions are expected to return a nested dictionary
        resp = self.v.actions(wavefront=wf,parameters=v)
        self.store(v, resp, self.trialCount)
        
    def store(self, v, results,  trialCount):
        
        # make a copy
        cv = copy.deepcopy(v)
        #strip the big stuff - need a better way to do this !
#
        cv['ws_res'] = None
        cv['si_res'] = None
        cv['w_res']  = None
        cv['actions'] = None
        
        trial = 'trial_{}'.format(trialCount)

        self.results.update({trial:
                               {'trial' : trialCount,
                                'name' : cv['name']}
                                })
        self.results = merge(self.results, { trial: {'parameters': cv,#vars(cv), 
                                                     'results' : results}})


        self.saveTrial(self.results[trial]) 
    
    def trials(self):
        return [k for k,v in self.results.items()]
       
    def resultsKeys(self):
        return [k for k,v  in self.results['trial_0']['results'].items()]
    
    def parameterKeys(self):
        return [k for k,v  in self.results['trial_0']['parameters'].items()]
    
    def printParameters(self):
        for trial in self.trials():
            pprint(self.results[trial]['parameters'])

    def printResults(self):
        for trial in self.trials():
            pprint(self.results[trial]['results'])
      
    def listValues(self,key):
        trials = self.trials()
        print('Trials:')
        print(trials)
        try:
            V =  [self.results[trial]['results'][key] for trial in trials] 
        except KeyError:
            try:
                V =  [self.results[trial]['parameters'][key] for trial in trials] 
            except KeyError:
                print('Valid values not found for ' + key)
                V=[]
        return V
    
    def plot(self,*args,**kwargs):
                
        xKey = kwargs['x']
        yKey = kwargs['y']
            
        x = self.listValues(xKey)
        y = self.listValues(yKey)
        
        #for debugging:
        print(x)
        print(y)
       
        if x !=[] and y!=[]:
            fontP = FontProperties()
            fontP.set_size('xx-small')    
            plt.plot(x,y,'o')   #label=...
            plt.xlabel(xKey)
            plt.ylabel(yKey)
            plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5), prop=fontP)
            plt.show()    
    
    def saveTrial(self, trialDict):
        filename = os.path.join(self.v.fdir, slugify(trialDict['name'])+'.pkl')
        fileObject = open(filename, 'wb')
        pkl.dump(trialDict, fileObject)
        fileObject.close()
        print('Wrote trial parameters and results to ' + filename)
    
    def saveAll(self):
        filename = os.path.join(self.v.fdir, 'results.pickle')
        fileObject = open(filename, 'wb')
        pkl.dump(self.results, fileObject)
        fileObject.close()
    
    

