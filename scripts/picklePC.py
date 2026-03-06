#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 14:06:35 2022

@author: -
"""
import pickle

def pickleProtocolChange(path,p=2):
    file = pickle.load(open(path, 'rb'))
    with open(path[0:int(len(path)-4)] + 'NEW.pkl', "wb") as f:
                pickle.dump(file, f, protocol=p)

def test():
    path = '/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/data/D_27.5um/dataStructure.pkl'
#    '/user/home/opt/xl/xl/experiments/maskLER2/data/dataStructure.pkl'
#    '/user/home/opt/xl/xl/experiments/correctedAngle_coherence4/data/sx100sy100/sx100sy100Efields.pkl'
    #'/user/home/opt/xl/xl/experiments/farField/data/farFieldEfield/farFieldEfieldEfields.pkl'
    #'/user/home/opt/xl/xl/experiments/correctedAngle_coherence/data/beforeBDA_efield_sx200sy200/beforeBDA_efield_sx200sy200Efields.pkl'
    #'/user/home/opt/xl/xl/experiments/correctedAngle_AEcoherence/data/aerialImageEfield/aerialImageEfieldEfields.pkl'
#    '/user/home/opt/xl/xl/experiments/correctedAngle_coherence/data/beforeBDA_efield_sx200sy200_10000e/beforeBDA_efield_sx200sy200_10000eEfields.pkl'
#    '/user/home/opt/xl/xl/experiments/correctedWBS_beamCharacterisation/data/maskExitEfield/maskExitEfieldEfields.pkl'
    #'/user/home/opt/xl/xl/experiments/EUVmaskLER1/dataStructureEUVmaskLER1.pkl'
    #'/user/home/opt/xl/xl/experiments/maskLER2/dataStructuremaskLER2.pkl'
#    '/user/home/opt/xl/xl/experiments/testBeamline/data/Vgrad25000/Vgrad25000Efields.pkl'
    #'/user/home/opt/xl/xl/experiments/maskLER1/data/rms40AerialImage.pkl'
    #'/user/home/opt/xl/xl/experiments/BEUVcoherence/data/75um_50SSAProfile.pkl'
    #'/user/home/opt/xl/xl/experiments/correctedWBS_beamCharacterisation/data/imagePlane/imagePlane.pkl'
    #'/user/home/opt/xl/xl/experiments/BEUVcoherence/data/300umProfile.pkl'
    #'/user/home/opt/xl/xl/experiments/correctedAngle_coherence/pickles/combined300.pkl'
    #'/user/home/opt/xl/xl/experiments/lowEnergyBeam/data/atM1/atM1Efields.pkl'#'/user/home/Downloads/dataStructure.pkl'
    pickleProtocolChange(path,p=2)
    
if __name__=='__main__':
    test()