import os
import sys
import glob
import numpy as np
import socket
import json

hostname 	= socket.gethostname()
hostID 		= int(hostname.split("x")[1])

file_dir        = "/data26/zhuww/psr_19beam_1bit/"
project 	= sys.argv[1]
date_list       = sorted(glob.glob(file_dir + project+'*'))
N_day           = len(date_list)
serv_list	= json.loads(sys.argv[2])
N_serv          = len(serv_list)
snr_cut		= sys.argv[3]
dm_cut		= sys.argv[4]
Codes_dir 	= "/data26/home/nch/FAST_Miner/"


for i in np.arange(N_day):

   ith = i%N_serv	
   if hostID == serv_list[ith]:

        date = date_list[i].split('/')[-1]

	cands_dir = Codes_dir + "Cands_Result/" + project + date + "/"
	
	Coin_dir = Codes_dir + "Coin_Result/" + project + date + "/"
	
	Overview_dir = Codes_dir + "Overview_plot/" + project + date + "/"
	
	result_dir = Codes_dir + "Gold_Mine/" + project + date + "/"
	
	if not os.path.exists(Coin_dir):
		os.makedirs(Coin_dir)
	
	if not os.path.exists(result_dir):
		os.makedirs(result_dir)
	
	if not os.path.exists(Overview_dir):
	        os.makedirs(Overview_dir)
	
	pathlist = sorted(glob.glob(cands_dir + "*_01*.cand"))
	for ii in range(len(pathlist)):
		t_stamp =  pathlist[ii].split('/')[-1].split('_')[0]
		cand_list = glob.glob(cands_dir+t_stamp+"*.cand")
		if len(cand_list) == 19:
			os.system("cd %s;coincidencer -n 19 %s*.cand > rubbish.txt"%(Coin_dir,cands_dir+t_stamp))
			gold_cand = result_dir+t_stamp + ".gold"
	#		if os.path.getsize(Coin_dir+t_stamp+'_all.cand') !=0 :
			os.system("frb_detector_fast.py -cands_file %s_all.cand -snr_cut %s -gdm %s > %s"%(Coin_dir+t_stamp,snr_cut,dm_cut,gold_cand))
			if os.path.getsize(gold_cand) == 0:
				os.remove(gold_cand)
	print "Date:%s, Done!!!"%date
#   else:
#	print 'Jump Out!'	
#	os.system("cat %s*_all.cand > %sSummary_%s.cand"%(Coin_dir,Overview_dir,date))
	
#	os.system("trans_gen_overview.py -nbeams 19 -nbeams_cut 4 -cands_file %s*.cand -snr_cut 8 -std_out > %sSummary_%s.png"%(Overview_dir,Overview_dir,date))
