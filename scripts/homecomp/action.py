#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 16:03:17 2020

@author: gvanriessen


Implements a 'plugin' architecture to be used for wavefront processing 'actions'.

Initially adapted, with  no significant changes, from https://github.com/gdiepen/python_plugin_example by Guido Diepen. 
 See also (https://www.guidodiepen.nl/2019/02/implementing-a-simple-plugin-framework-in-python/)

Modified to generalise arguments to perform_operation and to collect output of actions in dictionary.
"""

import inspect
import os
import pkgutil

from diskcache import Cache

import inspect

def inherits_from(child, parent_name):
    '''usage e.g. print inherits_from(possible_child_class, 'parent_class') '''
    if inspect.isclass(child):
        if parent_name in [c.__name__ for c in inspect.getmro(child)[1:]]:
            return True
    return False


class Action(object):
    """Base class that each plugin must inherit from. within this class
    you must define the methods that all of your actions must implement
    """

    def __init__(self):
        self.description = 'UNKNOWN'

    def perform_operation(self, *args, **kwargs):
        """The method that we expect all actions to implement. This is the
        method that our framework will call
        """
        raise NotImplementedError




class ActionCollection(object):
    """Upon creation, this class will read the actions package for modules
    that contain a class definition that is inheriting from the Action class
    """

    def __init__(self, action_package):
        """Constructor that initiates the reading of all available actions
        when an instance of the PluginCollection object is created
        """
        self.action_package = action_package
        self.reload_actions()
        
        self.cache = Cache()  


    def reload_actions(self):
        """Reset the list of all actions and initiate the walk over the main
        provided action package to load all available actions
        """
        self.actions = []
        self.seen_paths = []
        print()
        print(f'Looking for actions under package {self.action_package}')
        self.walk_package(self.action_package)


    def performAll(self, *args, **kwargs):
        """Perform all of the actions on the argument supplied to this function
        """
        resp = {}
        #print(f'Applying all actions on value {argument}:')
        for action in self.actions:
            #print(f'    Applying {action.description} on value {argument} yields value {action.perform_operation(argument)}')
            print (f'Performing action {action.description} ')#on argument of type {type(argument)}.')
            d = action.perform_operation(*args, **kwargs)
            # We expect actions to return a dict. Check:
            if type(d) is dict:
                #in case d does not include a self-description or unique keys:
                #resp.update( {action.description : d})
                #print(d)
                resp.update(d)
        
        return resp


    def walk_package(self, package):
        """Recursively walk the supplied package to retrieve all actions
        """
        imported_package = __import__(package, fromlist=['blah'])

        for _, actionname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if not ispkg:
                action_module = __import__(actionname, fromlist=['blah'])
                clsmembers = inspect.getmembers(action_module, inspect.isclass)
                
                for (_, c) in clsmembers:
                    # Only add classes that are a sub class of Plugin, but NOT Plugin itself
                    #if issubclass(c, Action)  & (c is not Action):
                    if inherits_from(c,'Action') & (c is not Action):

                        print(f'    Found action class: {c.__module__}.{c.__name__}')
                        self.actions.append(c())


        # Now that we have looked at all the modules in the current package, start looking
        # recursively for additional modules in sub packages
        all_current_paths = []
        if isinstance(imported_package.__path__, str):
            all_current_paths.append(imported_package.__path__)
        else:
            all_current_paths.extend([x for x in imported_package.__path__])

        for pkg_path in all_current_paths:
            if pkg_path not in self.seen_paths:
                self.seen_paths.append(pkg_path)

                # Get all sub directory of the current package path directory
                child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]

                # For each sub directory, apply the walk_package method recursively
                for child_pkg in child_pkgs:
                    self.walk_package(package + '.' + child_pkg)