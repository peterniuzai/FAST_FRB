import numpy as np
import socket
import os,sys
import glob
import time
import json

hostname = socket.gethostname()
hostID = int(hostname.split("x")[1])

file_dir	= "/data26/zhuww/psr_19beam_1bit/"
project		= sys.argv[1]
maxDM		= sys.argv[3]
date_list	= sorted(glob.glob(file_dir + project+'*'))
N_day		= len(date_list)
serv_list 	= json.loads(sys.argv[2])
N_serv		= len(serv_list)

#date_hostID	 = file_dir+ project+ "%02d"%hostID
#if date_hostID in date_list: 
for i in np.arange(N_day): 
	date = date_list[i].split('/')[-1]
	out_dir = "/data26/home/nch/FAST_Miner/Cands_Result/"+project+date+'/'
	if hostID == serv_list[(i)%N_serv]:
		time.sleep(1)
	
		if not os.path.exists(out_dir):
			os.makedirs(out_dir)	

		print "\n\nHostID:(%02d)Start Hunting Date:"%hostID+project+date+'/!'
		print '--------------------------------------------------\n\n'
		time.sleep(1)
		sys.stdout.flush()

		pathlist = glob.glob(file_dir + project + date+"/*.fil")
		pathlist = sorted(pathlist,key=lambda s:s.split("_")[-1].split(".")[-2])
		for ii in np.arange(len(pathlist)):	
		    if ii % 2 == 0:
			fil_file = pathlist[ii]
			print fil_file.split("/")[-1]
			sys.stdout.flush()
			os.system("heimdall -dm 10 %s -f %s -gpu_id 0 -output_dir %s"%(maxDM,fil_file,out_dir))
		print "Done!\n"
		sys.stdout.flush()




			

