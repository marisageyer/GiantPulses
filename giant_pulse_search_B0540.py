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
###################################
## Function
def Files(directory, extension):
    return sorted([f for f in os.listdir(directory) if f.endswith('.' + extension)])
###########

import matplotlib as mpl
label_size = 8
mpl.rcParams['xtick.labelsize'] = label_size 

parser = argparse.ArgumentParser(usage='describe usage here',
                                     description='description of script here.',epilog='Copyright (C) 2019 by Jones Chilufya')
parser.add_argument('-dir', dest='directory_name', metavar='<directory_name>', help='specify directory where archive directories with pulsar observations are')
parser.add_argument('-mask', dest='mask_file', metavar='<mask_file>', help='specify mask file where RFI mask lists are')
parser.add_argument('-ext', dest='file_ext', metavar='<file_ext>', help='specify the file extensions in dir in which to search for giant pulses. Default = "fullband"')
parser.add_argument('-nch', dest='num_chan', metavar='<num_chan>', type=int, help='specify the number of channels to fscrunch to before searching for giants. Default = 256')
parser.add_argument('-v', dest='verbose', action="store_true", help='verbose output')
parser.add_argument('-snr_cut', dest='snr_cut', metavar='<snr_cut>', type=float, help='specify SNR cut for finding giant pulses. Default is 10')
parser.add_argument('-fig_path', dest='fig_path', type=str, help='Specify pathway to where figures will be saved')
args = parser.parse_args()

## Giant pulse image plots path
if not args.fig_path:
    print "No figure path specified. Marisa add default here."
else:
    figpath = args.fig_path
 
################################

if not args.snr_cut:
    snr_max = 10.0
else:
    snr_max = args.snr_cut


#####
## Set nchans and nbins and npol=1
###########################################################
#for dir in directory_list[sdir:end]:
#print dir

if not args.file_ext:
   ext = 'fullband'
else:
   ext = args.file_ext
print "----------------------------------------------------------------"
print "Searching through files with extension %s in %s" %(ext,args.directory_name)

if not args.num_chan:
    nch = 256
else:
    nch = args.num_chan


