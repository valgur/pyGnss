#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 13:25:38 2017

@author: Sebastijan Mrak <smrak@gmail.com>
"""
import os
import glob
import platform
from time import sleep
import georinex as gr

def _convert(file, odir, i, tlim=None):
    print ('Converting file: ', file)
    try:
        gr.load(file,out=odir, useindicators=i, fast=False, tlim=tlim)
    except Exception as e:
        print (e)
    sleep(0.1)
    
def _iterate(file, odir, override, i, tlim=None):
    head, tail = os.path.split(file)
    rx = tail[0:8]
    if platform.system() == 'Linux':
        newfn = odir + '/' + rx + '.nc'
    elif platform.system() == 'Windows':
        newfn = odir + '\\' + rx + '.nc'
    if not override:
        if not os.path.exists(newfn):
            _convert(file, odir, i, tlim=tlim)
    else:
        _convert(file, odir, i, tlim=tlim)
        
def convertObs2HDF(folder=None, sufix=None, odir=None, override=False,
                   i=False, tlim=None):
    """
    This script converts RINEX 2.11 observation files in a given directory into
    a hdf5 organized data structure, utilizing pyRINEX script. Find the script
    in the main directory.
    """
    if os.path.isdir(folder):
        if sufix is None:
            wlist = ['*.**o', '*.**O', '*.**d']
        else:
            wlstr = sufix
        if odir is None:
            odir = folder
        for wlstr in wlist:
            filestr = os.path.join(folder,wlstr)
            flist = sorted(glob.glob(filestr))
            for file in flist:
                _iterate(file, odir, override, i, tlim=tlim)
    elif os.path.isfile(folder):
        if odir is None:
            odir = folder
        if folder[-1] == 'o' or folder[-1] == 'O' or folder[-1] == 'd' or folder[-1] == 'D': # Very stupid / change to match OBS file template
            head, tail = os.path.split(folder)
            odir = head
            file = folder
            _iterate(file, odir, override, i, tlim=tlim)
        else:
            print ('Not a RInex OBS file (.o or .d)')
    else:
        print ("Something went wrong, dude")
                    
if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('folder',type=str)
    p.add_argument('-odir', '--odir', help='Destination folder, if None-> the same as input folder', default=None)
    p.add_argument('-f', '--force', help="Force override, if the NC file already exist", action='store_true')
    p.add_argument('-i', '--indicators', help="Parse & store the indicators (lli/ssi)?", action='store_true')
    p.add_argument('-s', '--sufix', help='specify a sufix for desired observation files', type=str, default=None)
    p.add_argument('--tlim', help='set time limints for the file to cenvert', nargs=2)
    P = p.parse_args()
    
    convertObs2HDF(folder = P.folder, sufix=P.sufix, odir=P.odir, override=P.force, 
                   i=P.indicators, tlim=P.tlim)