import os
import sys
import glob
import numpy as np

Codes_dir = "/data26/home/nch/FAST_Miner/"

project = "201907/"
date 	= "01"

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
for i in range(len(pathlist)):
	t_stamp =  pathlist[i].split('/')[-1].split('_')[0]
	cand_list = glob.glob(cands_dir+t_stamp+"*.cand")
	if len(cand_list) == 19:
		os.system("cd %s;coincidencer -n 19 %s*.cand"%(Coin_dir,cands_dir+t_stamp))
#		os.system("trans_gen_overview.py -cands_file %s_all.cand -snr_cut 8 -std_out > %s.png"%(Coin_dir+t_stamp,Overview_dir+t_stamp))
		gold_cand = result_dir+t_stamp + ".gold"
		os.system("frb_detector_fast.py -cands_file %s_all.cand -snr_cut 6 > %s"%(Coin_dir+t_stamp,gold_cand))
		if os.path.getsize(gold_cand) == 0:
			os.remove(gold_cand)




	

