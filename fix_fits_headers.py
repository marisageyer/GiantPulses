#!/usr/bin/env python

from astropy.io import fits
import argparse

parser = argparse.ArgumentParser(usage='describe usage here',
                                     description='description of script here.',epilog='Copyright (C) 2019 by Marisa Geyer')
parser.add_argument('-f', dest='filename', metavar='<filename>', help='specify archive file from which to remove channels')
parser.add_argument('-v', dest='verbose', action="store_true", help='verbose output')
args = parser.parse_args()


print "Updating fits headers to correct OBSNCHAN and OBSBW values"

obsbw = 642.0
obsnchan = 768

fits.setval(args.filename, 'OBSBW', value=obsbw)
fits.setval(args.filename, 'OBSNCHAN', value=obsnchan)

print "Fits headers of %s have been updated to OBSBW:%.1f and OBSNCHAN:%d" %(args.filename, obsbw, obsnchan)


