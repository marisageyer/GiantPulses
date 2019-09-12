#!/usr/bin/python 

## Python Modules
import os
import argparse
import subprocess


def list_files(directory, extension):
    """Retrieve files in directory with specified extension"""
    return sorted([f for f in os.listdir(directory) if f.endswith('.' + extension)])


parser = argparse.ArgumentParser(usage='describe usage here',
                                     description='description of script here.',epilog='Copyright (C) 2019 by Marisa Geyer')
parser.add_argument('-dir', dest='directory_name', metavar='<directory_name>', help='specify directory where archive directories with pulsar observations with "fullband" extenstion (as produced by add_freq_bands.py) are')
#parser.add_argument('-par', dest='par_file', metavar='<par_file>', help='specify par file')
#parser.add_argument('-ext', dest='save_ext', metavar='<save_ext>', help='specify extension to save')
#parser.add_argument('-save_dir', dest='save_dir', metavar='<save_dir>', help='specify directory to save to')
args = parser.parse_args()

#dirname = '/scratch02/mgeyer/Jones_HonsProj/SEARCH_DATA/Marchdata/Singles_MBpar'
dirname = args.directory_name
dirlist = sorted([f for f in os.listdir(dirname) if f.startswith('2019')])
dirlisttouse = dirlist

os.chdir(dirname)


for dir in dirlisttouse:
    print dir
    totalfilename = '%s_totalfull' %dir
    print totalfilename
    dirpath = os.path.join(dirname,dir)
    print dirpath
    os.chdir(dirpath)
    
    command = ['psradd', '-v', '-o', totalfilename, '*fullband']
    zap_file = subprocess.Popen(command, shell=False, cwd='.', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (stdoutdata, stderrdata) = zap_file.communicate()
    return_code = zap_file.returncode
    #print stdoutdata.split("\r")
