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
parser.add_argument('-dir', dest='directory_name', metavar='<directory_name>', help='specify directory where archive directories with single pulse archives with extension args.ext are')
parser.add_argument('-ext', dest='ext', metavar='<ext>', help='specify extension of files to be added. Default is fullband.')
parser.add_argument('-save_ext', dest='save_ext', metavar='<save_ext>', help='specify extension to save to added archives. Default is total')
args = parser.parse_args()

#dirname = '/scratch02/mgeyer/Jones_HonsProj/SEARCH_DATA/Marchdata/Singles_MBpar'
dirname = args.directory_name
dirlist = sorted([f for f in os.listdir(dirname) if f.startswith('2019')])
dirlisttouse = dirlist

os.chdir(dirname)


if not args.ext:
   ext = 'fullband'
else: 
   ext = args.ext

if not args.save_ext:
   save_ext = 'total'
else:
   save_ext = args.save_ext


searchstr = '*'+ext 


for dir in dirlisttouse:
    print dir
    totalfilename = '%s.%s' %(dir,save_ext)
    print totalfilename
    dirpath = os.path.join(dirname,dir)
    print dirpath
    os.chdir(dirpath)
    
    command = ['psradd', '-v', '-o', totalfilename, searchstr]
    added_file = subprocess.Popen(command, shell=False, cwd='.', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (stdoutdata, stderrdata) = added_file.communicate()
    return_code = added_file.returncode
    #print stdoutdata.split("\r")


    commandfold = ['pam', '-e', 'T', '-T', totalfilename]
    fold_file = subprocess.Popen(commandfold, shell=False, cwd='.', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (stdout, stderr) = fold_file.communicate()
    print stdout

