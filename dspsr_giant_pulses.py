#!/usr/bin/python 

## Python Modules
import os
import argparse
import numpy as np
import subprocess
import psrchive
import glob
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def list_files(directory, extension):
    """Retrieve files in directory with specified extension"""
    return sorted([f for f in os.listdir(directory) if f.endswith('.' + extension)])


parser = argparse.ArgumentParser(usage='describe usage here',
                                     description='description of script here.',epilog='Copyright (C) 2019 by Marisa Geyer')
parser.add_argument('-dir', dest='directory_name', metavar='<directory_name>', help='specify directory where archive directories with pulsar observations are')
parser.add_argument('-par', dest='par_file', metavar='<par_file>', help='specify par file')
parser.add_argument('-input', dest='input_ext', metavar='<input_ext>', help='specify extension of input files to use. Default = ".sf"')
parser.add_argument('-ext', dest='save_ext', metavar='<save_ext>', help='specify extension to save')
parser.add_argument('-save_dir', dest='save_dir', metavar='<save_dir>', help='specify directory to save to')
args = parser.parse_args()


#corrected_filepath = '/scratch02/mgeyer/Jones_HonsProj/SEARCH_DATA/Marchdata/UpperBand/2019-03-26_sf_corrected/'
ext = args.save_ext
foldingpar = args.par_file
basedir = args.save_dir

if not args.input_ext:
    input_ext = 'sf'
else:
    input_ext = args.input_ext

  
##for the March data the input extension was 'corrected.lower' or 'corrected', since header corrections were run on them.
##extension = 'corrected.lower'

filelist = list_files(args.directory_name,input_ext)

#print filelist
filepaths=[]
for file in filelist:
    filepath = os.path.join(args.directory_name,file)
    filepaths.append(filepath)

selected_files = filepaths

for filetofold in selected_files:
    dirname = os.path.basename(filetofold).split('.')[0]
    dirtomake = os.path.join(basedir,dirname)
    print dirtomake
    if not os.path.exists(dirtomake):
        os.mkdir(dirtomake)
    os.chdir(dirtomake)   
    print filetofold
    command= ['dspsr', '-k','MeerKAT', '-scloffs','-K', '-s', '-E', foldingpar, '-b','1024', '-e',ext, filetofold]
    dspsr_file = subprocess.Popen(command, shell=False, cwd='.', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (stdoutdata, stderrdata) = dspsr_file.communicate()
    return_code = dspsr_file.returncode

#     if return_code != 0:
#         raise RuntimeError('Not able to execute dspsr: %s') %stdoutdata
        
    print stdoutdata.split("\r")
