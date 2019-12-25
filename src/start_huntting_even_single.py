import numpy as np
import socket
import os,sys
import glob
import time

hostname = socket.gethostname()
hostID = int(hostname.split("x")[1])

file_dir	= "/data5/zhuww/psr_19beam_1bit/"
project		= "201903/"
date_list	= sorted(glob.glob(file_dir + project+'*'))
N_day		= len(date_list)
serv_list 	= [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,20,21]
N_serv		= len(serv_list)
res		= N_day%N_serv

#date_hostID	 = file_dir+ project+ "%02d"%hostID
#if date_hostID in date_list: 
	#date = date_list[i].split('/')[-1]
date = '16'
out_dir = "/data26/home/nch/FAST_Miner/Cands_Result/"+project+date+'/'
if not os.path.exists(out_dir):
	os.makedirs(out_dir)	
time.sleep(1)
print "\n\nHostID:(%02d)Start Hunting Date:"%hostID+project+date+'/!'
print '--------------------------------------------------\n\n'
time.sleep(6)
sys.stdout.flush()

pathlist = glob.glob(file_dir + project + date+"/*.fil")
pathlist = sorted(pathlist,key=lambda s:s.split("_")[-1].split(".")[-2])
for ii in np.arange(len(pathlist)):	
    if ii % 2 == 0:
	fil_file = pathlist[ii]
	print fil_file.split("/")[-1]
	sys.stdout.flush()
	os.system("heimdall -dm 10 5000 -f %s -gpu_id 0 -output_dir %s"%(fil_file,out_dir))
print "Done!\n"
sys.stdout.flush()





			

