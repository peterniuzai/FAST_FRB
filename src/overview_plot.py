import os
import sys
import glob
import numpy as np

Codes_dir = "/data26/home/nch/FAST_Miner/"

project = "201905/"

file_dir        = "/data26/zhuww/psr_19beam_1bit/"
date_list       = sorted(glob.glob(file_dir + project+'*'))
N_day           = len(date_list)

for i in np.arange(N_day):

	date = date_list[i].split('/')[-1]

	Coin_dir = Codes_dir + "Coin_Result/" + project + date + "/"
	
	Overview_dir = Codes_dir + "Overview_plot/" + project + date + "/"
	
	
	if not os.path.exists(Coin_dir):
		os.makedirs(Coin_dir)
	
	
	if not os.path.exists(Overview_dir):
		os.makedirs(Overview_dir)

	os.system("cat %s*_all.cand > %sSummary_%s.cand"%(Coin_dir,Overview_dir,date))	
	if os.path.getsize(Overview_dir+"Summary_%s.cand"%date)!=0:
		os.system("trans_gen_overview.py -nbeams 19 -nbeams_cut 4 -cands_file %s*.cand -snr_cut 10 -std_out > %sSummary_%s.png"%(Overview_dir,Overview_dir,date))	    
	else:
		print "Date %s is not available!"%date




	

