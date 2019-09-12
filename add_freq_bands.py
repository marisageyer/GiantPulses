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
parser.add_argument('-dir', dest='directory_name', metavar='<directory_name>', help='specify directory where archive directories with pulsar observations are. This short script expects to find files with names <pulsar_number>.dedisp_single.lower and <pulsar_number>.dedisp_single.upper. It will use psradd -R to add these and output with extension "fullband".')

args = parser.parse_args()


dirname = args.directory_name
print dirname

lowerfiles = sorted(list_files(dirname,'lower'))
upperfiles = sorted(list_files(dirname, 'upper'))

print "Found %d lower files" %len(lowerfiles)
print "Found %d upper files" %len(upperfiles)

pulse_start = max(int(lowerfiles[0].split('_')[1].split('.')[0]),int(upperfiles[0].split('_')[1].split('.')[0]))
pulse_end = min(int(lowerfiles[-1].split('_')[1].split('.')[0]),int(upperfiles[-1].split('_')[1].split('.')[0]))

print "Single pulses range from %d to %d" %(pulse_start, pulse_end)

os.chdir(dirname)
for i in range(pulse_start, pulse_end+1):
        inlower = 'pulse_%d.dedisp_single.lower' %i
        inupper = 'pulse_%d.dedisp_single.upper' %i
        outname = 'pulse_%d.dedisp_single.fullband' %i

        command= ['psradd','-R','-o',outname, inlower, inupper]
        #print command
        #print "\n"
        psradd_file = subprocess.Popen(command, shell=False, cwd='.', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (stdoutdata, stderrdata) = psradd_file.communicate()
        return_code = psradd_file.returncode
        #print stdoutdata.split("\r")
