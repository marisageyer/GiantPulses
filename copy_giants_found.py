#!/usr/bin/python

## Python Modules
import os
import shutil
import argparse
import numpy as np
import subprocess
import psrchive
import glob
import matplotlib.pyplot as plt
import matplotlib.colors as colors
###################################
## Function
def Files(directory, extension):
    return sorted([f for f in os.listdir(directory) if f.endswith('.' + extension)])
###########

import matplotlib as mpl
label_size = 8
mpl.rcParams['xtick.labelsize'] = label_size

parser = argparse.ArgumentParser(usage='describe usage here',
                                     description='description of script here.',epilog='Copyright (C) 2019 by Marisa Geyer')
parser.add_argument('-dir', dest='directory_name', metavar='<directory_name>', help='specify directory where figures to copy are')
parser.add_argument('-dest', dest='dest', type=str, help='Specify destination to where giants will be saved')
args = parser.parse_args()


def figname_to_pathway(figpath):
    """figpath = path to giant .png figure saved"""
    basepath = os.path.dirname(figpath)
    figname = os.path.basename(figpath)
#    print figname
    arch = figname.split('_SNR')[0].replace('_pulse', '/pulse')
    datedir = figname.split('_')[0]
    datedir = figname.split('_')[0]
    pulse = figname.split('_')[2].split('.')[0]
    snr = figname.split('_')[5]
    return arch, datedir, pulse, snr




figlist = []
for fig in glob.glob(args.directory_name+'/*.png'):
#   print fig
   figlist.append(fig)


#print figlist

originpath = '/scratch02/mgeyer/Jones_HonsProj/SEARCH_DATA/Augdata/2019-08-27-23:35:47/dirs_with_singles/' 


for fig in figlist:
    arch, datedir, pulse, snr = figname_to_pathway(fig)
    wild_arch = arch.split('.p')[0]+'*'

#    print "Datedir:", datedir
    print "Archive:" , arch
    print "Wildcard archive", wild_arch
    print "Fullpath:", os.path.join(originpath,wild_arch)

    for file in glob.glob(originpath+wild_arch):
        print file
        shutil.copy(file, args.dest)