check_files_exist = Files(args.directory_name, '%s.p.nch%d.512nb' %(ext,nch)) 
if check_files_exist == []:
    print "----------------------------------------------------------------"
    print "Setting number of channels and bins"
    fullband_files = Files(args.directory_name, ext)
    if fullband_files == []:
        print "Did not find any files with extension %s." %ext
    else:
        for avg_file in fullband_files:
            avg_filepath = os.path.join(args.directory_name, avg_file)
            avg_comand = ['pam', '--setnch','%d' %nch, '--setnbin','512','-p', '-e', '%s.p.nch%d.512nb' %(ext,nch), avg_filepath]
            avg_comand_open = subprocess.Popen(avg_comand, shell=False, cwd='.', 
                                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            (stdoutdata, stderrdata) = avg_comand_open.communicate()
            if args.verbose:
                print stdoutdata, stderrdata
else:
    print "----------------------------------------------------------------"
    print "Files with extension %s.p.nch%d.512nb already exist. Skipping their creation." %(ext,nch)


if args.mask_file:

    with open(args.mask_file) as file:
        use_mask= file.read()
    
    
    ########################################################
    ### Paz Command
    print "Using mask:"
    print use_mask
    check_files_exist = Files(args.directory_name, '%s.p.nch%d.512nb.paz' %(ext,nch))
    if check_files_exist == []:
        print "----------------------------------------------------------------"
        print "Executing paz -z for %s" %args.directory_name
        pazi_files = Files(args.directory_name, '%s.p.nch%d.512nb' %(ext,nch))
        for pazi_file in pazi_files:
            pazi_path = os.path.join(args.directory_name, pazi_file)
            pazi_comand = ['paz', '-z', use_mask,'-e', '512nb.paz', '-v',pazi_path]
            pazi_comand_open = subprocess.Popen(pazi_comand, shell=False, cwd='.', 
                                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            (stdoutdata, stderrdata) = pazi_comand_open.communicate()
            if args.verbose:
                print stdoutdata, stderrdata
    else:
        print "----------------------------------------------------------------"
        print "Files with extension %s.p.nch%d.512nb.paz already exist. Skipping their creation." %(ext,nch)
        print "----------------------------------------------------------------"

else:
        print "----------------------------------------------------------------"
        print "No mask specified. Skipping RFI cleaning section."
 


######
### Signal to Noise and PLOTs

if args.mask_file:
    snr_data_files = Files(args.directory_name, '%s.p.nch%d.512nb.paz' %(ext,nch))
else:
    snr_data_files = Files(args.directory_name, '%s.p.nch%d.512nb' %(ext,nch))


for snr_file in snr_data_files:
    snr_path = os.path.join(args.directory_name, snr_file)
    snr_comand = ['psrstat', '-jF', '-c', 'snr=pdmp,snr','-Q', snr_path]
    snr_comand_open = subprocess.Popen(snr_comand, shell=False, cwd='.', 
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (stdoutdata, stderrdata) = snr_comand_open.communicate()
    print stdoutdata.split()
    snr = float(stdoutdata.split()[1])

    if snr >= snr_max:
       # print "High SNR in", snr
        archive_file = psrchive.Archive_load(snr_path)
        nchan = archive_file.get_nchan()
        nbin = archive_file.get_nbin()            
        weights = archive_file.get_weights().reshape(nchan)
        phase_values=np.linspace(0,1,nbin)
        archive_file.remove_baseline()
        freq_data = archive_file.get_data() ## frequency retained data array
        archive_file.fscrunch()
        plot_profile = archive_file.get_data()
        idx_max = np.argmax(plot_profile[0,0,0,:])
        phase_max = phase_values[idx_max]	

        #ph_lim0 = 0.30
        #ph_lim1 = 0.45
        #ph_lim2 = 0.50
        #ph_lim3 = 0.65
        ## These hard-coded phase windows can be changed to argse as well


        #if (phase_max > ph_lim0 and phase_max < ph_lim1) or (phase_max > ph_lim2 and phase_max < ph_lim3):
        fig, (ax1, ax2) = plt.subplots(2,1, sharex=True)
        fig.subplots_adjust(hspace=0)
        ax1.plot(phase_values, plot_profile[0,0,0,:], label='SNR = %.2f'%(snr))

        #ax1.fill_betweenx(y=[np.min(plot_profile[0,0,0,:]),np.max(plot_profile[0,0,0,:])], x1=ph_lim0,x2=ph_lim1, alpha=0.4, color='b')
        #ax1.fill_betweenx(y=[np.min(plot_profile[0,0,0,:]),np.max(plot_profile[0,0,0,:])], x1=ph_lim2,x2=ph_lim3, alpha=0.4, color='b')
        #ax1.axvline(x=ph_lim0, color='r', alpha=0.2, lw=2.0)
        #ax1.axvline(x=ph_lim1, color='r', alpha=0.2, lw=2.0)
        #ax1.axvline(x=ph_lim2, ls='dashed',alpha=0.2)
        #ax1.axvline(x=ph_lim3, ls='dashed',alpha=0.2)
        ax1.axvline(x=phase_max, ls='dotted',alpha=0.3)
        
        ax1.set_title((os.path.basename(args.directory_name),snr_file),fontsize=10) ###
        ax1.set_ylabel('Intensity', fontsize=10)
        ax1.legend(loc='best')
        spec_data = freq_data.reshape(nchan,nbin)
        
        data_weighted = np.ones((nchan, nbin))
        for n in range(nchan):
            data_weighted[n] =  weights[n]*spec_data[n,:]
        
        lower_freq = archive_file.get_centre_frequency() - archive_file.get_bandwidth()/2.0
        high_freq = archive_file.get_centre_frequency() + archive_file.get_bandwidth()/2.0
        min_phase = 0
        max_phase = 1
        if args.directory_name.endswith("/"):
            saven = os.path.basename(args.directory_name[0:-1])
        else:
            saven = os.path.basename(args.directory_name)
        figname = '%s_%s_SNR_%.2f_phase_%.2f.png' %(saven,snr_file, snr, phase_max)
        ax2.imshow(data_weighted, extent=(min_phase,max_phase,lower_freq, high_freq), aspect='auto', cmap='magma', origin='lower')
        ax2.set_xlabel('Pulse Phase', fontsize=10)
        ax2.set_ylabel('Frequency (MHz)',fontsize=10)
        #ax2.tick_params(axis='both', which='minor', labelsize=6)
        ax3 = ax2.twinx()
        ax3.set_ylim(0,nchan)
        ax3.set_ylabel('Channel Number')
        plt.rcParams.update({'figure.max_open_warning': 0})
        plt.savefig(os.path.join(figpath, figname))

        print "----------------------------------------------------------------"
        print "----------------------------------------------------------------"
        print 'figure saved as',os.path.join(figpath, figname)

        print "----------------------------------------------------------------"
        print "----------------------------------------------------------------"
        #plt.show()
        plt.close()
