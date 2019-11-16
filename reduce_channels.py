#!/usr/bin/env python

import psrchive
from astropy.io import fits
import argparse
import psrchive_utils as psru

parser = argparse.ArgumentParser(usage='describe usage here',
                                     description='description of script here.',epilog='Copyright (C) 2019 by Marisa Geyer')
parser.add_argument('-f', dest='filename', metavar='<filename>', help='specify archive file from which to remove channels')
parser.add_argument('-v', dest='verbose', action="store_true", help='verbose output')
args = parser.parse_args()

ch0=848
ch1=927
ch2=0
ch3=79

arch =  psrchive.Archive_load(args.filename)
if args.verbose:
    print "Original archive info"
    psru.get_archive_info(arch)

arch.get_frequencies()
arch.remove_chan(ch0,ch1)
arch.remove_chan(ch2,ch3)

print "Removing channels %d to %d and %d to %d to match search mode frequency channels" %(ch0,ch1,ch2,ch3)

freq = arch.get_frequencies()
newname = args.filename+".768ch"
arch.unload(newname)

print "New archive saved with name %s" %newname

if args.verbose:
    print "Updated info on new archive"
    psru.get_archive_info(arch)


print "Updating fits headers to correct OBSNCHAN and OBSBW values"

obsbw = 642.0
obsnchan = 768

fits.setval(newname, 'OBSBW', value=obsbw)
fits.setval(newname, 'OBSNCHAN', value=obsnchan)

print "Fits headers of %s have been updated to OBSBW:%.1f and OBSNCHAN:%d" %(newname, obsbw, obsnchan)

