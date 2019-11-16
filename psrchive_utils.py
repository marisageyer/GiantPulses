#!/usr/bin/env python

import numpy as np
import psrchive

"""A list of useful psrchive dependent functions to use in python"""
"""Just getting started - hoping to add to this. Please feel free to add your own functions too. 
and thanks for get_archive_info that was supplied by Maciej Serylak."""


def get_archive_info(archive):
   """Query archive attributes.
   Input:
       archive: loaded PSRCHIVE archive object.
   Output:
       Print attributes of the archive.
   """
   filename = archive.get_filename()
   nbin = archive.get_nbin()
   nchan = archive.get_nchan()
   npol = archive.get_npol()
   nsubint = archive.get_nsubint()
   obs_type = archive.get_type()
   telescope_name = archive.get_telescope()
   source_name = archive.get_source()
   ra = archive.get_coordinates().ra()
   dec = archive.get_coordinates().dec()
   centre_frequency = archive.get_centre_frequency()
   bandwidth = archive.get_bandwidth()
   DM = archive.get_dispersion_measure()
   RM = archive.get_rotation_measure()
   is_dedispersed = archive.get_dedispersed()
   is_faraday_rotated = archive.get_faraday_corrected()
   is_pol_calib = archive.get_poln_calibrated()
   data_units = archive.get_scale()
   data_state = archive.get_state()
   obs_duration = archive.integration_length()
   obs_start = archive.start_time().fracday() + archive.start_time().intday()
   obs_end = archive.end_time().fracday() + archive.end_time().intday()
   receiver_name = archive.get_receiver_name()
   receptor_basis = archive.get_basis()
   backend_name = archive.get_backend_name()
   backend_delay = archive.get_backend_delay()
   # low_freq = archive.get_centre_frequency() - archive.get_bandwidth() / 2.0
   # high_freq = archive.get_centre_frequency() + archive.get_bandwidth() / 2.0
   print 'file             Name of the file                           %s' % filename
   print 'nbin             Number of pulse phase bins                 %s' % nbin
   print 'nchan            Number of frequency channels               %s' % nchan
   print 'npol             Number of polarizations                    %s' % npol
   print 'nsubint          Number of sub-integrations                 %s' % nsubint
   print 'type             Observation type                           %s' % obs_type
   print 'site             Telescope name                             %s' % telescope_name
   print 'name             Source name                                %s' % source_name
   print 'coord            Source coordinates                         %s%s' % (ra.getHMS(), dec.getDMS())
   print 'freq             Centre frequency (MHz)                     %s' % centre_frequency
   print 'bw               Bandwidth (MHz)                            %s' % bandwidth
   print 'dm               Dispersion measure (pc/cm^3)               %s' % DM
   print 'rm               Rotation measure (rad/m^2)                 %s' % RM
   print 'dmc              Dispersion corrected                       %s' % is_dedispersed
   print 'rmc              Faraday Rotation corrected                 %s' % is_faraday_rotated
   print 'polc             Polarization calibrated                    %s' % is_pol_calib
   print 'scale            Data units                                 %s' % data_units
   print 'state            Data state                                 %s' % data_state
   print 'length           Observation duration (s)                   %s' % obs_duration
   print 'start            Observation start (MJD)                    %.10f' % obs_start
   print 'end              Observation end (MJD)                      %.10f' % obs_end
   print 'rcvr:name        Receiver name                              %s' % receiver_name
   print 'rcvr:basis       Basis of receptors                         %s' % receptor_basis
   print 'be:name          Name of the backend instrument             %s' % backend_name
   print 'be:delay         Backend propn delay from digi. input.      %s\n' % backend_delay
    
   
 
def get_lower_and_upper_freq(archive):
    lower_freq = archive.get_centre_frequency() - archive.get_bandwidth()/2.0
    high_freq = archive.get_centre_frequency() + archive.get_bandwidth()/2.0
    return lower_freq, high_freq
    

def apply_freq_weights(archive):
    """This function applies """
    nchan = archive.get_nchan()
    nbin = archive.get_nbin()
    nsubint = archive.get_nsubint()
    npol = archive.get_npol()
    print "Archive loaded to apply weights has:\n"
    print "%d freq chan" %nchan
    print "%d subints" %nsubint
    print "%d phase bins" %nbin
    print "%d polarisations" %npol
    print "This function applies weights to folded, polarisation scrunched data - for now"
    
    if nchan == 1:
        print "Applying weights doesn't make sense, data has already been f-scrunched"
    weights = archive.get_weights().reshape(nchan)
    freq_data = archive.get_data()
    spec_data = freq_data.reshape(nchan,nbin)
       
    data_weighted = np.ones((nchan, nbin))
    for n in range(nchan):
        data_weighted[n] =  weights[n]*spec_data[n,:]
    return data_weighted
